TOPIC : WIKIPEDIA BASED DOCUMENT - RANKING 

  Installation:
  i.	Ensure you have Python installed on your machine.
  ii.	Install the necessary libraries using pip:
  iii.	'pip install nltk  matplotlib'
  iv.	Download any additional pakages require to run code.

2. Download the dataset from the drive and place the documents in the code folder.
link : https://drive.google.com/file/d/1iXFaE93I1J2Cau25milsul2A6sqMP3NY/view?usp=drive_link


3.  Download the json fold of inverted index (inverted_index.json) from the drive and place them in the code folder
link : https://drive.google.com/file/d/1k8iEABgnskBifO5Ig-R0B4X0Vpr4hYEn/view?usp=drive_link

HOW TO THE RUN CODE :

Usage :
 i.	First run 'python app.py' by entering the command in the terminal ensure you are in the code folder.
 ii.	 Wait for few seconds to run the code then it asks 'Enter a query in the terminal'.
 iii.	Enter a query (EX: hardwood) in the terminal then it reterives all the documents contain the term hardwood
       Enter the Term "hardwood."or 
       Enter the Term "haredi."
 iv.	Give feedback for every document 1 if it relevant or 0 if it is not relevant.
 v.	In the code folder we have json folder in the ranked.json we have each document score 
 vi.	In the json we have ranked_docs.json we have all the relevant doc ID's 
 vii.	In the code folder  run 'python score.py'  in the termial precision and recall for every document is observed and 
 viii.	Graphs for the precision-recall and 11-point interpolated graphs are plotted .


FUNCTIONALITES:

App.py :
 (i) def index(self, query):
        # Function to create an index from a given query.
 (ii) def t_weights(self, tf):
        # Function to compute term weights based on term
 (iii) def calculate_document_frequency()
        # Function to calculate document frequency for query terms
 (iv) def euclidean_distance(self, vals):
        # Function to calculate Euclidean distance for normalization
 (v) def log_termfrequency(self, tf, idf):
        # Function to compute log term frequency by multiplying term frequency with inverse document frequency
 (vi) def cosine_score(self, doc_score, query_score):
        # Function to calculate cosine score between document and query

score .py 

 (i) # Function to calculate recall for a given set of retrieved and relevant documents
    def recall(retrieved, relevant)
 (ii) # Function to calculate precision for a given set of retrieved and relevant documents
    def precision(retrieved, relevant):
 (iii) # Function to calculate F1 score using precision and recall
     def F1(prec, rec):
 (iv) # Function to calculate 11-point interpolated precision
    def eleven_point_interpolation(prec, rec):
 (v)# Print values of 11-point interpolated precision
    print("Values of 11-point Interpolated Precision for Query {query}:".format(query=i))

generate_pr_curve()
Description: Generates and displays the precision-recall curve for the top 10 documents retrieved based on stored precision and recall value
