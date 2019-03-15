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

from os       import path, mkdir, listdir, rename, rmdir
from datetime import datetime

from .functions import *
from .testxml   import TestXML

logger = logging.getLogger("sttb-logger")

class BuildsDB():

  def __init__(self, theConfig, dbConfig, archiveDir=None):

    self.theConfig = theConfig
    self.jobsDir   = self.theConfig.jobsDir
    self.archDir   = archiveDir
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
    for jobEntry in sorted(listdir(workDir)):
      jobEntryPath = path.join(workDir,jobEntry)
      if path.isdir(jobEntryPath) and len(jobEntry) == 40:
        logger.info("%s: Scanning entry '%s'" % (workerName,jobEntry))
        for jobFile in sorted(listdir(jobEntryPath)):
          jobFilePath = path.join(jobEntryPath,jobFile)
          if path.isfile(jobFilePath) and len(jobFile) == 42 and jobFile[:6] == "Build_":
            logger.info("%s: Found build file '%s'" % (workerName,jobFile))
            iStat = self._importBuildFile(workerName, jobFilePath, buildLog)
            if iStat and self.archDir is not None:
              archDir = path.join(self.archDir,jobEntry)
              if not path.isdir(archDir):
                mkdir(archDir)
              rename(jobFilePath, path.join(archDir,jobFile))
              logger.info("%s: Archived build file '%s'" % (workerName,jobFile))
          elif path.isfile(jobFilePath) and len(jobFile) == 41 and jobFile[:5] == "Test_":
            logger.info("%s: Found test file '%s'" % (workerName,jobFile))
            iStat = self._importTestFile(workerName, jobFilePath, testLog)
            if iStat and self.archDir is not None:
              archDir = path.join(self.archDir,jobEntry)
              if not path.isdir(archDir):
                mkdir(archDir)
              rename(jobFilePath, path.join(archDir,jobFile))
              logger.info("%s: Archived test file '%s'" % (workerName,jobFile))
          else:
            logger.debug("%s: Skipping file '%s'" % (workerName,jobFile))
        if len(listdir(jobEntryPath)) == 0:
          logger.info("Deleting empty folder %s" % jobEntry)
          rmdir(jobEntryPath)
      else:
        logger.info("%s: Skipping entry '%s'" % (workerName,jobEntry))

    return

  def _importBuildFile(self, workerName, buildFile, doSave=False):
    theData = {
      "JobName"         : None,
      "BuildName"       : None,
      "BuildCompiler"   : None,
      "BuildType"       : None,
      "BuildFlags"      : None,
      "CompilerVersion" : None,
      "GitRef"          : None,
      "GitHash"         : None,
      "GitTime"         : None,
      "GitMessage"      : None,
      "WorkerName"      : None,
      "WorkerHost"      : None,
      "WorkerOS"        : None,
      "WorkerArch"      : None,
      "KernelName"      : None,
      "KernelRelease"   : None,
      "KernelVersion"   : None,
      "BuildStart"      : None,
      "CMakeStatus"     : None,
      "MakeStatus"      : None,
      "BuildEnd"        : None,
      "TestStart"       : None,
      "TestStatus"      : None,
      "TestEnd"         : None,
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
        return self._dbWriteBuildData(workerName, theData)

    return True

  def _importTestFile(self, workerName, testFile, doSave=False):

    theTests  = TestXML(testFile)
    fileName  = path.basename(testFile)
    buildName = "Build_%s" % fileName[5:37]

    # Find the BuildID
    qSelect = "SELECT ID FROM builds WHERE Name = %s"
    self.dbCursor.execute(qSelect, (buildName,))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    theRes = self.dbCursor.fetchone()

    if theRes is None:
      logger.error("Unknown build name '%s'" % buildName)
      return False

    buildID = theRes["ID"]
    nT, nP, nF = theTests.getTestCount()
    qUpdate = "UPDATE builds SET TestCount = %s, TestPass = %s, TestFail = %s, TestNotRun = %s WHERE ID = %s"
    self.dbCursor.execute(qUpdate,(nT,nP,nF,nT-nP-nF,buildID))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    self.dbConn.commit()

    qDelete = "DELETE FROM tests WHERE BuildID = %s"
    self.dbCursor.execute(qDelete,(buildID,))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    self.dbConn.commit()

    for testName in theTests.testRes.keys():
      if theTests.testRes[testName]["Status"] == "passed":
        tStatus = 0
      elif theTests.testRes[testName]["Status"] == "failed":
        tStatus = 1
      else:
        tStatus = -1
      qInsert = ("INSERT INTO tests ("
          "Name, BuildID, Status, RunTime"
        ") VALUES ("
          "%s, %s, %s, %s"
        ")"
      )
      self.dbCursor.execute(qInsert,(testName, buildID, tStatus, theTests.testRes[testName]["RunTime"]))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
    self.dbConn.commit()

    return True

  def _dbWriteBuildData(self, workerName, theData):

    repoID = self._dbRepository(
      theData["GitHash"],
      theData["GitRef"],
      theData["GitTime"],
      theData["GitMessage"]
    )
    if repoID is None:
      logger.error("Failed to save repository information")
      return False
    else:
      logger.info("Saved Git Hash '%s' with RepoID %d" % (theData["GitHash"],repoID))

    workerID = self._dbWorker(
      theData["WorkerName"],
      theData["WorkerHost"],
      theData["WorkerOS"],
      theData["WorkerArch"],
      fromUnixTime(int(theData["BuildStart"]),1e9)
    )
    if workerID is None:
      logger.error("Failed to save worker information")
      return False
    else:
      logger.info("Saved Worker '%s' with WorkerID %d" % (theData["WorkerName"],workerID))

    buildID = self._dbBuilds(theData, repoID, workerID)
    if buildID is None:
      logger.error("Failed to save build information")
      return False
    else:
      logger.info("Saved Build '%s' with BuildID %d" % (theData["BuildName"],buildID))

    return True

  def _dbBuilds(self, theData, repoID, workerID):

    # Check the Values
    buildName = theData["BuildName"]
    if len(buildName) != 38:
      logger.error("Invalid build name '%s'" % buildName)
      return None

    # Check if the build is already saved
    qSelect = "SELECT ID FROM builds WHERE Name = %s"
    self.dbCursor.execute(qSelect, (buildName,))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    theRes = self.dbCursor.fetchone()

    startTime = fromUnixTime(int(theData["BuildStart"]),1e9)
    buildTime = int((int(theData["BuildEnd"])-int(theData["BuildStart"]))/1e6)
    if theData["TestEnd"] is None:
      finishTime = fromUnixTime(int(theData["BuildEnd"]),1e9)
      testTime   = 0
    else:
      finishTime = fromUnixTime(int(theData["TestEnd"]),1e9)
      testTime   = int((int(theData["TestEnd"])-int(theData["TestStart"]))/1e6)

    if theRes is None:
      qInsert = ("INSERT INTO builds ("
          "Name, RepoID, WorkerID, StartTime, FinishTime, "
          "Description, Compiler, CompilerVersion, Type, Flags, "
          "KernelRelease, KernelVersion, "
          "CMakeStatus, MakeStatus, TestStatus, "
          "BuildTime, TestTime, "
          "TestCount, TestPass, TestFail, TestNotRun"
        ") VALUES ("
          "%s, %s, %s, %s, %s, "
          "%s, %s, %s, %s, %s, "
          "%s, %s, "
          "%s, %s, %s, "
          "%s, %s, "
          "%s, %s, %s, %s"
        ")"
      )
      self.dbCursor.execute(qInsert,(
        buildName, repoID, workerID, startTime, finishTime,
        theData["JobName"],         theData["BuildCompiler"],
        theData["CompilerVersion"], theData["BuildType"],
        theData["BuildFlags"],      theData["KernelRelease"],
        theData["KernelVersion"],   theData["CMakeStatus"],
        theData["MakeStatus"],      theData["TestStatus"],
        buildTime, testTime,
        0,0,0,0
      ))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
      self.dbConn.commit()
      return self.dbCursor.lastrowid

    else:
      logger.info("Build '%s' already saved, overwriting" % buildName)
      qUpdate = ("UPDATE builds SET "
          "RepoID = %s, WorkerID = %s, StartTime = %s, FinishTime = %s, "
          "Description = %s, Compiler = %s, CompilerVersion = %s, Type = %s, Flags = %s, "
          "KernelRelease = %s, KernelVersion = %s, "
          "CMakeStatus = %s, MakeStatus = %s, TestStatus = %s, "
          "BuildTime = %s, TestTime = %s "
          "WHERE ID = %s"
      )
      self.dbCursor.execute(qUpdate,(
        repoID, workerID, startTime, finishTime,
        theData["JobName"],         theData["BuildCompiler"],
        theData["CompilerVersion"], theData["BuildType"],
        theData["BuildFlags"],      theData["KernelRelease"],
        theData["KernelVersion"],   theData["CMakeStatus"],
        theData["MakeStatus"],      theData["TestStatus"],
        buildTime, testTime, theRes["ID"]
      ))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
      self.dbConn.commit()
      return theRes["ID"]

  def _dbRepository(self, gitHash, gitRef, gitTime, gitMessage):

    # Check the Values
    if gitHash is None:
      logger.error("No git hash provided.")
      return None
    elif len(gitHash) != 40:
      logger.error("Invalid git hash provided '%s'." % gitHash)
      return None

    if len(gitTime) > 19:
      gitTime = gitTime[0:19]

    # Check if the hash is already saved
    qSelect = "SELECT ID FROM repository WHERE GitHash = %s"
    self.dbCursor.execute(qSelect, (gitHash,))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    theRes = self.dbCursor.fetchone()

    if theRes is None:
      qInsert = ("INSERT INTO repository ("
          "GitHash, GitRef, GitTime, GitMessage"
        ") VALUES ("
          "%s, %s, %s, %s"
        ")"
      )
      self.dbCursor.execute(qInsert,(gitHash, gitRef, gitTime, gitMessage))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
      self.dbConn.commit()
      return self.dbCursor.lastrowid

    else:
      return theRes["ID"]

  def _dbWorker(self, workerName, workerHost, workerOS, workerArch, lastSeen):

    # Check the Values
    if workerName is None or len(workerName) == 0:
      logger.error("No worker name provided.")
      return None

    qSelect = "SELECT * FROM workers WHERE Name = %s"
    self.dbCursor.execute(qSelect, (workerName,))
    logger.debug("SQL: %s" % self.dbCursor._last_executed)
    theRes = self.dbCursor.fetchone()

    if theRes is None:
      qInsert = ("INSERT INTO workers ("
          "Name, HostName, OS, Architecture, LastSeen"
        ") VALUES ("
          "%s, %s, %s, %s, %s"
        ")"
      )
      self.dbCursor.execute(qInsert,(workerName, workerHost, workerOS, workerArch, lastSeen))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
      self.dbConn.commit()
      return self.dbCursor.lastrowid

    else:
      if theRes["OS"] != workerOS:
        logger.error("OS for worker '%s' does not match the database '%s' != '%s'" % (
          workerName, workerOS, theRes["OS"]
        ))
        return None
      if theRes["Architecture"] != workerArch:
        logger.error("Architecture for worker '%s' does not match the database '%s' != '%s'" % (
          workerName, workerArch, theRes["Architecture"]
        ))
        return None
      qUpdate = "UPDATE workers SET LastSeen = %s WHERE ID = %s"
      self.dbCursor.execute(qUpdate,(lastSeen,theRes["ID"]))
      logger.debug("SQL: %s" % self.dbCursor._last_executed)
      self.dbConn.commit()

      return theRes["ID"]

# END Class BuildsDB
