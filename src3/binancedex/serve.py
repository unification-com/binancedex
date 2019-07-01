import os
from logging.config import dictConfig
from pathlib import Path

from flask import Flask, json
from jinja2 import FileSystemLoader, Environment

from binancedex.stats import trade_groups_for_address
from binancedex.utils import reports_store

app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': 'binancedex.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'stdout': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'stdout']
    }
})


@app.route('/trader/<bnb_address>')
def trader(bnb_address):
    current_script = Path(os.path.abspath(__file__))
    source = current_script.parent / 'templates'

    loader = FileSystemLoader(str(source))
    environment = Environment(loader=loader)

    template = environment.get_template('trades.html')
    context = trade_groups_for_address(bnb_address)
    ret = template.render(context)

    return ret, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
