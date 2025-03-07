import requests
import difflib
import argparse
import json  
import sys 

# Fetch data from API
url = "https://www.fruityvice.com/api/fruit/all"
response = requests.get(url)

try:
    response = requests.get(url, timeout=5)  # Add timeout to avoid infinite waiting
    response.raise_for_status()  # Raises an error for HTTP errors (e.g., 404, 500)
    data = response.json()
except requests.exceptions.Timeout:
    print("Error: API request timed out. Please try again later.")
    exit()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Error: {http_err}")
    exit()
except requests.exceptions.ConnectionError:
    print("Error: Unable to connect to FruityVice API. Check your internet connection.")
    exit()
except requests.exceptions.RequestException as err:
    print(f"Unexpected error: {err}")
    exit()

# Convert response to JSON
data = response.json()

# Extract available fruit names for spell-checking
fruit_names = [fruit["name"].lower() for fruit in data]

# Function 1: Fetch fruit data
def fetch_fruit_data(data, search_name):
    search_name = search_name.lower().strip()

    for fruit in data:
        if fruit["name"].lower().strip() == search_name:
            return {
                "Full Name": fruit["name"],
                "ID Number": fruit["id"],
                "Family": fruit["family"],
                "Sugar (g)": fruit["nutritions"]["sugar"],
                "Carbohydrates (g)": fruit["nutritions"]["carbohydrates"],
            }
    return None  # Return None if not found

# Function 2: Format data in a human-readable way
def format_human_readable(fruit_data):
    output = "\nFruit Information:\n"
    for key, value in fruit_data.items():
        output += f"{key}: {value}\n"
    return output

# Function 3: Format data in a machine-readable (JSON) way
def format_machine_readable(fruit_data):
    return json.dumps(fruit_data, indent=4)  # Pretty-print JSON output

# Function to suggest correct fruit name in case of spelling mistakes
def suggest_fruit_name(search_name):
    suggestions = difflib.get_close_matches(search_name, fruit_names, n=3, cutoff=0.6)
    return suggestions if suggestions else None

def main():
    parser = argparse.ArgumentParser(description="Fetch fruit data from FruityVice API")
    parser.add_argument("fruit", type=str, nargs="?", help="Name of the fruit to lookup")
    parser.add_argument("--output", choices=["human", "json"], default="human", help="Output format")
    args = parser.parse_args()

    # Ensure 'data' is available here
    if args.fruit:
        result = fetch_fruit_data(data, args.fruit) 

        if result:
            if args.output == "json":
                print(format_machine_readable(result))
            else:
                print(format_human_readable(result))
        else:
            suggestions = suggest_fruit_name(args.fruit)
            print(f"Fruit not found. Did you mean: {', '.join(suggestions)}?" if suggestions else "Fruit not found.")
    else:
        print("No fruit provided. Please provide a fruit name as an argument.")
        sys.exit(1)  # Exit with non-zero status code to indicate an error
# Run the main function
if __name__ == "__main__":
    main()
