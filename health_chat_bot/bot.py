import spacy

# Load NLP model (MAKE SURE YOU INSTALL THIS FIRST)
# pip install spacy
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# ==========================
# Disease Database
# ==========================

disease_data = {
    "Fever": {
        "symptoms": ["fever", "temperature", "chill"],
        "solution": "Take paracetamol, drink plenty of fluids and rest.",
        "precautions": "Avoid cold drinks and monitor temperature."
    },
    "Common Cold": {
        "symptoms": ["cold", "cough", "sneeze", "runny nose"],
        "solution": "Take steam inhalation and drink warm water.",
        "precautions": "Avoid cold food and stay warm."
    },
    "Migraine": {
        "symptoms": ["headache", "migraine", "head pain"],
        "solution": "Rest in a quiet dark room and avoid stress.",
        "precautions": "Avoid loud noise and bright light."
    },
    "Food Poisoning": {
        "symptoms": ["vomit", "nausea", "stomach pain", "diarrhea"],
        "solution": "Drink ORS and stay hydrated.",
        "precautions": "Avoid outside and spicy food."
    },
    "Body Pain": {
        "symptoms": ["body pain", "joint pain", "back pain"],
        "solution": "Take rest and mild pain relief medicine.",
        "precautions": "Avoid heavy lifting."
    },
    "Weakness": {
        "symptoms": ["fatigue", "weakness", "tired"],
        "solution": "Eat nutritious food and get proper sleep.",
        "precautions": "Maintain balanced diet."
    }
}

# ==========================
# Prediction Function
# ==========================

def get_prediction(user_input):
    doc = nlp(user_input.lower())
    words = [token.lemma_ for token in doc]

    matched_diseases = {}

    for disease, info in disease_data.items():
        score = 0

        for symptom in info["symptoms"]:
            for word in words:
                if symptom in word:
                    score += 1

        if score > 0:
            matched_diseases[disease] = score

    if not matched_diseases:
        return None

    # Return top 2 matches
    sorted_diseases = sorted(matched_diseases,
                             key=matched_diseases.get,
                             reverse=True)

    return sorted_diseases[:2]


# ==========================
# Solution & Precautions
# ==========================

def get_solution(disease):
    return disease_data[disease]["solution"]


def get_precautions(disease):
    return disease_data[disease]["precautions"]