import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def analyze_idea(user_idea):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an AI system called "i2i (Idea to Implementation)".

Your job is to analyze a user's idea and convert it into a clean, structured, UI-ready implementation plan.

========================
STRICT OUTPUT RULES
========================
- Output MUST be valid JSON only
- Do NOT include markdown (no ``` or symbols)
- Do NOT include *, bullets, or formatting characters
- Do NOT add explanations outside JSON
- Keep text clean and readable
- Lists MUST be proper arrays of strings

========================
OUTPUT FORMAT (STRICT)
========================

{{
  "summary": "2–3 line clear explanation",
  "domain": "Short domain classification",
  "improvedIdea": "Refined version of idea in 3–5 lines",
  "uniquenessScore": "X% (Short reason)",
  "similarIdeas": ["App 1", "App 2", "App 3"],
  "uniqueFeatures": ["Feature 1", "Feature 2", "Feature 3"],
  "techStack": ["Frontend: ...", "Backend: ...", "Database: ..."],
  "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
  "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"]
}}

========================
CONTENT RULES
========================

summary:
- Simple, clear, non-technical

domain:
- Short, readable (e.g., "AI, Software, Gaming")

improvedIdea:
- More practical + structured version

uniquenessScore:
- Format exactly like: "85% (Reason for score)"

similarIdeas:
- STRICT RULE: MUST be real, existing companies or apps.
- STRICT RULE: Do NOT invent or make up names. If none exist, output ["No exact matches found"].

uniqueFeatures:
- Practical + differentiating

techStack:
- Format as an array of strings with category prefixes (e.g., "Frontend: React", "Backend: Python")
- STRICT RULE: Only use real, existing industry-standard frameworks.

steps:
- Clear progression (MVP → Development → Deployment)

challenges:
- Real technical/business issues

========================
USER IDEA
========================

{user_idea}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        result = json.loads(text.strip())

        list_keys = ["similarIdeas", "uniqueFeatures", "techStack", "steps", "challenges"]
        for key in list_keys:
            if key in result and isinstance(result[key], list):
                result[key] = "<br>• " + "<br>• ".join(str(item) for item in result[key])

        return result

    except Exception as e:
        return {"summary": f"Error: {str(e)}"}