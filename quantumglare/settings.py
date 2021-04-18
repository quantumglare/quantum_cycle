import os
from dotenv import load_dotenv

# Load environment variables from .env
#
dotenv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(dotenv):
    load_dotenv(dotenv)
