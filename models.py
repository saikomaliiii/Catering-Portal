from app import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    occasion = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    menu = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='bookings')

# Add relationship in User model
User.bookings = db.relationship('Booking', order_by=Booking.id, back_populates='user')
