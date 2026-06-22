import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load spaCy NLP model for preprocessing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# 2. HP Gas Distribution FAQ Data Store
HP_GAS_FAQ = [
    {
        "question": "How can I book an HP Gas cylinder refill?",
        "answer": "You can book a refill via the HPPay mobile app, online at the MyHPGas portal, by calling our IVRS number (8882434343), or via WhatsApp by texting 'BOOK' to 9222201122."
    },
    {
        "question": "What documents are required for a new HP Gas connection?",
        "answer": "To get a new domestic LPG connection, submit a Proof of Identity (Aadhaar, Passport, PAN) and a Proof of Address (Electricity bill, Rent agreement, Aadhaar) online or at your nearest HP Gas distributorship."
    },
    {
        "question": "How do I check my LPG subsidy status?",
        "answer": "Log into the MyHPGas portal and navigate to 'View Cylinder Booking History' to track your subsidy. Ensure your bank account and Aadhaar card are linked to your LPG connection to receive subsidies directly via DBTL."
    },
    {
        "question": "What should I do in case of an LPG gas leakage emergency?",
        "answer": "EMERGENCY SAFETY STEPS: Immediately close the cylinder regulating valve. Open all doors and windows for ventilation. Do not switch on/off any electrical appliances or light matches. Call our 24/7 emergency helpline instantly at 1906."
    },
    {
        "question": "How do I transfer my HP Gas connection to another city or distributor?",
        "answer": "For local transfers, request an e-CTA (Electronic Customer Transfer Advice) from your current distributor. For inter-city transfers, collect your Termination Voucher (TV) along with your domestic gas consumer card, and submit them to the new distributor in your target area."
    },
    {
        "question": "What is the current price of an HP Gas 14.2kg domestic cylinder?",
        "answer": "LPG cylinder pricing varies monthly by state and locality due to local taxes. Please check the 'Tariff Card' section on the official MyHPGas website or view the updated pricing directly inside the HPPay application."
    },
    {
        "question": "How can I update my registered mobile number (registered phone number)?",
        "answer": "You can change your mobile number online through your MyHPGas profile portal or by submitting a physical KYC update form to your local HP Gas distribution office."
    }
]

# Extract lists for vector operations
faq_questions = [item["question"] for item in HP_GAS_FAQ]
faq_answers = [item["answer"] for item in HP_GAS_FAQ]

# 3. Domain-Specific Text Preprocessing
def preprocess_text(text):
    """Tokenizes, cleans stop words, and lemmatizes text."""
    doc = nlp(text.lower().strip())
    cleaned_tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(cleaned_tokens)

# Preprocess the knowledge base
preprocessed_questions = [preprocess_text(q) for q in faq_questions]

# 4. Fit TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

# 5. Matching Engine
def get_hp_gas_response(user_query, threshold=0.25):
    """Calculates intent match using cosine similarity."""
    cleaned_query = preprocess_text(user_query)
    
    # Check if string is completely empty after cleaning
    if not cleaned_query.strip():
        return "Welcome to HP Gas Support. Please type a specific query (e.g., 'how to book a cylinder')."

    # Convert query to matrix space
    query_vector = vectorizer.transform([cleaned_query])
    
    # Compute similarity array
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Extract peak match
    best_match_idx = similarity_scores.argmax()
    highest_score = similarity_scores[best_match_idx]
    
    # Evaluate confidence threshold
    if highest_score >= threshold:
        return faq_answers[best_match_idx]
    else:
        return "I am sorry, I couldn't find an exact match for your HP Gas request. For assistance, you can call our helpline or register a ticket on the MyHPGas portal."

# 6. Interactive Terminal Chat Loop
def run_hp_bot():
    print("=" * 60)
    print("       HP GAS DISTRIBUTION CUSTOMER HELPDESK CHATBOT      ")
    print("=" * 60)
    print("Type your question below (e.g., 'my cylinder is leaking' or 'book gas')")
    print("Type 'exit' to end session.")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Chatbot: Thank you for choosing HP Gas. Have a safe day ahead!")
            break
            
        response = get_hp_gas_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    run_hp_bot()
