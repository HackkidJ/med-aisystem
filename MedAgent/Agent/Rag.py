from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from Tongyi import TongyiChat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# 初始化
embedding_path = "MedAgent\\models\\bge-large-zh-v1.5"
embeddings = HuggingFaceBgeEmbeddings(model_name=embedding_path)
llm = TongyiChat()

vectorstore = FAISS.from_texts(
    ["做医生要有行医资格证", "发烧了应该先服用消炎药，再好好休息进行理疗", "常见的消炎药有阿莫西林"],
    embedding=embeddings
)

retriever = vectorstore.as_retriever()

template = """
根据以下资料回答问题：
{context}

问题：{question}
"""

prompt = ChatPromptTemplate.from_template(template)
outputParser = StrOutputParser()

setup_and_retrieval = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
})

# 简化的适配器函数 - 直接提取文本内容
def tongyi_invoker(input_data):
    """提取文本内容后调用 TongyiChat"""
    # 如果是 ChatPromptValue，转换为字符串
    if hasattr(input_data, 'to_string'):
        text_content = input_data.to_string()
        return llm.invoke(text_content)
    # 如果有 messages 属性
    elif hasattr(input_data, 'messages'):
        # 提取所有消息内容
        messages_text = "\n".join([msg.content for msg in input_data.messages])
        return llm.invoke(messages_text)
    # 其他情况
    else:
        return llm.invoke(str(input_data))

tongyi_adapter = RunnableLambda(tongyi_invoker)

# 构建链
chain = (setup_and_retrieval | prompt | tongyi_adapter | outputParser)

# 测试调用
result = chain.invoke("常见的消炎药有哪些")
print(result)