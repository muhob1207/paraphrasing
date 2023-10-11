# Paraphrasing

Requirements:

python version==3.9.13

pip install sentence_transformers
pip install Django==4.2.1

# Model

The package sentence_transformers was used to get the embeddings of sentences and compute their similarity. Reference:
https://www.sbert.net/examples/applications/paraphrase-mining/README.html

Django was used to create UI and interaction between frontend and backend. 

The phrases are stored in the sql-lite database in the model called Phrase.

A UI to view, add, delete and update phrases has been created. The provided phrases have been added to the database.

A UI that allows a user to enter text, send it for analysis to the backend and receive&display results and suggestions has been created.

Further details and explanation can be found in the code.


# Guide

1)Download the folder called "suggestions" from this repository
2)Navigate to the "suggestions" folder through the terminal. When you type "ls", you should see the file "manage.py" there.
3)Run the command "python manage.py runserver". This will start your localhost. Open the localhost through your browser. At the home page you will be able to find the main UI, where the user can enter text and send it for analysis in the backend. To add phrases, navigate to 'Phrases list'.


