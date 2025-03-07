# FruityVice API Fruit Lookup

A Python program that fetches and displays information about fruits from the FruityVice API.

## Setup

Clone the repository: git clone https://github.com/yourusername/FruityVice-API.git
Navigate to the project directory: cd FruityVice-API
Install the dependencies: pip install -r requirements.txt or python3 -m pip install -r requirements.txt

## Usage
Example usage: (or python3 default for mac)
python fruityvice.py <fruit_name> (human readable format (default))
python fruityvice.py <fruit_name> --output json (machine readable format JSON)
Replace <fruit_name> with the name of the fruit you want to look up (e.g., Strawberry, Banana).

Example:
python fruityvice.py Strawberry
python fruityvice.py Strawberry --output json

## Testing
Run the following command to execute the tests:
python -m unittest test_fruityvice.py 



