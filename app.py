from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "¡Servidor activo en Render!"

if __name__ == "__main__":
    app.run()