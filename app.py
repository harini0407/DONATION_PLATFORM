from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from resources.volunteers import volunteer_bp
#from app import app, db
#from models import volunteer

#from Volunteer import volunteer_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize Flask extensions
socketio = SocketIO(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(volunteer_bp, url_prefix='/volunteers')
@app.route('/')
def home():
    return "Welcome to the Donation Platform!"
# Notification for new donation created
@app.route('/notify')
def notify():
    socketio.emit('new_donation', {'message': 'A new donation has been posted!'})
    return "Notification sent!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures database tables are created
    socketio.run(app, debug=True)
