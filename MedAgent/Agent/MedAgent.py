from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv;

print("系统环境变量里的Key是：", os.environ.get("DASHSCOPE_API_KEY"))
load_dotenv()
API_KEY = os.getenv('DASHSCOPE_API_KEY')
print(API_KEY)
