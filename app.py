from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# In-memory list to store todos
todos = []

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Gemini Key Loaded:", GEMINI_API_KEY is not None)  # Debugging line

@app.route('/')
def home():
    return render_template('index.html')

# =====================
# To-Do List Endpoints
# =====================

# READ all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# CREATE a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = {
        'id': data['id'],
        'text': data['text'],
        'completed': data.get('completed', False),
        'priority': data.get('priority', 'Normal'),
        'deadline': data.get('deadline', '')
    }
    todos.append(todo)
    return jsonify(todo), 201

# UPDATE a todo
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['text'] = data.get('text', todo['text'])
            todo['completed'] = data.get('completed', todo['completed'])
            todo['priority'] = data.get('priority', todo['priority'])
            todo['deadline'] = data.get('deadline', todo['deadline'])
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

# DELETE a todo
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'result': 'Todo deleted'})

# =====================
# Pages
# =====================

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    total = len(todos)
    completed = sum(1 for t in todos if t['completed'])
    pending = total - completed
    high_priority = sum(1 for t in todos if t['priority'] == 'High')
    deadlines = [t['deadline'] for t in todos if t['deadline']]
    return render_template(
        'dashboard.html',
        total=total,
        completed=completed,
        pending=pending,
        high_priority=high_priority,
        deadlines=deadlines,
        todos=todos
    )

# =====================
# Smart Chatbot with Gemini
# =====================

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')

    # 🔥 Add context: summarize all tasks
    total = len(todos)
    completed = sum(1 for t in todos if t['completed'])
    pending = total - completed

    tasks_summary = f"You have {total} total tasks, {completed} completed, and {pending} pending.\n\n"
    for t in todos:
        status = "✅" if t['completed'] else "❌"
        tasks_summary += f"- {status} {t['text']} (Priority: {t['priority']}, Deadline: {t['deadline']})\n"

    # Send both context + question to Gemini
    prompt = f"""
You are a helpful task assistant. Here is the user's current to-do list:

{tasks_summary}

Now answer this question concisely: {user_message}
"""

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=payload)
        print("Gemini API status:", response.status_code)
        print("Gemini API response:", response.text)

        if response.status_code == 200:
            try:
                reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"reply": reply})
            except Exception as e:
                print("Error parsing Gemini response:", e)
                return jsonify({"reply": "Error reading Gemini response."}), 500
        else:
            return jsonify({"reply": "Gemini API request failed."}), 500
    except Exception as e:
        print("Error contacting Gemini API:", e)
        return jsonify({"reply": "Could not reach Gemini API."}), 500


if __name__ == '__main__':
    app.run(debug=True)
