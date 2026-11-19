import random
import sys
import yaml

# 1. Load and parse the YAML file safely
try:
    with open("questions.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
except FileNotFoundError:
    print("❌ Error: The file 'questions.yaml' was not found. Please create the file first!")
    sys.exit()
except yaml.YAMLError:
    print("❌ Error: Failed to parse YAML file. Please check syntax/indentation!")
    sys.exit()

# 2. Validate that the root structure is a dictionary containing a 'questions' key
if not isinstance(data, dict) or "questions" not in data:
    print("❌ Error: Invalid structure! The file must contain a 'questions' key at root level.")
    sys.exit()

raw_questions = data.get("questions")

# 3. Ensure 'questions' holds a non-empty list
if not isinstance(raw_questions, list) or len(raw_questions) == 0:
    print("⚠️ Warning: No questions found in 'questions.yaml'. Please add questions before running the game!")
    sys.exit()

# 4. Filter out malformed entries, keeping only dicts with both 'question' and 'answer'
valid_questions = [
    q for q in raw_questions
    if isinstance(q, dict) and "question" in q and "answer" in q
]

if not valid_questions:
    print("❌ Error: Found items in the file, but none of them have both 'question' and 'answer' fields!")
    sys.exit()

# 5. Randomize question order and prompt the user to start
random.shuffle(valid_questions)

playing = input("Do you want to play? ").strip().lower()
if playing != "yes":
    print("Okay, maybe next time!")
    sys.exit()

print(f"\nOkay! Let's play :) (Loaded {len(valid_questions)} valid questions)\n")

# 6. Main quiz loop: ask questions, normalize answers, and track score
score = 0
for q in valid_questions:
    user_answer = input(f"{q['question']} ").strip().lower()
    # Convert answer to str in case YAML parsed it as a number or boolean
    if user_answer == str(q["answer"]).strip().lower():
        print("Correct!\n")
        score += 1
    else:
        print("Incorrect!\n")

# 7. Calculate and display final results
total_questions = len(valid_questions)
print(f"You got {score} out of {total_questions} questions correct!")
print(f"Your score: {(score / total_questions) * 100:.2f}%.")