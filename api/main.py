from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# السطرين بتوع البرمجة هما دول: 
# ضفنا (template_folder و static_folder) عشان السيرفر يعرف يوصل للفولدرات وهي بره مجلد api
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

def init_db():
    # تعديل مسار قاعدة البيانات لتكون في الفولدر الرئيسي
    db_path = os.path.join(os.path.dirname(__file__), '../firo_style.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, desc TEXT, img TEXT, img2 TEXT, img3 TEXT)''')
    try:
        c.execute('ALTER TABLE products ADD COLUMN img2 TEXT')
        c.execute('ALTER TABLE products ADD COLUMN img3 TEXT')
    except:
        pass 
    c.execute('SELECT * FROM products WHERE id=1')
    if not c.fetchone():
        desc = "✨ تفصيلة صغيرة… بس بتغير شكل المكان\n🍃 جدارية مكرمية ورق الشجر\n🧵 شغل هاند ميد قطن 100%"
        c.execute("INSERT INTO products (id, name, price, desc, img, img2, img3) VALUES (1, 'مكرمية واحة السلام اليدوية', 250, ?, 'main-macrame.jpg', '', '')", (desc,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    db_path = os.path.join(os.path.dirname(__file__), '../firo_style.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id=1')
    product = c.fetchone()
    conn.close()
    
    img_list = [product[4]]
    if product[5]: img_list.append(product[5])
    if product[6]: img_list.append(product[6])

    data = {
        "name": product[1], "price": product[2], "desc": product[3],
        "images": img_list, "whatsapp": "201557671143"
    }
    return render_template('index.html', product=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db_path = os.path.join(os.path.dirname(__file__), '../firo_style.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if request.method == 'POST':
        c.execute("UPDATE products SET name=?, price=?, desc=? WHERE id=1", 
                  (request.form['name'], request.form['price'], request.form['desc']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute('SELECT * FROM products WHERE id=1')
    product = c.fetchone()
    conn.close()
    return render_template('admin.html', product=product)

# هذا السطر مهم لـ Vercel
init_db()

if __name__ == '__main__':
    app.run(debug=True)