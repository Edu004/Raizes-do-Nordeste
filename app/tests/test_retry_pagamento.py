# Test suite para lógica de retry de pagamentos
# Coloque este arquivo em: app/tests/test_retry_pagamento.py

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

# Importar as funções a testar
import sys
sys.path.insert(0, '../')
from crud import (
    processar_pagamento,
    retentar_pagamento_recusado,
    obter_historico_tentativas_pagamento,
    obter_status_pedido,
    StatusPagamento,
    ConfigRetry,
    _processar_pagamento_com_retry,
    _simular_processamento_gateway
)


class TestStatusPagamento:
    """Testes para os enums de status"""
    
    def test_status_pendente(self):
        assert StatusPagamento.PENDENTE.value == "Pendente"
    
    def test_status_pago(self):
        assert StatusPagamento.PAGO.value == "Pago"
    
    def test_status_recusado(self):
        assert StatusPagamento.RECUSADO.value == "Recusado"


class TestConfigRetry:
    """Testes para configuração de retry"""
    
    def test_config_max_tentativas(self):
        assert ConfigRetry.MAX_TENTATIVAS == 3
    
    def test_config_delay(self):
        assert ConfigRetry.DELAY_ENTRE_TENTATIVAS == 2
    
    def test_config_delay_progressivo(self):
        assert ConfigRetry.DELAY_PROGRESSIVO == True


class TestSimularProcessamentoGateway:
    """Testes para a simulação de gateway de pagamento"""
    
    def test_retorna_dict(self):
        resultado = _simular_processamento_gateway(100.0)
        assert isinstance(resultado, dict)
        assert 'sucesso' in resultado
        assert 'motivo' in resultado
        assert 'detalhes' in resultado
    
    def test_motivo_pode_ser_aprovado_recusado_ou_erro(self):
        # Executar várias vezes para cobrir todas as possibilidades
        motivos = set()
        for _ in range(100):
            resultado = _simular_processamento_gateway(100.0)
            motivos.add(resultado['motivo'])
        
        # Deve ter pelo menos dois dos possíveis motivos
        assert len(motivos) >= 2


class TestProcessarPagamento:
    """Testes para a função principal de processamento de pagamento"""
    
    @pytest.fixture
    def mock_db(self):
        """Cria um mock da sessão do banco de dados"""
        db = Mock(spec=Session)
        return db
    
    @pytest.fixture
    def mock_pedido(self):
        """Cria um mock de um pedido"""
        pedido = Mock()
        pedido.id = 123
        pedido.status = StatusPagamento.PENDENTE.value
        pedido.total = 150.50
        return pedido
    
    def test_pedido_nao_encontrado(self, mock_db):
        """Testa quando o pedido não existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        resultado = processar_pagamento(mock_db, 999, 100.0)
        
        assert resultado['sucesso'] == False
        assert 'não encontrado' in resultado['mensagem'].lower()
        assert resultado['tentativas'] == 0
    
    def test_pedido_ja_pago(self, mock_db, mock_pedido):
        """Testa quando o pedido já foi pago"""
        mock_pedido.status = StatusPagamento.PAGO.value
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pedido
        
        resultado = processar_pagamento(mock_db, 123, 100.0)
        
        assert resultado['sucesso'] == True
        assert 'já foi pago' in resultado['mensagem'].lower()
    
    @patch('crud._processar_pagamento_com_retry')
    def test_chama_retry(self, mock_retry, mock_db, mock_pedido):
        """Testa se a função chama corretamente a função de retry"""
        mock_pedido.status = StatusPagamento.PENDENTE.value
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pedido
        mock_retry.return_value = {'sucesso': True, 'tentativas': 1}
        
        resultado = processar_pagamento(mock_db, 123, 100.0)
        
        mock_retry.assert_called_once()


class TestRetentarPagamentoRecusado:
    """Testes para a função de retentativa de pagamento"""
    
    @pytest.fixture
    def mock_db(self):
        db = Mock(spec=Session)
        return db
    
    @pytest.fixture
    def mock_pedido_recusado(self):
        pedido = Mock()
        pedido.id = 123
        pedido.status = StatusPagamento.RECUSADO.value
        pedido.total = 150.50
        return pedido
    
    def test_pedido_nao_encontrado(self, mock_db):
        """Testa quando o pedido não existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        resultado = retentar_pagamento_recusado(mock_db, 999, 100.0)
        
        assert resultado['sucesso'] == False
        assert 'não encontrado' in resultado['mensagem'].lower()
    
    def test_pedido_ja_pago_nao_retenta(self, mock_db, mock_pedido_recusado):
        """Testa que não retenta se pedido já está pago"""
        mock_pedido_recusado.status = StatusPagamento.PAGO.value
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pedido_recusado
        
        resultado = retentar_pagamento_recusado(mock_db, 123, 100.0)
        
        assert resultado['sucesso'] == True
        assert 'já foi pago' in resultado['mensagem'].lower()
    
    def test_pedido_com_status_invalido(self, mock_db, mock_pedido_recusado):
        """Testa que rejeita pedidos que não estão recusados"""
        mock_pedido_recusado.status = "Algo Inválido"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pedido_recusado
        
        resultado = retentar_pagamento_recusado(mock_db, 123, 100.0)
        
        assert resultado['sucesso'] == False
        assert 'não está em estado recusado' in resultado['mensagem'].lower()
    
    @patch('crud._processar_pagamento_com_retry')
    def test_retenta_pedido_recusado(self, mock_retry, mock_db, mock_pedido_recusado):
        """Testa que retenta um pedido recusado"""
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pedido_recusado
        mock_retry.return_value = {'sucesso': True, 'tentativas': 1}
        
        resultado = retentar_pagamento_recusado(mock_db, 123, 100.0)
        
        # Deve ter resetado o status para PROCESSANDO
        assert mock_pedido_recusado.status == StatusPagamento.PROCESSANDO.value
        mock_retry.assert_called_once()


