import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from langchain_core.prompts import ChatPromptTemplate
from Tongyi import TongyiChat
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from chatAgent import ChatAgent
from imageAI import MedicalImageDiagnosis

#配置日志
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)

class AIDoctorService: 
    def __init__(self, springboot_base_url:str,session_timeout:int = 1800):
        """
            初始化ai医生服务

            Args：
            springboot_base_url:Springboot服务器基础url
            session_timeout:会话超时时间(s)
        """

        self.imageAI = MedicalImageDiagnosis()
        self.springboot_base_url = springboot_base_url
        self.session_timeout = session_timeout
        self.session_id = None
        self.conversation_turn = 0
        self.last_activity_time = None
        self.agent = None
        #重试机制
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1, #退避因子 控制重试间隔时间
            status_forcelist=[429,500,502,503,504]
        )
        #应用重试机制
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://",adapter)
        self.session.mount("https://",adapter)

    def start_session(self,doctor_info:Dict,request_id:str,callback_url:str) -> bool:
        """
        开始新的对话会话
        
        Args:
            医生_info: 患者信息
            
        Returns:
            bool: 是否成功建立会话
        """
        try:
            # 生成会话ID
            self.session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(str(doctor_info))}"
            doc_id = doctor_info.get("id")
            self.agent = ChatAgent(doc_id=doc_id)
            greeting_message = self.agent.conversation(" ")
            
            # 构建问候消息数据
            callback_data = {
                "requestId": request_id,  # 关键：包含请求ID
                "sessionId": self.session_id,
                "messageType": "GREETING",
                "content": greeting_message,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "sessionId": self.session_id,
                    "content": greeting_message,
                    "type": "GREETING"
                }
            }
            
            # 发送POST请求到SpringBoot服务器
            response = self.session.post(
                callback_url,
                json=callback_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                logger.info(f"会话 {self.session_id} 启动成功 已回调springboot")
                self.last_activity_time = datetime.now()
                return (True,self.session_id)
            else:
                logger.error(f"回调springboot失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"启动会话时发生错误: {str(e)}")
            return False
    
    def _is_session_timeout(self) -> bool:
        """检查会话是否超时"""
        if not self.last_activity_time:
            return True
        
        elapsed_time = (datetime.now() - self.last_activity_time).total_seconds()
        return elapsed_time > self.session_timeout

    def process_user_message(self,user_input:str,requestId:str) ->Optional[Dict]:
        """
        处理用户输入并返回AI医生的回复
        
        Args:
            user_input: 用户输入的消息
            patient_info: 患者信息
            
        Returns:
            Dict: 包含AI回复的数据，如果失败返回None
        """
        try:
            if self._is_session_timeout():
                logger.warning(f"会话{self.session_id}超时")
                self.end_session("SESSION_TIMEOUT")
                self.agent.chat_history()
                self.conversation_turn = 0
                return None
            
            self.last_activity_time = datetime.now()
            reply = self.agent.conversation(user_input)
            self.conversation_turn += 1
            result_data = {
                "requestId":requestId,
                "sessionId":self.session_id,
                "messageType":"AI_RESPONSE",
                "content":reply,
                "timestamp":datetime.now().isoformat(),
                "conversationTurn": self.conversation_turn
            }

            #springboot 接口
            response = self.session.post(
                f"{self.springboot_base_url}/api/ai/message-callback",
                json = result_data,
                headers={"Content-Type":"application/json"}
                )

            if response.status_code == 200:
                logger.info(f"消息处理成功，会话id:{self.session_id}")
                return result_data
            else:
                logger.info(f"消息发送失败：{response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"处理用户消息时发生错误：{str(e)}")
            self._send_error_message(f"处理消息时发生错误：{str(e)}")
            return None
        
    def _send_error_message(self, error_message: str):
        """发送错误消息到SpringBoot服务器"""
        try:
            error_data = {
                "sessionId": self.session_id,
                "messageType": "ERROR",
                "content": error_message,
                "timestamp": datetime.now().isoformat()
            }
            
            #springboot api
            self.session.post(
                f"{self.springboot_base_url}/api/ai/error",
                json=error_data,
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            logger.error(f"发送错误消息失败: {str(e)}")

    def end_session(self,reason:str = "USER_REQUEST") -> bool:
        """
        结束当前会话
        
        Args:
            reason: 结束原因
            
        Returns:
            bool: 是否成功结束会话
        """
        try:
            end_data = {
                "sessionId":self.session_id,
                "endReason":reason,
                "endTime":datetime.now().isoformat(),
                "turns":self.conversation_turn,
            }

            response = self.session.post(
                f"{self.springboot_base_url}/api/ai/end_session",
                json=end_data,
                headers={"Content-Type:":"application/json"}
            )

            if response.status_code == 200:
                logger.info(f"会话{self.session_id}结束成功，原因{reason}")
                self._cleanup_session()
                return True
            else:
                logger.error(f"结束会话失败: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"结束会话时发生错误：{str(e)}")
            return False
    
    def _cleanup_session(self):
        """清理会话数据"""
        self.session_id = None
        self.conversation_history = 0
        self.last_activity_time = None

