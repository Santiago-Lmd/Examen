"""


Examen Unidad III 
Autor: [Tu Nombre]
Fecha: [Fecha Actual]

Descripción:
Objetivo del examen
Desarrollar una API básica con Flask que permita:

Crear un diccionario de dispositivos de red.
Agregar nuevos dispositivos.
Modificar dispositivos existentes.
Mostrar un listado de todos los dispositivos en formato HTML, 
donde cada dispositivo se muestre en un <div> con nombre, 
descripción y características

Requisitos técnicos

Usar Flask.
Usar un diccionario como estructura principal de almacenamiento.
Implementar al menos tres rutas:

GET /dispositivos_html: muestra todos los dispositivos en HTML.
POST /dispositivos: agrega un nuevo dispositivo.
PUT /dispositivos/<id>: modifica un dispositivo existente.

Ejemplo del Diccionario de dispositivos: 
{
  "id": "router01",
  "nombre": "Router Principal",
  "descripcion": "Router de borde para salida a Internet",
  "ip": "192.168.1.1",
  "mac": "00:1A:2B:3C:4D:5E",
  "ubicacion": "Sala de servidores",
  "tipo": "Router",
  "otros": ""
}

Recuerda tener al menos 3 commits en tu repositorio. 

Para puntos extra
Puedes ocupar css para añadir puntos a tu examen, perzonalizalo con estilos como el siguiente:
<style>
    .dispositivo {
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
    }
</style>

Puntos extra para añador formula en el cmapo de otros
la formula es la siguente: 

último octeto de la IP * 3 + longitud del nombre del dispositivo + ":" + nombre (Cambiando los espacios por _)

"""
from flask import Flask, jsonify, render_template_string, request, abort

app = Flask(__name__)

# Diccionario principal
dispositivos = {
}

# -------- Función para calcular el campo "otros" --------
def calcular_otros(ip, nombre):
    try:
        ultimo_octeto = int(ip.split(".")[-1])
    except:
        ultimo_octeto = 0
    valor = ultimo_octeto * 3 + len(nombre)
    return f"{valor}:{nombre.replace(' ', '_')}"

# -------- Ruta POST para agregar un nuevo dispositivo --------
@app.route('/dispositivos', methods=['POST'])
def agregar_dispositivo():
    if not request.is_json:
        abort(400, "El contenido debe ser JSON")
    data = request.get_json()

    # Validar campos obligatorios
    campos = ["id", "nombre", "descripcion", "ip", "mac", "ubicacion", "tipo"]
    for campo in campos:
        if campo not in data:
            abort(400, f"Falta el campo '{campo}'")

    if data["id"] in dispositivos:
        abort(409, "El ID ya existe")

    # Calcular "otros" si no se envía
    data["otros"] = data.get("otros", "") or calcular_otros(data["ip"], data["nombre"])

    dispositivos[data["id"]] = data
    return jsonify({"mensaje": "Dispositivo agregado correctamente", "dispositivo": data}), 201


# -------- Ruta GET para mostrar todos los dispositivos en HTML --------
@app.route('/dispositivos_html', methods=['GET'])
def mostrar_html():
    plantilla = """
    <html>
    <head>
        <title>Listado de Dispositivos</title>
        <style>
            body { font-family: Arial; background: #f8f8f8; }
            .dispositivo {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                margin: 10px;
                background: white;
            }
            h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Listado de Dispositivos</h1>
        {% for d in dispositivos %}
        <div class="dispositivo">
            <h2>{{ d.nombre }} ({{ d.id }})</h2>
            <p><b>Descripción:</b> {{ d.descripcion }}</p>
            <p><b>IP:</b> {{ d.ip }}</p>
            <p><b>MAC:</b> {{ d.mac }}</p>
            <p><b>Ubicación:</b> {{ d.ubicacion }}</p>
            <p><b>Tipo:</b> {{ d.tipo }}</p>
            <p><b>Otros:</b> {{ d.otros }}</p>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(plantilla, dispositivos=list(dispositivos.values()))

# -------- Inicio del servidor --------
if __name__ == '__main__':
    app.run(debug=True)