class TestObterStatusPedido:
    """Testes para obter status do pedido"""
    
    @pytest.fixture
    def mock_db(self):
        db = Mock(spec=Session)
        return db
    
    def test_pedido_nao_encontrado(self, mock_db):
        """Testa quando o pedido não existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        resultado = obter_status_pedido(mock_db, 999)
        
        assert 'erro' in resultado
        assert 'não encontrado' in resultado['erro'].lower()
    
    def test_retorna_info_corretamente(self, mock_db):
        """Testa que retorna informações corretas"""
        # Mock pedido
        pedido = Mock()
        pedido.id = 123
        pedido.status = StatusPagamento.PAGO.value
        pedido.total = 150.50
        
        # Mock pagamentos
        pag1 = Mock()
        pag1.id = 1
        pag1.status_pag = StatusPagamento.RECUSADO.value
        pag1.valor = 150.50
        
        pag2 = Mock()
        pag2.id = 2
        pag2.status_pag = StatusPagamento.PAGO.value
        pag2.valor = 150.50
        
        # Configurar mocks
        mock_db.query.return_value.filter.return_value.first.return_value = pedido
        mock_db.query.return_value.filter.return_value.all.return_value = [pag1, pag2]
        
        resultado = obter_status_pedido(mock_db, 123)
        
        assert resultado['pedido_id'] == 123
        assert resultado['status'] == StatusPagamento.PAGO.value
        assert resultado['total'] == 150.50
        assert resultado['quantidade_tentativas'] == 2
        assert resultado['ultimo_status_pagamento'] == StatusPagamento.PAGO.value
        assert len(resultado['pagamentos']) == 2


class TestObterHistoricoTentativas:
    """Testes para obter histórico de tentativas"""
    
    @pytest.fixture
    def mock_db(self):
        db = Mock(spec=Session)
        return db
    
    def test_retorna_lista_pagamentos(self, mock_db):
        """Testa que retorna lista de pagamentos"""
        pag1 = Mock()
        pag1.id = 1
        
        pag2 = Mock()
        pag2.id = 2
        
        mock_db.query.return_value.filter.return_value.all.return_value = [pag1, pag2]
        
        resultado = obter_historico_tentativas_pagamento(mock_db, 123)
        
        assert len(resultado) == 2
        assert resultado[0].id == 1
        assert resultado[1].id == 2
    
    def test_retorna_vazio_se_sem_pagamentos(self, mock_db):
        """Testa quando não há pagamentos"""
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        resultado = obter_historico_tentativas_pagamento(mock_db, 123)
        
        assert resultado == []


# Testes de integração (requerem banco de dados real)
@pytest.mark.integration
class TestIntegracaoRetry:
    """Testes de integração com banco de dados real"""
    
    def test_fluxo_completo_pagamento_sucesso(self):
        """Testa o fluxo completo de um pagamento bem-sucedido"""
        # Este teste requer um banco de dados configurado
        pass
    
    def test_fluxo_completo_pagamento_recusado_e_retentativa(self):
        """Testa o fluxo completo: recusa -> retentativa -> sucesso"""
        # Este teste requer um banco de dados configurado
        pass


if __name__ == '__main__':
    # Executar testes
    pytest.main([__file__, '-v'])
