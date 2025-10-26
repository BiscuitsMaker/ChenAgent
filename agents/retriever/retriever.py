from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import config
import os
from langchain.tools import Tool

def get_file_mtime(path: str) -> float:
    return os.path.getatime(path) if os.path.exists(path) else 0

def get_db_mtime(db_path: str) -> float:
    if not os.path.exists(db_path):
        return 0
    meta_path = os.path.join(db_path, "chroma.sqlite3")
    return os.path.getatime(meta_path) if os.path.exists(meta_path) else 0

def build_or_load_retriever(force_rebuild: bool = False):
    db_path = config.RAG_DB_PATH
    data_path = config.RAG_DATA_PATH
    embeddings = OpenAIEmbeddings(
        api_key = config.OPENAI_API_KEY,
        base_url = config.OPENAI_BASE_URL
    )

    # 判断是否需要重建
    file_mtime = get_file_mtime(data_path)
    db_mtime = get_db_mtime(db_path)

    need_rebuild = (
        force_rebuild or
        not os.path.exists(db_path) or
        not os.listdir(db_path) or
        file_mtime > db_mtime  # 文档更新后时间比数据库新
    )

    if need_rebuild and config.RAG_NEED_REBUILD:
        print("检测到数据库缺失或文档更新，开始重建向量库...")
        loader = TextLoader(data_path, encoding="utf-8")  
        documents = loader.load()  # 加载数据

        splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.RAG_CHUNK_SIZE,
            chunk_overlap = config.RAG_CHUNK_OVERLAP
        )
        texts = splitter.split_documents(documents)  # 切分数据

        vectorstore = Chroma.from_documents(
            documents = texts,
            embedding = embeddings,
            persist_directory = db_path
        )
        vectorstore.persist()
        print("向量数据库已经重建并保存")
    else:
        print("向量数据库已经最新，直接加载")
        vectorstore = Chroma(
            persist_directory = db_path,
            embedding_function = embeddings
        )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": config.RAG_TOP_K}
    )
    return retriever

def make_retriever_tool(retriever):
    def search_docs(query: str) -> str:
        try:
            docs = retriever.get_relevant_documents(query)
            if not docs:
                return "【没有检索到相关内容】"
            # 只返回前3个文本内容拼接
            return "\n\n".join([d.page_content for d in docs[:3]])
        except Exception as e:
            return f"【检索出错：{e}】"

    return Tool(
        name="kb_search",
        description="从本地知识库检索与问题最相关的段落，用于食品安全问答。",
        func=search_docs,
    )









