from flask import Flask
from .. import config

app = Flask(__name__)
app.config.from_object(config)

try:
    from flask_compress import Compress
    Compress(app)
except ImportError:
    pass

from . import streak

# Register tasks admin blueprint (simple UI for creating/editing YAML tasks)
try:
    from .tasks_admin import bp as tasks_admin_bp
    app.register_blueprint(tasks_admin_bp)
except Exception:
    # If import fails (e.g. before the file exists), ignore so app still runs
    pass
