import csv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Paths for saving the model
INDEX_PATH = 'D:\\Project\\FYP\\Final-Chatbot\\sberttest\\model\\faiss_index.index'
QA_PATH = 'D:\\Project\\FYP\\Final-Chatbot\\sberttest\\model\\qa_data.pkl'

# Ensure the directory exists
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

# Function to save the trained model
def save_model(index, questions, answers):
    try:
        faiss.write_index(index, INDEX_PATH)  # Save FAISS index
        with open(QA_PATH, 'wb') as f:
            pickle.dump((questions, answers), f)  # Save Q&A pairs
        print("Model saved successfully.")
    except Exception as e:
        print(f"Error saving model: {e}")

# Function to extract question and answer pairs from CSV
def extract_qa_from_csv(csv_path):
    questions = []
    answers = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row.get('Question', '').strip()
            answer = row.get('Answer', '').strip()
            if question and answer:
                questions.append(question)
                answers.append(answer)
    return questions, answers

# Generate embeddings using SBERT
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text_list):
    return model.encode(text_list)  # Generate embeddings for questions

# Create FAISS vector DB from embeddings
def create_vector_db(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))  # Ensure embeddings are numpy array
    return index

# Function to train chatbot and save the model
def train_chatbot_with_csvs(csv_paths):
    all_questions = []
    all_answers = []
    all_embeddings = []

    for csv_path in csv_paths:
        questions, answers = extract_qa_from_csv(csv_path)
        embeddings = generate_embeddings(questions)
        all_questions.extend(questions)
        all_answers.extend(answers)
        all_embeddings.append(embeddings)

    all_embeddings = np.vstack(all_embeddings)
    index = create_vector_db(all_embeddings)

    # Save the model after training
    save_model(index, all_questions, all_answers)

if __name__ == '__main__':
    # Paths to your CSV files
    csv_paths = [
        'D:/Project/FYP/Final-Chatbot/sberttest/data/faculty.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/greeting.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/incomplete_questions.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/university_about.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/more_about_faculty.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/university_qa.csv',
        'D:/Project/FYP/Final-Chatbot/sberttest/data/developed_by.csv'
    ]

    # Train and save the model
    train_chatbot_with_csvs(csv_paths)