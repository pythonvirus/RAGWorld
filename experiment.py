import sys
import pandas as pd
from datetime import datetime
from Exception import CustomException
from Services.chain import Service
from Components.evaluation import Evaluation
from Entity.config_entity import LLMConfig,EmbeddingConfig

def evaluate(ground_truth_file_path,experiment_name):
    questions,ground_truth=Evaluation.load_ground_truth(ground_truth_file_path)
    vector_store=Service.get_vectordb_instance()
    results=[]
    context=[]
    for question in questions:
        result,context1,context2,context3=Service.Rag_Chain_invoke(question,vector_store)
        results.append(result)
        context.append([context1,context2,context3])

    result=Evaluation.ragas_evaluate_rag_system(questions,results,context,ground_truth)
    result_df  = result.to_pandas()
    result_df['LLM']= LLMConfig.model_name  
    result_df['embedding']=EmbeddingConfig.model

    File_name="Experiments/"+experiment_name+".csv"

    result_df.to_csv(File_name, index=False)

if __name__ == '__main__':
    evaluate("Validation-Data\Q&A.xlsx","gpt-4o-text-embedding-3-small-prompt1")


    