# pocketworlds-faq
Pocket Worlds take home assignment for the Software Engineer (AI) position.

A conversational AI chatbot designed to assist users with Highrise-related questions. Built with FastAPI, React, and leveraging OpenAI models (read below for open-source, local model usage), deployed on a self-hosted Debian server with nginx.

**Notes and Basic Details**
- This uses RAG, or Retrieval Augmented Generation, to retrieve relevant information based on the user input.
- If a user input does not meet a certain similarity search threshold (when running retrieval on the vector database, currently set at 70%), this will return a default response asking for more information.
- I initially set this up with Vercel, but because of the size of the Chroma DB library and dependencies, I was running into deployment errors so I set up the application on my personal server.

**Additional (Optional) Features**
*Basic NLP techniques:* Using the NLTK library, and with RAG by default.
*User Feedback:* This is setup by a "like and dislike" button after each chat bot response. Sorted on the backend server in the logs directory.
*Open Source Model Hosting:* Not implemented because I don't have enough compute on my server but I have instructions below in the README.md on how I would do it. It is as simple as downloading a model and changing ~5 lines of code.

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

# Key Modules

## Data Pipeline


## Chat Bot
[View chat_bot.py](https://github.com/adamloec/pocketworlds-faq/blob/main/pocketworlds/server/chat/chat_bot.py)

- Chat Bot object that handles the chat bot processes:
1. Initialization extracts FAQ URLS and creates the vector database of each URL's web page content.
2. 

# Running Locally

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