def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

api_key_file = 'OPENAI_API_BOOK_KEY.key'
api_key = read_api_key(api_key_file)
print("API key:", api_key)
