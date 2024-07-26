import sys
import pandas as pd
from datetime import datetime
from Exception import CustomException
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_similarity,
    answer_correctness
)

class Evaluation:

    @classmethod
    def load_ground_truth(cls, file_path):
        try:            
            question = []
            ground_truth = []
            
            df = pd.read_excel(file_path)

            question = df['Question'].tolist()
            ground_truth= df['Answer'].tolist() 
                        
            return question,ground_truth
                    
        except Exception as e:
            raise CustomException(e, sys) from e
    @classmethod    
    def combine_dictionaries(cls,*dicts):
        result = {}
        for dictionary in dicts:
            result.update(dictionary)
        return result
        
    @classmethod
    def ragas_evaluate_rag_system(cls, question,answer,contexts,ground_truth=None):
        try:
            q={}
            a={}
            c={}
            gt={}
            
            if ground_truth:
                q['question'] = question
                a['answer']=answer
                c['contexts'] = contexts
                gt['ground_truth'] = ground_truth
                data_to_evaluate=cls.combine_dictionaries(q,a,c,gt)
                dataset=Dataset.from_dict(data_to_evaluate)
                result=evaluate(dataset=dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy,answer_similarity, answer_correctness])
                return result
            else:
                # Specify the file path and name
                file_path = 'Evaluation\evaluation.csv'
                q['question'] = question
                a['answer']=answer
                c['contexts'] = [contexts]
                data_to_evaluate=cls.combine_dictionaries(q,a,c)
                #print(data_to_evaluate)
                dataset=Dataset.from_dict(data_to_evaluate)
                result=evaluate(dataset=dataset, metrics=[faithfulness, answer_relevancy])
              
            result_df  = result.to_pandas()

            
            # Add system date and time as columns
            
            result_df['date'] = datetime.now().strftime('%Y-%m-%d')
            result_df['time'] = datetime.now().strftime('%H:%M:%S')

            # Check if the file exists
            if file_path:
                # Read the existing CSV file into a DataFrame
                existing_df = pd.read_csv(file_path)
                
                # Append the new DataFrame to the existing one
                df=pd.concat([existing_df, result_df], axis=0, ignore_index=True)
                

            # Write the DataFrame to the CSV file
            df.to_csv(file_path, index=False)

                  
                                
        except Exception as e:
            raise CustomException(e, sys) from e
        
  

    


    
