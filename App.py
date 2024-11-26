from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth
import os
import csv
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de OAuth
oauth = OAuth(app)

# Cargar credenciales desde el archivo JSON generado por Google
with open('credentials.json') as f:
    credentials = json.load(f)

google = oauth.remote_app(
    'google',
    consumer_key=credentials['web']['client_id'],  # CLIENT_ID desde el archivo JSON
    consumer_secret=credentials['web']['client_secret'],  # CLIENT_SECRET desde el archivo JSON
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Archivo CSV donde se guardarán los correos
CSV_FILE = 'records.csv'

def save_to_csv(email):
    """Guardar el correo en un archivo CSV"""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Email'])  # Encabezado del CSV
        writer.writerow([email])  # Agregar el correo

@app.route('/')
def index():
    """Página inicial: Redirigir al login de Google"""
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Iniciar el flujo de autenticación"""
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/callback')
def authorized():
    """Callback después de la autenticación"""
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Acceso denegado: Razón={} Error={}'.format(
            session.get('error_reason', 'Unknown'),
            session.get('error_description', 'Unknown')
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')  # Obtener información del usuario
    email = user_info.data['email']  # Extraer el correo del usuario

    # Guardar el correo en el CSV
    save_to_csv(email)

    # Redirigir al formulario de Google
    return redirect('https://minciencia.gob.cl/uploads/filer_public/f5/fc/f5fc81c1-a990-4eec-87be-f3b43108beeb/informe_ii-comision_contra_la_desinformacion-04-12-23.pdf')

@google.tokengetter
def get_google_oauth_token():
    """Obtener el token de acceso almacenado en sesión"""
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)
