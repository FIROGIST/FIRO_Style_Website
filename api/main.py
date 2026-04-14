from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '../firo_style.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # عشان نعرف ننادي الأعمدة بأسمائها
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER, desc TEXT, img TEXT, img2 TEXT, img3 TEXT)''')
    
    # التأكد من وجود الأعمدة الجديدة
    try: c.execute('ALTER TABLE products ADD COLUMN img2 TEXT')
    except: pass
    try: c.execute('ALTER TABLE products ADD COLUMN img3 TEXT')
    except: pass

    # إضافة منتج تجريبي إذا كانت القاعدة فارغة
    c.execute('SELECT * FROM products')
    if not c.fetchone():
        desc = "✨ جدارية مكرمية ورق الشجر هاند ميد قطن 100%"
        c.execute("INSERT INTO products (name, price, desc, img, img2, img3) VALUES (?, ?, ?, ?, ?, ?)", 
                  ('مكرمية واحة السلام', 250, desc, 'main-macrame.jpg', '', ''))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id=1').fetchone()
    conn.close()
    if product:
        img_list = [product['img']]
        if product['img2']: img_list.append(product['img2'])
        if product['img3']: img_list.append(product['img3'])
        data = {"name": product['name'], "price": product['price'], "desc": product['desc'], "images": img_list, "whatsapp": "201557671143"}
        return render_template('index.html', product=data)
    return "الموقع قيد التحديث"

@app.route('/shop')
def shop():
    conn = get_db_connection()
    all_products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('shop.html', products=all_products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    if request.method == 'POST':
        conn.execute("UPDATE products SET name=?, price=?, desc=? WHERE id=1", 
                     (request.form['name'], request.form['price'], request.form['desc']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    product = conn.execute('SELECT * FROM products WHERE id=1').fetchone()
    conn.close()
    return render_template('admin.html', product=product)

init_db()

if __name__ == '__main__':
    app.run(debug=True)