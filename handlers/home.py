import flask

blueprint = flask.Blueprint("home", __name__)

@blueprint.route("/")
def loadHomePage():
    """Loads a home page onto the main."""


    return flask.render_template('base.tmpl')
