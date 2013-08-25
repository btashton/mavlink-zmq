from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from mavlinkapp.frontend.views import mod as frontendModule
from mavlinkapp.graph.views import mod as graphModule
from mavlinkapp.raw.views import mod as rawModule
from mavlinkapp.viz3d.views import mod as viz3dModule
from mavlinkapp.socket_io.views import mod as socketioModule

app.register_blueprint(frontendModule)
app.register_blueprint(graphModule)
app.register_blueprint(rawModule)
app.register_blueprint(viz3dModule)
app.register_blueprint(socketioModule)
