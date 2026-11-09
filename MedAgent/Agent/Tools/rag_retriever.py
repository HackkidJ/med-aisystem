import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List
from pydantic import Field
from langchain_text_splitters import RecursiveCharacterTextSplitter

class HybridRetriever:
    """
    混合检索器：向量语义检索+BM25关键词检索
    """
    # vector_store: FAISS = Field(description="FAISS向量数据库实例")
    # bm25_retriever: BM25Retriever = Field(description="BM25检索器实例")
    # k: int = Field(default=3, description="返回的最终文档数量")
    def __init__(self, vector_store: FAISS, bm25_retriever: BM25Retriever, k: int = 3):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.k = k

    def _get_relevant_document(self,query:str,*,run_manager=None) -> List[Document]:
        
        # 向量检索
        vector_docs = self.vector_store.similarity_search(query,k=5)

        # BM25检索
        bm25_docs = self.bm25_retriever.invoke(query)

        # RRF倒数排名 打分排名 1/（rank+60）
        rrf_score = {}
        doc_map = {}

        # 处理向量检索结果
        for rank, doc in enumerate(vector_docs):
            doc_id = doc.page_content
            doc_map[doc_id] = doc
            rrf_score[doc_id] = rrf_score.get(doc_id,0) + (1.0 / (rank + 60))

        # 处理BM25 检索结果
        for rank, doc in enumerate(bm25_docs):
            doc_id = doc.page_content
            doc_map[doc_id] = doc
            rrf_score[doc_id] = rrf_score.get(doc_id, 0) + (1.0 / (rank + 60))
        
        # 融合后分数降序排序
        sorted_docs = sorted(rrf_score.items(), key=lambda x:x[1], reverse=True)

        # 取出Top K
        final_docs = [doc_map[doc_id] for doc_id, score in sorted_docs[:self.k]]

        return final_docs
    
    def build_hybrid_retriever(chunks: List[Document], embeddings, faiss_path="./faiss_index"):
        """
        构建混合检索器的工厂函数
        """
        print(" 初始化混合检索器...")

        if os.path.exists(faiss_path):
            vector_store = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)

        else:
            vector_store = FAISS.from_documents(chunks, embeddings)
            vector_store.save_local(faiss_path)
        
        bm25_retriever = BM25Retriever.from_documents(chunks)
        bm25_retriever.k = 5

        hybrid_retriever = HybridRetriever(
            vector_store=vector_store,
            bm25_retriever=bm25_retriever,
            k=3
        )

        print("混合检索器构建完成！")
        return hybrid_retriever

    def invoke(self, query: str) -> List[Document]:
        # 1. 向量检索：搜索 Top 5
        vector_docs = self.vector_store.similarity_search(query, k=5)
        
        # 2. BM25 检索：搜索 Top 5
        bm25_docs = self.bm25_retriever.invoke(query)
        
        # 3. RRF (Reciprocal Rank Fusion) 倒数排名融合算法
        rrf_score = {}
        doc_map = {}

        # 处理向量检索结果
        for rank, doc in enumerate(vector_docs):
            doc_id = doc.page_content
            doc_map[doc_id] = doc
            rrf_score[doc_id] = rrf_score.get(doc_id, 0) + (1.0 / (rank + 60))

        # 处理 BM25 检索结果
        for rank, doc in enumerate(bm25_docs):
            doc_id = doc.page_content
            doc_map[doc_id] = doc
            rrf_score[doc_id] = rrf_score.get(doc_id, 0) + (1.0 / (rank + 60))

        # 按照融合后的分数降序排序
        sorted_docs = sorted(rrf_score.items(), key=lambda x: x[1], reverse=True)
        
        # 取出 Top K
        final_docs = [doc_map[doc_id] for doc_id, score in sorted_docs[:self.k]]
        
        return final_docs

retriever_instance = None

# 单例模式检索器
def get_retriever():
    global retriever_instance
    if retriever_instance is not None:
        return retriever_instance
        
    print(" 正在加载 RAG 知识库...")

    current_file_path = os.path.abspath(__file__) # 获取 rag_retriever.py 的绝对路径
    tools_dir = os.path.dirname(current_file_path)
    project_root = os.path.dirname(os.path.dirname(tools_dir)) 
    
    # 拼接出真正的 Knowledge 和 faiss_index 路径
    knowledge_path = os.path.join(project_root, "Knowledge")
    faiss_path = os.path.join(project_root, "faiss_index")
    
    print(f" 找到知识库路径: {knowledge_path}")
    print(f" 找到 FAISS 路径: {faiss_path}")
    # 1. 初始化 Embedding (用通义的)
    from langchain_community.embeddings import DashScopeEmbeddings
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v4",
        dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
    )
    
    # 2. 加载 FAISS 向量库
    faiss_path = "./faiss_index"
    vector_store = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)

    # 3. 使用init_db脚本的获取原始chunks方法 用来重建BM25
    project_root = os.path.join(project_root,"Agent")
    knowledge_dir = os.path.join(project_root, "Knowledge")

    print(f"知识库路径为:{knowledge_dir}")

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

    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5

    retriever_instance = HybridRetriever(
        vector_store=vector_store,
        bm25_retriever=bm25_retriever,
        k=3
    )
    print("RAG知识库加载完成")
    return retriever_instance
    