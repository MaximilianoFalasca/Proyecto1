from flask import Flask
from routes import Usuarios_routes

app = Flask(__name__)

# Registrar el Blueprint
app.register_blueprint(Usuarios_routes)

if __name__ == '__main__':
    app.run(debug=True)
