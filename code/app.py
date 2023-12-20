# Importing necessary modules
import math  # Importing the math module for mathematical functions
import json  # Importing the json module for working with JSON data
import itertools  # Importing the itertools module for iteration utilities
import re  # Importing the re module for regular expressions

# Class definition for document retrieval and ranking
class Docs:
    def index(self, query):
        # Function to create an index from a given query
        query_words = query.split(" ")
        q_termfreq = {}
        for i in query_words:
            if i not in q_termfreq:
                q_termfreq[i] = 1
            else:
                q_termfreq[i] += 1
        return q_termfreq

    def t_weights(self, tf):
        # Function to compute term weights based on term frequencies
        t_weights_dict = {}
        for i in tf:
            if tf[i] != 0:
                t_weights_dict[i] = 1 + round(math.log10(tf[i]), 4)
            else:
                 t_weights_dict[i] = 0
        return t_weights_dict

    def calculate_document_frequency(self, doc_freq, tf):
        # Function to calculate document frequency for query terms
        qword_d_frequency = {}
        for i in tf:
            if i in doc_freq:
                qword_d_frequency[i] = doc_freq[i]
        return qword_d_frequency

    def calculate_logfrequency(self, doc_freq, N):
        # Function to compute logarithmic term frequency based on document frequency and total documents
        logtf_dictionary = {}
        for i in doc_freq:
            logtf_dictionary[i] =1 + round(math.log10(N/doc_freq[i]), 4)  
        return logtf_dictionary  

    def euclidean_distance(self, vals):
        # Function to calculate Euclidean distance for normalization
        e_dist = 0
        for i in vals:
            e_dist += vals[i] ** 2

        if e_dist != 0:
            normalized_vectors = {i: round(vals[i]/math.sqrt(e_dist), 4) for i in vals}
            return normalized_vectors
        else:
            return vals

    def log_termfrequency(self, tf, idf):
        # Function to compute log term frequency by multiplying term frequency with inverse document frequency
        log_tf_dict = {}
        for i in tf:
            log_tf_dict[i] = tf[i]*idf[i]
        return log_tf_dict

    def cosine_score(self, doc_score, query_score):
        # Function to calculate cosine score between document and query
        score = 0
        for i in doc_score:
            score += doc_score[i]*query_score[i]
        return score

    def calc_tf_idf(self, tf, doc_freq, N):
        # Function to calculate TF-IDF values for terms in the query
        t_weights_dict = self.t_weights(tf)
        qword_d_frequency = self.calculate_document_frequency(doc_freq,tf)
        logtf_dictionary = self.calculate_logfrequency(qword_d_frequency, N)
        tf_idf = self.log_termfrequency(t_weights_dict, logtf_dictionary)
        tf_idf_norm = self.euclidean_distance(tf_idf)
        return tf_idf_norm


# Creating an instance of the Docs class for document retrieval
docs_retrieval = Docs()

# Setting the total number of documents in the dataset
N = 100000

# Opening the inverted index file
f = open('inverted_index.json', "r")
# Loading the inverted index data from the file
data = json.load(f)
# Closing the file
f.close()

# Initializing query and query number
query = ""
q_num = 0

