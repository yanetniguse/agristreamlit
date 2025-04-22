# Description: A simple chatbot that generates AI-based responses using Hugging Face API.it's under development.
import requests

def get_ai_response(user_message):
    """Generate AI-based chatbot responses using Hugging Face API."""
    API_URL = ""

    headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}  # Optional if you have an API key

    try:
        response = requests.post(API_URL, json={"inputs": user_message}, headers=headers)
        response_data = response.json()

        if "error" in response_data:
            return "❌ Error: API limit reached or invalid request."

        return response_data.get("generated_text", "⚠️ No response generated.")
    except Exception as e:
        return f"❌ API Error: {str(e)}"


if __name__ == "__main__":
    while True:
        user_input = input("👨‍🌾 Ask a farming question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        response = get_ai_response(user_input)
        print(f"🤖 AgriChat: {response}")
