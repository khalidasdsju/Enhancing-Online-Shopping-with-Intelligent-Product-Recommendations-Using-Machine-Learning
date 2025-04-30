from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import logging
import os
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Start timing for model loading
start_time = time.time()
logger.info("Loading recommendation models...")

# Load models
try:
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    logger.info(f"Models loaded successfully in {time.time() - start_time:.2f} seconds")
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    raise

# Initialize Flask app
app = Flask(__name__)
logger.info("Flask application initialized")

@app.route('/')
def index():
    logger.info("Home page accessed")
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    logger.info("Recommendation page accessed")
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    start_time = time.time()
    user_input = request.form.get('user_input')
    logger.info(f"Recommendation requested for book: '{user_input}'")

    try:
        # Find the book in our pivot table
        if user_input not in pt.index:
            logger.warning(f"Book '{user_input}' not found in dataset")
            return render_template('recommend.html', error=f"Book '{user_input}' not found. Please try another book.")

        # Get the index of the book in pivot table
        index = np.where(pt.index == user_input)[0][0]

        # Get similar books based on similarity scores
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        # Prepare data for template
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        processing_time = time.time() - start_time
        logger.info(f"Recommendation for '{user_input}' generated in {processing_time:.2f} seconds")
        logger.info(f"Recommended books: {[item[0] for item in data]}")

        return render_template('recommend.html', data=data, input_book=user_input)

    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return render_template('recommend.html', error="An error occurred while generating recommendations. Please try again.")

if __name__ == '__main__':
    logger.info("Starting Book Recommendation System")
    logger.info(f"Dataset contains {len(books)} books and {len(pt.index)} unique titles for recommendations")
    logger.info(f"Top books list contains {len(popular_df)} entries")

    # Add a timestamp to know when the server started
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Server starting at: {current_time}")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)