import json

inf = "Idf.json"  # Your filename

def dumpp(data):  # Changed to accept data parameter
    with open(inf, "w") as d:
        json.dump(data, d, indent=4)  # Dump the data, not the filename

def loadd():
    try:
        with open(inf, "r") as f:
            return json.load(f)  # Use load() not loads() for files
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Return None if file doesn't exist or is invalid

# Load existing data
data = loadd()

# If you want to store "Hassan" as new data
new_data = "Hassan1"

# Save the new data
dumpp(new_data)  # This will overwrite the file with "Hassan"

# To verify it worked
loaded_data = loadd()
print(loaded_data)  # Should print "Hassan"