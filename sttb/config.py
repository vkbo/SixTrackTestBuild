# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging
import json

from os       import path
from datetime import datetime

logger = logging.getLogger("tbsixtrack")

class Config():

  def __init__(self, confFile):

    if not path.isfile(confFile):
      raise FileNotFoundError("Missing file: %s" % confFile)

    with open(confFile) as inFile:
      confData = json.load(inFile)

    self.logPath    = confData["logpath"]
    self.logLevel   = confData["loglevel"].upper()
    self.jobPath    = confData["jobpath"]
    self.sourcePath = confData["sourcepath"]
    self.buildPath  = confData["buildpath"]
    self.resultPath = confData["resultpath"]
    self.buildCores = int(confData["buildcores"])
    self.testCores  = int(confData["testcores"])

    self.logFile    = path.join(self.logPath, "testBuildSixTrack-"+datetime.now().strftime("%Y-%m")+".log")

    return

  def setupLogger(self):

    lvlMap = {
      "CRITICAL" : logging.CRITICAL, # 50
      "ERROR"    : logging.ERROR,    # 40
      "WARNING"  : logging.WARNING,  # 30
      "INFO"     : logging.INFO,     # 20
      "DEBUG"    : logging.DEBUG,    # 10
      "NOTSET"   : logging.NOTSET,   # 0
    }
    invMap = dict(zip(lvlMap.values(), lvlMap.keys()))
    if self.logLevel in lvlMap.keys():
      logLevel = lvlMap[self.logLevel]
    else:
      raise RuntimeError("Could not parse loglevel in config.")

    logFormat = logging.Formatter(
      fmt     = "[{asctime:}] {levelname:8}  {message}",
      datefmt = "%Y-%m-%d %H:%M:%S",
      style   = "{"
    )
    logger.handlers = []

    fHandle = logging.FileHandler(self.logFile)
    fHandle.setFormatter(logFormat)
    fHandle.setLevel(logLevel)
    logger.addHandler(fHandle)

    sHandle = logging.StreamHandler()
    sHandle.setFormatter(logFormat)
    sHandle.setLevel(logLevel)
    logger.addHandler(sHandle)

    logger.setLevel(logLevel)

    return

# END Class Config
