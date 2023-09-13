# Langchain Streamlit App with GPT-3.5

## 1. Configure app secrets

This app will use GPT-3.5, so we'll also need an OpenAI API key.

Create a `.streamlit` folder and a `secrets.toml` file with the following contents.

```toml
openai_key = "<your OpenAI API key here>"
```

**Note**: If you're using Git, be sure to add the name of this file to your `.gitignore` so you don't accidentally expose your API key. If you plan to deploy this app on Streamlit Community Cloud, the following contents should be added to your app's secrets via the Community Cloud modal.

## 2. Install dependencies

### 2.1. Local development

If you're working on your local machine, install dependencies using pip:

```bash
pip install streamlit openai llama-index nltk
```

### 2.2. Cloud development

If you're planning to deploy this app on Streamlit Community Cloud, create a `requirements.txt` file with the following contents:

```bash
streamlit
openai
llama-index
nltk
```

## 3. Build the app

The full app is only ~50 lines of code. Let's break down each section:

### 3.1. Import libraries

Required Python libraries for this app: streamlit, llama_index, openai, and nltk.

```python
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
```

# ←←

### 3.2. Initialize message history

- Set our OpenAI API key from the app's secrets.
- Add a heading for our app.
- Use session state to keep track of your chatbot's message history.
- Initialize the value of `st.session_state.messages` to include the chatbot's starting message, such as, "Hey, I'm a chatbot! Ask me a question."

# ←←

### 3.3. Load and index data

- We'll Store our Knowledge Base files in a folder called `data` within the app.

- We'll define a function `load_data()` to load and index data using LlamaIndex:

#### Function: `load_data()`

The `load_data()` function is responsible for loading and indexing data stored in a specific directory, typically the `data` directory at the base level of your repository.

Here's a step-by-step breakdown of what the function does:

1. **Using SimpleDirectoryReader**: LlamaIndex's `SimpleDirectoryReader` will take the path to your data directory as an argument. It's designed to automatically choose the right file reader based on the file extensions within the directory. In our case, it will select the reader for `.pdf` files. The reader will then load all the files recursively when you call `reader.load_data()`.

2. **Creating a ServiceContext Instance**: Construct an instance of LlamaIndex’s `ServiceContext`. This encapsulates a collection of resources utilized during a RAG pipeline's indexing and querying processes. One of the key features of `ServiceContext` is the ability to adjust settings. For instance, you can specify which LLM and embedding model you want to use.

3. **Setting up VectorStoreIndex**: Use LlamaIndex’s `VectorStoreIndex` to create an in-memory `SimpleVectorStore`. This structures your data in a manner optimized for quick context retrieval by your model. If you're interested in diving deeper, you can explore more about LlamaIndex’s indices and their inner workings.

4. **Caching**: This function is wrapped in Streamlit’s caching decorator `st.cache_resource` to minimize the number of times the data is loaded and indexed.

The function will return the `VectorStoreIndex` object upon completion.

# ←←

---

### 3.4. Create the chat engine

LlamaIndex offers various modes of chat engines. Here we will use the `condense_question` mode as it always queries the knowledge base which is optimal for our use-case.

# ←←

### 3.5. Prompt for user input and display message history

Use Streamlit's UI elements to gather user input and display the chatbot's message history.

# ←←

### 3.6. Pass query to chat engine and display response

After gathering the user's question, pass it to the chat engine to get a response, then display both the question and the answer in a chat-like interface.

# ←←

### 3.7. Run the app

Run the app with `streamlit run app.py`.

# ←←

### 3.8. Deploy the app

Deploy the app on Streamlit Community Cloud following this [guide](https://blog.streamlit.io/host-your-streamlit-app-for-free/).
