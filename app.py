from flask import Flask, request, render_template, jsonify, redirect, url_for
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

# Конфигурация подключения к базе данных MariaDB
db_config = {
    'host': 'localhost',
    'user                       
}

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True  # Включаем SSL
app.config['MAIL_USERNAME'] = ''  # Твой email
app.config['MAIL_PASSWORD'] = ''  # Пароль приложения
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)



# Подключение к базе данных
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

        
# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница успешной покупки
@app.route('/success')
def success():
    return render_template('success.html')

# Страница повторной покупки
@app.route('/repeat_purchase', methods=['GET'])
def repeat_purchase():
    email = request.args.get('email')  # Получаем email из параметров запроса
    return render_template('repeat_purchase.html', email=email)

@app.route('/sy-35')
def sy35_page():
    return render_template('sy-35.html')

@app.route('/mig-29')
def mig29_page():
    return render_template('mig-29.html')

@app.route('/sy-57')
def sy57_page():
    return render_template('sy-57.html')

@app.route('/mig-31')
def mig31_page():
    return render_template('mig-31.html')

@app.route('/sy-27')
def sy27_page():
    return render_template('sy-27.html')

@app.route('/sy-30')
def sy30_page():
    return render_template('sy-30.html')

@app.route('/mig-35')
def mig35_page():
    return render_template('mig-35.html')

@app.route('/sy-33')
def sy33_page():
    return render_template('sy-33.html')

@app.route('/sy-34')
def sy34_page():
    return render_template('sy-34.html')

@app.route('/sy-24')
def sy24_page():
    return render_template('sy-24.html')

@app.route('/sy-25')
def sy25_page():
    return render_template('sy-25.html')

@app.route('/ty-160')
def ty160_page():
    return render_template('ty-160.html')

@app.route('/ty-22m')
def ty22m_page():
    return render_template('ty-22m.html')

@app.route('/ty-95')
def ty95_page():
    return render_template('ty-95.html')

@app.route('/mi-28n')
def mi28n_page():
    return render_template('mi-28n.html')

@app.route('/ka-52')
def ka52_page():
    return render_template('ka-52.html')

@app.route('/mi-24')
def mi24_page():
    return render_template('mi-24.html')

# Обработка покупки билетов
@app.route('/submit', methods=['POST'])
def submit_ticket():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']
    ticket_count = int(request.form['ticket-count'])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Проверяем, есть ли уже билеты у пользователя
    check_query = "SELECT ticket_count FROM your_table_name WHERE email = %s OR phone = %s"
    cursor.execute(check_query, (email, phone))
    existing_data = cursor.fetchone()

    if existing_data:
        # Если билеты уже куплены, перенаправляем на repeat_purchase с email в параметрах
        return redirect(url_for('repeat_purchase', email=email))

    # Если билетов нет, оформляем первую покупку
    insert_query = """
    INSERT INTO your_table_name (name, surname, email, phone, ticket_count)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        cursor.execute(insert_query, (name, surname, email, phone, ticket_count))
        conn.commit()
        cursor.close()
        conn.close()

        send_ticket_email(email, name, ticket_count)
        return redirect(url_for('success'))

    except mysql.connector.Error as err:
        return jsonify({'message': f'Ошибка базы данных: {err}'}), 500

# Обработка докупки билетов
@app.route('/buy_more', methods=['POST'])
def buy_more():
    email = request.form['email']
    additional_tickets = int(request.form['additional-tickets'])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Обновляем количество билетов
    update_query = "UPDATE your_table_name SET ticket_count = ticket_count + %s WHERE email = %s"
    
    try:
        cursor.execute(update_query, (additional_tickets, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('success'))

    except mysql.connector.Error as err:
        return jsonify({'message': f'Ошибка базы данных: {err}'}), 500
    

def send_ticket_email(user_email, name, ticket_count):
    msg = Message(
        "Подтверждение покупки билетов",
        recipients=[user_email]
    )
    msg.body = f"Здравствуйте, {name}!\n\nВы успешно забронировали {ticket_count} билет(ты). Чтобы их приобрести приходите к главному входу и покажите это сообшение.\nСпасибо за понимание!"
    
    try:
        mail.send(msg)
        print(f"Email отправлен {user_email}")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
