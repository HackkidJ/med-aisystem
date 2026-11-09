from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
import os


# 1. 获取当前脚本所在的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 拼接出 Knowledge 文件夹的绝对路径
knowledge_dir = os.path.join(current_dir, "Knowledge")

loader = DirectoryLoader(
    path=knowledge_dir,
    glob='**/*.pdf',
    loader_cls=PyPDFLoader,
    show_progress=True,
    use_multithreading=True
)

documents = loader.load()

for doc in documents:
    source_path = doc.metadata.get("source","")

    path_parts = source_path.replace("\\","/").split("/")
    if len(path_parts) >= 3:
        department = path_parts[-2]
        doc.metadata["department"] = department

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)

chunks = text_splitter.split_documents(documents)

DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")


embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY
)

db_path = "./faiss_index"



print("正在将文本块转化为向量存入数据库....")
try:
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )
    vectorstore.save_local(db_path)
    # test
    # print("\n🔍 测试检索：急性胰腺炎该怎么处理？")
    # results = vectorstore.similarity_search("急性胰腺炎该怎么处理？", k=2)
    # for i, res in enumerate(results):
    #     print(f"\n--- 结果 {i+1} ---")
    #     print(f"科室：{res.metadata.get('department')}")
    #     print(f"内容：{res.page_content[:150]}...")


except Exception as e:
    print(f"错误类型：{type(e).__name__}")
    print(f"详细原因：{str(e)}")

# #索引测试
# query = "患者暴饮暴食后上腹部剧痛，放射到后背，该怎么处理？"
# print(f"\n🔍 正在检索相关问题：{query}")

# # 搜索最相似的 3 个文本块
# results = vectorstore.similarity_search(query, k=3)

# for i, res in enumerate(results):
#     print(f"\n--- 检索结果 {i+1} ---")
#     print(f"来源科室：{res.metadata.get('department')}")
#     print(f"内容片段：{res.page_content[:150]}...")

# print(f"✅ 切分完成！共生成 {len(chunks)} 个文本块（Chunks）。")

# # 3. 打印前两个块看看效果，检查科室标签还在不在
# for i, chunk in enumerate(chunks[:2]):
#     print(f"\n--- 第 {i+1} 块 ---")
#     print(f"文本内容：{chunk.page_content[:100]}...") # 只打印前100个字
#     print(f"元数据：{chunk.metadata}")

# print(f"成功读取了 {len(documents)} 页 PDF 内容。")
# print(f"第一页的元数据标签看看：{documents[0].metadata}")