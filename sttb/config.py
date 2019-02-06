# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from os       import path, mkdir, system, chdir, getcwd
from datetime import datetime

from .functions import *

logger = logging.getLogger("sttb-logger")

class Config():

  def __init__(self, workDir, jobsDir, logLevel="INFO"):

    if not path.isdir(workDir):
      raise FileNotFoundError("Missing folder: %s" % workDir)

    if not path.isdir(jobsDir):
      raise FileNotFoundError("Missing folder: %s" % jobsDir)
    else:
      self.jobsDir = jobsDir

    self.gitMode   = None
    self.gitTarget = None
    self.gitHash   = None
    self.gitTime   = None
    self.gitRef    = None
    self.gitMsg    = ""

    self.repoPath  = path.join(workDir, "repo")
    self.logPath   = path.join(workDir, "logs")
    self.logLevel  = logLevel.upper()
    self.logFile   = path.join(self.logPath, "SixTrackBuildTest-"+datetime.now().strftime("%Y-%m")+".log")

    if not path.isdir(self.logPath):  mkdir(self.logPath)
    if not path.isdir(self.repoPath): mkdir(self.repoPath)

    self._setupLogger()

    return

  def gitCheckout(self, theArgs):

    if len(theArgs) < 3:
      endExec("Not enough input arguments")
    if theArgs[1] in ("branch","pr","merge","tag"):
      self.gitMode   = theArgs[1]
      self.gitTarget = theArgs[2]
      if len(theArgs) > 3:
        self.gitHash = theArgs[3]
    else:
      endExec("First argument must be either 'branch', 'pr', 'merge' or 'tag'")

    mirrorPath = path.join(self.repoPath,"SixTrack.git")
    workingDir = getcwd()
    chdir(self.repoPath)
    if path.isdir(mirrorPath):
      chdir(mirrorPath)
      logger.info("Updating the SixTrack repository ...")
      stdOut, stdErr, exCode = sysCall("git remote update")
    else:
      logger.info("Cloning the SixTrack repository")
      exCode = system("git clone https://github.com/SixTrack/SixTrack.git --mirror")
      if exCode != 0:
        endExec("Failed to clone SixTrack repository")
      chdir(mirrorPath)

    if self.gitMode == "branch":
      self.gitRef = "refs/heads/%s" % self.gitTarget
    elif self.gitMode == "pr":
      self.gitRef = "refs/pull/%s/head" % self.gitTarget
    elif self.gitMode == "merge":
      self.gitRef = "refs/pull/%s/merge" % self.gitTarget
    elif self.gitMode == "tag":
      self.gitRef = "refs/tags/%s" % self.gitTarget

    stdOut, stdErr, exCode = sysCall("git show-ref %s" % self.gitRef)
    if exCode == 0:
      logger.info("Found: %s" % stdOut.strip())
      self.gitHash = stdOut[0:40]
    else:
      endExec("Unknown ref '%s'" % self.gitRef)
      return

    stdOut, stdErr, exCode = sysCall("git show -s --format=%%ci %s" % self.gitHash)
    self.gitTime = stdOut.strip()
    logger.info("TIME: '%s'" % self.gitTime)

    stdOut, stdErr, exCode = sysCall("git log --format=%%B -n 1 %s | head -n1" % self.gitHash)
    self.gitMsg = stdOut.strip()
    logger.info("MSG:  '%s'" % self.gitMsg)

    chdir(workingDir)

    return

  def _setupLogger(self):

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
      endExec("Could not parse loglevel in config.")

    logger.handlers = []

    logFormat = logging.Formatter(
      fmt     = "[{asctime:}] {levelname:8}  {message}",
      datefmt = "%Y-%m-%d %H:%M:%S",
      style   = "{"
    )
    fHandle = logging.FileHandler(self.logFile)
    fHandle.setFormatter(logFormat)
    fHandle.setLevel(logLevel)
    logger.addHandler(fHandle)

    logFormat = logging.Formatter(
      fmt     = "{levelname:8}  {message}",
      style   = "{"
    )
    sHandle = logging.StreamHandler()
    sHandle.setFormatter(logFormat)
    sHandle.setLevel(logLevel)
    logger.addHandler(sHandle)

    logger.setLevel(logLevel)

    logger.debug("Logger initialised")

    return

# END Class Config
