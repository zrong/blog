import os
import sys
import logging
import importlib
from zrong.base import slog, addLoggerHandler
from hhlb import base, config

def _build(name, conf, args, parser):
    pack = importlib.import_module("hhlb."+name)
    pack.build(conf, args, parser)

addLoggerHandler(slog, 
        handler=logging.StreamHandler(sys.stdout),
        debug=logging.DEBUG)
gconf = base.Conf()
workDir = os.path.split(os.path.abspath(__file__))[0]
confFile = os.path.join(workDir, "build_conf.py")
confFileTempl = os.path.join(workDir, "build.conf")
workDir = os.path.abspath(os.path.join(workDir, os.pardir))
if os.path.exists(confFile):
    gconf.readFromFile(confFile)
else:
    gconf.init(workDir, confFileTempl, confFile)
if not config.checkEnv(gconf):
    exit(1)

gargs, subParser = config.checkArgs()
if gargs:
    _build(gargs.sub_name, gconf, gargs, subParser)

