
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Base de datos simulada
motos_registradas = {}

registro_html = """
<!DOCTYPE html>
<html>
<head><title>Registro - Nomads Tag</title></head>
<body style="font-family:sans-serif; text-align:center; background-color:#f4f4f4;">
    <h1 style="color:#222;">Nomads Tag™</h1>
    <h2>Registrar Motocicleta</h2>
    <form method="post">
        <input type="text" name="tag_id" placeholder="Tag ID" required><br><br>
        <input type="text" name="make" placeholder="Marca (ej. Yamaha)" required><br><br>
        <input type="text" name="model" placeholder="Modelo (ej. MT-07)" required><br><br>
        <input type="submit" value="Registrar">
    </form>
</body>
</html>
"""

estado_html = """
<!DOCTYPE html>
<html>
<head><title>Estado - Nomads Tag</title></head>
<body style="font-family:sans-serif; text-align:center; background-color:#fff;">
    <h1>Nomads Tag™</h1>
    <h2>Motocicleta: {{ make }} {{ model }}</h2>
    <h3>Estado: {% if stolen %}⚠️ ROBADA {% else %}No reportada como robada{% endif %}</h3>
    {% if not stolen %}
    <form method="post">
        <input type="submit" name="report" value="Reportar como Robada">
    </form>
    {% endif %}
</body>
</html>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        tag_id = request.form['tag_id']
        make = request.form['make']
        model = request.form['model']
        motos_registradas[tag_id] = {'make': make, 'model': model, 'stolen': False}
        return redirect(url_for('status', tag_id=tag_id))
    return render_template_string(registro_html)

@app.route('/status/<tag_id>', methods=['GET', 'POST'])
def status(tag_id):
    moto = motos_registradas.get(tag_id)
    if not moto:
        return "Tag no encontrado.", 404
    if request.method == 'POST' and 'report' in request.form:
        moto['stolen'] = True
    return render_template_string(estado_html, make=moto['make'], model=moto['model'], stolen=moto['stolen'])

if __name__ == '__main__':
    app.run(debug=True)
