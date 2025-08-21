from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_name='default'):
    """î(ÂÇ˝p"""
    app = Flask(__name__)
    
    # Mnî(
    from .config.config import config
    app.config.from_object(config[config_name])
    
    # ˙≈ÅÑÓU
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
    
    # MnÂ◊
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            os.path.join(app.config['LOG_FOLDER'], 'app.log'),
            maxBytes=10240000, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Image Search API startup')
    
    # Ëå›˛
    from .api.routes import api_bp
    app.register_blueprint(api_bp)
    
    # ˚†9Ô1
    @app.route('/')
    def index():
        return {
            'message': 'Image Search API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'search': '/api/search (POST)',
                'search_by_url': '/api/search/url (POST)'
            }
        }
    
    return app