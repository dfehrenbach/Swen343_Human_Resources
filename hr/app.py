"""Run of the HR application """
import connexion
from flask import send_file

import logging

# from flask_cors import CORS

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

# Create connexion app and add the HR API
app = connexion.App(
    __name__,
    specification_dir='./specs/'
)
logger.info("Adding API")
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



@app.route('/oauth')
def oauth():
    return send_file('html/oauth.html')
@app.route('/')
@app.route('/view')
def view():
    return send_file('html/viewemployees.html')
@app.route('/add')
def add():
    return send_file('html/addemployee.html')
@app.route('/edit/<int:eId>')
def edit(eId=-1):
    return send_file('html/editemployee.html')
@app.route('/viewrewards')
def rewards():
    return send_file('html/rewards.html')

if __name__ == '__main__':
    logger.warning('App starting up.')
    app.run(
        port=80,
        debug=True
    )
