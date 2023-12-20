import statistics
import numpy as np
import matplotlib.pyplot as plt
import json

# List to store average precision values for each query
avg_precision = []

# Lists to store recall and precision values for each query
rec = []
prec = []

# Function to calculate recall for a given set of retrieved and relevant documents
def recall(retrieved, relevant):
    total_retrieved = 0
    for i in retrieved:
        for j in range(len(relevant)):
            if i == relevant[j]:
                total_retrieved += 1
        val = list(retrieved.keys()).index(i) + 1
        # Calculate and print recall at each position
        print('Recall at', val, 'is:', total_retrieved / float(len(relevant)))
        rec.append(total_retrieved / float(len(relevant)))

# Function to calculate precision for a given set of retrieved and relevant documents
def precision(retrieved, relevant):
    total_retrieved = 0
    for i in retrieved:
        for j in range(len(relevant)):
            if i == relevant[j]:
                total_retrieved += 1
        val = list(retrieved.keys()).index(i) + 1
        # Calculate and print precision at each position
        print('Precision at', val, 'is:', total_retrieved / float(val))
        prec.append(total_retrieved / float(val))

# Function to calculate F1 score using precision and recall
def F1(prec, rec):
    f1_score = 0.0
    for i in range(len(prec)):
        if rec[i] == 0.0 and prec[i] == 0.0:
            f1_score = 0.0
            print("F1 score at", i+1, "is : ", f1_score)
        else:
            f1_score = ((2*(prec[i])*(rec[i]))/(prec[i] + rec[i]))
            print("F1 score at", i+1, "is : ", f1_score)
        f1_score = 0.0

# Function to calculate 11-point interpolated precision
def eleven_point_interpolation(prec, rec):
    eleven_points_prec = []
    recall_levels = np.arange(0, 1.1, 0.1)

    for level in recall_levels:
        max_precision = 0.0
        for i in range(len(rec)):
            if rec[i] >= level:
                max_precision = max(max_precision, prec[i])
        eleven_points_prec.append(max_precision)

    return eleven_points_prec

# Load retrieved and relevant documents from JSON files
ret = {}
with open("json/ranked.json") as infile:
    ret = json.load(infile)

relevant = {}
with open("json/relevance_docs.json") as infile:
    relevant = json.load(infile)

# Iterate over queries
for i in ret:
    print(i)
    print("For Query {query}: ".format(query=i))
    recall(ret[i], relevant[i])
    print()
    precision(ret[i], relevant[i])

    F1(rec, prec)

    # Calculate Average Precision for query i
    sum_q = 0.0
    for j in range(len(prec)):
        sum_q = sum_q + prec[j]

    print(i)
    averagep_q = sum_q / (len(relevant[i]))
    print("Average precision {query} is : ".format(query=i), averagep_q)
    avg_precision.append(averagep_q)

    # Plot Precision-Recall curve for query i
    plt.figure(figsize=(8, 6))
    plt.plot(rec, prec, label='Precision-Recall Curve')
    plt.title('Precision-Recall curve for Query {query}'.format(query=i))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.grid()
    plt.savefig('precision-recall curve for query {query}.png'.format(query=i))
    plt.show()

    # Plot 11-point interpolated precision for query i
    plt.figure(figsize=(8, 6))
    eleven_points_prec = eleven_point_interpolation(prec, rec)
    plt.plot(np.arange(0, 1.1, 0.1), eleven_points_prec, marker='o', linestyle='dashed', label='11-point Interpolated Precision')
    plt.title('11-point Interpolated Precision for Query {query}'.format(query=i))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.grid()
    plt.savefig('11-point interpolated precision for query {query}.png'.format(query=i))
    plt.show()

    # Print values of 11-point interpolated precision
    for j in range(len(eleven_points_prec)):
        print("Recall =", np.around(j * 0.1, 1), "Precision =", np.around(eleven_points_prec[j], 2))

    # Clear lists for the next iteration
    rec.clear()
    prec.clear()

    print()

# Calculate Mean Average Precision
mean_avg_precision = statistics.mean(avg_precision)
print("Average Precision query {i}  : ".format(i=len(ret)), mean_avg_precision)
