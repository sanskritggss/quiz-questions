import json
import os
import math
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Load .env variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz():
    # 1. Load your source data
    try:
        with open('data.json', 'r') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'data.json' not found.")
        return

    total_sections = len(source_data)
    target_total = 100
    # Calculate questions per section (distribute evenly)
    questions_per_section = math.ceil(target_total / total_sections)
    
    all_questions = []
    question_counter = 1

    print(f"🎯 Target: 100 questions from {total_sections} sections.")

    # 2. Process each section
    for item in source_data:
        if len(all_questions) >= target_total:
            break
            
        section_name = item.get('section')
        story_content = item.get('data')
        
        # Adjust for last section to hit exactly 100
        remaining = target_total - len(all_questions)
        num_to_ask = min(questions_per_section, remaining)

        print(f"🔄 Generating {num_to_ask} questions for: {section_name}...")

        prompt = f"""
        Extract exactly {num_to_ask} quiz questions from the text below.
        
        TEXT: {story_content}
        
        STRICT RULES:
        1. ANSWERS: Must be a single word or a specific entity name (e.g., 'The Hand of Krishna').
        2. DIFFICULTY: You MUST use only the integers 0, 1, or 2. 
           - 0 = Easy
           - 1 = Med
           - 2 = Hard
        3. NO HALLUCINATIONS: Use ONLY the provided text.
        4. SECTION: Use '{section_name}'.
        
        RETURN FORMAT (JSON ONLY):
        {{
            "questions": [
                {{
                    "question_number": int,
                    "question": "string",
                    "answer": "string",
                    "difficulty_level": int,
                    "section": "{section_name}"
                }}
            ]
        }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a JSON-only extractor. Output difficulty as 0, 1, or 2 only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            data_out = json.loads(response.choices[0].message.content)
            q_list = data_out.get("questions", [])

            for q in q_list[:num_to_ask]:
                q['question_number'] = question_counter
                all_questions.append(q)
                question_counter += 1

        except Exception as e:
            print(f"⚠️ Error in {section_name}: {e}")

    # 3. Save to JSON
    with open('quiz_pratibha_2026.json', 'w') as f:
        json.dump(all_questions, f, indent=4)
    
    # 4. Save to Excel and apply color coding
    output_excel = 'quiz_pratibha_2026.xlsx'
    df = pd.DataFrame(all_questions)
    cols = ['question_number', 'section', 'difficulty_level', 'question', 'answer']
    df = df[cols]
    df.to_excel(output_excel, index=False)

    # 5. Apply Formatting (Colors)
    wb = load_workbook(output_excel)
    ws = wb.active

    # Define fills
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid") # Easy
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid") # Med
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")    # Hard

    # Difficulty level is in column C (index 3)
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=3)
        try:
            val = int(cell.value)
            if val == 0:
                cell.fill = green_fill
            elif val == 1:
                cell.fill = yellow_fill
            elif val == 2:
                cell.fill = red_fill
        except:
            pass

    wb.save(output_excel)
    print("-" * 30)
    print(f"✅ Completed! {len(all_questions)} questions generated.")
    print(f"📂 JSON: quiz_pratibha_2026.json")
    print(f"📂 Excel: {output_excel} (Color-coded difficulty)")

if __name__ == "__main__":
    generate_quiz()