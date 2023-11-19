# app.py

from flask import Flask, render_template, request, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def read_instructions_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_dockerfile', methods=['POST'])
def check_dockerfile():
    filename = 'talimatlar.txt'
    dockerfile_header = read_instructions_from_file(filename)
    dockerfile_content = request.json['content']

    response_text = check_dockerfile_with_api(dockerfile_header, dockerfile_content)
    return jsonify({'message': response_text})

def check_dockerfile_with_api(header, content):
    api_url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
    
    prompt = f"Talimatlar:{header}\n\nDockerfile içeriği:\n{content}\nTüm satırları analiz et. Typo hatası varsa söyle.Yanlış yazılmış bir kelime veya kütüphane adı varsa beni uyar. Tam kapsamlı bir kontrol yap ve sonucu söyle."
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app.config['OPENAI_API_KEY']}",
    }

    data = {
        "prompt": prompt,
        "max_tokens": 350,
    }

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return f"API isteği başarısız: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
