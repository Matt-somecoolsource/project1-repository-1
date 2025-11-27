import json
import os

# Define the name of our fact archive file
ARCHIVE_FILE = "facts.json"

def load_facts():
    """Loads the list of facts from the JSON file."""
    # 💡 Best Practice: Check if the file exists before trying to read it.
    if not os.path.exists(ARCHIVE_FILE):
        return []  # Return an empty list if the file doesn't exist yet

    try:
        with open(ARCHIVE_FILE, 'r') as f:
            # Load the JSON data and return it. It will be a list of dictionaries.
            return json.load(f)
    except json.JSONDecodeError:
        # Handle cases where the file is empty or corrupted
        return []

def save_facts(facts):
    """Saves the list of facts to the JSON file."""
    with open(ARCHIVE_FILE, 'w') as f:
        # Write the list to the file, with nice formatting (indent=4)
        json.dump(facts, f, indent=4)
    print(f"✅ Facts successfully saved to {ARCHIVE_FILE}")

def add_fact(new_fact_text):
    """
    Adds a new fact to the archive if it's not already present.
    This is the main logic function.
    """
    print(f"🎯 Attempting to add new fact: '{new_fact_text}'")
    
    # 1. Load existing facts from the file
    facts = load_facts()
    
    # 2. Check for duplicates (CRUCIAL LOGIC)
    # We create a temporary set of existing fact texts for a fast lookup.
    existing_fact_texts = {fact['text'] for fact in facts}
    
    if new_fact_text in existing_fact_texts:
        print("⚠️  Duplicate fact found. Not adding.")
        return False  # Indicate that the fact was not added
    
    # 3. If it's a new fact, add it to our list
    # We can add more data later, but for now, the text is enough.
    new_fact_entry = {'text': new_fact_text}
    facts.append(new_fact_entry)
    print("🚀 New unique fact! Adding to archive.")
    
    # 4. Save the updated list back to the file
    save_facts(facts)
    return True # Indicate that the fact was successfully added

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Digital Fact Collector: Archive Test ---")
    
    # Simulate fetching some facts
    fetched_fact_1 = "The Eiffel Tower can be 15 cm taller during the summer."
    fetched_fact_2 = "A group of flamingos is called a 'flamboyance'."
    fetched_fact_3 = "The Eiffel Tower can be 15 cm taller during the summer." # A duplicate!

    # Run the logic
    add_fact(fetched_fact_1)
    print("-" * 20)
    add_fact(fetched_fact_2)
    print("-" * 20)
    add_fact(fetched_fact_3) # This one should be rejected
    print("-" * 20)

    # You can check your 'facts.json' file now to see the result!