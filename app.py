
from flask import Flask, render_template, jsonify, request
from Services.chain import Service
from Components.evaluation import Evaluation
import threading
from Exception import CustomException
import sys
import phoenix as px
import asyncio


app = Flask(__name__)

vector_store=Service.get_vectordb_instance()

#print(session)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        question = request.form["msg"]
        #print("checking active session....")
        session = px.active_session()
        print(f"session: {session}")
        if session is None:
            print("start phoenix")
            Evaluation.start_phoenix()
        
        result,context1,context2,context3=Service.Rag_Chain_invoke(question,vector_store)
        client=px.Client()
        print(client)
         
        evaluation_thread_uptrain = threading.Thread(target=Evaluation.uptrain_evaluate_rag_system, args=([question],[result],[context1,context2,context3]))
        evaluation_thread_uptrain.start()
        
        evaluation_thread = threading.Thread(target=asyncio.run, args=(Evaluation.phoenix_eval(),))
        evaluation_thread.start()
        
        evaluation_thread_ragas = threading.Thread(target=Evaluation.ragas_evaluate_rag_system, args=([question],[result],[context1,context2,context3]))
        evaluation_thread_ragas.start()

        

       

       
      
    
        return result
    except Exception as e:
            raise CustomException(e, sys) from e
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000,debug= True)
