import random

# Define PYQs and new questions dictionaries
pyqs = {
    2: [
        {"question": "PYQ1", "marks": 2, "subtopic": "Subtopic1"},
        {"question": "PYQ2", "marks": 2, "subtopic": "Subtopic2"},
        {"question": "PYQ3", "marks": 2, "subtopic": "Subtopic3"},
        # Add more questions here...
    ],
    5: [
        {"question": "PYQ4", "marks": 5, "subtopic": "Subtopic4"},
        {"question": "PYQ5", "marks": 5, "subtopic": "Subtopic5"},
        {"question": "PYQ6", "marks": 5, "subtopic": "Subtopic6"},
        # Add more questions here...
    ]
}

new_questions = {
    2: [
        {"question": "NQ1", "marks": 2, "subtopic": "Subtopic1"},
        {"question": "NQ2", "marks": 2, "subtopic": "Subtopic2"},
        {"question": "NQ3", "marks": 2, "subtopic": "Subtopic3"},
        # Add more questions here...
    ],
    5: [
        {"question": "NQ4", "marks": 5, "subtopic": "Subtopic4"},
        {"question": "NQ5", "marks": 5, "subtopic": "Subtopic5"},
        {"question": "NQ6", "marks": 5, "subtopic": "Subtopic6"},
        # Add more questions here...
    ]
}

# Define focus topics
focus_topics = ["Subtopic1", "Subtopic4"]

# Define section-wise parameters
section1_params = {"marks": 2, "num_questions": 6}
section2_params = {"marks": 5, "num_questions": 4}

# Define weightage for PYQs
pyq_weightage = 40

# Calculate PYQ allocation using weightage calculator function
def calculate_pyq_allocation(total_questions, pyq_weightage):
    return int((pyq_weightage / 100) * total_questions)

# Calculate PYQ allocation for each section
section1_pyq_allocation = calculate_pyq_allocation(section1_params["num_questions"], pyq_weightage)
section2_pyq_allocation = calculate_pyq_allocation(section2_params["num_questions"], pyq_weightage)

# Select questions randomly based on allocation and marks
def select_questions(dictionary, marks, num_questions, focus_topics=None):
    if not isinstance(num_questions, int) or num_questions <= 0:
        raise ValueError("num_questions must be a positive integer")
    
    questions = [q for q in dictionary[marks] if (focus_topics is None or q["subtopic"] in focus_topics)]
    
    if num_questions > len(questions):
        print(f"Warning: num_questions ({num_questions}) exceeds available questions ({len(questions)}).")
        num_questions = len(questions)
    
    return random.sample(questions, num_questions)

# Select PYQs and new questions for each section
section1_pyqs = select_questions(pyqs, section1_params["marks"], section1_pyq_allocation, focus_topics)
section1_new_questions = select_questions(new_questions, section1_params["marks"], section1_params["num_questions"] - section1_pyq_allocation, focus_topics)

section2_pyqs = select_questions(pyqs, section2_params["marks"], section2_pyq_allocation, focus_topics)
section2_new_questions = select_questions(new_questions, section2_params["marks"], section2_params["num_questions"] - section2_pyq_allocation, focus_topics)

# Print the selected questions
print("Section 1 (2 marks):")
for q in section1_pyqs:
    print(f"PYQ: {q['question']} ({q['marks']} marks)")
for q in section1_new_questions:
    print(f"New Question: {q['question']} ({q['marks']} marks)")

print("\nSection 2 (5 marks):")
for q in section2_pyqs:
    print(f"PYQ: {q['question']} ({q['marks']} marks)")
for q in section2_new_questions:
    print(f"New Question: {q['question']} ({q['marks']} marks)")