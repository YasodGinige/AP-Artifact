from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pentestgpt.utils.APIs.module_import import dynamic_import
from pentestgpt.utils.prompt_select import prompt_ask
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys


class RepititionIdentifier_module():
    def __init__(self, api_key):
        self.text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
        self.dataChunks = None
        self.vectorStore = None
        self.retriever = None
        self.defaultInfo = None
        self.API_key = api_key


    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def format_and_append_info(self, docs):
        formatted_docs = "\n\n".join(doc.page_content for doc in docs)
        complete_context = formatted_docs + "\n" + self.default_info
        return complete_context

    def detect(self, query, output_history, vectorPath):
        min_score = 1
        highest_match = ''
        if not self.vectorStore:
            
            self.dataChunks = output_history
            self.vectorStore = Chroma.from_texts(texts=self.dataChunks,
                                        embedding=OpenAIEmbeddings(openai_api_key=self.API_key),

                                        persist_directory=vectorPath)
            self.vectorStore.persist()
            
        results = self.vectorStore.similarity_search_with_score(query)
        for doc, score in results:
            if score < min_score:
                min_score = score
                highest_match = doc
                
        print('\nscore:', min_score, ' |  highest_match:', doc)
        print(results)
         

        new_embedding = OpenAIEmbeddings(openai_api_key=self.API_key).embed_query(query)
        self.vectorStore.add_texts(texts=[query],embeddings=[new_embedding])

        if min_score < 0.12:
            return True, highest_match
        else:
            return False, highest_match

    def human_react(self,PTT, last_step , highest_match, console, whoami = False):
        if whoami:
            console.print("Metasploit exploit was successful. The output of the 'whoami' command:\n\n")
            console.print(PTT)
            user_input = prompt_ask("Did you get access? Answer Yer or No: ", multiline=True)
            return user_input

        else:
            console.print("It seems like PentestLLM has stuck in a loop. Would you like to give an input here. Following are the information gathered.\n\n")
            console.print("Pentest Tree\n" + PTT + "\n\n")
            console.print("Attempted Last step:\n" + last_step + "\n")
            console.print("Matching Previous step:")
            console.print(highest_match)
            user_input = prompt_ask("Your input: ", multiline=True)

            return user_input
