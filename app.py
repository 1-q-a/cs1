import re
from flask import Flask, render_template, request
from markupsafe import Markup  # 追加

app = Flask(__name__)

kinoko_count = 3
takenoko_count = 5
messages = ['Kinoko is wonrderful!', 'Takenoko is awesome!']

# URLをリンクに変換する関数を定義
def convert_urls_to_links(text):
    # 正規表現パターンを定義
    url_pattern = r'(https?://\S+)'

    def replace_url(match):
        url = match.group(1)
        return '<a href="{}">{}</a>'.format(url, url)

    return re.sub(url_pattern, replace_url, text)

@app.route('/')
def top():
    return render_template('index.html', **vars())

@app.route('/vote', methods=['POST'])
def answer():
    global kinoko_count, takenoko_count, messages
    if request.form.get("item") == 'kinoko':
        kinoko_count += 1
    elif request.form.get("item") == 'takenoko':
        takenoko_count += 1

    messages.append(request.form.get("message"))
    if len(messages) > 3:
        messages = messages[-3:]
    
    kinoko_percent = kinoko_count / (kinoko_count + takenoko_count) * 100
    takenoko_percent = takenoko_count / (kinoko_count + takenoko_count) * 100

    message_html = ''
    for i in range(len(messages)):
        message = messages[i]
        message = re.sub(r'&', r'&amp;', message)
        message = re.sub(r'<', r'&lt;', message)
        message = re.sub(r'>', r'&gt;', message)
        message = re.sub(r'\*(.+)\*', r'<strong>\1</strong>', message)
        message = re.sub(r'(\d{2,3})-\d+-\d+', r'\1-****-****', message)
        message = convert_urls_to_links(message)  # URLをリンクに変換
        message_html += '<div class="alert {1}" role="alert">{0}</div>\n'.format(
            Markup(message), 'alert-warning ms-5' if i % 2 == 0 else 'alert-success me-5')  # Markupでエスケープを無効化

    return render_template('vote.html', **vars())

if __name__ == '__main__':
    app.run(debug=True)
