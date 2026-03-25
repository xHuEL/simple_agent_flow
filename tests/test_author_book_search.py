#!/usr/bin/env python3
"""
作者-图书搜索工具测试

测试 author_book_search_tool 的各种功能场景。
"""

import unittest
from unittest.mock import Mock, patch
from tools.author_book_search import author_book_search_tool, get_book_title


class TestAuthorBookSearch(unittest.TestCase):
    """测试作者-图书搜索工具"""

    def test_get_book_title_mapping(self):
        """测试图书ID到书名的映射功能"""
        # 测试中文图书映射
        self.assertEqual(get_book_title("lu_xun_kuang_ren_ri_ji"), "狂人日记")
        self.assertEqual(get_book_title("lao_she_cha_guan"), "茶馆")
        
        # 测试英文图书映射
        self.assertEqual(get_book_title("hemingway_the_old_man_and_the_sea"), "老人与海")
        self.assertEqual(get_book_title("jk_rowling_harry_potter"), "哈利·波特与魔法石")
        
        # 测试未知图书ID返回原值
        self.assertEqual(get_book_title("unknown_book_id"), "unknown_book_id")

    @patch('tools.author_book_search.create_es_client')
    def test_successful_author_search(self, mock_create_es_client):
        """测试成功的作者搜索"""
        # 模拟ES客户端和响应
        mock_es_client = Mock()
        mock_es_client.search.return_value = [
            {'slotName': '鲁迅', 'slotReName': 'lu_xun_kuang_ren_ri_ji'},
            {'slotName': '鲁迅', 'slotReName': 'lu_xun_a_q_zheng_zhuan'}
        ]
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索
        result = author_book_search_tool.invoke({"query": "鲁迅"})
        
        # 验证结果
        expected = "作者名：鲁迅，书名：狂人日记\n作者名：鲁迅，书名：阿Q正传"
        self.assertEqual(result, expected)
        
        # 验证ES搜索被调用
        mock_es_client.search.assert_called_once_with(
            index="slots_index", 
            query={
                "multi_match": {
                    "query": "鲁迅",
                    "fields": ["slotName^2.0", "slotReName^1.0"],
                    "fuzziness": "AUTO",
                    "type": "best_fields"
                }
            },
            size=10
        )

    @patch('tools.author_book_search.create_es_client')
    def test_successful_book_search(self, mock_create_es_client):
        """测试成功的图书搜索"""
        # 模拟ES客户端和响应
        mock_es_client = Mock()
        mock_es_client.search.return_value = [
            {'slotName': '鲁迅', 'slotReName': 'lu_xun_kuang_ren_ri_ji'}
        ]
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索
        result = author_book_search_tool.invoke({"query": "狂人日记"})
        
        # 验证结果
        self.assertEqual(result, "作者名：鲁迅，书名：狂人日记")

    @patch('tools.author_book_search.create_es_client')
    def test_no_results_found(self, mock_create_es_client):
        """测试无结果的情况"""
        # 模拟ES客户端返回空结果
        mock_es_client = Mock()
        mock_es_client.search.return_value = []
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索
        result = author_book_search_tool.invoke({"query": "不存在的作者"})
        
        # 验证结果
        self.assertEqual(result, "未找到与 '不存在的作者' 相关的作者图书信息")

    @patch('tools.author_book_search.create_es_client')
    def test_mixed_chinese_english_query(self, mock_create_es_client):
        """测试中英文混合查询"""
        # 模拟ES客户端和响应
        mock_es_client = Mock()
        mock_es_client.search.return_value = [
            {'slotName': 'J.K.罗琳', 'slotReName': 'jk_rowling_harry_potter'}
        ]
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索
        result = author_book_search_tool.invoke({"query": "Harry Potter"})
        
        # 验证结果
        self.assertEqual(result, "作者名：J.K.罗琳，书名：哈利·波特与魔法石")

    @patch('tools.author_book_search.create_es_client')
    def test_elasticsearch_connection_error(self, mock_create_es_client):
        """测试Elasticsearch连接错误"""
        # 模拟ES客户端抛出异常
        mock_es_client = Mock()
        mock_es_client.search.side_effect = Exception("Connection failed")
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索
        result = author_book_search_tool.invoke({"query": "鲁迅"})
        
        # 验证错误处理
        self.assertIn("搜索服务暂时不可用", result)
        self.assertIn("Connection failed", result)

    @patch('tools.author_book_search.create_es_client')
    def test_custom_index_parameter(self, mock_create_es_client):
        """测试自定义索引参数"""
        # 模拟ES客户端和响应
        mock_es_client = Mock()
        mock_es_client.search.return_value = [
            {'slotName': '鲁迅', 'slotReName': 'lu_xun_kuang_ren_ri_ji'}
        ]
        mock_create_es_client.return_value = mock_es_client
        
        # 执行搜索，使用自定义索引 - 需要调用invoke方法
        result = author_book_search_tool.invoke({"query": "鲁迅", "index": "custom_index"})
        
        # 验证索引参数被正确传递
        mock_es_client.search.assert_called_once_with(
            index="custom_index", 
            query={
                "multi_match": {
                    "query": "鲁迅",
                    "fields": ["slotName^2.0", "slotReName^1.0"],
                    "fuzziness": "AUTO",
                    "type": "best_fields"
                }
            },
            size=10
        )

    def test_tool_decorator_metadata(self):
        """测试工具装饰器的元数据"""
        # 验证工具函数有正确的元数据
        self.assertTrue(hasattr(author_book_search_tool, 'name'))
        self.assertEqual(author_book_search_tool.name, 'author_book_search_tool')
        
        # 验证有文档字符串
        self.assertIsNotNone(author_book_search_tool.description)
        self.assertIn('作者-图书搜索', author_book_search_tool.description)
        self.assertIn('模糊查询', author_book_search_tool.description)
        self.assertIn('短语匹配', author_book_search_tool.description)


if __name__ == '__main__':
    unittest.main()