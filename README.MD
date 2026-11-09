# 🏥 AI 辅助诊疗系统

## 📖 项目简介
本项目是一个面向临床医生端的全栈 AI 辅助决策系统。医生输入患者的非结构化主诉后，系统基于本地医学指南知识库，提供结构化的病历提取、鉴别诊断与临床建议。

## 🛠️ 技术架构（三端分离）
*   **前端**：Vue3 ，负责医生端交互与流式输出渲染。(SSE在当前版本未实现)
*   **业务后端**：Spring Boot + MyBatis + MySQL，负责患者管理、鉴权与核心业务逻辑。
*   **AI 服务端**：Python + FastAPI + LangChain，负责大模型接入与 RAG 检索。

## ✨ 核心亮点
*   **混合检索 (Hybrid Search)**：为了解决大模型在医疗领域的“幻觉”问题，我封装了 `HybridRetriever` 检索器。
    *   结合 **FAISS**（向量语义检索）与 **BM25**（关键词精确匹配）。
    *   引入 **RRF (倒数排名融合)** 算法对两路结果进行重排，大幅提升了对医学术语的召回准确率。
*   **多智能体工具调用 (Function Calling)**：基于大模型的 Agent 能力，实现了自动查阅本地知识库、对患者信息CRUD等工具调度。
*   **工程化重构**：排查并解决了 ChromaDB 在 Windows 环境下的底层 C++ 库崩溃问题，平滑切换为 FAISS 以保障系统稳定性。
*   **账户安全性设计**：对账户密码不采用明文存储，使用加盐哈希算法进行加密。

## 🚀 快速启动指南 
1. **前端**：在'medaisystem'路径下 `npm install` -> `npm run serve`
2. **业务后端**：导入 `db.sql` 至 MySQL，修改 `application.yml` 中的数据库配置，运行 SpringBoot 启动类。
3. **AI 服务端**：`cd medagent` -> `pip install -r requirements.txt` -> 在 `.env` 文件中配置 `DASHSCOPE_API_KEY`（通义千问的KEY） -> 运行`server.py`

## 🔒 安全说明
本项目源码已进行脱敏处理，未包含任何真实的大模型 API Key 或数据库密码，请自行配置 `.env` 文件。