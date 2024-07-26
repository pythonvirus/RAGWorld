import sys
from langchain.schema.output_parser import StrOutputParser
from Entity.config_entity import OutputConfig
from Logger import CustomLogger
from Exception import CustomException

logging = CustomLogger("Output_parser_logger")
class LLMOutput(OutputConfig):
    output_config = OutputConfig
    
    @classmethod  
    def output_parser_obj(cls):
        try:
            logging.info("Entered the output_parser method of LLMOutput class")
            if cls.output_config.parser_name == "StrOutputParser":                
                output_parser=StrOutputParser()                
                logging.info("Successfully return output parser object")                
                return output_parser
        except Exception as e:
            raise CustomException(e, sys) from e