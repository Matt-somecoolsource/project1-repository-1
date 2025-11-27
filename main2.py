import json
import os
import requests  # For making HTTP requests to the API
import time      # For pausing the script

# Define the name of our fact archive file
ARCHIVE_FILE = "facts.json"
# Define the API endpoint to get random facts
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

def load_facts():
    """Loads the list of facts from the JSON file."""
    if not os.path.exists(ARCHIVE_FILE):
        return []
    try:
        with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_facts(facts):
    """Saves the list of facts to the JSON file."""
    with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4, ensure_ascii=False)
    print(f"✅ Facts successfully saved to {ARCHIVE_FILE}")

def fetch_random_fact():
    """Fetches a single random fact from the API."""
    try:
        print("📡 Fetching a new fact from the API...")
        response = requests.get(API_URL)
        # Raise an exception for bad status codes (like 404 or 500)
        response.raise_for_status() 
        
        data = response.json()
        # The fact is stored in the 'text' key of the JSON response
        return data['text']
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error fetching fact from API: {e}")
        return None
    except KeyError:
        print("⚠️  Could not find 'text' key in API response. Response format may have changed.")
        return None

def add_fact(new_fact_text):
    """Adds a new fact to the archive if it's not already present."""
    if not new_fact_text:
        return False # Don't process empty facts

    print(f"🎯 Processing fact: '{new_fact_text}'")
    
    facts = load_facts()
    existing_fact_texts = {fact['text'] for fact in facts}
    
    if new_fact_text in existing_fact_texts:
        print("⚖️  Duplicate fact found. Not adding.")
        return False
    
    new_fact_entry = {'text': new_fact_text, 'source': API_URL}
    facts.append(new_fact_entry)
    print("🚀 New unique fact! Adding to archive.")
    
    save_facts(facts)
    return True

# --- Main Automation Loop ---
if __name__ == "__main__":
    print("--- 🚀 Automated Digital Fact Collector: ENGAGED ---")
    print("Press Ctrl+C to stop the collector.")
    
    fetch_interval_seconds = 30  # Fetch a new fact every 30 seconds

    try:
        while True:
            # 1. Fetch a new fact from the online API
            fact = fetch_random_fact()
            
            # 2. If a fact was successfully fetched, try to add it to our archive
            if fact:
                add_fact(fact)
            
            # 3. Wait for the defined interval before fetching the next one
            print(f"--- Sleeping for {fetch_interval_seconds} seconds... ---")
            time.sleep(fetch_interval_seconds)

    except KeyboardInterrupt:
        print("\n🛑 Collector stopped by user. Goodbye!")
