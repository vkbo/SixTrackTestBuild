# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - Database Class
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging
import pymysql.cursors

from os import path, mkdir, listdir

from .functions import *

logger = logging.getLogger("sttb-logger")

class BuildsDB():

  def __init__(self, theConfig, dbConfig, archiveDir=None):

    self.theConfig = theConfig
    self.jobsDir   = self.theConfig.jobsDir
    self.dbConfig  = dbConfig
    self.dbConn    = None
    self.dbCursor  = None
    try:
      self.dbConn = pymysql.connect(**self.dbConfig, cursorclass=pymysql.cursors.DictCursor)
    except Exception:
      endExec("Could not connect to MySQL database on host '%s'" % self.dbConfig["host"])
    else:
      logger.info("Connect to MySQL database on host '%s'" % self.dbConfig["host"])
      self.dbCursor = self.dbConn.cursor()

    if archiveDir is not None:
      if not path.isdir(archiveDir):
        endExec("Archive folder not found.")

    return

  def importResults(self, workerName, buildLog=False, testLog=False):

    workDir = path.join(self.jobsDir,workerName)
    logger.info("%s: Scanning jobs directory" % workerName)
    for jobEntry in listdir(workDir):
      jobEntryPath = path.join(workDir,jobEntry)
      if path.isdir(jobEntryPath) and len(jobEntry) == 40:
        logger.info("%s: Scanning entry '%s'" % (workerName,jobEntry))
        for jobFile in listdir(jobEntryPath):
          jobFilePath = path.join(jobEntryPath,jobFile)
          if path.isfile(jobFilePath) and len(jobFile) == 42 and jobFile[:6] == "Build_":
            logger.info("%s: Found build file '%s'" % (workerName,jobFile))
            self._importBuildFile(workerName, jobFilePath, buildLog)
          else:
            logger.debug("%s: Skipping file '%s'" % (workerName,jobFile))
      else:
        logger.info("%s: Skipping entry '%s'" % (workerName,jobEntry))

    return

  def _importBuildFile(self, workerName, buildFile, doSave=False):
    theData = {
      "BuildName"       : "Unknown",
      "BuildCompiler"   : "Unknown",
      "BuildType"       : "Unknown",
      "BuildFlags"      : "Unknown",
      "CompilerVersion" : "Unknown",
      "GitRef"          : "Unknown",
      "GitHash"         : "Unknown",
      "GitTime"         : "Unknown",
      "GitMessage"      : "Unknown",
      "WorkerName"      : "Unknown",
      "WorkerHost"      : "Unknown",
      "WorkerOS"        : "Unknown",
      "WorkerArch"      : "Unknown",
      "KernelName"      : "Unknown",
      "KernelRelease"   : "Unknown",
      "KernelVersion"   : "Unknown",
      "BuildStart"      : "0",
      "CMakeStatus"     : "-1",
      "MakeStatus"      : "-1",
      "BuildEnd"        : "0",
      "TestStart"       : "0",
      "TestStatus"      : "-1",
      "TestEnd"         : "0",
    }
    fileName = path.basename(buildFile)
    logger.info("%s: Importing file '%s'" % (workerName, fileName))
    with open(buildFile, "r") as inFile:
      inLines = [inLine.strip() for inLine in inFile]
      nLines  = len(inLines)
      if nLines == 0:
        logger.error("%s: File '%s' is truncated" % (workerName, fileName))
        return False
      if not inLines[0] == "## BEGIN BuildLog":
        logger.error("%s: File '%s' is not a build log file" % (workerName, fileName))
        return False
      if not inLines[-1] == "## END BuildLog":
        logger.error("%s: File '%s' is not finished" % (workerName, fileName))
        return False
      for inLine in inLines[1:-1]:
        if len(inLine) < 20:
          logger.warning("%s: Invalid line '%s'" % (workerName, inLine))
          continue
        lnName = inLine[2:18].strip()
        lnVal  = inLine[19:].strip()
        if lnName in theData.keys():
          theData[lnName] = lnVal
        else:
          logger.warning("%s: Unknown variable '%s'" % (workerName, lnName))
      if doSave:
        self._dbWriteBuildData(workerName, theData)

    return True

  def _dbWriteBuildData(self, workerName, theData):
    return True

# END Class BuildsDB
