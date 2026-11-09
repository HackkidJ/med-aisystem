from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import markdown
import logging
from Tongyi import TongyiChat

logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self, doc_id):
        self.llm = TongyiChat()
        self.name = "怀特医生"  # 默认叫怀特医生
        self.doc_id = doc_id
        self.chat_history = []

        # 创建系统提示
        self.system_prompt = """你是一个专业的医疗助手，你叫{name}。你负责与id为{doc_id}的医生对话，医生会给你患者的症状，你根据丰富的医学知识和患者的病历得出病根和治疗方案。

你拥有一个庞大的临床医学知识库。当医生向你描述了患者症状，或者你需要查阅医学指南来辅助诊断时，请**必须严格按照以下步骤执行**：
1. 调用 `search_medical_knowledge` 工具，传入患者的症状描述或你想检索的医学关键词。
2. 仔细阅读工具返回的【医学知识库检索结果】。
3. 严格基于检索结果中提供的文献片段，结合你的医学常识，向医生给出鉴别诊断和治疗建议。
4. 在回复的最后，请注明参考的文献来源（如：参考《肠胃内科指南》）。

【重要规则】
- 严禁凭空捏造医学知识，必须做到“有据可查”。
- 如果检索结果为空，请直接回答“知识库中暂无相关指南依据”。
- 你的回答需要专业、严谨，语气像一位资深的主任医师。

请根据医生的具体问题和自己的需要，智能选择相关的学科和文献进行查阅。在回复中请注明参考的文献来源，只在必要的时候翻阅资料，尽量减少翻阅资料的次数。
 
当你需要添加病患信息时，可使用addPatient函数。
当你需要知道患者信息时，可使用getPatientByName和getPatientById两个函数
只有医师让你添加患者信息时才添加，不要擅自做此操作。
"""

    def clearHistory(self):
        self.chat_history = []

    def conversation(self, input_text):
        try:
            # 构建消息列表
            messages = [
                SystemMessage(content=self.system_prompt.format(name=self.name, doc_id=self.doc_id))
            ]
            
            # 添加聊天历史
            messages.extend(self.chat_history)
            
            # 添加当前用户输入
            messages.append(HumanMessage(content=input_text))
            
            logger.info(f"开始处理用户输入: {input_text}")
            
            # 使用支持函数调用的方法
            result = self.llm.invoke_with_tool_call(messages)
            
            reply = result.content
            logger.info(f"AI回复: {reply}")
            
            # 使用markdown库转换为HTML
            formatted_reply = markdown.markdown(reply, extensions=['extra'])
            
            # 更新聊天历史
            self.chat_history.append(HumanMessage(content=input_text))
            self.chat_history.append(AIMessage(content=reply))
            
            return formatted_reply
            
        except Exception as e:
            logger.error(f"对话处理失败: {str(e)}")
            error_message = "抱歉，处理您的请求时出现了问题，请稍后重试。"
            formatted_error = markdown.markdown(error_message, extensions=['extra'])
            return formatted_error