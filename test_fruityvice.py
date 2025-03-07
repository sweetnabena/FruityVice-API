import unittest
from unittest.mock import patch
from fruityvice import fetch_fruit_data, format_human_readable, format_machine_readable, suggest_fruit_name, main

class TestFruityViceFunctions(unittest.TestCase):

    def setUp(self):
        # Mock data to simulate the fruit data returned by the API
        self.mock_data = [
            {
                "name": "Strawberry",
                "id": 1,
                "family": "Rosaceae",
                "nutritions": {"sugar": 4.9, "carbohydrates": 7.7}
            },
            {
                "name": "Banana",
                "id": 2,
                "family": "Musaceae",
                "nutritions": {"sugar": 12.0, "carbohydrates": 27.0}
            }
        ]
        # Extract available fruit names for spell-checking
        self.fruit_names = [fruit["name"].lower() for fruit in self.mock_data]

    # Test 1: Fetch fruit data
    def test_fetch_fruit_data(self):
        result = fetch_fruit_data(self.mock_data, "Strawberry")
        expected = {
            "Full Name": "Strawberry",
            "ID Number": 1,
            "Family": "Rosaceae",
            "Sugar (g)": 4.9,
            "Carbohydrates (g)": 7.7
        }
        self.assertEqual(result, expected)
        
        result = fetch_fruit_data(self.mock_data, "Orange")
        self.assertIsNone(result)  # Should return None

    # Test 2: Format human-readable data
    def test_format_human_readable(self):
        fruit_data = {
            "Full Name": "Strawberry",
            "ID Number": 1,
            "Family": "Rosaceae",
            "Sugar (g)": 4.9,
            "Carbohydrates (g)": 7.7
        }
        expected = "\nFruit Information:\nFull Name: Strawberry\nID Number: 1\nFamily: Rosaceae\nSugar (g): 4.9\nCarbohydrates (g): 7.7\n"
        result = format_human_readable(fruit_data)
        self.assertEqual(result, expected)

    # Test 3: Format machine-readable data
    def test_format_machine_readable(self):
        fruit_data = {
            "Full Name": "Strawberry",
            "ID Number": 1,
            "Family": "Rosaceae",
            "Sugar (g)": 4.9,
            "Carbohydrates (g)": 7.7
        }
        expected = '''{
    "Full Name": "Strawberry",
    "ID Number": 1,
    "Family": "Rosaceae",
    "Sugar (g)": 4.9,
    "Carbohydrates (g)": 7.7
}'''
        result = format_machine_readable(fruit_data)
        self.assertEqual(result, expected)

    # Test 4: Suggest fruit name (with typo)
    def test_suggest_fruit_name(self):
        result = suggest_fruit_name("Strawbery")
        self.assertIn("strawberry", [name.lower() for name in result])

        result = suggest_fruit_name("Watermelon")
        self.assertIn("watermelon", [name.lower() for name in result])  

# Test 5: CLI testing for main function (Simulating command-line)
@patch('fruityvice.requests.get')  # Mocking the requests.get() call
@patch('fruityvice.fetch_fruit_data')  # Mocking fetch_fruit_data to return the desired result
@patch('builtins.print')  # Mocking print so we can assert the output
def test_main(self, mock_print, mock_fetch, mock_get):
    # Mock the response from the API when fetch_fruit_data is called in the main function
    mock_get.return_value.json.return_value = [ 
        {
            "name": "Strawberry",
            "id": 3,
            "family": "Rosaceae",
            "nutritions": {
                "sugar": 5.4,
                "carbohydrates": 5.5
            }
        }
    ]
    # Mock fetch_fruit_data to return a mock fruit data when searched for "Strawberry"
    mock_fetch.return_value = {
        "Full Name": "Strawberry",
        "ID Number": 3,
        "Family": "Rosaceae",
        "Sugar (g)": 5.4,
        "Carbohydrates (g)": 5.5
    }
    # Simulate calling the main function (which would internally call print)
    main()  
    # The expected output from the main function should be this JSON format:
    mock_print.assert_called_with('{\n    "Full Name": "Strawberry",\n    "ID Number": 3,\n    "Family": "Rosaceae",\n    "Sugar (g)": 5.4,\n    "Carbohydrates (g)": 5.5\n}')

if __name__ == "__main__":
    unittest.main()
