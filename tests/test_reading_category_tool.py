import pytest
import os
import json
from unittest.mock import mock_open, patch
from tools.reading_category_tool import reading_category_tool, read_json_categories, format_categories


def test_format_categories():
    """测试分类信息格式化功能。"""
    # 测试正常分类列表
    categories = ["文学", "科幻", "历史"]
    result = format_categories(categories)
    expected = "1. 文学\n2. 科幻\n3. 历史"
    assert result == expected
    
    # 测试空列表
    result = format_categories([])
    assert result == "未找到分类信息。"
    
    # 测试单个分类
    result = format_categories(["文学"])
    assert result == "1. 文学"


def test_read_json_categories_success():
    """测试成功读取 JSON 分类文件。"""
    test_data = ["文学", "科幻", "历史"]
    
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        categories = read_json_categories("dummy.json")
        assert categories == ["文学", "科幻", "历史"]


def test_read_json_categories_invalid_json():
    """测试无效 JSON 文件处理。"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(ValueError, match="JSON 文件格式错误"):
            read_json_categories("invalid.json")


def test_read_json_categories_not_list():
    """测试非列表格式 JSON 文件处理。"""
    test_data = {"categories": ["文学", "科幻"]}
    
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        with pytest.raises(ValueError, match="JSON 文件应该包含一个分类列表"):
            read_json_categories("not_list.json")


def test_reading_category_tool_success():
    """测试工具成功读取分类文件。"""
    test_data = ["文学", "科幻", "历史"]
    
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        with patch("os.path.exists", return_value=True):
            result = reading_category_tool("test.json")
            assert "1. 文学" in result
            assert "2. 科幻" in result
            assert "3. 历史" in result


def test_reading_category_tool_file_not_exists():
    """测试文件不存在时的错误处理。"""
    with patch("os.path.exists", return_value=False):
        result = reading_category_tool("nonexistent.json")
        assert "不存在" in result


def test_reading_category_tool_unsupported_format():
    """测试不支持的文件格式处理。"""
    with patch("os.path.exists", return_value=True):
        result = reading_category_tool("test.txt")
        assert "不支持的文件格式" in result


def test_reading_category_tool_empty_file():
    """测试空文件处理。"""
    with patch("builtins.open", mock_open(read_data=json.dumps([]))):
        with patch("os.path.exists", return_value=True):
            result = reading_category_tool("empty.json")
            assert "未找到分类信息" in result


def test_reading_category_tool_json_decode_error():
    """测试 JSON 解析错误处理。"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            result = reading_category_tool("invalid.json")
            assert "错误" in result
            assert "JSON" in result


def test_reading_category_tool_with_test_data():
    """使用实际测试数据文件进行测试。"""
    test_file = "/Users/rotile/code/simple_agent_flow/test_data/categories.json"
    
    if os.path.exists(test_file):
        result = reading_category_tool(test_file)
        # 检查结果包含预期的分类信息
        assert "文学" in result
        assert "科幻" in result
        assert "历史" in result
        # 检查格式正确
        assert "1." in result
        assert "2." in result
    else:
        pytest.skip("测试数据文件不存在")


def test_tool_decorator_present():
    """测试工具装饰器存在。"""
    assert hasattr(reading_category_tool, 'name')
    assert hasattr(reading_category_tool, 'description')
    assert reading_category_tool.name == 'reading_category_tool'
    assert '从文件中读取阅读领域的所有分类信息' in reading_category_tool.description


if __name__ == "__main__":
    pytest.main([__file__, "-v"])