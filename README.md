Simple Disease Identification System

This project is a rule-based disease identification system implemented in Python. It allows users to enter symptoms and get likely diseases based on fuzzy matching. The program also lets users view, add, and list diseases stored in a JSON database.


---

🚀 Features

Identify possible diseases based on entered symptoms.

Fuzzy matching for slight spelling variations.

Interactive CLI tool for entering symptoms or commands.

Persistent storage using a diseases.json file.

Ability to:

Add new diseases interactively.

List all diseases.

Show details of a specific disease.




---

📂 Project Files

project.py → Main Python script.

diseases.json → Auto-created database storing diseases, symptoms, descriptions, and treatments.



---

🛠 How It Works

1. Database Loading

If diseases.json does not exist, the program creates it with a default set of diseases.

Otherwise, it loads the existing data.


2. Symptom Parsing

Users input symptoms separated by commas.

Input is cleaned, lowercased, and punctuation is removed.


3. Scoring & Identification

Each entered symptom is compared to disease symptoms.

Exact matches score 1 point.

Fuzzy matches score 0.8 points.

A confidence score percentage is calculated for each disease.


4. User Interaction Commands

You can type:

help → Show available commands.

add → Add a disease interactively.

list → List all diseases.

show <disease> → View a specific disease.

exit / quit / q → Exit the program.

Or simply type symptoms to identify diseases.



---

▶ Running the Program

Interactive Mode

python project.py

You will see:

Disease Identification System
Enter symptoms separated by commas (e.g. fever, cough). Type 'help' for options.

Command-Line Identification Mode

python project.py --identify fever cough


---

✨ Example Usage

Input:
