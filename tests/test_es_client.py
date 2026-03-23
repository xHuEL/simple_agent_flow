import pytest
from unittest.mock import Mock, patch
from common.es_client import ESClient, create_es_client


def test_es_client_singleton():
    """测试 ESClient 单例模式。"""
    client1 = ESClient()
    client2 = ESClient()
    
    assert client1 is client2
    assert id(client1) == id(client2)


def test_es_client_initialization():
    """测试 ESClient 初始化。"""
    config = {
        'ES_HOST': 'test-host',
        'ES_PORT': '9200',
        'ES_USER': 'test-user',
        'ES_PASSWORD': 'test-pass'
    }
    
    client = ESClient(config)
    assert client.config == config
    assert client._client is None


def test_create_es_client():
    """测试 create_es_client 工厂函数。"""
    config = {'ES_HOST': 'test-host'}
    client = create_es_client(config)
    
    assert isinstance(client, ESClient)
    # 检查配置包含提供的值
    assert client.config['ES_HOST'] == 'test-host'
    # 检查默认值也被设置
    assert 'ES_PORT' in client.config
    assert 'ES_USER' in client.config
    assert 'ES_PASSWORD' in client.config


@patch('common.es_client.Elasticsearch')
def test_connect_method_signature(mock_elasticsearch):
    """测试 connect 方法签名和参数处理。"""
    mock_client = Mock()
    mock_client.ping.return_value = True
    mock_elasticsearch.return_value = mock_client
    
    config = {
        'ES_HOST': 'config-host',
        'ES_PORT': '9300',
        'ES_USER': 'config-user',
        'ES_PASSWORD': 'config-pass'
    }
    
    client = ESClient(config)
    client.connect()
    
    # 验证使用配置中的参数
    mock_elasticsearch.assert_called_once()
    call_args = mock_elasticsearch.call_args[0][0]
    assert call_args[0] == 'config-host:9300'


@patch('common.es_client.Elasticsearch')
def test_connect_with_explicit_parameters(mock_elasticsearch):
    """测试使用显式参数连接。"""
    mock_client = Mock()
    mock_client.ping.return_value = True
    mock_elasticsearch.return_value = mock_client
    
    client = ESClient()
    client.connect(
        host='explicit-host',
        port=9400,
        username='explicit-user',
        password='explicit-pass'
    )
    
    # 验证使用显式参数
    mock_elasticsearch.assert_called_once()
    call_args = mock_elasticsearch.call_args[0][0]
    assert call_args[0] == 'explicit-host:9400'


def test_search_method_signature():
    """测试 search 方法签名。"""
    client = ESClient()
    
    # 验证方法存在且参数正确
    assert hasattr(client, 'search')
    import inspect
    sig = inspect.signature(client.search)
    assert 'index' in sig.parameters
    assert 'query' in sig.parameters
    assert 'size' in sig.parameters
    assert sig.parameters['size'].default == 10


def test_get_document_method_signature():
    """测试 get_document 方法签名。"""
    client = ESClient()
    
    # 验证方法存在且参数正确
    assert hasattr(client, 'get_document')
    import inspect
    sig = inspect.signature(client.get_document)
    assert 'index' in sig.parameters
    assert 'doc_id' in sig.parameters


def test_close_method():
    """测试 close 方法。"""
    client = ESClient()
    client._client = Mock()
    
    client.close()
    
    assert client._client is None


@patch('common.es_client.Elasticsearch')
def test_connection_error_handling(mock_elasticsearch):
    """测试连接错误处理。"""
    mock_client = Mock()
    mock_client.ping.return_value = False  # 模拟连接失败
    mock_elasticsearch.return_value = mock_client
    
    client = ESClient()
    
    with pytest.raises(ConnectionError, match="无法连接到 Elasticsearch 集群"):
        client.connect()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])