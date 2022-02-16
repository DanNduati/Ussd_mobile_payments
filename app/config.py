import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

# Mpesa
consumer_key = os.environ.get("CONSUMER_KEY", None)
consumer_secret = os.environ.get("CONSUMER_SECRET", None)
accesstoken_url = os.environ.get("ACCESSTOKEN_URL", None)
