from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import fitz  # PyMuPDF
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Get key from env

# Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)


def extract_resume_text():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(base_dir, 'chatbot', 'data', 'Efrain_Granados_Frontend_Engineer_Resume_July_2025.pdf')

    if not os.path.exists(pdf_path):
        return "Resume file not found."

    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading resume: {str(e)}"


@csrf_exempt
def make_question(request):
    if request.method == 'POST':
        try:
            # Try to create session if there's not one
            try:
                if not request.session.session_key:
                    request.session.create()
            except Exception as e:
                print("Session creation error:", e)

            data = json.loads(request.body)
            question = data.get('question')
            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)

            resume_text = extract_resume_text()

            if resume_text.startswith("Error") or resume_text.startswith("Resume file not found"):
                return JsonResponse({
                    'error': 'Resume could not be loaded',
                    'details': resume_text
                }, status=500)

            try:
                chat_history = request.session.get("chat_history", [])
            except Exception:
                chat_history = []

            # Gemini Chat history
            context = "\n".join(
                [f"User: {entry['user']}\nAssistant: {entry['assistant']}" for entry in chat_history]
            )

            prompt = f"""
You are a professional assistant who knows Efraín Granados very well. You have access to his resume and can answer questions about his experience, technologies, and skills.

Please respond in a professional and concise tone, avoiding repetition. Structure the answer clearly and use confident, natural language. Refer to him in the third person (e.g., "Efraín has experience with...", "He has contributed to...").

Use only the information from the resume below. Do not make up facts. If the information is not in the resume, respond with: "The resume does not mention this information."

Resume:
{resume_text}

Previous conversation:
{context}

User: {question}
"""

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            chat_history.append({
                "user": question,
                "assistant": response.text.strip()
            })

            try:
                request.session["chat_history"] = chat_history
            except Exception as e:
                print("Session save error:", e)

            return JsonResponse({
                'question': question,
                'response': response.text.strip()
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def reset_conversation(request):
    if request.method == 'POST':
        try:
            if request.session is not None:
                request.session["chat_history"] = []
        except Exception as e:
            return JsonResponse({'error': 'Session error', 'details': str(e)}, status=500)
        return JsonResponse({'message': 'Conversation reset successfully'})
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def health_check(request):
    return JsonResponse({"status": "ok"})
