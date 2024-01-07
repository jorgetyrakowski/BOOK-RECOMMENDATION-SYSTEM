import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the datasets
books_path = 'Data/Books.csv'
users_path = 'Data/Users.csv'
ratings_path = 'Data/Ratings.csv'

dtype_dict = {'columna_3': str}

try:
    books_df = pd.read_csv(books_path, low_memory=False)
    users_df = pd.read_csv(users_path)
    ratings_df = pd.read_csv(ratings_path)

    # Display the first few rows of each dataset
    books_head = books_df.head()
    users_head = users_df.head()
    ratings_head = ratings_df.head()
except Exception as e:
    error_message = str(e)

# Cleaning the Books Dataset

# Convert Year-Of-Publication to numeric, set errors to NaN
books_df['Year-Of-Publication'] = pd.to_numeric(books_df['Year-Of-Publication'], errors='coerce')

# Replace invalid years with NaN (e.g., years in the future or too far in the past)
current_year = pd.Timestamp.now().year
books_df.loc[(books_df['Year-Of-Publication'] > current_year) | (books_df['Year-Of-Publication'] < 1800), 'Year-Of-Publication'] = None

# Check for missing values in important columns
missing_values_books = books_df.isnull().sum()

# Drop rows where important information is missing
books_df_cleaned = books_df.dropna(subset=['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher'])

# Cleaning the Users Dataset

# Handling missing values in 'Age'
# Replace invalid ages (e.g., less than 5 and greater than 100) with NaN
users_df['Age'] = users_df['Age'].apply(lambda x: x if 5 <= x <= 100 else None)

# Check for missing values
missing_values_users = users_df.isnull().sum()

# Validate the ISBN references
# Keep only those ratings where the ISBN exists in the books dataset
ratings_df_cleaned = ratings_df[ratings_df['ISBN'].isin(books_df_cleaned['ISBN'])]

# Check for any anomalies in the 'Book-Rating' field
# Assuming ratings should be within a specific range (e.g., 0-10)
ratings_df_cleaned = ratings_df_cleaned[(ratings_df_cleaned['Book-Rating'] >= 0) & (ratings_df_cleaned['Book-Rating'] <= 10)]

# Check for missing values and the size of the cleaned dataset
missing_values_ratings = ratings_df_cleaned.isnull().sum()
cleaned_ratings_size = ratings_df_cleaned.shape

# Reattempting Step 1: Filter the Data

# Filtering users who have rated at least 50 books
users_with_50_ratings = ratings_df_cleaned['User-ID'].value_counts()
users_with_50_ratings = users_with_50_ratings[users_with_50_ratings >= 50].index.tolist()

filtered_ratings = ratings_df_cleaned[ratings_df_cleaned['User-ID'].isin(users_with_50_ratings)]

# Filtering books that have been rated by at least 50 users
books_with_50_ratings = filtered_ratings['ISBN'].value_counts()
books_with_50_ratings = books_with_50_ratings[books_with_50_ratings >= 50].index.tolist()

filtered_ratings = filtered_ratings[filtered_ratings['ISBN'].isin(books_with_50_ratings)]

# Creating a pivot table for the similarity matrix
pivot_table = filtered_ratings.pivot_table(index='ISBN', columns='User-ID', values='Book-Rating').fillna(0)

# Calculating cosine similarity between items (books)
cosine_sim = cosine_similarity(pivot_table)

# Creating a DataFrame for the similarity matrix for better readability
similarity_matrix = pd.DataFrame(cosine_sim, index=pivot_table.index, columns=pivot_table.index)

def get_book_title(isbn, books_df):
    """ Get the book title given an ISBN. """
    title = books_df.loc[books_df['ISBN'] == isbn, 'Book-Title'].iloc[0]
    return title

def recommend_books(isbn, similarity_matrix, books_df, num_recommendations=5):
    """
    Recommend books based on a given ISBN using the item similarity matrix.
    """
    # Retrieve similar books
    similar_books = similarity_matrix[isbn].sort_values(ascending=False)

    # Remove the book itself from the recommendation
    similar_books = similar_books[similar_books.index != isbn]

    # Get the top N similar books
    top_similar_books = similar_books.head(num_recommendations).index.tolist()

    # Get book titles
    recommended_books = [get_book_title(book_isbn, books_df) for book_isbn in top_similar_books]

    return recommended_books

def get_book_info(isbn, books_df):
    """ Get the book title and image URL given an ISBN. """
    book_info = books_df.loc[books_df['ISBN'] == isbn, ['Book-Title', 'Image-URL-L']].iloc[0]
    return book_info

def recommend_books_with_images(isbn, similarity_matrix, books_df, num_recommendations=5):
    """
    Recommend books based on a given ISBN using the item similarity matrix,
    and include their images.
    """
    # Retrieve similar books
    similar_books = similarity_matrix[isbn].sort_values(ascending=False)

    # Remove the book itself from the recommendation
    similar_books = similar_books[similar_books.index != isbn]

    # Get the top N similar books
    top_similar_books = similar_books.head(num_recommendations).index.tolist()

    # Get book titles and image URLs
    recommended_books_info = [get_book_info(book_isbn, books_df) for book_isbn in top_similar_books]

    return recommended_books_info

def streamlit_app():
    st.title('Book Recommendation System')

    # Create a dictionary to map book titles to their ISBNs, only for books in the similarity matrix
    valid_isbns = similarity_matrix.index.tolist()
    books_df_filtered = books_df[books_df['ISBN'].isin(valid_isbns)]
    title_to_isbn = books_df_filtered.set_index('Book-Title')['ISBN'].to_dict()

    # Allow the user to select a book by its name
    selected_title = st.selectbox('Choose a book to get recommendations:', books_df_filtered['Book-Title'].unique())
    selected_isbn = title_to_isbn[selected_title]

    # Show the selected book's title and image
    book_info = get_book_info(selected_isbn, books_df_filtered)
    st.image(book_info['Image-URL-L'], width=200)

    # Button to get recommendations
    if st.button('Recommend Books'):
        try:
            recommended_books_info = recommend_books_with_images(selected_isbn, similarity_matrix, books_df_filtered)
            st.write('Recommendations:')

            # Create columns for each recommendation to display images side by side
            cols = st.columns(len(recommended_books_info))  # Adjust the number of columns based on the recommendations
            for col, book in zip(cols, recommended_books_info):
                with col:
                    st.image(book['Image-URL-L'], width=150)  # Adjust width as needed
                    st.write(book['Book-Title'])
        except KeyError as e:
            st.error(f'An error occurred with the selected book: {e}')

# Run the Streamlit application
if __name__ == '__main__':
    streamlit_app()