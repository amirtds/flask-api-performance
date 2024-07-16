import os
from appsignal import Appsignal

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

appsignal = Appsignal(
    active=True,
    name="flask-api-performance",
    push_api_key=os.getenv("APPSIGNAL_PUSH_API_KEY"),
)