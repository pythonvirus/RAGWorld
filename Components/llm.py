from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from Entity.config_entity import APILoaderConfig,LLMConfig
from Exception import CustomException
import sys

from Logger import CustomLogger

logging = CustomLogger("LLMLoader_logger")
class LLMLoader(APILoaderConfig):
    api_loader_config = APILoaderConfig
    @classmethod  
    def get_llm_model(cls):
        try:
            logging.info("Entered the get_llm method of LLMLoader class")
            if LLMConfig.llm_name == "OpenAI":
                open_ai_api_key = cls.api_loader_config.OPENAI_API_KEY
                llm_model=ChatOpenAI(openai_api_key=open_ai_api_key,model_name=LLMConfig.model_name)                           
                logging.info(f"Successfully returned LLM Model")                
                return llm_model
        except Exception as e:
            raise CustomException(e, sys) from e