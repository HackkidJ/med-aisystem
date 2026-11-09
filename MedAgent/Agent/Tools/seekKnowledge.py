from typing import List,Dict,Optional
import os


def find_folders_from_knowledges():
    """
        第一步先调用该函数 定位到知识库中
    """
    knowledges_path = "Agent\\knowledges\\pdfs\\医学教材"
    os.chdir(knowledges_path)
    print(os.listdir())
    
def get_listdir()->List[str]:
    """
        调用该函数 列出文件夹中的文件 找到你需要的文件或文件夹
    """
    return os.listdir()

def chdir(folder_name:str):
    """
        找到你需要的文件夹名字后 调用该函数传入文件夹的名字进入该路径
    """
    os.chdir(folder_name)

def form_complete_path(subject,file):
    """
        最后找到需要参考的pdf文件 调用该函数形成完整的路径 再用pdf阅读的函数 读取pdf中的内容
    """
    return "Agent/knowledges/pdfs/医学教材/"+subject+"/"+file