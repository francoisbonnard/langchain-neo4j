from decouple import Config
config = Config(".env")
openai_api_key = config("OPENAI_API_KEY")
print("OpenAI API Key:", openai_api_key)