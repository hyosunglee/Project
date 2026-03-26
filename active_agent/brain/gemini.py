import google.generativeai as genai
import os
import json
import re

def extract_json(text):
    """
    Tries to extract a JSON object from a string that might contain other text.
    """
    # Try finding content between ```json and ```
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)

    # Try finding content between ``` and ```
    code_match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
    if code_match:
        return code_match.group(1)

    # Try finding the first '{' and last '}'
    start_index = text.find('{')
    end_index = text.rfind('}')
    if start_index != -1 and end_index != -1 and end_index > start_index:
        return text[start_index:end_index+1]

    return text

def judge_intervention(memory_info, research_results, user_context):
    """
    Calls the Gemini API to determine if the collected information is worth an intervention.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY is not set.")
        return False, {"error": "Gemini API key is missing."}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')

    research_summary = "\n".join([f"- {p['title']}: {p['summary'][:300]}..." for p in research_results]) if research_results else "No new papers found."

    prompt = f"""
    You are an active AI agent for a user on a Mac Mini (M2, 16GB).
    User Context: {user_context}
    System Memory Status: {memory_info} (Total: {memory_info.get('total_gb')}GB)
    Latest Research ('AI Feedback Loop'):
    {research_summary}

    Based on the above information, decide if the agent should intervene (notify the user) right now.
    Intervention Criteria:
    1. System Criticality: Memory usage is over 90% (percent_used: {memory_info.get('percent_used')}%).
    2. High Relevance: At least one of the latest research papers is highly relevant to "AI Feedback Loop" and the user's context (AI paper writing).
    3. Contextual Interest: Something else that matches the user's interests (gaming, AI) that seems urgent or highly beneficial.

    Return your decision STRICTLY in JSON format:
    {{
        "should_intervene": boolean,
        "reason": "short explanation of why you decided this",
        "message": "A personalized notification message in the user's preferred language (Korean) if appropriate, reflecting their context (AI researcher, gamer)."
    }}
    """

    try:
        response = model.generate_content(prompt)
        content = extract_json(response.text.strip())

        decision = json.loads(content)
        return decision.get("should_intervene", False), decision
    except Exception as e:
        print(f"🔥 Error calling Gemini API: {e}")
        return False, {"error": str(e)}

if __name__ == "__main__":
    # Test JSON extraction
    test_text = "Here is the result: ```json {\"should_intervene\": true} ``` and some extra text."
    print(f"Extracted: {extract_json(test_text)}")
