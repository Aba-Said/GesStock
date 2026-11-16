from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Product Model (Gestion de Stock)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create database tables within application context
with app.app_context():
    db.create_all()

# Route: View All Products (Dashboard / Stock List)
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Route: Add a New Product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        category = request.form['category']

        new_product = Product(name=name, quantity=quantity, price=price, category=category)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Route: Edit an Existing Product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = int(request.form['quantity'])
        product.price = float(request.form['price'])
        product.category = request.form['category']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', product=product)

# Route: Delete a Product
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)