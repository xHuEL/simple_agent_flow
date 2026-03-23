import os
from typing import Optional, Dict, Any, List
from elasticsearch import Elasticsearch


class ESClient:
    """Elasticsearch 客户端封装类，使用单例模式管理连接。"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize only once
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        if not self._initialized:
            self._initialized = True
            self._client = None
            self.config = {}
        
        # Always update config if provided
        if config:
            self.config.update(config)
            # Update connection values
            self.host = self.config.get('ES_HOST', 'localhost')
            self.port = int(self.config.get('ES_PORT', 9200))
            self.username = self.config.get('ES_USER')
            self.password = self.config.get('ES_PASSWORD')
            
    def connect(self, host: str = None, port: int = None, 
                username: str = None, password: str = None) -> None:
        """连接到 Elasticsearch 集群。"""
        host = host or self.host
        port = port or self.port
        username = username or self.username
        password = password or self.password
        
        http_auth = (username, password) if username and password else None
        
        self._client = Elasticsearch(
            [f"{host}:{port}"],
            http_auth=http_auth,
            verify_certs=False,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )
        
        # 测试连接
        try:
            if not self._client.ping():
                raise ConnectionError("无法连接到 Elasticsearch 集群")
            print(f"成功连接到 Elasticsearch: {host}:{port}")
        except Exception as e:
            raise ConnectionError(f"Elasticsearch 连接失败: {e}")
    
    def search(self, index: str, query: str, size: int = 10) -> List[Dict[str, Any]]:
        """执行全文搜索。"""
        if self._client is None:
            self.connect()
        
        try:
            response = self._client.search(
                index=index,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["*"],
                            "fuzziness": "AUTO"
                        }
                    },
                    "size": size
                }
            )
            
            return [hit["_source"] for hit in response['hits']['hits']]
            
        except Exception as e:
            raise Exception(f"搜索执行失败: {e}")
    
    def get_document(self, index: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """获取特定文档。"""
        if self._client is None:
            self.connect()
        
        try:
            response = self._client.get(index=index, id=doc_id)
            return response['_source']
        except Exception as e:
            print(f"获取文档失败: {e}")
            return None
    
    def close(self) -> None:
        """关闭连接。"""
        if self._client:
            self._client.close()
            self._client = None


def create_es_client(config: Optional[Dict[str, str]] = None) -> ESClient:
    """创建并返回 ESClient 实例。"""
    client = ESClient(config)
    return client