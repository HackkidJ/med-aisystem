import base64
import aiohttp
from fastapi import FastAPI,HTTPException,BackgroundTasks
from pydantic import BaseModel
from typing import Dict
from imageAI import MedicalImageDiagnosis
from service import AIDoctorService
import logging
from datetime import datetime,timedelta
import asyncio
import sys

app = FastAPI(title="Ai医生服务api")

active_sessions:Dict[str,AIDoctorService] = {}

class StartSessionRequest(BaseModel):
    doctorInfo:Dict

class UserMessageRequest(BaseModel):
    sessionId:str
    userInput:str
    requestId:str

class EndSessionRequest(BaseModel):
    sessionId:str
    reason: str = "USER_REQUEST"


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler('ai_service.log')
                    ])
logger = logging.getLogger(__name__)
tool_logger = logging.getLogger('tool_calls')
tool_logger.setLevel(logging.INFO)

@app.post("/start-session")
async def start_session(request:dict):
    """Python服务器的start-session端点"""
    try:
        ai_service = AIDoctorService(springboot_base_url="http://localhost:8081")
        doctor_info = request.get("doctorInfo", {})
        request_id = request.get("requestId")
        callback_url = request.get("callbackUrl")
        
        logger.info(f"收到SpringBoot启动会话请求，requestId: {request_id}")
        
        # 调用业务逻辑
        success = ai_service.start_session(doctor_info, request_id, callback_url)
        active_sessions[success[1]] = ai_service
        return {"success": success[0], "message": "正在处理会话启动"}
        
    except Exception as e:
        logger.error(f"处理启动会话请求失败: {str(e)}")
        return {"success": False, "message": str(e)}
    
@app.post("/process-message")
async def process_message(request:UserMessageRequest):
    try:
        if request.sessionId not in active_sessions:
            raise HTTPException(status_code=404,detail="会话不存在或已过期")
        
        ai_service = active_sessions[request.sessionId]
        result = ai_service.process_user_message(request.userInput,request.requestId)

        if result:
            return{"success":True,"data":result}
        else:
            raise HTTPException(status_code=500,detail="处理消息失败")

    except Exception as e:
        logger.error(f"处理消息api错误：{str(e)}")
        raise HTTPException(status_code=500,detail=str(e))

@app.post("/image-diagnosis")
async def image_diagnosis(request:dict):
    try:
        doctor_info = request.get("doctorInfo", {})
        request_id = request.get("requestId")
        image_data = request.get("imageData")
        image_name = request.get("imageName")
        content_type = request.get("contentType")
        callback_url = request.get("callbackUrl")
        logger.info(f"收到医学影像诊断请求，请求ID: {request_id}")
        logger.info(f"医生信息: {doctor_info}")
        logger.info(f"图片名称: {image_name}")
        
        # 将base64图片数据转换为二进制
        image_bytes = base64.b64decode(image_data)
        
        # 调用之前封装的MedicalImageDiagnosis类
        diagnosis = MedicalImageDiagnosis()
        result = diagnosis.diagnose_from_bytes(image_bytes)
        
        # 构建返回数据
        result_data = {
            "requestId": request_id,
            "content": result,
            "type": "IMAGE_DIAGNOSIS",
            "timestamp": datetime.now().isoformat(),
            "imageName": image_name
        }

        # 发送回调到SpringBoot
        callback_payload = {
            "requestId": request_id,
            "data": result_data,
            "timestamp": datetime.now().isoformat()
        }
        asyncio.create_task(send_callback(callback_url,callback_payload))
        
        return {"success": True, "data": "图像诊断处理中，请等待回调"}
        
    except Exception as e:
        logger.error(f"医学影像诊断处理失败: {str(e)}")
        return {"success": False, "message": str(e)}

async def send_callback(callback_url: str, payload: dict):
    """异步发送回调请求"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(callback_url, json=payload) as response:
                if response.status == 200:
                    logger.info(f"回调发送成功，请求ID: {payload['requestId']}")
                else:
                    logger.error(f"回调发送失败，状态码: {response.status}")
    except Exception as e:
        logger.error(f"发送回调时发生错误: {str(e)}")

@app.post("/end-session")
async def end_session(request:EndSessionRequest):
    try:
        if request.sessionId not in active_sessions:
            return {"success":False,"message":"会话不存在"}
        
        ai_service = active_sessions[request.sessionId]
        success = ai_service.end_session(request.reason)
        
        if success:
            del active_sessions[request.sessionId]
            return {"success":True,"message":"会话结束成功"}
        else:
            raise HTTPException(status_code=500,detail="会话结束失败")
    
    except Exception as e:
        logger.error(f"结束会话api错误:{str(e)}")
        raise HTTPException(status_code=500,detail=str(e))

#会话状态检查
@app.get("/health")
async def health_check():
    return {"status":"healthy","timestamp":datetime.now().isoformat()}

#后台任务：清理会话
async def cleanup_expired_sessions():
    while True:
        try:
            current_time = datetime.now()
            expired_sessions = []

            for session_id , ai_service in active_sessions.items():
                if ai_service._is_session_timeout():
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                logger.info(f"清理过期会话：{session_id}")
                ai_service = active_sessions[session_id]
                ai_service.end_session("SESSION_TIMEOUT")
                del active_sessions[session_id]
            
            await asyncio.sleep(300) #300秒检查一次
        
        except Exception as e:
            logger.error(f"清理会话任务错误：{str(e)}")
            await asyncio.sleep(60) #60秒后重试
    
@app.on_event("startup")
async def start_event():
    asyncio.create_task(cleanup_expired_sessions())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8082)
