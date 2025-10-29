import sys
import pytest

# 将项目根目录添加到 Python 路径中，以便导入我们的模块
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

def test_load_default_settings():
    """
    测试默认配置文件 `config.settings` 是否能被加载，
    并包含正确的 `MODELS` 和 `DATA_SOURCE` 属性。
    """
    # 导入配置文件，这会执行 config/settings.py
    from config import settings

    # 断言 MODELS 属性存在且类型为列表
    assert hasattr(settings, 'MODELS'), "配置文件中应包含 'MODELS' 属性"
    assert isinstance(settings.MODELS, list), "'MODELS' 属性应为列表类型"

    # 断言 DATA_SOURCE 属性存在且类型为字典
    assert hasattr(settings, 'DATA_SOURCE'), "配置文件中应包含 'DATA_SOURCE' 属性"
    assert isinstance(settings.DATA_SOURCE, dict), "'DATA_SOURCE' 属性应为字典类型"

def test_load_dotenv_settings():
    """
    测试能否从 .env 文件加载环境变量。
    """
    # 确保 dotenv 加载了我们的 .env 文件
    from config import settings
    import os
    
    # 重新加载模块以确保 dotenv 生效
    import importlib
    importlib.reload(settings)

    assert hasattr(settings, 'DEEPSEEK_API_KEY'), "配置中应包含 'DEEPSEEK_API_KEY'"
    assert settings.DEEPSEEK_API_KEY == "sk-1234"