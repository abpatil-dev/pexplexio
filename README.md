# Perplexio

This is a comprehensive system that integrates web scraping, content extraction, large language models, and front-end development to create an interactive chatbot capable of answering user queries by retrieving relevant content from the web.

The project includes:

- **Flask Backend**: Handles API requests and communicates with external APIs.
- **Streamlit Front-End**: Provides a smooth, interactive UI for users to input their queries and receive responses.
- **Gemini Flash Model**: Powers the response generation and ensures accuracy and fluency in the answers.
- **Multilingual Support**: Both translation and transliteration are available for user queries.
- **Spell Check**: Automatically checks and corrects spelling errors in queries.
- **Content Retrieval & Relevancy Scoring**: The system uses web scraping to find the most relevant content and ranks URLs based on their relevance.
- **Conversation Memory**: The chatbot remembers the last 20 interactions for efficient responses.
- **Recent Event Knowledge**: The system is aware of recent events and includes this in its answers.
- **Routing Logic**: The system intelligently decides whether to answer the query directly, retrieve information from the web, or use another knowledge source.
- **Langchain Integration**: Ensures seamless communication between the language model and other data sources.

## Features

- Streamlit front-end with smooth interaction
- Flask backend to handle the service logic
- Language model (Gemini Flash) for response generation
- Multilingual support, including translation and transliteration
- Automatically performs spell checks
- URL references attached to answers with relevancy scoring
- Recent events knowledge integration
- Memory of the last 20 interactions to make conversations more fluid
- Smart query routing based on query nature
- Free to use for small-scale users (2-3 people, 50-60 questions daily)

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.x
- `pipenv` (for virtual environment management)
- Required API keys for Google and Tavily

### Setup Instructions

1. **Create a `.env` file**:
    Before running the project, you must create a `.env` file in the root directory of the project to store your API keys.

    Your `.env` file should contain the following:

    ```
    GOOGLE_API_KEY = "AIzxxxxxxxxxxxxxxxxxxxxxxxx"
    TAVILY_API_KEY = "tvly-3Dxxxxxxxxxxxxxxxxxxxxxx"
    ```

2. **Install dependencies**:
    ```bash
    pipenv install -r requirements.txt
    ```

3. **Select the Python interpreter**:
    - Open the command palette and select the Python interpreter associated with the virtual environment.

4. **Activate the virtual environment**:
    ```bash
    pipenv shell
    ```

5. **Run the Flask backend**:
    - Start the Flask backend service with the following command:
    ```bash
    Flask --app flask_app/flask_app run
    ```
    - This will run the backend on port `5000`.

6. **Run the Streamlit front-end**:
    - Start the Streamlit app with the following command:
    ```bash
    streamlit run streamlit_app/stlit_app.py
    ```
    - The front-end will run on port `8501`.

7. **Access the Streamlit app**:
    - Open your browser and navigate to [http://localhost:8501](http://localhost:8501) to interact with the chatbot.

8. **Set the best experience**:
    - In the Streamlit app, go to the top-right corner (3 dots).
    - Select "Settings" and set the theme to "Light" for the best experience.

9. **Start chatting**:
    - Once the app is running, you can start chatting with the bot and get answers to your queries!

## Notes

- The system is free to use for 2-3 people asking 50-60 questions daily, as it relies on free APIs.
- The backend uses external APIs to retrieve relevant web pages, and the LLM processes the content to provide responses.
- The system remembers the last 20 conversations to provide more personalized and context-aware answers.
- The chatbot behaves professionally and is designed for a smooth user experience.
