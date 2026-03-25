import os
from typing import Dict, Any, Optional, List
from elasticsearch import Elasticsearch, NotFoundError


class ESClient:
    """Elasticsearch 客户端封装类，提供连接管理和基本操作。"""
    
    _instance = None
    
    def __new__(cls, config: Optional[Dict[str, str]] = None):
        if cls._instance is None:
            cls._instance = super(ESClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        if not self._initialized:
            self.config = self._get_default_config()
            if config:
                self.config.update(config)
            self._client = None
            self._initialized = True
    
    def _get_default_config(self) -> Dict[str, str]:
        """获取默认配置。"""
        return {
            'ES_HOST': os.getenv('ES_HOST', 'localhost'),
            'ES_PORT': os.getenv('ES_PORT', '9200'),
            'ES_USER': os.getenv('ES_USER', ''),
            'ES_PASSWORD': os.getenv('ES_PASSWORD', '')
        }
    
    def connect(self, host: Optional[str] = None, port: Optional[int] = None, 
               username: Optional[str] = None, password: Optional[str] = None) -> Elasticsearch:
        """连接到 Elasticsearch 服务。"""
        
        # 使用显式参数或配置中的值
        host = host or self.config['ES_HOST']
        port = port or int(self.config['ES_PORT'])
        username = username or self.config['ES_USER']
        password = password or self.config['ES_PASSWORD']
        
        # 构建连接参数
        hosts = [f"{host}:{port}"]
        
        if username and password:
            http_auth = (username, password)
        else:
            http_auth = None
        
        # 创建 Elasticsearch 客户端
        self._client = Elasticsearch(
            hosts=hosts,
            http_auth=http_auth,
            verify_certs=False,
            request_timeout=30
        )
        
        # 测试连接
        if not self._client.ping():
            raise ConnectionError("无法连接到 Elasticsearch 服务")
        
        return self._client
    
    def get_client(self) -> Elasticsearch:
        """获取 Elasticsearch 客户端实例。"""
        if self._client is None:
            self.connect()
        return self._client
    
    def search(self, index: str, query: Dict[str, Any], size: int = 10) -> List[Dict[str, Any]]:
        """执行搜索查询。"""
        client = self.get_client()
        
        try:
            response = client.search(
                index=index,
                body={"query": query},
                size=size
            )
            
            # 提取命中的文档
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
            
        except NotFoundError:
            return []
        except Exception as e:
            raise Exception(f"搜索执行失败: {str(e)}")
    
    def create_index(self, index_name: str, mappings: Dict[str, Any]) -> Dict[str, Any]:
        """创建索引。"""
        client = self.get_client()
        
        try:
            # 检查索引是否已存在
            if client.indices.exists(index=index_name):
                return {"acknowledged": True, "message": f"索引 {index_name} 已存在"}
            
            # 创建索引
            response = client.indices.create(
                index=index_name,
                body={"mappings": mappings}
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"创建索引失败: {str(e)}")
    
    def index_document(self, index: str, document: Dict[str, Any], doc_id: Optional[str] = None) -> Dict[str, Any]:
        """索引文档。"""
        client = self.get_client()
        
        try:
            response = client.index(
                index=index,
                body=document,
                id=doc_id,
                refresh=True  # 立即刷新使文档可搜索
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"索引文档失败: {str(e)}")
    
    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """删除索引。"""
        client = self.get_client()
        
        try:
            if client.indices.exists(index=index_name):
                response = client.indices.delete(index=index_name)
                return response
            else:
                return {"acknowledged": True, "message": f"索引 {index_name} 不存在"}
            
        except Exception as e:
            raise Exception(f"删除索引失败: {str(e)}")
    
    def get_mapping(self, index_name: str) -> Dict[str, Any]:
        """获取索引的映射信息。"""
        client = self.get_client()
        
        try:
            response = client.indices.get_mapping(index=index_name)
            return response
            
        except NotFoundError:
            return {}
        except Exception as e:
            raise Exception(f"获取映射失败: {str(e)}")


def create_es_client(config: Optional[Dict[str, str]] = None) -> ESClient:
    """创建 ESClient 实例的工厂函数。"""
    return ESClient(config)