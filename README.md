to-do-list-

A To-Do List app with AI assistant

🚀 Overview

This is a lightweight To-Do List application enhanced with an AI assistant to help you manage, organize, and streamline your daily tasks.
You can create, update, delete tasks, and even interact with an AI to get task suggestions or summaries.

📝 Features

✅ Task Management: Add, update, and delete tasks with ease.

🤖 AI Assistant Integration: Get suggestions, summaries, or categorization from an AI helper.

💻 Simple Interface: Clean and intuitive design.

⚡ Lightweight: Minimal setup, quick to run.

🛠️ Built With:

HTML (frontend)

Python (backend – Flask recommended)

⚙️ Installation & Setup
Prerequisites

Before running this project, make sure you have:

Python 3.x installed

pip (Python package manager)

(Optional) virtual environment tool (venv or virtualenv)

Steps

Clone the repository

git clone https://github.com/Sanath00007/to-do-list-.git
cd to-do-list-


Set up virtual environment (recommended)

python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt



Configure AI Assistant (if using AI)

Get your API key (e.g., from OpenAI).

Set it as an environment variable:

export AI_API_KEY="your_api_key_here"


(On Windows PowerShell: setx AI_API_KEY "your_api_key_here")

Run the application

python app.py


or (if using Flask directly):

flask run


Then visit: http://127.0.0.1:5000/

🎯 Usage

Add tasks using the form on the homepage.

View tasks in a list, mark them complete, or delete them.

Use the AI assistant to:

Generate task suggestions.

Summarize existing tasks.

Categorize tasks automatically.
