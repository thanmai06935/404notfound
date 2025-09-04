from flask import Flask, request, render_template_string
from transformers import AutoTokenizer, AutoModelForCausalLM
import pyttsx3

app = Flask(__name__)

# Load model and tokenizer (using a small DialoGPT for demo)
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = ""
    bot_reply = ""
    user_type = "student"  # default role


    if request.method == "POST":
        user_input = request.form["query"]
        user_type = request.form["role"]

        prefix = {
            "student": "As a student, how can I",
            "professional": "As a working professional, how can I",
            "investor": "As an investor, how can I",
            "businessman": "As a businessman, how can I",
            "other": "How can I"
        }.get(user_type, "How can I")

        prompt = f"{prefix} {user_input}"

        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        outputs = model.generate(**inputs, max_length=100)
        bot_reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

        speak(bot_reply)

    html = """
    <h2>Personal Finance Bot</h2>
    <form method="post">
      I am a:
      <select name="role">
        <option value="student" {{'selected' if user_type=='student' else ''}}>Student</option>
        <option value="professional" {{'selected' if user_type=='professional' else ''}}>Working Professional</option>
        <option value="investor" {{'selected' if user_type=='investor' else ''}}>Investor</option>
        <option value="businessman" {{'selected' if user_type=='businessman' else ''}}>Businessman</option>
        <option value="other" {{'selected' if user_type=='other' else ''}}>Other</option>
      </select><br><br>
      Ask: <input type="text" name="query" size="50" value="{{ user_input }}"><br><br>
      <input type="submit" value="Ask">
    </form>
    {% if user_input %}
      <p><b>You:</b> {{ user_input }}</p>
      <p><b>Bot:</b> {{ bot_reply }}</p>
    {% endif %}
    """
    return render_template_string(html, user_input=user_input, bot_reply=bot_reply, user_type=user_type)

if __name__ == "__main__":
    print("Running bot at http://127.0.0.1:5000")
    app.run(debug=True)
