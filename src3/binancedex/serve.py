from logging.config import dictConfig

from flask import Flask, json

from binancedex.cli import process_trades

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


@app.route('/traders')
def traders():
    d = process_trades()
    data = json.dumps(d, indent=2, separators=(',', ':'))
    return data, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
