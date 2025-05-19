import requests
from config import N8N_WEBHOOK_URL, N8N_AUTH

def forward_to_n8n(payload: dict) -> tuple[str, str]:
    try:
        resp = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            auth=N8N_AUTH,
            timeout=10
        )
        resp.raise_for_status()
        return 'success', resp.text
    except requests.RequestException as e:
        return 'error', str(e)