from flask import Flask, jsonify, request
from gpt import ai


app = Flask(__name__)
model_name = "355M" # Overwrite with set_model_name()
chat_ai = ai.ChatAI() # Ready the GPT2 AI generator
chat_ai.load_model() # Load the GPT2 model

@app.route('/', methods=['GET'])
def home():
    rawdatajson = request.get_json()
    
    
    response = "None"

    rawdata = self.chat_ai.get_bot_response(self.model_name, rawdatajson["name"], rawdatajson["input"])
    data = rawdata.split("me:", 1)[1].splitlines()[0]
    response = data
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)