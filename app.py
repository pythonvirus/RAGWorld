from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from Services.chain import Service

app = Flask(__name__)

load_dotenv()

vector_store=Service.get_vectordb_instance()

@app.route("/")
def index():
    return render_template('chat.html')    


@app.route("/get", methods=["GET", "POST"])
def chat():
    question = request.form["msg"]    
    result=Service.Rag_Chain_invoke(question,vector_store)
    #result=chain.invoke(input)
    print("Response : ", result)
    return str(result)   

    #Service.evaluate_rag(vector_store)
    #return "Success"

if __name__ == '__main__':
    app.run(debug= True)


