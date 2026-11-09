from langchain.llms.base import LLM
from langchain_core.messages.ai import AIMessage
import os
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from dotenv import load_dotenv
from openai import OpenAI
from typing import Iterator, List, Optional, Any, Dict
from Tools.patient import addPatient,getPatientById,getPatientByName,updatePatient
from Tools.pdfReader import readPdf
from Tools.seekKnowledge import find_folders_from_knowledges, get_listdir, chdir, form_complete_path
from Tools.rag_retriever import get_retriever
from langchain_core.language_models.chat_models import BaseChatModel
import json
import logging

load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def search_medical_knowledge(query: str) -> str:
    """执行 RAG 混合检索，返回相关医学知识片段"""
    retriever = get_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "未检索到相关医学指南"
    
    result_text = "[医学知识库检索结果] \n"
    for i, doc in enumerate(docs):
        dept = doc.metadata.get('department', '未知科室')
        result_text += f"\n[来源：{dept} 指南] \n{doc.page_content}\n"
    return result_text

# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "addPatient",
            "description": "当你需要往数据库中添加病患信息的时候，就使用该函数。务必传入所有的参数 哪怕为空值的也要传入",
            "parameters": {
                "type": "object",
                "properties": {
                    "identityId": {
                        "type": "string",
                        "description": "患者身份证号（必填）"
                    },
                    "name": {
                        "type": "string",
                        "description": "患者姓名（必填）"
                    },
                    "gender": {
                        "type": "string",
                        "enum": ["男", "女"],
                        "description": "患者性别，必须是 '男' 或 '女'（必填）"
                    },
                    "doc_id": {
                        "type": "string",
                        "description": "主治医生的 ID，即与你对话的医生 ID（必填）"
                    },
                    "phone": {
                        "type": "string",
                        "description": "患者联系电话，可为空值，但必须传入"
                    },
                    "address": {
                        "type": "string",
                        "description": "患者家庭住址，可为空值，但必须传入"
                    },
                    "PMH": {
                        "type": "string",
                        "description": "既往病史（Past Medical History），可为空值，但必须传入"
                    },
                    "PI": {
                        "type": "string",
                        "description": "现病史（Present Illness），可为空值，但必须传入"
                    },
                    "CC": {
                        "type": "string",
                        "description": "主诉（Chief Complaint），可为空值，但必须传入"
                    }
                },
                "required": ["identityId", "name", "gender", "doc_id"]
            }
        }
    },
    {
         "type": "function",
        "function": {
            "name": "search_medical_knowledge",
            "description": "当需要查阅医学指南、寻找病症诊断依据、治疗方案时，调用此函数。输入应为患者的症状描述或医学问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "检索关键词或患者的症状描述"
                    }
                },
                "required": ["query"]
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "find_folders_from_knowledges",
    #         "description": "第一步调用该函数定位到医学知识库中",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {},
    #             "required": []
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_listdir",
    #         "description": "调用该函数列出当前文件夹中的文件，找到需要的文件或文件夹",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {},
    #             "required": []
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "chdir",
    #         "description": "找到需要的文件夹名字后，调用该函数传入文件夹的名字进入该路径",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "folder_name": {
    #                     "type": "string",
    #                     "description": "要进入的文件夹名称"
    #                 }
    #             },
    #             "required": ["folder_name"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "form_complete_path",
    #         "description": "找到需要参考的pdf文件后，调用该函数形成完整的路径",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "subject": {
    #                     "type": "string",
    #                     "description": "学科名称"
    #                 },
    #                 "file": {
    #                     "type": "string",
    #                     "description": "文件名"
    #                 }
    #             },
    #             "required": ["subject", "file"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "readPdf",
    #         "description": "传入完整路径，返回pdf文本内容作为参考资料去回答用户问题",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "path": {
    #                     "type": "string",
    #                     "description": "PDF文件的完整路径"
    #                 }
    #             },
    #             "required": ["path"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "getPatientByName",
            "description": "传入姓名，获取患者的信息，用来辅助诊断",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "患者姓名"
                    }
                }
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "getPatientById",
            "description": "传入身份证号，获取患者的信息，用来辅助诊断",
            "parameters": {
                "type": "object",
                "properties": {
                    "identityId": {
                        "type": "string",
                        "description": "患者身份证号码"
                    }
                }
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "updatePatient",
        "description": "修改患者信息，可以根据身份证号更新患者的姓名、性别、电话、地址、病史等信息",
        "parameters": {
            "type": "object",
            "properties": {
                "identityId": {
                    "type": "string",
                    "description": "患者的身份证号码（必填）"
                },
                "name": {
                    "type": "string",
                    "description": "患者姓名（可选）"
                },
                "gender": {
                    "type": "string",
                    "enum": ["男", "女"],
                    "description": "患者性别（可选）"
                },
                "phone": {
                    "type": "string",
                    "description": "患者联系电话（可选）"
                },
                "address": {
                    "type": "string",
                    "description": "患者家庭住址（可选）"
                },
                "PMH": {
                    "type": "string",
                    "description": "既往病史（可选）"
                },
                "PI": {
                    "type": "string",
                    "description": "现病史（可选）"
                },
                "CC": {
                    "type": "string",
                    "description": "主诉（可选）"
                },
                "doc_id": {
                    "type": "string",
                    "description": "主治医生ID（可选）"
                }
            },
            "required": ["identityId"]
        }
    }
}
]

