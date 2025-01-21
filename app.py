from flask import Flask, render_template

from api.config import config
from api.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    
    from api.models import db
    db.init_app(app)

    from api.schemas import ma
    ma.init_app(ma)

    app.register_blueprint(routes)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

