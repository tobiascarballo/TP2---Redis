from flask import Flask, jsonify, request
from redis import Redis
from flask import render_template

app = Flask(__name__)

r = Redis(host='localhost', port=6379, decode_responses=True)

# lista de capítulos de la Temporada 1 
CAPITULOS = {
    # Temporada 1
    "1": "El mandaloriano", "2": "El niño", "3": "El pecado",
    "4": "Santuario", "5": "El pistolero", "6": "El prisionero",
    "7": "El ajuste de cuentas", "8": "Redención",
    # Temporada 2
    "9": "El mariscal", "10": "La pasajera", "11": "La heredera",
    "12": "El asedio", "13": "La Jedi", "14": "La tragedia",
    "15": "El creyente", "16": "El rescate",
    # Temporada 3
    "17": "El apóstata", "18": "Las minas de Mandalore", "19": "El converso",
    "20": "El huérfano", "21": "El pirata", "22": "Pistoleros a sueldo",
    "23": "Los espías", "24": "El regreso"
}

# PUNTO 1: ruta para listar caps y su estado
@app.route('/capitulos', methods=['GET'])
def listar_capitulos():
    lista = []
    for id_cap, nombre in CAPITULOS.items():
        estado = r.get(f"mando:{id_cap}")
        if not estado:
            estado = "disponible"
        lista.append({"id": id_cap, "nombre": nombre, "estado": estado})
    return jsonify(lista)

# PUNTO 2: ruta para alquilar (reserva de 4 minutos)
@app.route('/reservar/<id_cap>', methods=['POST'])
def reservar(id_cap):
    if id_cap not in CAPITULOS:
        return "Capítulo no encontrado", 404
    
    # vemos si esta ocupado
    if r.exists(f"mando:{id_cap}"):
        return "El capítulo no está disponible", 400

    # seteamos con expiracion de 4 min
    r.set(f"mando:{id_cap}", "reservado", ex=240)
    return f"Capítulo {id_cap} reservado por 4 minutos. Pendiente de pago."

# PUNTO 3: ruta para confirmar pago (alquiler por 24 hs)
@app.route('/pagar', methods=['POST'])
def confirmar_pago():
    data = request.get_json()
    id_cap = data.get('id')
    precio = data.get('precio')
    
    # vemos si esta reservado antes de pagar
    if r.get(f"mando:{id_cap}") == "reservado":
        # registramos por 24 horas
        r.set(f"mando:{id_cap}", "alquilado", ex=86400)
        return f"Pago de ${precio} confirmado. Alquiler valido por 24hs."
    else:
        return "La reserva expiro o el cap no esta reservado", 400

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)