# 工具函数映射
tool_functions = {
    "addPatient": addPatient,
    # "find_folders_from_knowledges": find_folders_from_knowledges,
    # "get_listdir": get_listdir,
    # "chdir": chdir,
    # "form_complete_path": form_complete_path,
    # "readPdf": readPdf,
    "getPatientByName": getPatientByName,
    "getPatientById": getPatientById,
    "updatePatient": updatePatient,
    "search_medical_knowledge":search_medical_knowledge
}

class TongyiChat(BaseChatModel):
    client: Optional[Any] = None
    API_KEY: str = os.getenv('DASHSCOPE_API_KEY')
    model_name: str = "qwen-flash"  # 使用qwen-plus以支持函数调用

    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=self.API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    
    @property
    def _llm_type(self):
        return "Tongyi"
    
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, 
                 run_manager: Optional[Any] = None, **kwargs) -> ChatResult:
        """生成聊天回复，支持函数调用"""
        # 转换消息格式
        formatted_messages = self._convert_messages_to_openai_format(messages)
        
        # 调用模型，传入工具定义
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            tools=tools
        )
        
        assistant_message = response.choices[0].message
        
        # 处理函数调用
        if assistant_message.tool_calls:
            logger.info("检测到函数调用请求")
            # 这里可以添加函数调用处理逻辑
            # 由于BaseChatModel的限制，我们返回包含工具调用的消息
            content = assistant_message.content or ""
            message = AIMessage(
                content=content,
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        } for tool_call in assistant_message.tool_calls
                    ]
                }
            )
        else:
            content = assistant_message.content or "No response content"
            message = AIMessage(content=content)
        
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    def _stream(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, 
               run_manager: Optional[Any] = None, **kwargs) -> Iterator[ChatGeneration]:
        """流式生成（简化版）"""
        result = self._generate(messages, stop, run_manager, **kwargs)
        yield result.generations[0]
    
    def _convert_messages_to_openai_format(self, messages: List[BaseMessage]) -> List[Dict]:
        """将LangChain消息格式转换为OpenAI格式"""
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                # 处理工具调用结果
                if hasattr(msg, 'additional_kwargs') and 'tool_calls' in msg.additional_kwargs:
                    formatted_messages.append({
                        "role": "assistant", 
                        "content": msg.content,
                        "tool_calls": msg.additional_kwargs['tool_calls']
                    })
                else:
                    formatted_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                formatted_messages.append({"role": "system", "content": msg.content})
            else:
                formatted_messages.append({"role": "user", "content": str(msg.content)})
        return formatted_messages
    
    def invoke_with_tool_call(self, messages: List[BaseMessage], max_iterations: int = 20) -> AIMessage:
        """支持函数调用的对话方法 - 严格按照OpenAI格式"""
        current_messages = self._convert_messages_to_openai_format(messages)
        
        for iteration in range(max_iterations):
            logger.info(f"第 {iteration + 1} 轮对话")
            
            # 调用模型
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=current_messages,
                tools=tools
            )
            
            assistant_message = response.choices[0].message
            
            # 如果没有工具调用，直接返回
            if not assistant_message.tool_calls:
                logger.info("无需调用工具，直接返回回复")
                return AIMessage(content=assistant_message.content or "")
            
            # 添加AI的工具调用消息到历史
            current_messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    } for tool_call in assistant_message.tool_calls
                ]
            })
            
            # 处理每个工具调用
            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}
                
                logger.info(f"调用工具 [{func_name}]，参数: {arguments}")
                
                # 执行工具函数
                if func_name in tool_functions:
                    try:
                        # 根据参数数量调用函数
                        if arguments:
                            tool_result = tool_functions[func_name](**arguments)
                        else:
                            tool_result = tool_functions[func_name]()
                        logger.info(f"工具返回: {tool_result}")
                    except Exception as e:
                        tool_result = f"工具调用失败: {str(e)}"
                        logger.error(f"工具调用异常: {e}")
                else:
                    tool_result = f"未知工具: {func_name}"
                    logger.warning(f"未知工具: {func_name}")
                
                # 严格按照OpenAI格式添加工具结果消息
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
        
        # 最后一次调用获取最终回复
        final_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=current_messages,
            tools=tools
        )
        
        final_content = final_response.choices[0].message.content or ""
        logger.info(f"最终回复: {final_content}")
        return AIMessage(content=final_content)
    
    def invokeConversation(self, prompt, history=[]):
        """原有的对话方法，保持兼容性"""
        if history is None:
            history = []
        
        # 处理prompt参数 Langchain 转换openai格式
        if isinstance(prompt, list) and prompt and hasattr(prompt[0], 'type'):
            processed_prompt = []
            for msg in prompt:
                role = msg.type
                if role == "human":
                    role = "user"
                elif role == "ai":
                    role = "assistant"
                processed_prompt.append({"role": role, "content": msg.content})
            history.extend(processed_prompt)
        else:
            # 如果是单个消息，直接添加
            if isinstance(prompt, str):
                history.append({"role": "user", "content": prompt})
            else:
                history.append(prompt)
            
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=history
        )
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            content = response.choices[0].message.content
        else:
            content = "No response content"

        return AIMessage(content=content)
    
    def streamConversation(self, prompt, history=[]):
        """流式对话方法"""
        if history is None:
            history = []
            
        # 处理prompt参数 Langchain 转换openai格式
        if isinstance(prompt, list) and prompt and hasattr(prompt[0], 'type'):
            processed_prompt = []
            for msg in prompt:
                role = msg.type
                if role == "human":
                    role = "user"
                elif role == "ai":
                    role = "assistant"
                processed_prompt.append({"role": role, "content": msg.content})
            history.extend(processed_prompt)
        else:
            history.append(prompt)
            
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=history,
            stream=True
        )

        reasoning_content = ""
        answer_content = ""
        is_answering = False
        
        for chunk in response:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            
            if hasattr(delta, 'content') and delta.content is not None:
                if not is_answering:
                    is_answering = True
                answer_content += delta.content
        
        if reasoning_content:
            full_content = f"思考过程：{reasoning_content}\n\n最终回答：{answer_content}"
        else:
            full_content = answer_content
            
        return AIMessage(content=full_content)