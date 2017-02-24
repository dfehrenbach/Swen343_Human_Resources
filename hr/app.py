'''Run of the HR application '''
import connexion
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

if __name__ == '__main__':
    app.run(
        port=8080,
        debug=True
    )
