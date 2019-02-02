# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from os         import path
from time       import time
from hashlib    import md5

from .compilers import Compilers

logger = logging.getLogger("sttb-logger")

class Worker():

  def __init__(self, theConfig, workerName):

    self.theConfig    = theConfig
    self.workerName   = workerName
    self.theCompilers = Compilers(self.theConfig)
    self.theJobs      = []
    self.gitHash      = None

    self.addCompiler  = self.theCompilers.addCompiler

    return

  def setCurrentHash(self, gitHash):
    self.gitHash = gitHash.strip()
    logger.info("Current git hash is: %s" % self.gitHash)
    return

  def addJob(self, jobName, buildCompiler, buildType, buildFlags, testFlags=None):
    if self.theCompilers.checkCompiler(buildCompiler) == False:
      logger.warning("Skipping job with compiler %s for flags %s" % (jobCompiler, jobFlags))
      return
    if buildType not in ["Release","Debug"]:
      logger.warning("Skipping job with unknown build type %s for flags %s" % (buildType, jobFlags))
      return
    theJob = BuildJob(self.theConfig, jobName, buildCompiler, buildType, buildFlags, testFlags)
    self.theJobs.append(theJob)
    return

  def addTest(self, testFlags, jobFlags, withCompilers=[], buildTypes=["Release"]):
    for jobCompiler in withCompilers:
      for buildType in buildTypes:
        for aJob in self.theJobs:
          if aJob.checkKey(jobFlags, jobCompiler, buildType):
            aJob.setTest(testFlags)
            continue
    return

  def writeJobFiles(self):
    jobNo = 0
    for aJob in self.theJobs:
      jobNo += 1
      aJob.writeJobFile(jobNo)
    return

# END Class JobsWrapper

class BuildJob():

  def __init__(self, theConfig, jobName, buildCompiler, buildType, buildFlags, testFlags):

    self.jobName       = jobName.strip()
    self.buildCompiler = buildCompiler
    self.buildType     = buildType
    self.buildFlags    = buildFlags.split()
    self.testFlags     = testFlags

    self.gitHash       = theConfig.gitHash

    self.buildOpt    = self._makeOptString(self.buildFlags, self.buildCompiler, self.buildType)
    self.buildKey    = self._makeKey(self.buildOpt)
    self.buildName   = "Build_"+self.buildKey

    if self.testFlags is None:
      logger.info("Added build job '%s'" % self.buildOpt)
    else:
      logger.info("Added build job '%s' with test '%s'" % (self.buildOpt,self.testFlags))


    return

  def setTest(self, testFlags):
    self.testFlags = testFlags.strip()
    self.jobFlags.append("BUILD_TESTING")
    self.buildOpt  = self._makeOptString(self.jobFlags, self.jobCompiler, self.buildType)
    self.buildKey  = self._makeKey(self.buildOpt)
    self.buildName = "Build_"+self.buildKey
    logger.info("Added tests '%s' for job '%s'" % (self.testFlags,self.buildOpt))
    return

  def writeJobFile(self, jobNo):

    bldPath = path.join(self.buildPath, self.buildName)
    shName  = "Build_%04d_%s.sh" % (jobNo, self.buildKey)
    shPath  = path.join(self.jobPath, shName)
    with open(shPath, mode="w+") as shFile:
      shFile.write("#!/bin/bash\n")
      shFile.write("mkdir %s\n" % bldPath)
      shFile.write("cd %s\n" % bldPath)
      shFile.write("cmake %s %s\n" % (self.sourcePath, self._assembleCMakeFlags()))
      shFile.write("make -j%d\n" % self.buildCores)

    if self.testFlags is None:
      return

    shName = "Test_%04d_%s.sh" % (jobNo, self.buildKey)
    shPath = path.join(self.jobPath, shName)
    with open(shPath, mode="w+") as shFile:
      shFile.write("#!/bin/bash\n")
      shFile.write("cd %s\n" % bldPath)
      shFile.write("ctest %s -j%d\n" % (self.testFlags, self.testCores))

    return

  def checkKey(self, jobFlags, jobCompiler, buildType):
    tmpOpt = self._makeOptString(jobFlags.split(), jobCompiler, buildType)
    tmpKey = self._makeKey(tmpOpt)
    return tmpKey == self.buildKey

  def _makeOptString(self, jobFlags, compExec, buildType):
    return ("%s %s %s" % (compExec, buildType.strip(), " ".join(jobFlags))).strip()

  def _makeKey(self, optString):
    return md5((self.gitHash+"_"+optString).encode("utf-8")).hexdigest()

  def _assembleCMakeFlags(self):
    theFlags  = "-G \"Unix Makefiles\""
    theFlags += "-DCMAKE_Fortran_COMPILER=%s " % self.jobCompiler
    theFlags += "-DCMAKE_BUILD_TYPE=%s "       % self.buildType
    for jobFlag in self.jobFlags:
      if jobFlag == "": continue
      if jobFlag[0] == "-":
        theFlags += "-D%s=OFF " % jobFlag[1:]
      else:
        theFlags += "-D%s=ON " % jobFlag
    return theFlags

# END Class BuildJob
