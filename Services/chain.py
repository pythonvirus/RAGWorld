from Components.document_loader import DocumentLoader
from Components.text_splitter import Splitter
from Components.embedding import EmbeddingLoader
from Components.save_vector import VectorLoader
from Components.retriever import Retriever
from Components.llm import LLMLoader
from Components.outputparser import LLMOutput
from Components.prompt import prompt_template
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from typing import List
from langchain_core.documents import Document
from Exception import CustomException
from Entity.config_entity import OutputConfig
import sys
from Logger import CustomLogger

logging = CustomLogger("chain_logger")

class Service(OutputConfig):
    output_config = OutputConfig

    @classmethod  
    def format_docs(cls,docs: List[Document]):
        return "\n\n".join(doc.page_content for doc in docs)
    
    @classmethod  
    def doc_loader_wrapper(cls):
        try:
            embeddings=EmbeddingLoader.get_embedding_obj()
            docs=DocumentLoader.doc_loader()
            split_documents=Splitter.split_document(docs)
            vectorstore=VectorLoader.save_vector(documents=split_documents,embeddings=embeddings)
            
            return vectorstore

        except Exception as e:
            raise CustomException(e, sys) from e
    @classmethod  
    def get_vectordb_instance(cls):
            try:
                embeddings=EmbeddingLoader.get_embedding_obj()
                vectorstore=VectorLoader.load_vector(embeddings)
                return vectorstore

            except Exception as e:
                raise CustomException(e, sys) from e
    
    @classmethod  
    def Rag_Chain_invoke(cls,question,vectorstore):
        try:

                
            logging.info("Entered the Rag_Chain_invoke method of RAGChain class")
            retriever=Retriever.get_retriever_obj(vectorstore)
            llm_model=LLMLoader.get_llm_model()
            prompt=ChatPromptTemplate.from_template(prompt_template)
            output_parser=LLMOutput.output_parser_obj()
            
            rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: cls.format_docs(x["context"])))
            | RunnableLambda(logging.inspect)
            | prompt
            | llm_model
            | output_parser
            )

            retrieve_docs = (lambda x:  x["question"]) | retriever

                      
            chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
                answer=rag_chain_from_docs
            )  
            result = chain.invoke({"question": question})
            context1=result['context'][0].page_content
            context2=result['context'][1].page_content
            context3=result['context'][1].page_content
            logging.info("Successfully returned the answer from RAG Chain")   
            return result["answer"],context1,context2,context3
       

        except Exception as e:
            raise CustomException(e, sys) from e



