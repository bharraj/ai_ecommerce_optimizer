import os
from dotenv import load_dotenv

# Load .env from this directory
load_dotenv()

# Flask configuration
FLASK_HOST = os.environ["FLASK_HOST"]
FLASK_PORT = int(os.environ["FLASK_PORT"])

# n8n webhook credentials
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_AUTH = (os.getenv("N8N_USER"), os.getenv("N8N_PASS"))