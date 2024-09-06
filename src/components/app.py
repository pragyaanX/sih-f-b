from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from hdf5_processing import process_hdf5 as process_hdf5_function
import os

app = Flask(__name__, static_folder='../hdf5-upload-app/build', static_url_path='/')

# Enable CORS globally
CORS(app)

TEMP_FOLDER = 'temp'
if not os.path.exists(TEMP_FOLDER):
    print(f'{TEMP_FOLDER} directory created')
    os.makedirs(TEMP_FOLDER)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process_hdf5', methods=['POST'])
def process_hdf5_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    print('formData', request)
    file = request.files['file']
    print(file)
    selected_band = request.form.get('selected_band')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(TEMP_FOLDER, file.filename)
    file.save(file_path)
    print(f"{file_path} file generated")
    
    try:
        print('before cog', selected_band)
        cog_output_tiff = process_hdf5_function(file_path, selected_band)
        print('after cog')
        return send_file(cog_output_tiff, as_attachment=True, download_name=f"{selected_band}_COG.tif")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/thank_you')
def thank_you():
    return '<h1>Thanks</h1>'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
