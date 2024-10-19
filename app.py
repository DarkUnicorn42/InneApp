from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create the SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

# App factory function
def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inneapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the app with the db instance
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Import the models
    from models import Therapist, Customer, Room, PaymentType, TherapyOption, Session, Location

    # Initialize the database
    with app.app_context():
        db.create_all()

    # Route for the index page
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
