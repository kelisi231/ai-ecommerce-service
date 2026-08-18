from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()


llm = ChatOpenAI(
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("LLM_API_KEY"),
    temperature=0.1
)



if __name__ == "__main__":
    response = llm.invoke("简单介绍一下自己")
    print(response.content)