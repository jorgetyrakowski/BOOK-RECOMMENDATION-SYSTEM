The application for this project is a Book Recommendation System. It uses collected data from the internet (details in Data Sources segment) to predict what books a user is likely to enjoy based on a similar book they have read/are interested in.
The Recommendation System uses mainly the method known as Collaborative Filtering (CF) to achieve this. The underlying assumption of CF is that if a person A has the same opinion as a person B on an issue, A is more likely to have B's opinion on a different issue than that of a random person.

Brief Model Explanation:
Data Matrix: We start with a matrix where each row corresponds to a user, and each column corresponds to an item (in our case, books). The matrix entries are the ratings users have given to the books.
Similarity Assessment: The model looks for similarities between users based on their ratings. If two users have rated a set of books similarly, the model infers that they have similar tastes.
Predicting Ratings: For a given user, the model predicts how they would rate books they haven't yet interacted with by aggregating the ratings of similar users. These predictions are based on the weighted average of the ratings from similar users, adjusted for the active user's overall rating behavior.


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
