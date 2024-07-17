"""
    LLMChain Class for creating/ instantiating  architecture , chain and model.
"""


from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers 
from langchain_community.vectorstores import Chroma 
from langchain.chains.retrieval_qa.base import RetrievalQA 
import chromadb
from prompt_templates import memory_prompt_template, summarize_prompt_template
import yaml
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# Load the config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


# Create llm with desired model, type and configurations.
def create_llm(model_path = config["model_path"]["large"], model_type = config["model_type"], model_config = config["model_config"]):
    llm = CTransformers(model=model_path,model_type= model_type, config= model_config, callbacks=[StreamingStdOutCallbackHandler()])
    return llm


# Create Embeddings for Input To LLM Path.
def create_embeddings(embeddings_path = config["embeddings_path"]):
    return HuggingFaceInstructEmbeddings(model_name=embeddings_path)


# Creating LLM Chain.
def create_llm_chain(llm, chat_prompt, memory=None):
    return LLMChain(llm=llm, prompt=chat_prompt,memory=memory)


# Creating a Buffer To Be Remembered with a Desired Window Size
def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key="history", chat_memory=chat_history, k=3)


# Passes the initialization in our current prompt_template
def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)


# Returns chatChain object with indicated chat_history
def load_normal_chain(chat_history):
    return chatChain(chat_history)


# Returns pdfChatChain object with indicated chat_history
def load_pdf_chat_chain(chat_history):
    return pdfChatChain(chat_history)


# Returns summarizeChatChain object with indicated chat_history
def load_summarize_chat_chain(chat_history):
    return summarizeChatChain(chat_history)

# Creates a local, persistent client and building a local vector database.
# Returns db instance.
def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient("local_database") # If error : Check for doc, it may changed. They are providing sample code.

    langchain_chroma = Chroma(
        client= persistent_client,
        collection_name="pdfs",
        embedding_function=embeddings,
    )
    return langchain_chroma


def load_retrieval_chain(llm , memory , vector_db):
    return RetrievalQA.from_llm(llm=llm, memory=memory, retriever=vector_db.as_retriever())
    

# A class for caching important features : 
#   - memory ( chat history for a chat_session )
#   - llm ( our in usage model )
#   - chat_prompt (  )
#   - llm_chain ( Chain of llm - prompt - chat_history )
class chatChain :

    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt, self.memory)


    # To get response from LLM
    # to avoid hallucinations we need stop so we use run function. 
    def run(self, user_input):
        print("Chat Chain is active and just started to running...")
        return self.llm_chain.run(human_input=user_input, history= self.memory.chat_memory.messages , stop=["Human:"])
    

class summarizeChatChain :

    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm()
        chat_prompt = create_prompt_from_template(summarize_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt, self.memory)


    def runsum(self, user_input):
        print("Summarizing the context and finding a title for the chat session...")
        return self.llm_chain.run(human_input=user_input, history= self.memory.chat_memory.messages, stop=["Human:"])


class pdfChatChain :
    
    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        self.vector_db = load_vectordb(create_embeddings())
        llm = create_llm()
        self.llm_chain = load_retrieval_chain(llm, self.memory, self.vector_db)


    def run(self, user_input):
        print("PDF Chat Chain is active and just started to running...")
        return self.llm_chain.run(query=user_input, history= self.memory.chat_memory.messages , stop=["Human:"])