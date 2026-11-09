
import os
import pdfplumber


def readPdf(path:str) -> str:
    """
        调用该函数传入完整路径 返回pdf文本内容 作为你的参考资料 去回答用户问题
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join("e:/source_design/MedAgent", path)
    
    # 检查路径是否存在
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"文件不存在: {full_path}")
    content = ""
    with pdfplumber.open(full_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            content += f"第{i+1}页:\n{text}\n\n"
    return content



if __name__ == "__main__":
    print(readPdf("Agent\\knowledges\\pdfs\\医学教材\\儿科学\\新生儿疾病.pdf"))