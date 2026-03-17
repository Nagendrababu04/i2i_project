from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


def analyze_idea_logic(idea):
    idea_lower = idea.lower()

    
    if "web" in idea_lower or "website" in idea_lower or "flask" in idea_lower:
        idea_type = "Web Application"
        tech_stack = ["Flask", "HTML", "CSS", "JavaScript"]
    elif "mobile" in idea_lower or "android" in idea_lower:
        idea_type = "Mobile Application"
        tech_stack = ["Flutter", "Firebase", "Dart"]
    elif "ai" in idea_lower or "machine learning" in idea_lower:
        idea_type = "AI Based System"
        tech_stack = ["Python", "TensorFlow", "Flask"]
    else:
        idea_type = "General Software Product"
        tech_stack = ["Python", "Flask", "JavaScript"]

    steps = [
        "Define the problem clearly",
        "Design system architecture",
        "Develop MVP (Minimum Viable Product)",
        "Test with users",
        "Deploy and improve"
    ]

    challenges = [
        "User adoption",
        "Technical complexity",
        "Scalability"
    ]

    summary = f"This idea looks like a {idea_type} that can solve real-world problems."

    return {
        "summary": summary,
        "tech_stack": tech_stack,
        "steps": steps,
        "challenges": challenges
    }


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    idea = data['idea']

    print("Received idea:", idea)

    result = analyze_idea_logic(idea)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)