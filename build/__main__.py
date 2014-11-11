import os
import sys
import logging
import importlib
from zrong.base import slog, addLoggerHandler
import base

def _build(name, conf, args, parser):
    pack = importlib.import_module(name)
    pack.build(conf, args, parser)

addLoggerHandler(slog,
    handler=logging.StreamHandler(sys.stdout),
    debug=logging.DEBUG)
gconf = base.Conf()
workDir = os.path.abspath(
    os.path.join(os.path.split(
    os.path.abspath(__file__))[0], os.pardir))
confFile = os.path.join(workDir, "build.conf.py")
if os.path.exists(confFile):
    gconf.readFromFile(confFile)
else:
    gconf.init(workDir, confFile)
    slog.info('Please modify build.conf.py!')
    exit(1)

gargs, subParser = base.check_args()
if gargs:
    _build(gargs.sub_name, gconf, gargs, subParser)
