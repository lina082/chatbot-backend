from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Para evitar problemas de CORS
import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Ruta principal (renderiza el frontend)
@app.route("/")
def index():
    return render_template("index.html")

# Ruta de chat (maneja los mensajes)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # Llamada al modelo de OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar en producción (para Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
