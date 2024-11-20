from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from helper_functions import get_local_time, get_answer_status, get_chat_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
llm_model = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash-latest',
    temperature=0.1
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('user_input')
        chat_history = data.get('chat_history', [])
        
        converted_history = []
        for msg in chat_history:
            if msg['role'] == 'human':
                converted_history.append(HumanMessage(content=msg['content']))
            else:
                converted_history.append(AIMessage(content=msg['content']))

        recent_chat_history = converted_history[-20:]

        local_time = get_local_time("India")
        status_dict = get_answer_status(
            llm_model,
            user_input,
            recent_chat_history,
            local_time
        )

        response, urls = get_chat_response(
            llm_model,
            status_dict,
            user_input,
            recent_chat_history,
            local_time
        )
        
        return jsonify({
            'response': response,
            'urls': urls or []
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)