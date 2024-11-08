from flask import Flask, render_template
from flask_login import LoginManager
from .db import db
from .config import get_config
from .controllers.etl_controller import run_etl_pipeline,save_to_db
from .models.user import User
from .routes import dashboard_bp
from flask_migrate import Migrate

migrate = Migrate()
app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirects to login if unauthenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    
    
    app.config.from_object(get_config())

    app.secret_key = "SECRET KEY"
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_bp)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/run-etl')
    def run_etl():
        combined_data,etl_status = run_etl_pipeline()
        save_to_db(combined_data)  
        data = {
            "columns": combined_data.columns.tolist(),
            "data": combined_data.values.tolist()
        }
        return render_template('etl_result.html', data_preview=data,etl_status=etl_status)
    
    return app
