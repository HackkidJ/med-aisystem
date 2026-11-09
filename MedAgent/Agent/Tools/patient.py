import requests
import json
import logging

def getPatientByName(name):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s',force=True)
    logger = logging.getLogger('tool_calls')
    logger.info("正在尝试通过身份证号获取患者信息")
    logger.info(f"📋 参数: name={name}")
    """
        当你需要知道某个患者的信息，但你只有姓名，就通过该函数来获取,注意该函数可能返回重名的人多个结果
        具体是哪一个人 你可以询问医生
        name:姓名（必填）
    """
    url = "http://localhost:8081/medsystem/patient/getPatientByName"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "name":name
    }
    logger.info("正在发起请求")
    print("🔄 正在发送请求到后端...")
    try:
        response = requests.get(url,params=params,headers=headers,timeout=30)
        logger.info(f"请求结果：{response.status_code}")
        if response.status_code == 200:
            patient = response.json()
            logger.info(f"获取到患者信息{patient}")
            return patient
        else:
            logger.error(f"获取患者信息失败，状态码: {response.status_code}")
            print(f"❌ 获取患者信息失败，状态码: {response.status_code}")
            if response.status_code == 404:
                return "未找到该身份证号对应的患者信息"
            elif response.status_code == 403:
                return "权限不足，无法访问患者信息"
            else:
                return f"请求失败，状态码: {response.status_code}"
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return "请求超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        logger.error("连接错误")
        return "无法连接到服务器，请检查网络连接"
    except Exception as e:
        logger.error(f"异常：{e}")
        return f"请求异常: {str(e)}"

def getPatientById(identityId):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s',force=True)
    logger = logging.getLogger('tool_calls')
    logger.info("正在尝试通过身份证号获取患者信息")
    logger.info(f"📋 参数: identityId={identityId}")
    """
        当你需要知道某个患者的信息，但你只有身份证号码，就通过该函数来获取
        identityId:身份证号（必填）
    """
    url = "http://localhost:8081/medsystem/patient/getPatientById"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
         "identityId":identityId
    }
    logger.info("正在发起请求")
    print("🔄 正在发送请求到后端...")
    try:
        response = requests.get(url,params=params,headers=headers,timeout=30)
        logger.info(f"请求结果：{response.status_code}")
        if response.status_code == 200:
            patient = response.json()
            logger.info(f"成功获取患者信息：{patient}")
            return patient

        else:
            logger.error(f"获取患者信息失败，状态码: {response.status_code}")
            print(f"❌ 获取患者信息失败，状态码: {response.status_code}")
            if response.status_code == 404:
                return "未找到该身份证号对应的患者信息"
            elif response.status_code == 403:
                return "权限不足，无法访问患者信息"
            else:
                return f"请求失败，状态码: {response.status_code}"
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return "请求超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        logger.error("连接错误")
        return "无法连接到服务器，请检查网络连接"
    except Exception as e:
        logger.error(f"异常：{e}")
        return f"请求异常: {str(e)}"



def addPatient(identityId,name,gender,doc_id,phone=None,address=None,PMH=None,PI=None,CC=None):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s',force=True)
    logger = logging.getLogger('tool_calls')
    print("🎯 addPatient函数被调用!")
    print(f"📋 参数: identityId={identityId}, name={name}, gender={gender}, doc_id={doc_id}")
    logger.info("该函数已调用")
    logger.info(f"📋 参数: identityId={identityId}, name={name}, gender={gender}, doc_id={doc_id}")
    logger.info(f"📞 电话: {phone}, 地址: {address}")
    """
        这个函数用来向数据库添加病患信息
        identityId:身份证号 (必填)
        name:姓名 (必填)
        gender:性别 (男/女) (必填)
        phone:电话号码
        address:家庭住址
        PMH:既往病史
        PI:现病史
        CC:主诉
        doc_id:主治医生的id即与你对话的医生的id (必填) 

        以上参数除了标记有必填的参数 其他都可以传入空值
    """
    url = "http://localhost:8081/medsystem/patient/addPatient"
    # url = "https://29ae5f0e9729.ngrok-free.app/medsystem/patient/addPatient"
     
    payload = {
    "patient_data":{
        "identityId": identityId,
        "name": name,
        "gender": gender,  # 枚举类型，确保和后端Gender枚举一致
        "phone": phone,
        "address": address,
        "pmh": PMH,
        "pi": PI,
        "cc": CC,
        "doc_id": doc_id
    },
    "isAI":True}


    headers = {
        "Content-Type": "application/json"
    }
    logger.info("正在发起录入请求")
    print("🔄 正在发送请求到后端...")
    try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            logger.info(f"录入结果: {response.status_code}")
            print(f"✅ 请求完成，状态码: {response.status_code}")
            
            # 打印响应内容
            if response.status_code != 201:
                print(f"❌ 错误响应: {response.text}")
            else:
                print("🎉 患者信息添加成功!")
                
            return response.status_code
    except Exception as e:
            logger.error(f"请求异常: {e}")
            print(f"💥 请求异常: {e}")
            return 500
    
def updatePatient(identityId, name=None, gender=None, phone=None, address=None, PMH=None, PI=None, CC=None, doc_id=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s', force=True)
    logger = logging.getLogger('tool_calls')
    logger.info("正在尝试修改患者信息")
    logger.info(f"📋 参数: identityId={identityId}, name={name}, gender={gender}, phone={phone}, address={address}")
    
    """
    当你需要修改患者信息时，使用该函数
    identityId: 身份证号（必填，用于识别患者）
    其他参数：需要修改的字段（可选）
    """
    url = "http://localhost:8081/medsystem/patient/updatePatient"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 构建请求数据
    patient_data = {
        "identityId": identityId
    }
    
    # 只添加非空的字段
    if name is not None:
        patient_data["name"] = name
    if gender is not None:
        patient_data["gender"] = gender
    if phone is not None:
        patient_data["phone"] = phone
    if address is not None:
        patient_data["address"] = address
    if PMH is not None:
        patient_data["PMH"] = PMH
    if PI is not None:
        patient_data["PI"] = PI
    if CC is not None:
        patient_data["CC"] = CC
    if doc_id is not None:
        patient_data["doc_id"] = doc_id
    
    payload = {
        "patient_data": patient_data,
        "isAI": True
    }
    
    logger.info("正在发起修改请求")
    print("🔄 正在发送修改请求到后端...")
    
    try:
        response = requests.patch(url, json=payload, headers=headers, timeout=30)
        logger.info(f"修改结果：{response.status_code}")
        
        if response.status_code == 200:
            patient_data = response.json()
            logger.info(f"成功修改患者信息")
            return f"患者信息修改成功: {patient_data}"
        else:
            logger.error(f"修改患者信息失败，状态码: {response.status_code}")
            if response.status_code == 404:
                return "未找到该身份证号对应的患者信息"
            else:
                return f"修改失败，状态码: {response.status_code}"
                
    except Exception as e:
        logger.error(f"异常：{e}")
        return f"请求异常: {str(e)}"
if __name__ == "__main__":
    # addPatient("512230200450021130","ak","男","4231313","asdld","","","","asd123sad")
    print(getPatientById("123230200408040456"))