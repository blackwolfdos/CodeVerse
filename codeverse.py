from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.id

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    item = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Order %r>' % self.id
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        item = request.form['item']
        quantity = request.form['quantity']
        address = request.form['address']
        
        new_order = Order(username=username, item=item, quantity=quantity, address=address)

        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/cosuccses')
        except:
            return 'error memasukkan order baru'
        
    else:
        items = Product.query.order_by(Product.id).all()
        return render_template('index.html', items=items)
    
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form['item']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']

        new_item = Product(name=name, description=description, price=price, image_url=image_url)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'error membuat produk'
        
    else:
        orders = Order.query.order_by(Order.order_date).all()
        items = Product.query.order_by(Product.id).all()
        return render_template('admin.html', items = items, orders=orders)
        
@app.route('/admin/delete/<int:id>')
def delete(id):
    item_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'error menghapus item'
    
@app.route('/admin/done/<int:id>')
def done(id):
    order_done = Order.query.get_or_404(id)

    try:
        order_done.done = True
        db.session.commit()
        return redirect('/admin')
    except:
        return 'error menyelesaikan item'

@app.route('/checkout/<string:name>', methods=['POST','GET'])
def checkout(name):
        item = Product.query.filter_by(name=name).first()
        return render_template('checkout.html', item=item)

@app.route('/cosuccses')
def susccses():
    return render_template('cosuccses.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)