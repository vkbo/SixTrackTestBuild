# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from os      import path
from time    import time
from hashlib import md5

logger = logging.getLogger("tbsixtrack")

class JobsWrapper():

  def __init__(self, theConfig, theCompilers):

    self.theConfig    = theConfig
    self.theCompilers = theCompilers
    self.theJobs      = []

    self.gitHash      = None

    return

  def setCurrentHash(self, gitHash):
    self.gitHash = gitHash.strip()
    logger.info("Current git hash is: %s" % self.gitHash)
    return

  def addJob(self, jobName, jobFlags, withCompilers=[], buildTypes=["Release"]):
    if self.gitHash is None:
      raise ValueError("No git hash set in JobsWrapper")
    for jobCompiler in withCompilers:
      if self.theCompilers.checkCompiler(jobCompiler) == False:
        logger.warning("Skipping job with compiler %s for flags %s" % (jobCompiler, jobFlags))
        continue
      for buildType in buildTypes:
        if buildType not in ["Release","Debug"]:
          logger.warning("Skipping job with build type %s for flags %s" % (buildType, jobFlags))
          continue
        theJob = BuildJob(self.theConfig, self.gitHash, jobName, jobFlags, jobCompiler, buildType)
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

  def __init__(self, theConfig, gitHash, jobName, jobFlags, jobCompiler, buildType="Release"):

    self.jobPath     = theConfig.jobPath
    self.buildPath   = theConfig.buildPath
    self.sourcePath  = theConfig.sourcePath
    self.buildCores  = theConfig.buildCores
    self.testCores   = theConfig.testCores

    self.gitHash     = gitHash
    self.jobName     = jobName.strip()
    self.jobFlags    = jobFlags.split()
    self.jobCompiler = jobCompiler
    self.buildType   = buildType
    self.testFlags   = None

    self.buildOpt    = self._makeOptString(self.jobFlags, jobCompiler, buildType)
    self.buildKey    = self._makeKey(self.buildOpt)
    self.buildName   = "Build_"+self.buildKey

    logger.info("Added build job '%s'" % self.buildOpt)

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
    return ("%s %s %s" % (compExec, buildType.strip().lower(), " ".join(jobFlags))).strip()

  def _makeKey(self, optString):
    return md5((self.gitHash+"_"+optString).encode("utf-8")).hexdigest()

  def _assembleCMakeFlags(self):
    theFlags  = "-DCMAKE_Fortran_COMPILER=%s " % self.jobCompiler
    theFlags += "-DCMAKE_BUILD_TYPE=%s "       % self.buildType
    for jobFlag in self.jobFlags:
      if jobFlag == "": continue
      if jobFlag[0] == "-":
        theFlags += "-D%s=OFF " % jobFlag[1:]
      else:
        theFlags += "-D%s=ON " % jobFlag
    return theFlags

# END Class BuildJob
