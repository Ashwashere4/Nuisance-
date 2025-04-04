
import json
# Function to load the existing data from a JSON file
def load_data_from_json():
    try:
        with open('songs_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save the updated data back to the JSON file
def save_data_to_json(data):
    with open('songs_data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Load the existing song data
song_data = load_data_from_json()