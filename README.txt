Docker Elasticsearch 部署指南
============================

本指南提供从Docker拉取和运行Elasticsearch的完整步骤。

1. 拉取Elasticsearch镜像
--------------------------------
使用以下命令拉取官方Elasticsearch镜像：

docker pull elasticsearch/elasticsearch:7.17.25

2. 运行Elasticsearch容器
--------------------------------
运行单节点Elasticsearch容器：

docker run -d --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  elasticsearch/elasticsearch:7.17.25

3. 验证服务运行
--------------------------------
等待几秒钟后，验证Elasticsearch是否正常运行：

curl -X GET "http://localhost:9200/"

正常响应应该类似：
{
  "name" : "node-1",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "abcd1234",
  "version" : {
    "number" : "8.13.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "abcdef",
    "build_date" : "2024-01-01",
    "build_snapshot" : false,
    "lucene_version" : "9.10.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}