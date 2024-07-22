from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pentestgpt.utils.APIs.module_import import dynamic_import


class Rag_module():
    def __init__(self, datapath, apiKey = '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'):
        self.loader = DirectoryLoader(datapath,glob="*.pdf",loader_cls=PyPDFLoader)
        self.text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
        self.dataChunks = None
        self.vectorStore = None
        self.retriever = None
        self.defaultInfo = None
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0.2, openai_api_key=apiKey)

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def format_and_append_info(self, docs):
        formatted_docs = "\n\n".join(doc.page_content for doc in docs)
        complete_context = formatted_docs + "\n" + self.default_info
        return complete_context

    def rag_init(self,vectorPath , apiKey = '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'):

        default_file = open('./resources/attacker_details.txt','r')
        default_info = default_file.read()
        self.default_info = 'Attack Network Information:\n' + default_info
        documents = self.loader.load()
        self.dataChunks = self.text_splitter.split_documents(documents)
        self.vectorStore = Chroma.from_documents(documents=self.dataChunks,
                                    embedding=OpenAIEmbeddings(openai_api_key=apiKey),
                                    persist_directory=vectorPath)
        self.vectorStore.persist()
        self.retriever = self.vectorStore.as_retriever(search_kwargs={'k':15})
        print(type(self.retriever))
        prompt = hub.pull('rlm/rag-prompt')

        #prompt.messages[0].prompt.template = "You are a Cybersecurity expert for question-answering tasks. Use the following pieces of retrieved context to answer the question. If the context doesn't contain a direct answer, combine these commands to generate the expected outcome. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:"
        prompt.messages[0].prompt.template = "You are a Cybersecurity expert for question-answering tasks. Use the following pieces of retrieved context and your existing knowledge to answer the question. If the context doesn't contain a direct answer, combine these commands and your existing knowledge to generate the expected outcome. You must replace Target IP, Your IP and wordlist with informaion under Attack Network Information in the context. \nQuestion: {question} \nContext: {context} \nAnswer:"
        rag_chain = ({"context": self.retriever  | (lambda docs: self.format_and_append_info(docs)), "question": RunnablePassthrough()}| prompt| self.llm| StrOutputParser())
        return rag_chain