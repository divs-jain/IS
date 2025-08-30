import re
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy

# ===============================
# Load spaCy (passive)
# ===============================
spacy_nlp = spacy.load("en_core_web_sm")

def identify_entities_spacy(text):
    """Identify entities using spaCy (passive)."""
    doc = spacy_nlp(text)
    results = []
    for ent in doc.ents:
        entity_type = ent.label_
        pii_type = "PII" if entity_type in ["PERSON", "GPE", "ORG", "DATE"] else "Factual"
        results.append({
            "text": ent.text,
            "label": entity_type,
            "type": pii_type,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return results

# ===============================
# Flair NER (active)
# ===============================
tagger = SequenceTagger.load("flair/ner-english-ontonotes-fast")

def identify_entities_flair(text):
    """Identify PII entities using Flair NER."""
    sentence = Sentence(text)
    tagger.predict(sentence)
    results = []

    for entity in sentence.get_spans('ner'):
        label = entity.get_label("ner").value
        ent_type = "PII" if label in ["PERSON", "ORG", "LOC", "GPE"] else "Factual"
        results.append({
            "text": entity.text,
            "label": label,
            "type": ent_type,
            "start": entity.start_position,
            "end": entity.end_position
        })
    return results

# ===============================
# Age detection
# ===============================
def detect_age(text):
    """Detect age patterns like '47 years old'."""
    pattern = r'\b\d{1,3}\s+years?\s+old\b'
    matches = re.finditer(pattern, text)
    return [{
        "text": match.group(),
        "label": "AGE",
        "type": "Factual",
        "start": match.start(),
        "end": match.end()
    } for match in matches]

# ===============================
# Disease detection
# ===============================
diseases = ["hypertension", "diabetes", "asthma", "cancer"]

def detect_diseases(text):
    """Detect known diseases in text."""
    results = []
    for disease in diseases:
        start = text.lower().find(disease.lower())
        if start != -1:
            results.append({
                "text": disease,
                "label": "DISEASE",
                "type": "Factual",
                "start": start,
                "end": start + len(disease)
            })
    return results

# ===============================
# Unified identification
# ===============================
def identify_entities(text, use_flair=True, use_bert=False, use_spacy=False):
    """
    Detect entities in text.
    - Flair: Active
    - spaCy/BERT: Passive
    """
    entities = []

    if use_flair:
        entities.extend(identify_entities_flair(text))

    if use_bert:
        from pii_module.bert_identification import identify_entities_bert
        entities.extend(identify_entities_bert(text))

    if use_spacy:
        entities.extend(identify_entities_spacy(text))

    entities.extend(detect_age(text))
    entities.extend(detect_diseases(text))

    return entities
