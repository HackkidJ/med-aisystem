from langchain_core.prompts import ChatPromptTemplate
from Tongyi import TongyiChat
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage


llm = TongyiChat()
chat_template = ChatPromptTemplate.from_messages(
    [
        ("system","""
        你是一名经验丰富的ai医生，你叫{name},你负责为每位病患问诊看病，可以翻看他们的病历，通过对话问诊的方式得出病患的病因，并给出对应治疗方案。
        要求：
        1.注意礼貌用语，说话要柔和。
        2.对待病患要负责，不能妄自下诊断。 
        3.你不需要每次说话都要做自我介绍
""")
    ]
)

messages = chat_template.format_messages(name="怀特医生")
response = llm.invokeConversation(messages)
print(response.content)
