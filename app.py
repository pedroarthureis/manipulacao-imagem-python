from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename


from modules import mod1_basic, mod2_transform, mod3_color, mod4_format, mod5_filters, mod6_alpha

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'data/input'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50MB max-limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data/output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Servir arquivos gerados para o frontend
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

@app.route('/api/run/<module_id>', methods=['POST'])
def run_module(module_id):
    # Valores padrão apenas para fallback, mas agora com a interface completa o usuário deve fazer upload
    default_files = {
        '1': 'data/input/sample.jpg',
        '2': 'data/input/sample.jpg',
        '3': 'data/input/sample.jpg',
        '4': 'data/input/sample.jpg',
        '5': 'data/input/sample.jpg',
        '6': 'data/input/sample.jpg'
    }
    
    file_path = default_files.get(module_id)

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Arquivo não encontrado."}), 400

    # Extrair parâmetros do formulário
    params = request.form.to_dict()

    try:
        if module_id == '1':
            result = mod1_basic.run(file_path, params)
        elif module_id == '2':
            result = mod2_transform.run(file_path, params)
        elif module_id == '3':
            result = mod3_color.run(file_path, params)
        elif module_id == '4':
            result = mod4_format.run(file_path, params)
        elif module_id == '5':
            result = mod5_filters.run(file_path, params)
        elif module_id == '6':
            result = mod6_alpha.run(file_path, params)
        else:
            return jsonify({"error": "Módulo inválido."}), 400

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Falha ao processar a imagem."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
