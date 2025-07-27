import requests
import csv

# Change this if your FastAPI server is on a different port
API_URL = "http://127.0.0.1:8000/chat"

questions = [
    "What are the facilities at Changi Airport?",
    "Where is the Ground Transport Concierge located?",
    "What shopping options are available at Changi Airport?",
    "What are the dining options at Jewel Changi?",
    "How can I get from Changi Airport to the city?",
    "Are there any attractions at Jewel Changi?",
    "Where can I find shower facilities in the airport?",
    "What services are available for families?",
    "Are there hotel facilities inside the airport?",
    "Which terminal handles international departures?",
    "What are the public transport options from Changi?",
    "Where are the transport service counters in Changi?"
]

# Create or overwrite the output CSV file
with open("responses.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Question", "Answer"])

    for question in questions:
        try:
            response = requests.get(API_URL, params={"query": question})
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer found.")
            else:
                answer = f"Error {response.status_code}: {response.text}"
        except Exception as e:
            answer = f"Request failed: {str(e)}"

        print(f"Q: {question}\nA: {answer}\n{'-'*60}")
        writer.writerow([question, answer])
