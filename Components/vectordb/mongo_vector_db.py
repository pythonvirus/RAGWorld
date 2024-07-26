import sys
from os.path import dirname, join,abspath
sys.path.append(abspath(join(dirname(__file__), '..')))
from Components.vectordb.vector_DB import VectorDB
from pymongo.mongo_client import MongoClient
from Entity.config_entity import MongoDBConfig
#from config_entity import MongoDBConfig
from Exception import CustomException
#from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_mongodb import MongoDBAtlasVectorSearch
from Logger import logging
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
class MongoDBVectorStore(VectorDB):
    def __init__(self, mongo_db_config : MongoDBConfig):
        self.mongo_db_config = mongo_db_config

    
    def create_client(self):        
        uri = "mongodb+srv://{0}:{1}@{2}.{3}.mongodb.net/?retryWrites=true&w=majority&appName={2}".format(self.mongo_db_config.user_name, 
                                                                                                          self.mongo_db_config.password,
                                                                                                          self.mongo_db_config.cluster,
                                                                                                        self.mongo_db_config.region)
                
        print(uri)
        logging.info("Mongo DB URI created")
        client = MongoClient(uri)
        logging.info("Mongo DB Client created")        
        try:
            client.admin.command('ping')
            logging.info("Pinged your deployment. You successfully connected to MongoDB!")        
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(e)
            raise CustomException(e, sys) from e
        
    def create_database(self):
        try:
            client = self.create_client()
            #db = client[self.mongo_db_config.db_name]
            db = client["Paper_DB"]
            print("DB created successfully on  MongoDB!")
            llm_paper_coll = db["Paper_Records_Collection"]
            print("Collection created successfully on  MongoDB!")
            paper_index = "paper_records_index"
        except Exception as e:
            print(e)
            raise CustomException(e, sys) from e

        '''
        data ={"name":"Abhishek",
               "Class":"Data Science",
               "Time":"Flexi"}

        llm_paper_coll.insert_one(data)
        '''

    def add_document(self):
        pass

    def format_docs(self,doc):
        return doc.page_content.replace("\n"," ")
    
        
    def save_vector_document(self,db_name,collection_name, index_name,emmbeddings, documents):
        try:
            mongo_client = self.create_client()
            collection = mongo_client[db_name][collection_name]  

            vectorstore  = MongoDBAtlasVectorSearch(
            #documents=documents,
            embedding=emmbeddings,
            collection=collection,
            index_name=index_name,
            )

            #vectorstore.create_index(dimensions=1536)

            vector_search = MongoDBAtlasVectorSearch.from_documents(
            documents=documents,
            embedding=emmbeddings,
            collection=collection,
            index_name=index_name,
            )

            return vector_search
            '''
            client = self.create_client()
            #db = client[self.mongo_db_config.db_name]
            db = client[db_name]
            print("DB created successfully on  MongoDB!")
            llm_paper_coll = db[collection_name]
                      
            #print(type(documents))
            #print((documents[1]).page_content)
            #print((documents[1]).metadata)
            #print(documents[1])
            df = pd.DataFrame(columns=["Embedded_Page_Content"])

            dn = []
            
            for doc in documents:
                #print(type(doc.page_content))
                df1=pd.DataFrame({'Page_Content':[self.format_docs(doc)]})
                #df1=pd.DataFrame({'Page_Content':[doc.page_content]})
                dn.append(df1)

            dn= pd.concat(dn, axis=0)
            print(dn.describe())
            print(dn.head(1))
            
            df = []
            for index, row in dn.iterrows():
                ebd = self.get_embedding(row['Page_Content'],emmbeddings)
                print(ebd)
                df2=pd.DataFrame({'Embedded_Page_Content':[row['Page_Content']]})
                df.append(df2)

            df = pd.concat(df, axis=0)

            print(df.describe())
            print(df.head(1))

            
            dn['Page_Embbed'] = dn.apply(lambda x: self.get_embedding(dn['Page_Content'],emmbeddings), axis=1)
            print(dn.shape)
            print(dn.head(1))
            '''

            '''
            df = pd.DataFrame({'Page_Content':[str(doc.page_content)] for doc in documents})
            print(df.shape)
            print(df.head(1))
            print(df[0])
            

            #df["Content_Embedings"] = df["Page_Content"].apply(lambda x)
            df['Page_Embbed'] = df.apply(lambda x: self.get_embedding(df['Page_Content'],emmbeddings), axis=1)
            print(df.head(1))
            '''
        except Exception as e:
            print(e)
            raise CustomException(e, sys) from e
        
    def get_embedding(self,text,emmbeddings):
    # Check for valid input
        if not text or not isinstance(text, str):
            return None
        try:
            # Call OpenAI API to get the embedding
            embed = emmbeddings.create(input=text).data[0].embedding
            return embed
        except Exception as e:
            print(f"Error in get_embedding: {e}")
            return None
    
        '''
        vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name="multidoc_vector",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    namespace=ASTRA_DB_KEYSPACE,)
    '''

'''
if __name__ == '__main__':
    mongodb_config = MongoDBConfig()
    mongodb=MongoDBVectorStore(mongodb_config)
    mongodb.create_client()

'''
    


