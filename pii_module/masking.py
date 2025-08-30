def mask_pii(text, entities, mask_pii=True, mask_factual=False):
    """
    Replace PII/Factual entities with tags.
    """
    masked_text = text
    for ent in sorted(entities, key=lambda x: x["start"], reverse=True):
        if ent["start"] == -1 or ent["end"] == -1:
            continue
        if ent["type"] == "PII" and mask_pii:
            masked_text = masked_text[:ent["start"]] + "<PII>" + masked_text[ent["end"]:]
        elif ent["type"] == "Factual" and mask_factual:
            masked_text = masked_text[:ent["start"]] + "<FACT>" + masked_text[ent["end"]:]
    return masked_text
