from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    
    print("Recebido:")
    print(f"idRegister: {data.get('idRegister')}")
    print(f"captureDateTime: {data.get('captureDateTime')}")
    print(f"plate: {data.get('plate')}")
    print(f"idCam: {data.get('idCam')}")
    print(f"latitude: {data.get('latitude')}")
    print(f"longitude: {data.get('longitude')}")
    print(f"image: {data.get('image')[:30]}...")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True,host="127.0.0.1",port="5000")
