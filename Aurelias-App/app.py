import os
from flask import Flask, render_template_string, request, flash, redirect, url_for, send_from_directory
from datetime import datetime, timedelta
import urllib.parse

app = Flask(__name__)
app.secret_key = "aurelias_key_2026"

# --- DATOS DE LA PASTELERÍA ---
PASTELERIA_INFO = {
    'nombre': "AURELIA'S Pastelería Fina",
    'telefono_ventas': "51949091136",
    'telefono_proforma': "51901014860",
    'logo_archivo': 'logo_aurelias.png' # El nombre de tu imagen
}

PRECIOS_TAMANOS = {
    'Molde 18': "S/ 55-50", 'Molde 24': "S/ 85-80", 'Número 30': "S/ 140-135",
    '#20x30': "S/ 95-90", '25x35': "S/ 150", '30x40': "S/ 185-180"
}

VALORES_PRECIOS = {
    'Molde 18': 55, 'Molde 24': 85, 'Número 30': 140,
    '#20x30': 95, '25x35': 150, '30x40': 185
}

# Ruta para que Flask pueda leer la imagen desde tu carpeta
@app.route('/logo_aurelias.png')
def logo():
    return send_from_directory(os.getcwd(), 'logo_aurelias.png')

# --- DISEÑO CON COLORES DEL LOGO ---
HTML_PROFORMA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ info.nombre }}</title>
    <style>
        :root {
            --guinda: #5d1a24; /* El color de la tela */
            --rosa: #f2a2b1;   /* El color de las letras AURELIA'S */
            --dorado: #c4a457; /* El color de PASTELERÍA FINA */
        }
        body { font-family: 'Segoe UI', sans-serif; background: #fdf5f6; margin: 0; padding: 10px; }
        .card { max-width: 550px; margin: auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #eee; }
        
        .header { background: var(--guinda); text-align: center; padding: 30px 15px; }
        .logo-img { width: 100%; max-width: 450px; height: auto; border-radius: 10px; margin-bottom: 10px; }
        .header h1 { color: var(--rosa); margin: 0; font-size: 20px; text-transform: uppercase; letter-spacing: 1px; display: none; } /* Oculto porque ya está en el logo */
        
        section { padding: 20px; border-bottom: 1px solid #f9f9f9; }
        h3 { color: var(--guinda); font-size: 15px; text-transform: uppercase; margin-bottom: 15px; border-left: 5px solid var(--dorado); padding-left: 12px; }
        
        input, select, textarea { width: 100%; padding: 12px; margin-top: 5px; border: 1.5px solid #eee; border-radius: 10px; box-sizing: border-box; font-size: 14px; }
        input:focus { border-color: var(--dorado); outline: none; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .radio-group { display: flex; align-items: center; margin-bottom: 10px; font-size: 14px; color: #444; cursor: pointer; }
        .radio-group input { width: auto; margin-right: 12px; transform: scale(1.2); }
        
        .btn-ws { background: #25d366; color: white; border: none; width: 100%; padding: 20px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-ws:hover { background: #1eb954; }
        
        .btn-doble { background: var(--guinda); color: var(--dorado); text-decoration: none; display: block; text-align: center; padding: 12px; border: 2px solid var(--dorado); border-radius: 10px; margin: 15px 0; font-weight: bold; }
        
        .alert { background: #fff1f2; color: #be123c; padding: 12px; margin: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 13px; border: 1px solid #fda4af; }
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <i
            <img src="/static/logo_aurelias.png" alt="Logo Aurelia's" class="logo-img">

<img src="/static/logo_aurelias.png?v=1" alt="Logo Aurelia's" class="logo-img">
            <p style="color: white; font-size: 12px; margin: 0;">Av. Juan Lecaros N° 107 - Puente Piedra</p>
        </div>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}<div class="alert">⚠️ {{ message }}</div>{% endfor %}
          {% endif %}
        {% endwith %}

        <form action="/procesar" method="post">
            <section>
                <h3>👤 Datos del Cliente</h3>
                <input type="text" name="nombre" placeholder="Nombre completo" required>
                <div class="grid" style="margin-top:12px">
                    <input type="tel" name="telefono" placeholder="Número de celular" required>
                    <input type="text" value="Encargada: Aurelia's" readonly style="background:#f5f5f5; color:#888;">
                </div>
            </section>

            <section>
                <h3>🎂 Tipo de Pastel (Elija 1)</h3>
                <div class="grid">
                    <div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Tres Leches" required> Tres Leches</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Bizcochuelo"> Bizcochuelo</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Chocolate"> Chocolate</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Keke Inglés"> Keke Inglés</div>
                    </div>
                    <div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Red Velvet"> Red Velvet</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Arándano"> Arándano</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Zanahoria"> Zanahoria</div>
                        <div class="radio-group"><input type="radio" name="tipo" value="Chispas (+S/5)"> Chispas (+S/5)</div>
                    </div>
                </div>
            </section>

            <section>
                <h3>🍓 Rellenos (Máx 2)</h3>
                <div class="grid">
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Manjar Blanco"> Manjar Blanco</div>
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Vainilla"> Vainilla</div>
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Fudge"> Fudge</div>
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Merm. Fresa"> Merm. Fresa</div>
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Durazno"> Durazno</div>
                    <div class="radio-group"><input type="checkbox" name="relleno" value="Lúcuma"> Lúcuma</div>
                </div>
            </section>

            <section>
                <h3>📐 Tamaño y Cubierta</h3>
                <select name="tamano" required>
                    <option value="">Seleccione el tamaño...</option>
                    {% for t, p in precios.items() %}
                        <option value="{{ t }}">{{ t }} ({{ p }})</option>
                    {% endfor %}
                </select>
                <div class="grid" style="margin-top:15px">
                    <div class="radio-group"><input type="radio" name="cubierta" value="Chantilly" checked> Chantilly</div>
                    <div class="radio-group"><input type="radio" name="cubierta" value="Masa Elástica"> Masa Elástica</div>
                </div>
                <a href="https://wa.me/{{ info.telefono_proforma }}" class="btn-doble">🎀 TORTAS DE DOBLE ALTURA (WhatsApp)</a>
            </section>

            <section>
                <h3>⏰ Entrega</h3>
                <div class="grid">
                    <input type="date" name="fecha" required>
                    <input type="time" name="hora" required>
                </div>
                <textarea name="descripcion" placeholder="¿Algún detalle especial o nombre en la torta?" style="margin-top:12px"></textarea>
            </section>

            <button type="submit" class="btn-ws">CONFIRMAR PEDIDO VÍA WHATSAPP</button>
        </form>
    </div>
</body>
</html>
"""

# --- LÓGICA DE PROCESAMIENTO ---

@app.route('/')
def index():
    return render_template_string(HTML_PROFORMA, info=PASTELERIA_INFO, precios=PRECIOS_TAMANOS)

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.form
    rellenos = data.getlist('relleno')
    
    if len(rellenos) > 2:
        flash("Por favor, elige como máximo 2 rellenos.")
        return redirect(url_for('index'))

    try:
        entrega = datetime.strptime(f"{data['fecha']} {data['hora']}", "%Y-%m-%d %H:%M")
        ahora = datetime.now()
        if (entrega - ahora) < timedelta(hours=5):
            flash("Lo sentimos, no atendemos pedidos con menos de 5 horas de anticipación.")
            return redirect(url_for('index'))
    except:
        flash("Error en la fecha u hora.")
        return redirect(url_for('index'))

    precio_base = VALORES_PRECIOS.get(data['tamano'], 0)
    adicional = 0
    if data['cubierta'] == "Masa Elástica": adicional += 135
    if data['tipo'] == "Chispas (+S/5)": adicional += 5
    
    total = precio_base + adicional

    mensaje = (
        f"*NUEVO PEDIDO AURELIA'S*%0A"
        f"----------------------------%0A"
        f"*Cliente:* {data['nombre']}%0A"
        f"*Celular:* {data['telefono']}%0A"
        f"*Pastel:* {data['tipo']}%0A"
        f"*Rellenos:* {', '.join(rellenos)}%0A"
        f"*Cubierta:* {data['cubierta']}%0A"
        f"*Tamaño:* {data['tamano']}%0A"
        f"*Entrega:* {data['fecha']} a las {entrega.strftime('%I:%M %p')}%0A"
        f"*Detalles:* {data['descripcion']}%0A"
        f"----------------------------%0A"
        f"*TOTAL ESTIMADO:* S/ {total}.00%0A"
        f"----------------------------"
    )

    return redirect(f"https://wa.me/{PASTELERIA_INFO['telefono_ventas']}?text={mensaje}")

if __name__ == '__main__':
    app.run(debug=True)