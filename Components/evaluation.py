import sys
import pandas as pd
from datetime import datetime
from Exception import CustomException
from datasets import Dataset
from ragas import evaluate
#from ragas.metrics.critique  import harmfulness, maliciousness, coherence, correctness, conciseness
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_similarity,
    answer_correctness
)


import json
from getpass import getpass
from urllib.request import urlopen

import nest_asyncio
import numpy as np
import pandas as pd
import phoenix as px
from langchain.chains import RetrievalQA
from phoenix.evals import (
    HallucinationEvaluator,
    OpenAIModel,
    QAEvaluator,
    RelevanceEvaluator,
    run_evals,
)
from phoenix.session.evaluation import get_qa_with_reference, get_retrieved_documents
from phoenix.trace import DocumentEvaluations, SpanEvaluations
from phoenix.trace.langchain import LangChainInstrumentor
from phoenix.trace.dsl import SpanQuery

from uptrain import EvalLLM, Evals, CritiqueTone, Settings, ResponseMatching
from Entity.config_entity import APILoaderConfig


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
    def start_phoenix(cls):
        try:
            
                 
            session=px.launch_app()
            LangChainInstrumentor().instrument() #this will start streaming into phoenix
                     
                    
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
                result=evaluate(dataset=dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy,answer_similarity, 
                                                          answer_correctness])
                # result=evaluate(dataset=dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy,answer_similarity, 
                #                                           answer_correctness,harmfulness, maliciousness, coherence, correctness, conciseness])
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
        
    @classmethod
    async def phoenix_eval(cls):
        try:
            client=px.Client()
            LangChainInstrumentor().instrument()
            print("evaluation started")
            print(f"client:{client}")
            

            query = SpanQuery().where(
                # Filter for the `RETRIEVER` span kind.
                # The filter condition is a string of valid Python boolean expression.
                "span_kind == 'RETRIEVER'",
            ).select(
                # Extract the span attribute `input.value` which contains the query for the
                # retriever. Rename it as the `input` column in the output dataframe.
                input="input.value",
                output="output.value",
            ).explode(
                # Specify the span attribute `retrieval.documents` which contains a list of
                # objects and explode the list. Extract the `document.content` attribute from
                # each object and rename it as the `reference` column in the output dataframe.
                "retrieval.documents",
                reference="document.content",
            )

            # The Phoenix Client can take this query and return the dataframe.
            queries_df1=px.Client().query_spans(query)
            queries_df = get_qa_with_reference(client)
            retrieved_documents_df = get_retrieved_documents(client)
            print(f"Readed Data shape {queries_df.columns}, {retrieved_documents_df.columns}")

            print(queries_df.head())
            print(queries_df.shape)

            print("spam df ")
            print(queries_df1.columns)
            print(queries_df1.head())

        
            print("*"*20)
            print(retrieved_documents_df.head())
            eval_model = OpenAIModel(
                model="gpt-4-turbo-preview",
                    )
            hallucination_evaluator = HallucinationEvaluator(eval_model)
            qa_correctness_evaluator = QAEvaluator(eval_model)
            relevance_evaluator = RelevanceEvaluator(eval_model)

            hallucination_eval_df, qa_correctness_eval_df = run_evals(
                dataframe=queries_df1,
                evaluators=[hallucination_evaluator, qa_correctness_evaluator],
                provide_explanation=True,
            )
            relevance_eval_df = run_evals(
                dataframe=retrieved_documents_df,
                evaluators=[relevance_evaluator],
                provide_explanation=True,
            )[0]

            hallucination_eval_df = hallucination_eval_df.reset_index(level='document_position')
            print(f"evaluation data shape {hallucination_eval_df.shape}")
            print(hallucination_eval_df.head())

            qa_correctness_eval_df = qa_correctness_eval_df.reset_index(level='document_position')
            print(f"evaluation data shape {qa_correctness_eval_df.shape}")
            print(qa_correctness_eval_df.head())



            print(f"evaluation data shape {relevance_eval_df.shape}")
            print(relevance_eval_df.head())



            client.log_evaluations(
                SpanEvaluations(eval_name="Hallucination", dataframe=hallucination_eval_df.drop(columns=['document_position'])),
                SpanEvaluations(eval_name="QA Correctness", dataframe=qa_correctness_eval_df.drop(columns=['document_position'])),
                DocumentEvaluations(eval_name="Relevance", dataframe=relevance_eval_df),
            )
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @classmethod
    def uptrain_evaluate_rag_system(cls, question,answer,contexts,ground_truth=None):
        try:
            print("uptrain started")            
            if ground_truth:
                print("under if")
                data = [{"question": question,"context": contexts, "response": answer, "ground_truth": ground_truth}]
                eval_llm = EvalLLM(openai_api_key=APILoaderConfig.OPENAI_API_KEY)
                result = eval_llm.evaluate(data = data, checks = [Evals.CONTEXT_RELEVANCE, 
                                                           Evals.RESPONSE_RELEVANCE,
                                                           Evals.VALID_RESPONSE,
                                                           Evals.RESPONSE_CONSISTENCY,
                                                           Evals.RESPONSE_COMPLETENESS,
                                                           Evals.RESPONSE_CONCISENESS,
                                                           Evals.RESPONSE_COMPLETENESS_WRT_CONTEXT,
                                                           Evals.FACTUAL_ACCURACY,
                                                           Evals.CRITIQUE_LANGUAGE,
                                                           Evals.CODE_HALLUCINATION,
                                                           Evals.PROMPT_INJECTION,
                                                           [ResponseMatching(method = 'llm')]
                                                          ])
                return result
            else:
                # Specify the file path and name
                file_path = 'Evaluation\evaluation.csv'
                print("uptrain started under else")
                data = [{"question": question,"context": contexts, "response": answer}]
                eval_llm = EvalLLM(openai_api_key=APILoaderConfig.OPENAI_API_KEY)
                result = eval_llm.evaluate(data = data, checks = [Evals.CONTEXT_RELEVANCE, 
                                                           Evals.RESPONSE_RELEVANCE,
                                                           Evals.VALID_RESPONSE,
                                                           Evals.RESPONSE_CONSISTENCY,
                                                           Evals.RESPONSE_COMPLETENESS,
                                                           Evals.RESPONSE_CONCISENESS,
                                                           Evals.RESPONSE_COMPLETENESS_WRT_CONTEXT,
                                                           Evals.FACTUAL_ACCURACY,
                                                           Evals.CRITIQUE_LANGUAGE,
                                                           Evals.CODE_HALLUCINATION,
                                                           Evals.PROMPT_INJECTION
                                                          ])
              
            result_df  = pd.DataFrame(result)
            # Add system date and time as columns   
            result_df['Framwork'] = "Uptrain"
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
            print(f"uptrain complete {df.shape}")   

                  
                                
        except Exception as e:
            raise CustomException(e, sys) from e

# To fix the RuntimeWarning, add the following line at the end of your code:
nest_asyncio.apply()
        


        


        
