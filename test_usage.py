from message_handler import usage
import os
import dotenv


dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("Api Key Not Found")

print(usage(api_key))
