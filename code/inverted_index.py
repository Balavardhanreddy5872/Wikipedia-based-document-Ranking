import json

def document_tokenization(doc, delimiters, after_delimiters, stop_words, docId):
    # Replace delimiters with space
    for i in delimiters:
        doc = str(doc).replace(i, ' ')

    # Replace stop words with space
    for i in stop_words:
        doc = str(doc).replace(" "+i+" ", ' ')

    # Replace after_delimiters with space
    for i in after_delimiters:
        doc = str(doc).replace(i, ' ')

    # Split the document into terms
    split_terms = str(doc).split(' ')
    tokenized_terms = []

    # Create a list of tokenized terms
    for i in split_terms:
        if(i.lower() not in stop_words and i != ''):
            tokenized_terms.append({'term': i.lower(), 'docId': docId})
    return tokenized_terms

def create_invertedindex(dictionary):
    term_postings = {}

    # Iterate through the dictionary to create an inverted index
    for i in dictionary:
        if term_postings.get(i['term']) == None:
            term_postings[i['term']] = {'frequency': 0, 'posting_list': {}}

        # Update the posting list and frequency
        if i['docId'] not in term_postings[i['term']]['posting_list'].keys():
            term_postings[i['term']]['posting_list'][i['docId']] = 1
        else:
            term_postings[i['term']]['posting_list'][i['docId']] += 1
        term_postings[i['term']]['frequency'] = term_postings[i['term']]['frequency'] + 1

    return term_postings

if __name__ == '__main__':
    # Open the stop words file
    stop_words_file = open('json/stop.txt', 'r+', encoding='utf8')

    # Define delimiters and after_delimiters
    delimiters = ['.', ',', '“', '”', '-', "’s","'s", "\n", "\t", '—', '/',
                  '(', ')', "!", "&", "~", "@", "#", "$", "%", "^", "*", "_", "₹", '\\',
                  "+", "=", "`", "<", ">", "?", "|", "[", "]", "{", "}", ":", ";", "\xa0", "'", '"',"'", "’", "‘"]

    after_delimiters = ["'", "’", "‘"]

    # Read stop words from the file
    stop_words = stop_words_file.read().split('\n')
    dictionary = []  # List to store tokenized terms

    # Iterate through documents
    for number in range(0, 100010):
        number = number + 1
        if number % 5000 == 0:
            print('Indexing document {num}'.format(num=number))
        try:
            # Open each document
            document = open('./Wiki_Dataset/{}.txt'.format(str(number)), 'r+', encoding='utf8')

            # Tokenize the document
            words_after_filtering = document_tokenization(document.read().lower(), delimiters, after_delimiters,
                                                          stop_words, number)

            # Add the tokenized terms to the dictionary
            dictionary = dictionary + words_after_filtering
            document.close()
        except:
            print("Page not in correct form")

    stop_words_file.close()

    # Sort the dictionary based on terms
    dictionary = sorted(dictionary, key=lambda k: k['term'])

    # Create the inverted index
    term_postings = create_invertedindex(dictionary)

    # Convert the inverted index to JSON format
    json_dta = {}
    for i in term_postings:
        json_dta[i] = {"postings": [{"doc": str(x), "freq": str(term_postings[i]['posting_list'][x])}
                                     for x in term_postings[i]['posting_list'].keys()]}

    # Save the inverted index as a JSON file
    with open('inverted_index.json', 'w') as f:
        json.dump(json_dta, f, indent=4)
    f.close()
