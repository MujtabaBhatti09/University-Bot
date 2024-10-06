from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Paths for loading the model
INDEX_PATH = 'D:\\Project\\FYP\\Final-Chatbot\\sberttest\\model\\faiss_index.index'
QA_PATH = 'D:\\Project\\FYP\\Final-Chatbot\\sberttest\\model\\qa_data.pkl'

# Load the SBERT model for embedding queries
model = SentenceTransformer('all-MiniLM-L6-v2')

# Flask application
app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# Function to load the saved model
def load_model():
    if os.path.exists(INDEX_PATH) and os.path.exists(QA_PATH):
        try:
            index = faiss.read_index(INDEX_PATH)
            with open(QA_PATH, 'rb') as f:
                questions, answers = pickle.load(f)
            print("Model loaded successfully.")
            return index, questions, answers
        except Exception as e:
            print(f"Error loading model: {e}")
            return None, [], []
    else:
        print("No saved model found.")
        return None, [], []

# Function to query the FAISS index and return the most relevant answer
def query_vector_db(query, index, questions, answers, top_n=1, confidence_threshold=0.9):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=top_n)

    for i, idx in enumerate(indices[0]):
        if distances[0][i] < confidence_threshold:  # Apply confidence threshold
            if idx < len(answers):
                return answers[idx]  # Return the corresponding answer

    return "Sorry, I don't have an answer for that."

# Handle inappropriate queries
def handle_inappropriate_query(query):
    inappropriate_words = ["fuck", "shit", "bitch", "asshole", "ass hole", "ass wipe", "motherfucker", "mf", "bharway", "bharwa", "gandu", "dalla", "randi", "bharwi", "mc", "madar chod", "bhen k loray", "lora"]
    if any(word in query.lower() for word in inappropriate_words):
        return "Please use appropriate language."
    return None

# Load the model once when the app starts
index, questions, answers = load_model()
@app.route('/', methods=["GET"])
def welcome():
    return jsonify({'response':"Hello Chatbot Loaded"})

# API route for querying the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    # Check for inappropriate words
    inappropriate_response = handle_inappropriate_query(user_input)
    if inappropriate_response:
        return jsonify({'response': inappropriate_response})
    
    # Query the FAISS index
    response = query_vector_db(user_input, index, questions, answers)
    return jsonify({'response': response})

# Run the Flask application
if __name__ == '__main__':
    # app.run(debug=True)
        app.run(host='0.0.0.0', port=5000, debug=True)