# Loop for accepting queries until the user enters "quit"
while query != "quit":
    # Resetting the query and query postings
    query = ""
    query_postings = {}
    
    # If the query is empty, prompt the user for a new query
    if query == "":
        print("-----------------------------Wikipedia-Based Document Ranking------------------------------\n")
        query = input("Query to search : ")
        q_num += 1  # Incrementing query number
        if query == "quit":
            break  # Exit the loop if the user enters "quit"

    # Convert the query to lowercase
    q = query.lower()
    # Create an index for the query terms
    q_tf = docs_retrieval.index(q)

    # Get the number of unique words in the query
    words_list = len(q_tf)
    words_notfound = 0

    # Loop through query terms and retrieve postings from the inverted index
    for word in q_tf:
        try:
            query_postings[word] = data[word]
        except:
            words_notfound += 1

    # If all query terms are not found in the inverted index, decrement the query number
    if words_notfound == words_list:
        q_num -= 1

    # Close the file
    f.close()
    # Dictionary to store term frequencies for query terms in postings
    iquery_tf = {}
    
    # Populate iquery_tf with term frequencies for query terms in postings
    for word in query_postings:
        iquery_tf[word] = q_tf[word]

    # List to store unique document IDs from postings
    merged_lists = []

    # Loop through query postings and create a list of unique document IDs
    for word in query_postings:
        for i in query_postings[word]['postings']:
            if i["doc"] not in merged_lists:
                merged_lists.append(i["doc"])

    # Dictionary to store term frequencies for each document in merged_lists
    docs_tf = {}

    # Loop through documents in merged_lists and populate docs_tf
    for doc in merged_lists:
        doc_tf = {}
        # Open the document file and read its content
        f = open('Wiki_Dataset/{}.txt'.format(str(doc)), encoding='utf8')
        lines = f.read()
        # Use regular expressions to remove symbols from the document text
        c = re.sub('([^a-zA-Z0-9+])', " ", lines)
        f.close()
        # Create an index for the cleaned document text
        idoc_tf = docs_retrieval.index(c.lower())
        
        # Populate doc_tf with term frequencies for terms in the current document
        for word in idoc_tf:
            if word in data:
                doc_tf[word] = idoc_tf[word]
        docs_tf[doc] = doc_tf

    # Dictionary to store cosine similarity scores for each document
    cosine_scores = {}

    # Loop through documents in merged_lists and calculate cosine similarity scores
    for doc in merged_lists:
        query_tf = {}

        # Populate query_tf with term frequencies for terms in the current document
        for word in docs_tf[doc]:
            if word in iquery_tf:
                query_tf[word] = iquery_tf[word]
            else:
                query_tf[word] = 0
        
        doc_freq = {}

        # Loop through terms in query_tf and calculate document frequencies
        for word in query_tf:
            freq_sum = 0
            for i in data[word]['postings']:
                freq_sum += int(i["freq"])
            doc_freq[word] = freq_sum

        # Calculate TF-IDF values for the query and document
        tf_idf_query = docs_retrieval.calc_tf_idf(query_tf, doc_freq, N)
        tf_idf_doc = docs_retrieval.calc_tf_idf(docs_tf[doc], doc_freq, N)

        # Calculate cosine similarity score for the document
        cosine_score = docs_retrieval.cosine_score(tf_idf_doc, tf_idf_query)
        cosine_scores[doc] = cosine_score

    # Dictionary to store ranked documents based on cosine similarity scores
    ranked_docs = {}
    ranked_docs = {k: v for k, v in sorted(cosine_scores.items(), key=lambda item: item[1])}
    
    # Dictionary to store final ranked documents with additional information
    final_ranked_docs = {}

    # Initialize rank counter
    rank = 0
    
    # Loop through ranked documents and store additional information
    for doc_id in reversed(ranked_docs):
        doc_info = {}
        rank += 1  # Increment rank
        doc_info["score"] = cosine_scores[doc_id]
        doc_info["rank"] = rank
        final_ranked_docs[doc_id] = doc_info

    # Display the final ranked documents with text
    print()
    print("Final ranked documents with text:")
    
    for doc_id in final_ranked_docs:
        doc_info = final_ranked_docs[doc_id]
        
        print(f"Document ID: {doc_id}, Rank: {doc_info['rank']}, Score: {doc_info['score']}")
        
        # Open the document file and read its content
        with open('Wiki_Dataset/{}.txt'.format(str(doc_id)), encoding='utf8') as f:
            document_text = f.read()
            # Remove symbols and print only text
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', document_text)
            print("Document Text:\n", cleaned_text)  # Print the entire document
            
        print("\n" + "=" * 150)

        # Stop after printing the top 10 documents
        if doc_info['rank'] == 10:
            break

    # Display document IDs and ranks for the top 10 retrieved documents
    print("\nDocument IDs and Ranks for the top 10 retrieved documents:")
    
    for doc_id, doc_info in final_ranked_docs.items():
        print(f"Document ID: {doc_id}, Rank: {doc_info['rank']}")

    # Dictionary to store a sample of the top 10 retrieved documents
    sample = {}
    try:
        sample = dict(itertools.islice(final_ranked_docs.items(), 10))
    except:
        sample = dict(itertools.islice(final_ranked_docs.items(), 10))

    # Dictionary to store retrieved results in JSON format
    ret = {}
    
    # Read existing retrieved results from the file
    if str(q_num) != "1":
        with open("json/ranked.json") as infile:
            ret = json.load(infile)
            ret[str(q_num)] = sample
            ret = json.dumps(ret, indent=4)
        with open("json/ranked.json", "w") as outfile:
            outfile.write(ret)
    else:
        with open("json/ranked.json", "w") as outfile:
            ret[str(q_num)] = sample
            outfile.write(json.dumps(ret, indent=4))

    # Dictionary to store relevance information for retrieved documents
    relevant_documents = {}
    
    # Read existing relevance information from the file
    if str(q_num) != "1":
        with open("json/relevance_docs.json") as infile:
            relevant_documents = json.load(infile)
    else:
        relevant_documents = {}

    # List to store relevant document IDs
    relevant_list = []
    
    # Loop through the sample and ask user for relevance feedback
    for doc_id in sample:
        relevance = int(input(f"Document {doc_id} relevant? or not press 0 or 1: "))
        if relevance == 1:
            relevant_list.append(doc_id)

    # Store relevant document IDs for the current query
    relevant_documents[str(q_num)] = relevant_list

    # Write the updated relevance information to the file
    with open("json/relevance_docs.json", "w") as outfile:
        relevant = json.dumps(relevant_documents, indent=4)
        outfile.write(relevant)

# End of the main loop

# Close the last open file
f.close()

# Display a message indicating the end of the program
print("Program terminated. Have a nice day!")
