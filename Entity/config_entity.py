from dataclasses import dataclass
from Constants import *
import os


@dataclass
class DocumentLoaderConfig:
    document_loader:str = DOCUMENT_LOADER
    document_folder:str = DOCUMENT_FOLDER

@dataclass
class APILoaderConfig:
   OPENAI_API_KEY:str = OPENAI_API_KEY
        #OPENAI_API_KEY:str = OPENAI_API_KEY

@dataclass
class EmbeddingConfig:
    embedding:str = EMBEDDINGS
    model:str=EMBEDDING_MODEL

@dataclass
class SplitterConfig:
    text_splitter:str = TEXT_SPLITTER
    chunk_size:int = CHUNK_SIZE
    chunk_overlap:int = CHUNK_OVERLAP

@dataclass
class PineconeConfig:
    api_key:str=PINECONE_API_KEY
    cloud:str=PINECONE_CLOUD
    region:str=PINECONE_REGION
    metric:str=METRIC
    index_dimension:int=INDEX_DIMENSION
    namespace:str=NAMESPACE

@dataclass
class MongoDBConfig:
    cluster:str = CLUSTER
    region:str = REGION
    user_name:str = USER_NAME
    password:str =  PASSWORD


@dataclass
class VectorDBConfig:
    vectordb:str = VECTOR_DB
    local_index_path:str = LOCAL_INDEX_PATH
    index_name:str=INDEX_NAME

@dataclass
class LLMConfig:
    llm_name:str = LLM_NAME
    model_name:str = MODEL_NAME

@dataclass
class OutputConfig:
    parser_name:str = PARSER_NAME

  



'''
@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.BUCKET_NAME = BUCKET_NAME
        self.ZIP_FILE_NAME = ZIP_FILE_NAME
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_IMBALANCE_DATA_DIR)
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_RAW_DATA_DIR)
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,self.ZIP_FILE_NAME)



@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.DATA_TRANSFORMATION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.TRANSFORMED_FILE_PATH = os.path.join(self.DATA_TRANSFORMATION_ARTIFACTS_DIR,TRANSFORMED_FILE_NAME)
        self.ID = ID
        self.AXIS = AXIS
        self.INPLACE = INPLACE 
        self.DROP_COLUMNS = DROP_COLUMNS
        self.CLASS = CLASS 
        self.LABEL = LABEL
        self.TWEET = TWEET



@dataclass
class ModelTrainerConfig: 
    def __init__(self):
        self.TRAINED_MODEL_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,MODEL_TRAINER_ARTIFACTS_DIR) 
        self.TRAINED_MODEL_PATH = os.path.join(self.TRAINED_MODEL_DIR,TRAINED_MODEL_NAME)
        self.X_TEST_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, X_TEST_FILE_NAME)
        self.Y_TEST_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, Y_TEST_FILE_NAME)
        self.X_TRAIN_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, X_TRAIN_FILE_NAME)
        self.MAX_WORDS = MAX_WORDS
        self.MAX_LEN = MAX_LEN
        self.LOSS = LOSS
        self.METRICS = METRICS
        self.ACTIVATION = ACTIVATION
        self.LABEL = LABEL
        self.TWEET = TWEET
        self.RANDOM_STATE = RANDOM_STATE
        self.EPOCH = EPOCH
        self.BATCH_SIZE = BATCH_SIZE
        self.VALIDATION_SPLIT = VALIDATION_SPLIT



@dataclass
class ModelEvaluationConfig: 
    def __init__(self):
        self.MODEL_EVALUATION_MODEL_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR, MODEL_EVALUATION_ARTIFACTS_DIR)
        self.BEST_MODEL_DIR_PATH: str = os.path.join(self.MODEL_EVALUATION_MODEL_DIR,BEST_MODEL_DIR)
        self.BUCKET_NAME = BUCKET_NAME 
        self.MODEL_NAME = MODEL_NAME 



@dataclass
class ModelPusherConfig:

    def __init__(self):
        self.TRAINED_MODEL_PATH = os.path.join(os.getcwd(),ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)
        self.BUCKET_NAME = BUCKET_NAME
        self.MODEL_NAME = MODEL_NAME
    '''
