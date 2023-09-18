import json
import jsonschema

# read a file and load into a string
with open('azure-oai-models.json', 'r') as file:
    models = file.read()

# Load the JSON response as a dictionary
response = json.loads(models)

# Generate a schema from the response
schema = jsonschema.Draft7Validator(response).schema

# Print the schema
print(schema)