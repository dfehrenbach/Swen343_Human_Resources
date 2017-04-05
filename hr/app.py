"""Run of the HR application """
import connexion
from flask import send_file
# from flask_cors import CORS

# Create connexion app and add the HR API
app = connexion.App(
    __name__,
    specification_dir='./specs/'
)
app.add_api(
    'swagger.yaml',
    arguments={'title': 'HR API'}
)
'''
# Configure cross origin request sources.
CORS(
    app.app,
    resources={
        r"/*": {
            "origins": CONFIG.frontend['allowed_hosts']
        }
    }
)
'''
# Expose application var for WSGI support
application = app.app


@app.route('/')
def index():
    return send_file('html/index.html')
@app.route('/view')
def view():
    return send_file('templates/viewemployees.html')
@app.route('/add')
def add():
    return send_file('templates/addemployee.html')
@app.route('/edit')
def edit():
    return send_file('templates/editemployee.html')
@app.route('/delete')
def delete():
    return send_file('templates/deleteemployee.html')

if __name__ == '__main__':
    app.run(
        port=8080,
        debug=True
    )
