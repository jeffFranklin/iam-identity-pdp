"""
Logging configuration to be consumed in settings by the LOGGING attribute.
"""
import os

HANDLERS = ('debuglog', 'audit')
LOGGERS = ('django.request', 'pdp', 'resttools', 'idbase', 'audit')

is_file_logging = os.environ.get('DJANGO_FILE_LOGGING', False)

handlers = {}
for handler in HANDLERS:
    conf = {'level': 'DEBUG',
            'formatter': 'less_verbose' if handler == 'audit' else 'verbose'}
    if not is_file_logging:
        conf.update({'class': 'logging.StreamHandler',
                     'stream': 'ext://sys.stdout'})
    else:
        filename = 'process' if handler != 'audit' else 'audit'
        conf.update({
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/logs/pdp/{}.log'.format(filename),
            'when': 'midnight'})
    handlers[handler] = conf


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s %(levelname)s '
                       '%(module)s.%(funcName)s():%(lineno)d: '
                       '%(message)s')
        },
        'less_verbose': {
            'format': ('%(asctime)s %(levelname)s '
                       '%(message)s')
        },
    },
    'handlers': handlers,
    'loggers': {
        logger: {
            'handlers': ['debuglog' if logger != 'audit' else 'audit'],
            'level': 'DEBUG',
            'propagate': True,
        }
        for logger in LOGGERS}
}
