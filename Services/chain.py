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
from Components.evaluation import Evaluation

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
            logging.info("Successfully returned the answer from RAG Chain")   
            return result["answer"]

        except Exception as e:
            raise CustomException(e, sys) from e
        
    @classmethod  
    def evaluate_rag(cls,vector_store, question_file = "Data\Evaluation\Q&A.xlsx"):
            try:
                answer_from_rag = []
                context_from_rag = []

                questions, ground_truth = Evaluation.load_excel(question_file)

                print(questions)
                print(ground_truth)
                
                for question in questions:
                     answer_from_rag.append(cls.Rag_Chain_invoke(question,vector_store))
                     context_from_rag.append([cls.doc_loader_wrapper().get_relevant_documents(question)])
                
                data_to_evaluate = {"question": questions, "answer": answer_from_rag, "contexts": context_from_rag,"ground_truths": ground_truth}
                Evaluation.evaluate_rag_system(data_to_evaluate)

            except Exception as e:
                raise CustomException(e, sys) from e



