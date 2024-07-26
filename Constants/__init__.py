import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Common constants
#TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M")


#Document Loader Constants
#DOCUMENT_LOADER = "UnstructuredPDFLoader"
DOCUMENT_LOADER = "PyPDFLoader"
DOCUMENT_FOLDER = "Data"


#API Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Embedding Constants
EMBEDDINGS = "OpenAIEmbeddings"
EMBEDDING_MODEL= "text-embedding-3-small"  #"text-embedding-3-large" #'text-embedding-ada-002'

#Text Splitter
TEXT_SPLITTER = "RecursiveCharacterTextSplitter"

#Chunk Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP  = 200

#VectorDB
#VECTOR_DB = "MongoDB"
VECTOR_DB = "FAISS"
#VECTOR_DB = "PINECONE"
INDEX_NAME=os.getenv("INDEX_NAME")

#Local index path
LOCAL_INDEX_PATH ="Components\\vectordb\index.faiss"
#Pinecone Constants
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_CLOUD=os.getenv("PINECONE_CLOUD")
PINECONE_REGION=os.getenv("PINECONE_REGION")
METRIC="cosine"
INDEX_DIMENSION=1536
NAMESPACE='EGL'


#LLM Constants
LLM_NAME = "OpenAI"
MODEL_NAME= "gpt-3.5-turbo" #"gpt-4-turbo" #"gpt-4o"

#Output parser Config
PARSER_NAME="StrOutputParser"

#MongoDB Constants
CLUSTER = "cluster0"
REGION = "i28zl9i"
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

'''
# Data ingestion constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_IMBALANCE_DATA_DIR = "imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_DIR = "raw_data.csv"


# Data transformation constants 
DATA_TRANSFORMATION_ARTIFACTS_DIR = 'DataTransformationArtifacts'
TRANSFORMED_FILE_NAME = "final.csv"
DATA_DIR = "data"
ID = 'id'
AXIS = 1
INPLACE = True
DROP_COLUMNS = ['Unnamed: 0','count','hate_speech','offensive_language','neither']
CLASS = 'class'


# Model training constants
MODEL_TRAINER_ARTIFACTS_DIR = 'ModelTrainerArtifacts'
TRAINED_MODEL_DIR = 'trained_model'
TRAINED_MODEL_NAME = 'model.h5'
X_TEST_FILE_NAME = 'x_test.csv'
Y_TEST_FILE_NAME = 'y_test.csv'

X_TRAIN_FILE_NAME = 'x_train.csv'

RANDOM_STATE = 42
EPOCH = 1
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2


# Model Architecture constants
MAX_WORDS = 50000
MAX_LEN = 300
LOSS = 'binary_crossentropy'
METRICS = ['accuracy']
ACTIVATION = 'sigmoid'


# Model  Evaluation constants
MODEL_EVALUATION_ARTIFACTS_DIR = 'ModelEvaluationArtifacts'
BEST_MODEL_DIR = "best_Model"
MODEL_EVALUATION_FILE_NAME = 'loss.csv'


MODEL_NAME = 'model.h5'
APP_HOST = "0.0.0.0"
APP_PORT = 8080
'''
