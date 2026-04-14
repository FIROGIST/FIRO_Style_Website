from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# تحديد المسار الرئيسي للمشروع (الفولدر الكبير)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'), 
            static_folder=os.path.join(BASE_DIR, 'static'))

def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'firo_style.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER, desc TEXT, img TEXT, img2 TEXT, img3 TEXT)''')
    conn.commit()
    
    # إضافة منتج افتراضي إذا كانت القاعدة فارغة
    c.execute('SELECT * FROM products')
    if not c.fetchone():
        desc = "✨ جدارية مكرمية ورق الشجر هاند ميد قطن 100%"
        c.execute("INSERT INTO products (name, price, desc, img) VALUES (?, ?, ?, ?)", 
                  ('مكرمية واحة السلام', 250, desc, 'main-macrame.jpg'))
        conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id=1').fetchone()
    conn.close()
    if product:
        # تحويل بيانات المنتج لشكل يفهمه الـ HTML
        data = {
            "name": product['name'], 
            "price": product['price'], 
            "desc": product['desc'], 
            "images": [product['img']], 
            "whatsapp": "201557671143"
        }
        return render_template('index.html', product=data)
    return "الموقع قيد التحديث"

@app.route('/shop')
def shop():
    conn = get_db_connection()
    all_products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('shop.html', products=all_products)

init_db()

if __name__ == '__main__':
    app.run(debug=True)