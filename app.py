from flask import Flask, render_template, request, session, redirect, url_for
from generate_doc import generate_document_from_template
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Это нужно для работы сессий

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'docs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Загружаем сохранённые данные формы из сессии
    form_data = session.get('form_data', {})
    return render_template('index.html', form_data=form_data)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict(flat=False)
    print("Полученные данные формы:", data)  # Выводим все данные, чтобы убедиться, что они правильные

    act_data = {
        "act_number": data['act_number'][0],
        "act_date": data['act_date'][0],
        "client_name": data['client_name'][0],
        "client_address": data['client_address'][0],
        "client_phone": data['client_phone'][0],
        "client_email": data['client_email'][0],
        "invoice_number": data['invoice_number'][0],
        "invoice_date": data['invoice_date'][0],
        "services": [],
        "client_signature": data['client_signature'][0],  # Подпись заказчика
        "executor_name": data['executor_name'][0],
        "executor_address": data['executor_address'][0],
        "executor_phone": data['executor_phone'][0],
        "executor_email": data['executor_email'][0],
        "executor_signature": data['executor_signature'][0]
    }

    print("Данные для генерации документа:", act_data)  # Выводим передаваемые данные

    # Считываем услуги и добавляем их в список 'services'
    for i in range(len(data['service_name'])):
        service_data = {
            "date": data['service_date'][i],
            "car_number": data['car_number'][i],
            "service_name": data['service_name'][i],
            "quantity": int(data['quantity'][i]),
            "price": float(data['price'][i]),
            "total": float(data['total'][i])
        }
        act_data['services'].append(service_data)


    # Путь к шаблону Word
    template_path = os.path.join(os.getcwd(), 'templates', 'шаблон_акта.docx')

    # Генерация документа с использованием шаблона
    word_path = generate_document_from_template(act_data, template_path)

    print("Путь к сгенерированному файлу:", word_path)  # Выводим путь к сгенерированному файлу

    # Сохраняем путь к файлу в сессии
    session['act_data'] = {
        'word': word_path
    }

    return redirect(url_for('downloads'))

@app.route('/downloads')
def downloads():
    if 'act_data' in session:
        word_path = session['act_data']['word']
        return render_template('downloads.html', word_path=word_path)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
