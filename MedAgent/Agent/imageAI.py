import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

class MedicalImageDiagnosis:
    def __init__(self, api_key=None, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化医学影像诊断类
        
        Args:
            api_key: DashScope API密钥，如果为None则从环境变量读取
            base_url: API基础URL
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        self.base_url = base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        self.ai_character = '你是一名经验丰富的医生'
        self.requirement = '请你作为一名有经验的医生，对提交的医学光片进行诊断'
        self.reasoning_content = ""  # 存储完整的思考过程
        
    def encode_image_from_bytes(self, image_bytes, image_format="png"):
        """
        将图片二进制数据编码为base64
        
        Args:
            image_bytes: 图片的二进制数据
            image_format: 图片格式，如png、jpg等
            
        Returns:
            base64编码的图片字符串
        """
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return base64_image
    
    def encode_image_from_file(self, image_path):
        """
        从文件路径编码图片为base64
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            base64编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def diagnose_from_bytes(self, image_bytes, image_format="png", custom_requirement=None):
        """
        从图片二进制数据进行医学影像诊断
        
        Args:
            image_bytes: 图片的二进制数据
            image_format: 图片格式
            custom_requirement: 自定义诊断要求，如果为None则使用默认要求
            
        Returns:
            str: 诊断结果（不包含思考过程）
        """
        # 重置思考过程
        self.reasoning_content = ""
        
        # 编码图片
        base64_image = self.encode_image_from_bytes(image_bytes, image_format)
        
        # 使用自定义要求或默认要求
        requirement = custom_requirement or self.requirement
        
        try:
            completion = self.client.chat.completions.create(
                model="qvq-max",
                messages=[  
                    {"role": "system", "content": self.ai_character},
                    {"role": "user", "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/{image_format};base64,{base64_image}"},
                         },
                        {"type": "text", "text": requirement},
                    ]},
                ],
                stream=True,
            )
            
            return self._process_stream_completion(completion)
            
        except Exception as e:
            raise Exception(f"诊断过程中发生错误: {str(e)}")
    
    def diagnose_from_file(self, image_path, custom_requirement=None):
        """
        从图片文件进行医学影像诊断
        
        Args:
            image_path: 图片文件路径
            custom_requirement: 自定义诊断要求
            
        Returns:
            str: 诊断结果（不包含思考过程）
        """
        # 获取文件扩展名作为图片格式
        image_format = image_path.split('.')[-1].lower()
        if image_format == 'jpg':
            image_format = 'jpeg'
            
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            
        return self.diagnose_from_bytes(image_bytes, image_format, custom_requirement)
    
    def _process_stream_completion(self, completion):
        """
        处理流式响应，分离思考过程和最终回复
        
        Args:
            completion: 流式响应对象
            
        Returns:
            str: 诊断结果（不包含思考过程）
        """
        reasoning_content = ""
        answer_content = ""
        is_answering = False
        
        for chunk in completion:
            if not chunk.choices:
                continue
                
            delta = chunk.choices[0].delta
            
            # 处理思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            
            # 处理最终回复
            if hasattr(delta, 'content') and delta.content is not None:
                if not is_answering:
                    is_answering = True
                answer_content += delta.content
        
        # 保存完整的思考过程到实例变量
        self.reasoning_content = reasoning_content
        
        return answer_content
    
    def get_reasoning_content(self):
        """
        获取完整的思考过程
        
        Returns:
            str: 完整的思考过程内容
        """
        return self.reasoning_content
    
    def set_ai_character(self, character_description):
        """
        设置AI角色描述
        
        Args:
            character_description: 角色描述字符串
        """
        self.ai_character = character_description
    
    def set_requirement(self, requirement_text):
        """
        设置诊断要求
        
        Args:
            requirement_text: 诊断要求文本
        """
        self.requirement = requirement_text



if __name__ == "__main__":

    diagnosis = MedicalImageDiagnosis()
    
    #  从文件诊断
    try:
        result = diagnosis.diagnose_from_file("E:/source_design/MedAgent/Agent/Temp/fructure.png")
        print("诊断结果:", result)
        print("思考过程:", diagnosis.get_reasoning_content())  # 可以单独获取思考过程
    except Exception as e:
        print(f"诊断失败: {e}")
    
    # 从二进制数据诊断
    try:
        with open("E:/source_design/MedAgent/Agent/Temp/fructure.png", "rb") as f:
            image_bytes = f.read()
        
        # 使用自定义诊断要求
        custom_req = "请详细分析这张X光片中的骨骼结构，特别注意是否有骨折迹象"
        result = diagnosis.diagnose_from_bytes(image_bytes, "png", custom_req)
        print("诊断结果:", result)
        # 思考过程已存储在 diagnosis.reasoning_content 中
    except Exception as e:
        print(f"诊断失败: {e}")