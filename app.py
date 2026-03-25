from flask import Flask
from auth import auth_bp
from process_manager import process_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(process_bp)

if __name__ == '__main__':
    app.run(debug=True)
