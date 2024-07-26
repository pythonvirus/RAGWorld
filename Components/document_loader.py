import os
import sys
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from Exception import CustomException
from Entity.config_entity import DocumentLoaderConfig
from Logger import CustomLogger

logging = CustomLogger("doc_loader_logger")
class DocumentLoader(DocumentLoaderConfig):
    
    document_loader_config = DocumentLoaderConfig
    @classmethod  
    def doc_loader(cls):
        try:
            logging.info("Entered the get_loader_object method of DocumentLoader class")
            if cls.document_loader_config.document_loader == "UnstructuredPDFLoader":                
                loaders = [UnstructuredPDFLoader(os.path.join(cls.document_loader_config.document_folder, fn)) for fn in os.listdir(cls.document_loader_config.DOCUMENT_FOLDER)]
                return loaders
            if cls.document_loader_config.document_loader == "PyPDFLoader":
                documents = []
                for file in os.listdir(cls.document_loader_config.document_folder):
                    if file.endswith('.pdf'):
                        pdf_path = os.path.join(cls.document_loader_config.document_folder, file)
                        loader = PyPDFLoader(pdf_path)
                        documents.extend(loader.load())
                logging.info("Successfully Loaded the document using PyPDF from the folder")                
                return documents
        except Exception as e:
            raise CustomException(e, sys) from e