import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LLM_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def load_prompt_template():
  with open("prompts/cold_email.txt", "r") as file:
    return file.read()

def generate_email(prompt):
  response = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
  )
  return response.choices[0].message.content.strip()

def personalize_and_generate():
  with open("leads.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    prompt_template = load_prompt_template()

    with open("outputs/generated_emails.csv", "w", newline='') as outfile:
      fieldnames = ["name", "email"]
      writer = csv.DictWriter(outfile, fieldnames=fieldnames)
      writer.writeheader()

      for row in reader:
        prompt = prompt_template.format(
          name=row["name"],
          company=row["company"],
          role=row["role"],
          website=row["website"]
        )
        email = generate_email(prompt)
        writer.writerow({"name": row["name"], "email": email})

if __name__ == "__main__":
  personalize_and_generate()