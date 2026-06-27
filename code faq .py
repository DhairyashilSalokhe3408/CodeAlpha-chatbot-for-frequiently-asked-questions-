import spacy 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
# load spacy nlp model for preprocessing 
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
# hp gas distributon faq stored q ans 
hp_gas_faq = [
    {
        "question":"how can i book hp gas cylinder refill?",
        "answer":"you can book a refill via the hp pay mobile app, online at the myhpgas portal, by calling our number(0000000000)"
    },
    {
        "question":" what documents are required for a new hp gas connection?",
        "answer": " to get a new domestic lpg connection submit a proof of identity aadhar or a pan card and a proof of address electricity bill online or your nearest lpg gas station"
    },
    {
        "question":"how do i cheak my LPG sabsidy status?",
        "answer":" log in to your my hp gas portal and navigare to 'view cylinder booking histary' to track your subsidy. cheak your bank account and aadhar are linked to your lpg connection"
    },
    {
        "question":"what i do in case of an lpg gas leakage emergency?",
        "answer":" immediate close the cylinder regulating volve, open the all doors and windows for ventilation. don't on off any electric equipment and go to a safe place"
    },
    {
        "question":"whar are the current prise of hp gas 14.2 kg domastic cylinder ?",
        "answer":" the prise of a lpg gas varies monthly causes of taxces to local and state taxces. please cheak the 'tariff Card ' section on the official hp gas website or view the updated pricing directly inside the hp pay application"
    },
    {
        "question":" how can i update my registered mobile number ?",
        "answer":"you can change your mobile number online through your MY HP GAS profile portal or by submitting a physycal KYC update from to your local HP gas distribution office"
    }
]
# extract list for vector operation 
faq_questions = [item["question"] for item in hp_gas_faq]
faq_answer = [item["answer"] for item in hp_gas_faq]
# domain spacific text processing 
def preprocess_text(text):
    """tocanizer, cleans stop words, and lemmatizes text """
    doc = nlp(text.lower().strip())
    cleaned tokens =[
        token.lemma_for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return" ".join(clened_tokens)

# process the knowledge base 
preprocessed_questions = [preprocess_text(q) for q in faq_questions]
# fit tf idf vectorizer 
vectorizer = TfidVectorizer.fit_transform(preprocessed_questions)
#machine engine 
def get_hp_gas_responce(user_query,threshold = 0.25):
    """calculate intent match using cosine similarity."""
    clened_query = preprocess_text (user_quary)

# cheak if string is completely empty after clening 
if not clened_quary.strip():
    return "welcome to hp gas support. please type a specific query (eg 'how to book a cylinder ')."

#convert quary into matrix space 
quary_vector = vectorizer.transform([clened_query])
# compute similarity array
similarity_scores= cosine_similarity(quary_vector,tfidf_matrix).flatten()
#extract peak match
best_match_idx = similarity_scorcs.argmax()
highest_score = similarity_scores[best_match_idx]

#evaluate confidance threshold 
if highest_score>=threshold:
    return faq_answer[best_match_idx]
else:
    return"i am sorry, i couldn't find an exact match for your hp gas request. For assistance, you can call our helpline or register a ticket on the My HP Gas portal."

#interactive terminal chat loop 
def run_hp_bot():
    print ("="*60)
    print("          HP GAS DISTRIBUTION CUSTOMER HELPDESK CHATBOT ")
    print("="*60)
    print(type your question below (eg. 'my cylinder is leaking' or 'book gas'))
    print("type 'exit' to end the session .")
    print("-"*60)
    while true: 
        user_input = input("\nyou:")
        if user_input.lower() in ['quit','exit','bye']:
            print("chatbot : thank you for choosing hp gas. have a safe day ahead!")

break

responce = get_hp_gas_response(user_input)
print(f"chatbot :{response}")
if __name__=="__main__":
    run_hp_bot()
        



    
