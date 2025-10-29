import os
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# 读取环境变量
DEEPSEEK_API_KEY = os.getenv("Deepseek_API_KEY")
DEEPSEEK_API_BASE = os.getenv("Deepseek_API_BASE")
DEEPSEEK_API_MODEL = os.getenv("Deepseek_API_MODEL")

# AI 交易代理的默认配置

# 交易模型的配置
# 格式: ['模块路径.类名']
MODELS = [
    'models.simple_model.SimpleModel',
    'models.llm_model.LLMModel'
]

# 数据源的配置
# 我们将使用一只常见的指数基金作为示例
DATA_SOURCE = {
    'fund_code': '000001' # 华夏成长混合
}