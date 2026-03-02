import json
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Initialize OpenAI using the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz():
    # 1. Load your source data
    try:
        with open('data.json', 'r') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'data.json' not found in this directory.")
        return

    all_questions = []
    question_counter = 1

    # 2. Iterate through sections
    for item in source_data:
        section_name = item.get('section')
        story_content = item.get('data')

        print(f"🔄 Processing: {section_name}...")

        prompt = f"""
        Extract quiz questions from the text provided below.
        
        CONTEXT: {story_content}
        
        STRICT RULES:
        1. ANSWERS: Must be a single word OR a specific entity name (e.g., 'The Hand of Krishna', 'Mount Govardhana', 'Arjuna').
        2. NO HALLUCINATIONS: Use only facts found in the provided text.
        3. DIFFICULTY: Categorize as 'easy', 'med', or 'hard'.
        4. SECTION: Use '{section_name}' for the section field.
        
        Return the data as a JSON object with a key "questions" containing a list of objects.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a JSON-only data extractor. No conversational filler."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            # Parse and extract
            raw_content = response.choices[0].message.content
            data_out = json.loads(raw_content)
            q_list = data_out.get("questions", [])

            for q in q_list:
                # Standardizing the dictionary keys to your requirement
                final_q = {
                    "question_number": question_counter,
                    "question": q.get("question"),
                    "answer": q.get("answer"),
                    "difficulty_level": q.get("difficulty_level"),
                    "section": section_name
                }
                all_questions.append(final_q)
                question_counter += 1

        except Exception as e:
            print(f"⚠️ Error in {section_name}: {e}")

    # 3. Save to JSON
    with open('quiz_pratibha_2026.json', 'w') as f:
        json.dump(all_questions, f, indent=4)
    
    # 4. Save to Excel
    df = pd.DataFrame(all_questions)
    df.to_excel('quiz_pratibha_2026.xlsx', index=False)
    
    print("-" * 30)
    print(f"✅ Success! Generated {len(all_questions)} questions.")
    print("📂 Files created: quiz_pratibha_2026.json, quiz_pratibha_2026.xlsx")

if __name__ == "__main__":
    generate_quiz()