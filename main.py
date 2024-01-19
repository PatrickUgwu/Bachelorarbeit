from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
socketio = SocketIO(app)

# Dictionary zum Speichern der Benutzer und ihrer Texte
user_texts = {}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('text_input')
def handle_text_input(data):
    user_id = request.sid  # Benutzer anhand der Socket.IO-Sitzungs-ID identifizieren
    text = data['text']

    # Text des Benutzers speichern
    user_texts[user_id] = text

    # Aktualisierten Text an alle anderen Benutzer senden
    emit('update_editor', {'text': text, 'user': user_id}, broadcast=True, include_self=False)

    # Aktuelle Texte aller Benutzer senden
    emit('update_texts', user_texts, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

