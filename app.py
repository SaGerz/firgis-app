from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
import os
import torch
import cv2
import numpy as np
import requests
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# model = torch.hub.load('ultralytics/yolov5', path='Models/best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Models/best.pt', force_reload=True)
# model.eval()

# app = Flask(__name__)
# app.static_folder = 'static'
# app = Flask(__name__, '/Static')
# app = Flask(__name__, static_folder='Static', static_url_path='/Static')
app = Flask(__name__, static_folder='Static', template_folder='templates')
application = app

@app.route("/")
def home():
    return render_template("1_halaman_utama.html")

@app.route("/welcome")
def welcome():
    return render_template("2_welcome.html")

@app.route("/our_feature")
def our_feature():
    return render_template("3_our_feature.html")

@app.route("/penjelasan_live_camera")
def penjelasan_live_camera():
    return render_template("4_penjelasan_live_camera.html")

@app.route("/detect")
def live_camera():
    return render_template("5_live_camera.html")

@app.route("/penjelasan_foto_galeri")
def penjelasan_foto_galeri():
    return render_template("6_penjelasan_foto_galeri.html")

@app.route("/foto_galeri")
def foto_galeri():
    return render_template("7_foto_galeri.html")

@app.route("/details")
def details():
    return render_template("8_details.html")

@app.route("/creator")
def creator():
    return render_template("9_creator.html")

from flask import send_from_directory

@app.route('/assets/<path:filename>')
def assets (filename):
    return send_from_directory('assets', filename)

@app.route("/mulut_1_2")
def mulut_1_2():
    return render_template("10_Mulut_(1_2).html")

@app.route("/mulut_3_4")
def mulut_3_4():
    return render_template("11_Mulut_(3_4).html")

@app.route("/mulut_5")
def mulut_5():
    return render_template("12_Mulut_(5).html")

@app.route("/sirip_dada")
def sirip_dada():
    return render_template("13_Sirip_Dada.html")

@app.route("/sirip_perut")
def sirip_perut():
    return render_template("14_Sirip_Perut.html")

@app.route("/sirip_dubur")
def sirip_dubur():
    return render_template("15_Sirip_Dubur.html")

@app.route("/sirip_punggung")
def sirip_punggung():
    return render_template("16_Sirip_Punggung.html")

@app.route("/sirip_ekor")
def sirip_ekor():
    return render_template("17_Sirip_Ekor.html")

@app.route("/morfometrik")
def morfometrik():
    return render_template("18_Morfometrik.html")

@app.route("/meristik")
def meristik():
    return render_template("19_Meristik.html")

@app.route("/quiz_gform")
def quiz_gform():
    return render_template("20_Quiz_Gform.html")

@app.route("/quiz_quizizz")
def quiz_quizizz():
    return render_template("21_Quiz_(Quizizz).html")

@app.route("/referensi")
def referensi():
    return render_template("22_Referensi.html")

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # Ambil data gambar dari base64 string
        image = Image.open(BytesIO(base64.b64decode(image_data)))

        # Proses gambar dengan model YOLOv5 atau apapun yang Anda gunakan
        # ...
        # Simpan gambar di dalam folder static/images
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Gunakan model yolov5 untuk melakukan deteksi pada gambar
        results = model(image)

        # hasil deteksi
        detections = results.xyxy[0].cpu().numpy()
        print(detections)

        # Konversi gambar ke format NumPy
        image_np = np.array(image)

        # Gambar kotak deteksi pada gambar
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_idx = detection
            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        # Warna dan label berdasarkan class_idx (jika diperlukan)
            color = (0, 255, 0)  # Misalnya, gunakan warna hijau
            label = f'Class {int(class_idx)}'


            label_text = f'Class {int(class_idx)}'
            if class_idx == 0: 
                label_text = "Mulut"
            elif class_idx == 1:
                label_text = "Sirip Anal"
            elif class_idx == 2:
                label_text = "Sirip Dada"
            elif class_idx == 3:
                label_text = "Sirip Ekor"
            elif class_idx == 4:
                label_text = "Sirip Perut"
            elif class_idx == 5:
                label_text = "Sirip Punggung"

            # Gambar kotak deteksi
            cv2.rectangle(image_np, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image_np, label_text, (x_min, y_min - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            # cv2.putText(image_np, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Simpan hasil
            # result_image = Image.fromarray(image_np)
            # image.save(result_image_path)
            # result_image.save('Static/Images/detected_image.jpg')
            # result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
            result_image = Image.fromarray(image_np)
            result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
            result_image.save(result_image_path)

        with open(result_image_path, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # image.save(os.path.join(os.getcwd(), 'Static/Images/detected.jpg'))
        # image.save('Static/Images/detected.jpg')  # Ganti dengan path yang sesuai

        # return send_file('Static/Images/detected.jpg', as_attachment=True)
        return jsonify({'message': 'Image processed successfully', 'detections': detections.tolist(), 'result_image_base64': image_base64})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#Fungsi untuk menentukan jenis file yang diizinkan
def allowed_file(Filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/foto_galeri', methods=['POST'])        
def handle_uploaded_image():
    try:
        # Get image file from request
        image_file = request.files['image']

        # Open image
        image = Image.open(image_file)

        # Perform object detection using YOLOv5 model
        # (Pastikan model YOLOv5 telah diinisialisasi sebelumnya)
        results = model(image)

        # hasil deteksi
        detections = results.xyxy[0].cpu().numpy()
        print(detections)

        # Konversi gambar ke format NumPy
        image_np = np.array(image)

        # Gambar kotak deteksi pada gambar
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_idx = detection
            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

            # Warna dan label berdasarkan class_idx (jika diperlukan)
            color = (0, 255, 0)  # Misalnya, gunakan warna hijau
            label = f'Class {int(class_idx)}'

            label_text = f'Class {int(class_idx)}'
            if class_idx == 0: 
                label_text = "Mulut"
            elif class_idx == 1:
                label_text = "Sirip Anal"
            elif class_idx == 2:
                label_text = "Sirip Dada"
            elif class_idx == 3:
                label_text = "Sirip Ekor"
            elif class_idx == 4:
                label_text = "Sirip Perut"
            elif class_idx == 5:
                label_text = "Sirip Punggung"

            # Gambar kotak deteksi
            cv2.rectangle(image_np, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image_np, label_text, (x_min, y_min - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Simpan hasil
        result_image = Image.fromarray(image_np)
        result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
        result_image.save(result_image_path)

        # Return path to the processed image
        return jsonify({'message': 'Image processed successfully', 'result_image_path': 'detected_image.jpg'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/detected_image", methods=['GET'])
def get_detected_image():
    try:
        result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
        return send_file(result_image_path, mimetype='image/jpg')
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error:str(e)'}), 500



# if __name__ == "__main__":  
#     app.run(debug=True)
# if __name__ == "__main__":  
#     app.run(debug=False)


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":  
#     app.debug = False
#     app.run()

