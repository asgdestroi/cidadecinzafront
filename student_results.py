import json
import os

RESULTS_FILE = 'student_results.json'

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_results(results):
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

student_results = load_results()


