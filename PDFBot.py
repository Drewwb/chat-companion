from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core._api import LangChainDeprecationWarning
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import OnlinePDFLoader
import tkinter as tk
from tkinter import scrolledtext

import os
import warnings

# Try to suppress deprecated warnings
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Read PDF file
pdfreader = PdfReader('test.pdf')

rawText = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        rawText += content

# Initialize text splitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(rawText)

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Create FAISS index for document search
document_search = FAISS.from_texts(texts, embeddings)

# Load question answering chain
chain = load_qa_chain(OpenAI(), chain_type="stuff")

# Method used for Testing
def get_bot_response(message):
    """
    Function to get the bot's response for a given message.
    Used for Testing.

    Args:
        message (str): The message to send to the bot.

    Returns:
        str: The bot's response.
    """
    docs = document_search.similarity_search(message)
    response_from_bot = chain.run(input_documents=docs, question=message)
    return response_from_bot

def send_message(event=None):
    """
    Function to send a message to the chatbot.

    Args:
        event (tk.Event, optional): Event object. Defaults to None.
    """
    message = user_input.get("1.0", tk.END).strip()
    if message:
        chat_log.insert(tk.END, "You: " + message + "\n")
        docs = document_search.similarity_search(message)
        response_from_bot = chain.run(input_documents=docs, question=message)
        chat_log.insert(tk.END, "Chatbot: " + response_from_bot + "\n")
        user_input.delete("1.0", tk.END)

# Create a tkinter window
root = tk.Tk()
root.title("PDF Bot")

# Text area for displaying chat log
chat_log = scrolledtext.ScrolledText(root, width=60, height=20)
chat_log.pack()

# Text box for user input
user_input = tk.Text(root, width=60, height=5)
user_input.pack()

# Bind the Enter key to the send_message function
user_input.bind("<Return>", send_message)

# Button to send the message
send_button = tk.Button(root, text="Enter", command=send_message)
send_button.pack()

# Start the GUI
root.mainloop()

