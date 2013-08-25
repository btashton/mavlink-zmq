from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from mavlinkapp import db

mod = Blueprint('raw', __name__, template_folder='templates', url_prefix='/raw')

@mod.route('/')
def index():
    return render_template("raw.html")
