# pocketworlds-takehome
Pocket Worlds take home assignment for the Software Engineer (AI) position.

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