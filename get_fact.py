# Import the 'requests' library to handle HTTP connections.
import requests

def fetch_random_fact():
    """
    Connects to the useless-facts API, fetches a random fact, 
    and returns it.
    """
    # This is the specific URL for getting a random fact in English.
    api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    
    print("Connecting to the fact stream...")
    
    try:
        # Make the GET request to the API.
        response = requests.get(api_url)
        
        # Raise an exception if the request was unsuccessful (e.g., 404, 500 errors).
        response.raise_for_status() 
        
        # Parse the JSON response into a Python dictionary.
        data = response.json()
        
        # Extract the fact text from the dictionary. The fact is stored under the key 'text'.
        fact = data['text']
        
        print("✅ Success! Fact received.")
        return fact
        
    except requests.exceptions.RequestException as e:
        # Handle potential network errors (no internet, DNS failure, etc.).
        print(f"⚠️ Error connecting to the API: {e}")
        return None

# This is the main part of our script.
if __name__ == "__main__":
    random_fact = fetch_random_fact()
    
    # If a fact was successfully fetched, print it.
    if random_fact:
        print("\n--- Your Random Fact ---")
        print(random_fact)
        print("------------------------")