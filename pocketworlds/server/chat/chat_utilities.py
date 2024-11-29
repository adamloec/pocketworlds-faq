"""
Author: Adam Loeckle
Date: 11/26/2024

"""

from typing import Tuple, Optional
import nltk
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
import random

nltk.download('punkt_tab', download_dir="/var/www/pocketworlds-faq/pocketworlds/server/")

def check_greeting_farewell(user_message: str) -> Tuple[Optional[str], bool]:
    """
    Checks if a user's message is a greeting or farewell using fuzzy matching.
    
    :param user_message: The message from the user
    :return: Tuple(response, is_greeting_or_farewell)
    """
    # Define core intents with variations
    intent_patterns = {
        'greeting': {
            'base_words': ['hello', 'hi', 'hey', 'greetings'],
            'phrases': ['good morning', 'good afternoon', 'good evening'],
            'responses': [
                "Hi! I'm here to help you with questions about Highrise. What would you like to know?",
                "Hello! How can I assist you with Highrise today?",
                "Hey there! Feel free to ask me any questions about Highrise."
            ]
        },
        'farewell': {
            'base_words': ['bye', 'goodbye', 'farewell'],
            'phrases': ['see you', 'thank you', 'thanks', 'good night'],
            'responses': [
                "Goodbye! Feel free to return if you have more questions about Highrise.",
                "Thanks for chatting! Have a great day!",
                "See you later! Don't hesitate to ask if you need more help."
            ]
        }
    }

    user_message = user_message.lower().strip()
    tokens = word_tokenize(user_message)
    
    # Check each intent
    for intent, patterns in intent_patterns.items():
        # Check single words with fuzzy matching
        if any(any(fuzz.ratio(token, base_word) > 85 
                  for base_word in patterns['base_words'])
               for token in tokens):
            return random.choice(patterns['responses']), True
            
        # Check phrases
        if any(phrase in user_message for phrase in patterns['phrases']):
            return random.choice(patterns['responses']), True
    
    return None, False

def check_relevance(retriever: None, user_message: str) -> bool:
    """
    Determines if a user's message is relevant to the chatbot's domain.

    :param retriever: The retriever object for checking relevance based on embeddings
    :param user_message: The message from the user
    :return: True if the message is relevant, False otherwise
    """
    if not retriever:
        raise Exception("Relevance checking requires a retriever object.")
        
    retrieved_docs = retriever.invoke(user_message)
    if not retrieved_docs:
        return False
    return True

def get_supporting_urls(retriever: None, user_message: str):
    """
    Retrieves supporting URLs for a user's message using the retriever.

    :param retriever: The retriever object for searching relevant documents
    :param user_message: The message from the user
    :return: A list of URLs relevant to the user's query
    """
    if not retriever:
        raise Exception("Creating supporting data requires a retriever object.")
    
    retrieved_docs = retriever.invoke(user_message)
    supporting_urls = set()
    for doc in retrieved_docs:
        supporting_urls.add(doc.metadata.get('source'))
    return supporting_urls

def create_clarification() -> str:
    """
    Generates a clarification message for when the chatbot cannot understand or process 
    a user's message.

    :return: A predefined clarification message
    """
    clarification_templates = [
        "I'm not quite sure about that. Could you rephrase your question about the Highrise app?",
        "I want to help, but I need more details. What specific feature are you asking about?",
        "I don't have enough information in the FAQ about that. Could you be more specific about what you're looking for?",
        "That's not covered in our FAQ. Are you asking about a specific Highrise feature?"
    ]

    return random.choice(clarification_templates)