import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Exception import CustomException
from Entity.config_entity import SplitterConfig
from Logger import CustomLogger

logging = CustomLogger("split_doc_logger")


class Splitter:
    splitter_config = SplitterConfig
    @classmethod
    def split_document(cls,document):
        try:
            logging.info("Entered the get_splitter_object method of Splitter class")
            if cls.splitter_config.text_splitter == "RecursiveCharacterTextSplitter":                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=cls.splitter_config.chunk_size, chunk_overlap=cls.splitter_config.chunk_overlap)
                documents=text_splitter.split_documents(document)
                logging.info("successfully return splitter object")
                return documents
            
        except Exception as e:
            raise CustomException(e, sys) from e
    



    
