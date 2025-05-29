import requests

url = "http://localhost:8000/generate"
headers = {
    "Content-Type": "application/json"
}
payload = {
    "donor_name": "Dr. Testing Dude",
    "donation_amount": 150.00,
    "donation_date": "2025-05-28",
    "currency": "USD",
    "campaign": "Annual Fund",
    "organization_name": "Helping Hands Foundation",
    "contact_email": "info@helpinghands.org",
    "org_represnetative": "Chris Provolt",
    "tone": "warm",
    "language": "en",
    "letter_length": "standard",
    "impact_statements": [
        "Provided scholarships to 5 first‑generation college students",
        "Funded mentorship programs reaching over 200 youth"
    ]
}

response = requests.post(url, json=payload, headers=headers)

# Check for errors
response.raise_for_status()

# Print out the generated letter
data = response.json()
print("Generated Letter:\n")
print(data["letter"])
