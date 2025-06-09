from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados en memoria
mensajes = []
contador_id = 1

@app.route('/mensajes', methods=['GET'])
def obtener_mensajes():
    return jsonify(mensajes)

@app.route('/mensajes/<int:id>', methods=['GET'])
def obtener_mensaje(id):
    mensaje = next((m for m in mensajes if m['id'] == id), None)
    if mensaje:
        return jsonify(mensaje)
    return jsonify({'error': 'Mensaje no encontrado'}), 404

@app.route('/mensajes', methods=['POST'])
def crear_mensaje():
    global contador_id
    data = request.get_json()
    nuevo_mensaje = {
        'id': contador_id,
        'user': data.get('user'),
        'mensaje': data.get('mensaje')
    }
    mensajes.append(nuevo_mensaje)
    contador_id += 1
    return jsonify(nuevo_mensaje), 201

@app.route('/mensajes/<int:id>', methods=['PUT'])
def actualizar_mensaje(id):
    data = request.get_json()
    for m in mensajes:
        if m['id'] == id:
            m['user'] = data.get('user', m['user'])
            m['mensaje'] = data.get('mensaje', m['mensaje'])
            return jsonify(m)
    return jsonify({'error': 'Mensaje no encontrado'}), 404

@app.route('/mensajes/<int:id>', methods=['DELETE'])
def eliminar_mensaje(id):
    global mensajes
    mensajes = [m for m in mensajes if m['id'] != id]
    return jsonify({'mensaje': 'Mensaje eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True)
