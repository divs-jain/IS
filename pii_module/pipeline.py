from pii_module.identification import identify_entities
from pii_module.masking import mask_pii

def process_text(text, prompt_type="reasoning"):
    """
    Process text through entity detection and masking.
    prompt_type options:
    - reasoning: Mask only PII
    - full_anonymization: Mask PII + factual entities
    """
    entities = identify_entities(text)

    if prompt_type == "reasoning":
        masked_text = mask_pii(text, entities, mask_pii=True, mask_factual=False)
    elif prompt_type == "full_anonymization":
        masked_text = mask_pii(text, entities, mask_pii=True, mask_factual=True)
    else:
        masked_text = text

    return {
        "original_text": text,
        "masked_text": masked_text,
        "entities": entities
    }

# Quick test
if __name__ == "__main__":
    sample = "My name is Arjun, I am 47 years old and have hypertension."
    print(process_text(sample, "full_anonymization"))
