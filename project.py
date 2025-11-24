import json
import os
import sys
import difflib
import string

#!/usr/bin/env python3
"""
project.py - Simple Disease Identification System (rule-based)
Creates/uses diseases.json in the same folder. Run and follow prompts.
"""


DB_FILE = "diseases.json"
DEFAULT_DB = {
    "Common Cold": {
        "symptoms": ["sneezing", "cough", "sore throat", "runny nose", "congestion"],
        "description": "A mild viral infection of the upper respiratory tract.",
        "treatment": "Rest, fluids, OTC cold medicines."
    },
    "Influenza": {
        "symptoms": ["fever", "chills", "muscle aches", "cough", "fatigue", "headache"],
        "description": "A viral infection causing systemic and respiratory symptoms.",
        "treatment": "Antivirals if early, rest, fluids, symptomatic care."
    },
    "Migraine": {
        "symptoms": ["headache", "nausea", "sensitivity to light", "sensitivity to sound"],
        "description": "A neurological condition characterized by intense headache episodes.",
        "treatment": "Pain relievers, triptans, lifestyle changes."
    },
    "Gastroenteritis": {
        "symptoms": ["diarrhea", "vomiting", "abdominal pain", "nausea", "fever"],
        "description": "Inflammation of the stomach and intestines, often infectious.",
        "treatment": "Hydration, rest, rehydration solutions; antibiotics if bacterial."
    }
}


def normalize(text):
    text = text.lower().strip()
    return text.translate(str.maketrans("", "", string.punctuation))


def load_db(path=DB_FILE):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DB, f, indent=2)
        return DEFAULT_DB.copy()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db, path=DB_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def parse_symptoms(input_text):
    parts = [normalize(p) for p in input_text.split(",") if p.strip()]
    # also split on semicolons or newlines
    flat = []
    for p in parts:
        flat.extend([normalize(x) for x in p.replace(";", ",").split(",") if x.strip()])
    return list(dict.fromkeys([s for s in flat if s]))


def score_match(query_symptoms, disease_symptoms):
    # exact matches
    ds_norm = [normalize(s) for s in disease_symptoms]
    matched = 0
    for q in query_symptoms:
        if q in ds_norm:
            matched += 1
        else:
            # fuzzy match any disease symptom
            close = difflib.get_close_matches(q, ds_norm, n=1, cutoff=0.8)
            if close:
                matched += 0.8  # partial credit
    # confidence: matched / average of lengths to avoid bias
    denom = max(1, (len(query_symptoms) + len(ds_norm)) / 2)
    return matched / denom


def identify(disease_db, input_symptoms, top_n=5, min_confidence=0.05):
    qs = parse_symptoms(input_symptoms)
    if not qs:
        return []
    results = []
    for name, info in disease_db.items():
        s = score_match(qs, info.get("symptoms", []))
        if s >= min_confidence:
            results.append((name, round(s * 100, 1), info))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


def add_disease_interactive(db):
    name = input("Disease name: ").strip()
    if not name:
        print("Name required.")
        return
    if name in db:
        print("Disease already exists.")
        return
    syms = input("Symptoms (comma-separated): ").strip()
    desc = input("Short description: ").strip()
    treat = input("Common treatment/advice: ").strip()
    db[name] = {
        "symptoms": [s.strip() for s in syms.split(",") if s.strip()],
        "description": desc,
        "treatment": treat
    }
    save_db(db)
    print(f"Added '{name}' to database.")


def interactive_loop():
    db = load_db()
    print("Disease Identification System")
    print("Enter symptoms separated by commas (e.g. fever, cough). Type 'help' for options.")
    while True:
        try:
            user = input("\nSymptoms> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        if not user:
            continue
        cmd = user.lower()
        if cmd in {"exit", "quit", "q"}:
            print("Goodbye.")
            break
        if cmd == "help":
            print("Commands: help | add | list | show <disease> | exit")
            print("Or enter symptoms to identify possible diseases.")
            continue
        if cmd == "add":
            add_disease_interactive(db)
            continue
        if cmd == "list":
            for name in sorted(db.keys()):
                print("-", name)
            continue
        if cmd.startswith("show "):
            name = user[5:].strip()
            info = db.get(name)
            if not info:
                print("Not found.")
            else:
                print(f"{name}\n  Symptoms: {', '.join(info.get('symptoms', []))}")
                print(f"  Description: {info.get('description','')}")
                print(f"  Treatment: {info.get('treatment','')}")
            continue
        # otherwise treat as symptoms input
        results = identify(db, user)
        if not results:
            print("No likely matches found. Try different symptom wording or add the disease with 'add'.")
            continue
        print("Top matches:")
        for name, conf, info in results:
            print(f"- {name} ({conf}%)")
            print(f"    Symptoms: {', '.join(info.get('symptoms', []) )}")
            print(f"    Description: {info.get('description','')}")
            print(f"    Treatment: {info.get('treatment','')}")
        # loop


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"--identify", "-i"}:
        db = load_db()
        inp = " ".join(sys.argv[2:]) or input("Enter symptoms: ")
        for name, conf, info in identify(db, inp, top_n=10):
            print(f"{name}: {conf}%")
    else:
        interactive_loop()