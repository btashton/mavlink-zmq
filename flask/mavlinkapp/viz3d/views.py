from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from mavlinkapp import db

mod = Blueprint('viz3d', __name__, template_folder='templates', url_prefix='/3d')

@mod.route('/')
def index():
    return render_template("3d.html")
