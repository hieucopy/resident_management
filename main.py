from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# Kết nối với cơ sở dữ liệu
def get_db_connection():
    conn = sqlite3.connect('residents.db')
    conn.row_factory = sqlite3.Row
    return conn

# Tạo bảng residents nếu chưa tồn tại
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS residents (
            id TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            gender TEXT,
            address TEXT
        )
    ''')
    conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    residents = conn.execute('SELECT * FROM residents').fetchall()
    conn.close()
    return render_template('index.html', residents=residents)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']

        if not id or not name or not dob or not gender or not address:
            flash('Vui lòng nhập đầy đủ thông tin!')
        else:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO residents (id, name, dob, gender, address) VALUES (?, ?, ?, ?, ?)',
                             (id, name, dob, gender, address))
                conn.commit()
                flash('Thêm cư dân thành công!')
            except sqlite3.IntegrityError:
                flash('ID đã tồn tại!')
            conn.close()
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM residents WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Xóa cư dân thành công!')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
