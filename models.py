from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Therapist Model
class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    certifications = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.JSON, nullable=True)  # JSON for flexible scheduling
    contact_info = db.Column(db.JSON, nullable=False)  # Email, phone, etc.
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"Therapist('{self.name}', '{self.specialty}')"


# Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact_info = db.Column(db.JSON, nullable=False)  # Email, phone, etc.
    health_records = db.Column(db.JSON, nullable=True)  # Optional field for therapy history or notes
    preferred_therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=True)
    payment_preferences = db.Column(db.JSON, nullable=True)  # Payment types (Card, Cash, Insurance, etc.)

    def __repr__(self):
        return f"Customer('{self.name}', '{self.age}')"


# Room Model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.JSON, nullable=True)  # Optional equipment
    availability = db.Column(db.JSON, nullable=True)  # Availability time slots
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"Room('{self.room_number}', '{self.capacity}')"


# PaymentType Model
class PaymentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # e.g., "Cash", "Card", "Insurance"
    discount = db.Column(db.Float, nullable=True)  # Optional discount field

    def __repr__(self):
        return f"PaymentType('{self.type}')"


# TherapyOption Model
class TherapyOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Cognitive Therapy", "Physical Therapy"
    type = db.Column(db.String(50), nullable=False)  # e.g., "Individual", "Group", "Specialized"
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    price = db.Column(db.Float, nullable=False)
    equipment_needed = db.Column(db.JSON, nullable=True)  # Optional equipment required
    therapist_specialty_required = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"TherapyOption('{self.name}', '{self.type}')"


# Session Model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    therapy_option_id = db.Column(db.Integer, db.ForeignKey('therapy_option.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    status = db.Column(db.String(50), nullable=False)  # e.g., "Scheduled", "Completed", "Canceled"
    feedback = db.Column(db.Text, nullable=True)  # Optional customer feedback
    payment_status = db.Column(db.String(50), nullable=False)  # e.g., "Pending", "Completed"
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"Session('{self.date}', '{self.status}')"


# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.JSON, nullable=False)  # Phone, email, etc.
    
    # Relationships (reverse links to therapists, rooms, sessions)
    therapists = db.relationship('Therapist', backref='location', lazy=True)
    rooms = db.relationship('Room', backref='location', lazy=True)
    sessions = db.relationship('Session', backref='location', lazy=True)

    def __repr__(self):
        return f"Location('{self.name}', '{self.address}')"
