"""Web-based Remote Script Runner."""

from flask import Flask, render_template, request, jsonify
from auth import AuthManager
from ssh_manager import SSHManager
from salt_manager import SaltManager
from config import SYSTEMS

app = Flask(__name__)
auth_manager = AuthManager()
ssh_manager = SSHManager(username="", key_path="")  # Set proper credentials
salt_manager = SaltManager()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if auth_manager.validate_credentials(username, password):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', systems=SYSTEMS)

@app.route('/execute', methods=['POST'])
def execute_script():
    data = request.get_json()
    system_label = data.get('system')
    script_path = data.get('script_path')
    
    try:
        if system_label == "All Systems":
            output, error = salt_manager.execute_script(script_path)
        else:
            system = SYSTEMS[system_label]
            if not system:
                raise ValueError(f"Invalid system: {system_label}")
            
            ssh_manager.connect(system)
            output, error = ssh_manager.execute_script(script_path)
        
        return jsonify({
            'success': True,
            'output': output,
            'error': error
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)