## The application for this project is a Book Recommendation System. 
It uses collected data from the internet (details in Data Sources segment) to predict what books a user is likely to enjoy based on a similar book they have read/are interested in.
The Recommendation System uses mainly the method known as Collaborative Filtering (CF) to achieve this. The underlying assumption of CF is that if a person A has the same opinion as a person B on an issue, A is more likely to have B's opinion on a different issue than that of a random person.

### Brief Model Explanation:
Data Matrix: We start with a matrix where each row corresponds to a user, and each column corresponds to an item (in our case, books). The matrix entries are the ratings users have given to the books.
Similarity Assessment: The model looks for similarities between users based on their ratings. If two users have rated a set of books similarly, the model infers that they have similar tastes.
Predicting Ratings: For a given user, the model predicts how they would rate books they haven't yet interacted with by aggregating the ratings of similar users. These predictions are based on the weighted average of the ratings from similar users, adjusted for the active user's overall rating behavior.

### What the application does, step by step.
##### 1.	Setup
Using predetermined Database Connection Parameters (IP, port, name, user, password), we create a connection to our database on AWS with python and the psycopg2 package, then create an “engine” to manage said connection with AWS, using the sqlalchemy package.
With this setup, we use SQL queries with the pandas package to store our tables as dataframes.

##### 2.	Cleaning
The next step is cleaning and preparing the data in these dataframes. This process involves handling missing values, outliers, and normalizing formats, for each dataframe.

Details:
The cleaning of the Books dataset has been completed with the following steps:
-	Converted Year-Of-Publication to numeric, setting non-numeric values to NaN.
-	Replaced invalid years (those in the future or before 1800) with NaN.
-	Checked for missing values in key columns (Book-Author, Year-Of-Publication, Publisher). We found:
-	Book-Author: 1 missing value
-	Year-Of-Publication: 4,635 missing values
-	Publisher: 2 missing values
-	Dropped rows with missing values in these critical columns.
The cleaning of the Users dataset has been done with these steps:
-	Invalid ages (less than 5 or greater than 100) have been replaced with NaN.
-	There are 112,010 missing values in the Age field.
-	We chose not to impute ages due to potential inaccuracies, and because removing all rows with missing ages could significantly reduce the dataset.
-	The Location field has been left as is for now, as normalization can be complex and may not be crucial for the recommendation system.
The cleaning of the Ratings dataset has been completed with the following steps:
-	Validated ISBN references, ensuring all ratings correspond to books present in the cleaned Books dataset.
-	Checked for anomalies in Book-Rating, confirming all ratings are within the expected range (0-10).
-	No missing values were found in the cleaned Ratings dataset.
-	The size of the cleaned Ratings dataset is 1,017,065 rows.

##### 3.	Build the Item Similarity Matrix
We will calculate the similarity between items (books) using the user ratings. Commonly used methods for similarity include cosine similarity, Pearson correlation, or Jaccard similarity. We'll select cosine similarity for our current project. 
This matrix represents the similarity between each pair of books based on user ratings. In the matrix, each row and column correspond to a book's ISBN, and the values represent the similarity score between books.
Small 5x5 example section of an Item Similarity Matrix, using ISBN as indices:
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/db8fe685-4b8e-48c8-bd65-3ae4aa6101fe)

##### 4.	Generating Book Recommendations
In this step, we'll use the Item Similarity Matrix to generate book recommendations using the recommend_books() function (Identical to recommend_books_with_images but without URLs).
The process involves:
-	Selecting a book as input (either randomly or based on a specific ISBN).
-	Finding similar books based on the similarity matrix.
-	Ranking these similar books to recommend the most similar ones.
Code Excerpt and example with a book from the dataset (“Rising Tides”):
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/61548065-6ad6-4287-a79f-2b580c64a0c4)
As we can see by the titles alone, these books share some similarities.

##### 5.	Streamlit app & UI
The app we built with streamlit first run steps one to 3 detailed in this section, then allows us to select a book from the dataset, and it uses this book to recommend us 5 other books we may like with the recommend_books_with_images() function.
Python code is shown in section 7.

#### DEMO:
Choose Book by Title, we can do this by typing in the name or selecting from the drop down list:
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/81237767-6dcb-4b0a-aa00-6d05b0ea5ad6)
To choose a book, we click on it from the drop down list, and wait for it to load:
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/4104bb4f-043c-41ad-8df3-acec915b8382)
To get our Book Recommendation, we press the Recommend Books button, and wait for it to finish processing.
After this, we should see our book recommendations below:
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/c70cffac-20d0-4a50-9c87-d3a902877594)
Example with a different book (Lord of the Flies):
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/2b83c827-8772-442a-b179-f89f6dfac0eb)
Example with a different book (Anee of Green Gables):
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/05a119e5-1172-43d7-aff7-ef5e6295ccd9)
How to run the app:
First install necessary packages, then run the app from the console (preferably):
![image](https://github.com/jorgetyrakowski/BOOK-RECOMMENDATION-SYSTEM/assets/88347278/4db471ce-3415-4da9-aeda-87b67baf4ec4)
As we can see, the recommendations are of good quality, as they are either related to our original book, its themes, or more accurately, its target demographic.
