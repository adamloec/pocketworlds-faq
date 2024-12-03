# pocketworlds-faq
Pocket Worlds take home assignment for the Software Engineer (AI) position.

A conversational AI chatbot designed to assist users with Highrise-related questions. Built with FastAPI, React, and leveraging OpenAI models (read below for open-source, local model usage), deployed on a self-hosted Debian server with nginx.

**Next Steps**
- Feedback learning loop for training the generation model and embedding model for more accurate retrieval (Probably using Open-source models at this point)

**Notes and Basic Details**
- This uses RAG, or Retrieval Augmented Generation, to retrieve relevant information based on the user input.
- If a user input does not meet a certain similarity search threshold (when running retrieval on the vector database, currently set at 70%), this will return a default response asking for more information.
- I initially set this up with Vercel, but because of the size of the Chroma DB library and dependencies, I was running into deployment errors so I set up the application on my personal server.

**Additional (Optional) Features**
- *Basic NLP techniques:* Using the NLTK library, and with RAG by default.
- *Learning Mode:* I did not implement this, but using the user feedback logs you could create a feedback loop that trains the model on live data. This could improve the relevance of generated responses and possibly be used to train the embedding model for more accurate context retrieval.
- *User Feedback:* This is setup by a "like and dislike" button after each chat bot response. Sorted on the backend server in the logs directory.
- *Open Source Model Hosting:* Not implemented because I don't have enough compute on my server but I have instructions below in the README.md on how I would do it. It is as simple as downloading a model and changing ~5 lines of code.

# Design Approach

The chatbot implements a Retrieval-Augmented Generation (RAG) pipeline with the following components:

1. Data Collection and Processing:
- Custom web scraper extracts article content from Highrise support pages.
- Content is broken down into chunks for embeddings.
- Web loader automatically follows and extracts content from article URLs.

2. Vector Database Implementation (Chroma DB):
- ChromaDB for efficient similarity search.
- Document embeddings stored locally for quick retrieval.
- Semantic search for finding relevant content based on user queries/questions.

3. Prompt Chain (Langchain):
- User queries are embedded using the same model for consistency.
- Vector similarity search finds relevant documentation.
- Context is injected into the prompt for accurate responses.

4. Chat Memory
- Created a last exchange that gets updated for every new message. 
- This previous message pair gets injected into the context, incase a user has specific questions about a response from the system.

# Key Modules

## Data Pipeline
[View Data Pipeline Code](https://github.com/adamloec/pocketworlds-faq/blob/main/pocketworlds/server/chat/data_pipeline.py)

- Accesses the support home page, and iterates through each collection to extract and return all article URLs.


## Chat Bot
[View Chat Bot Code](https://github.com/adamloec/pocketworlds-faq/blob/main/pocketworlds/server/chat/chat_bot.py)
[View Chat NLP Utilities Code](https://github.com/adamloec/pocketworlds-faq/blob/main/pocketworlds/server/chat/chat_utilities.py)

1. Chat Bot object that handles the chat bot processes:
- Initialization creates the chat conversation chain (Prompts, LLM, retriever) and the vector database of URL and article embeddings (Chroma DB).
-  Process message runs inference on the conversation chain and returns a response. This function handles logic for checking if it is a greeting or farewell message, if the message can retrieve context, and if not, return a "need more context" response, and grabs supporting URLs to return to the user for more information.

2. Chat utilities code that contains functions for handling greeting and farewell messages, checking for relevant context, getting supporting URLs, and creating default clarification messages.

## API and Logging
[View API Code](https://github.com/adamloec/pocketworlds-faq/blob/main/pocketworlds/server/main.py)

1. The API has 3 endpoints:

- /api/initialize: This endpoint creates the chatbot and logger object for that specific session.
- /api/chat: This endpoint is responsible for running the chatbot and processing a user's message. Each message is logged to that sessions log file.
    - If the chat bot returns false for completing a request, it needs more context. This log file gets copied into the /logs/needs_context
    dirctory.
- /api/feedback/{feedback_type}: This endpoint recieves a disliked or liked feedback type, and copies the log file for that session into either the /logs/disliked or logs/liked directory.

## Frontend

If you are interested in viewing the front end code, this can be found under the pocketworlds/client directory.

# Local Model Alternative

The current implementation uses OpenAI's models, but the architecture is designed for easy switching to local open-source models:

1. Model Replacement:

```python
# Current OpenAI implementation
from langchain.llms import OpenAI
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Local model alternative, using mistral
from langchain.llms import HuggingFacePipeline
llm = HuggingFacePipeline.from_model_id(
    model_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    device="cuda"
)
```

2. Embedding Model Replacement:

```python
# Replace OpenAI embeddings
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)
``` 

# Running

## Setup

1. Create a .env file in the root directory: pocketworlds-takehome/.env
2. Create an OpenAI API key, and a variable inside of the .env file:

```
OPENAI_API_KEY="Your Key Here"
```

3. Install server dependencies, create either a new Python env or Conda.

```
cd pocketworlds/server
pip install -r requirements.txt
```

4. Install client dependencies. This requires node.js (npm/npx)

```
cd pocketworlds/client
npm install
```

5. Start the server.

```
uvicorn main:app --reload
```

6. Start the client.

```
npm start dev
```