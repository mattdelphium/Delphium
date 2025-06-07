import os
import requests

# Load your API key
api_key = os.getenv("OPENAI_API_KEY")  # or set directly: "sk-..."

# Define headers
headers = {
    "Authorization": f"Bearer {api_key}",
}

# Get credit balance
response = requests.get(
    "https://api.openai.com/v1/dashboard/billing/credit_grants",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    total = data.get("total_granted", 0)
    used = data.get("total_used", 0)
    remaining = data.get("total_available", 0)

    print(f"Total granted: ${total:.2f}")
    print(f"Total used: ${used:.2f}")
    print(f"Remaining: ${remaining:.2f}")
else:
    print("Failed to retrieve balance:", response.status_code, response.text)
