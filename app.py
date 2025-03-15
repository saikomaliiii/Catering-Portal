from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class CateringGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    dishes = db.relationship('Dish', backref='group', lazy=True)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    meal_type = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('catering_group.id'), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('event_options'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! You can now log in.')
        return redirect(url_for('event_options'))

    return render_template('signup.html')

@app.route('/event_options')
def event_options():
    events = [
        {'name': 'Pelli Bhojanam', 'image': 'pellibhojanam.jpg'},
        {'name': 'Birthday Party', 'image': 'birthdayparty.jpg'},
        {'name': 'Get Together', 'image': 'gettogether.jpg'},
        {'name': 'Events', 'image': 'events.jpg'}
    ]
    return render_template('event_options.html', events=events)

@app.route('/view_options/<event_type>')
def view_event_groups(event_type):
    if event_type == 'pellibhojanam':
        groups = [
            {'id': 1, 'name': 'Vivaha Bhojanambu', 'image': 'vivahabhojanambu.png'},
            {'id': 2, 'name': 'Subbayyagari Hotel', 'image': 'subbayyagarihotel.jpg'}
        ]
        background_image = 'pelli.jpg'
    elif event_type == 'birthdayparty':
        groups = [
            {'id': 3, 'name': 'Little Moments', 'image': 'littlemoments.png'},
            {'id': 4, 'name': 'Tasty Bites', 'image': 'tastybites.png'}
        ]
        background_image = 'bday.jpg'
    elif event_type == 'gettogether':
        groups = [
            {'id': 5, 'name': 'Vanabhojanam', 'image': 'vanabhojanam.jpg'},
            {'id': 6, 'name': 'Aritaku Bhojanam', 'image': 'aritakubhojanam.jpg'},
            {'id': 7, 'name': 'ItsPartyTime', 'image': 'itspartytime.jpg'}
        ]
        background_image = 'get.jpg'
    elif event_type == 'events':
        groups = [
            {'id': 1, 'name': 'Vivaha Bhojanambu', 'image': 'vivahabhojanambu.png'},
            {'id': 2, 'name': 'Subbayyagari Hotel', 'image': 'subbayyagarihotel.jpg'},
            {'id': 3, 'name': 'Little Moments', 'image': 'littlemoments.png'},
            {'id': 5, 'name': 'Vanabhojanam', 'image': 'vanabhojanam.jpg'},
            {'id': 6, 'name': 'Aritaku Bhojanam', 'image': 'aritakubhojanam.jpg'},
            {'id': 7, 'name': 'ItsPartyTime', 'image': 'itspartytime.jpg'},
            {'id': 4, 'name': 'Tasty Bites', 'image': 'tastybites.png'}
        ]
        background_image = 'eve.jpg'
    else:
        groups = []
        background_image = 'default.jpg'

    return render_template('view_options.html', groups=groups, event_type=event_type, background_image=background_image)

@app.route('/select_package/<int:group_id>/<string:event_type>', methods=['GET'])
def select_package(group_id, event_type):
    group = CateringGroup.query.get_or_404(group_id)

    if group.id in [1, 2]:
        background_image = 'pelli.jpg'
    elif group.id in [3, 4]:
        background_image = 'bday.jpg'
    elif group.id in [5, 6, 7]:
        background_image = 'get.jpg'
    else:
        background_image = 'default.jpg'

    dishes = Dish.query.filter_by(group_id=group.id).all()
    
    return render_template('select_package.html', group=group, dishes=dishes, background_image=background_image)

@app.route('/view_dishes/<int:group_id>/<string:event_type>', methods=['GET'])
def view_dishes(group_id, event_type):
    group = CateringGroup.query.get_or_404(group_id)
    return redirect(url_for('select_package', group_id=group.id, event_type=event_type))
@app.route('/basic_package')
def basic_package():
    return render_template('basic_package.html')
@app.route('/premium_package')
def premium_package():
    return render_template('premium_package.html')
@app.route('/custom_package')
def custom_package():
    return render_template('custom_package.html')
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Handle the form submission here
        number_of_plates = request.form.get('number_of_plates')
        coupon_code = request.form.get('coupon_code')
        payment_method = request.form.get('payment_method')

        # Logic for calculating total and applying coupon
        total_value = calculate_total_value(number_of_plates, coupon_code)  # Adjust pricing as needed
        return render_template('cart_confirmation.html', total_value=total_value, payment_method=payment_method)

    return render_template('cart.html')
def calculate_total_value(number_of_plates, coupon_code):
    base_price = 100  # Example base price per plate; adjust as needed
    total = base_price * int(number_of_plates)

    # Example coupon logic
    if coupon_code == 'SAVE10':
        total *= 0.9  # Apply a 10% discount
    elif coupon_code == 'SAVE20':
        total *= 0.8  # Apply a 20% discount

    return total
@app.route('/cart_confirmation', methods=['GET'])
def cart_confirmation():
    # Here, you can add logic to handle the confirmation
    return render_template('cart_confirmation.html')




def create_tables():
    with app.app_context():  # Create application context
        db.create_all()

        # Check if groups already exist before adding
        groups = [
            {'name': 'Vivaha Bhojanambu'},
            {'name': 'Subbayyagari Hotel'},
            {'name': 'Little Moments'},
            {'name': 'Tasty Bites'},
            {'name': 'Vanabhojanam'},
            {'name': 'Aritaku Bhojanam'},
            {'name': 'ItsPartyTime'}
        ]

        for group_data in groups:
            # Check if the group already exists
            group = CateringGroup.query.filter_by(name=group_data['name']).first()
            if not group:
                new_group = CateringGroup(name=group_data['name'])
                db.session.add(new_group)

        db.session.commit()

        # Add Dishes for Vivaha Bhojanambu if not already present
        group1 = CateringGroup.query.filter_by(name='Vivaha Bhojanambu').first()

        dishes_vivaha = [
            {'name': 'Idli', 'price': 100, 'meal_type': 'basic', 'category': 'tiffins'},
            {'name': 'Vada', 'price': 150, 'meal_type': 'basic', 'category': 'tiffins'},
            {'name': 'Veg Meals', 'price': 200, 'meal_type': 'basic', 'category': 'lunch'},
            {'name': 'Premium Meals', 'price': 300, 'meal_type': 'premium', 'category': 'dinner'}
        ]

        for dish_data in dishes_vivaha:
            # Check if dish already exists
            dish = Dish.query.filter_by(name=dish_data['name'], group=group1).first()
            if not dish:
                new_dish = Dish(name=dish_data['name'], price=dish_data['price'], meal_type=dish_data['meal_type'], category=dish_data['category'], group=group1)
                db.session.add(new_dish)

        db.session.commit()


if __name__ == '__main__':
    create_tables()  # Create tables on startup
    app.run(debug=True)
