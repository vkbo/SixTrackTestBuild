# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - Worker and BuildJob Classes
 ====================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from os         import path, mkdir
from time       import time
from hashlib    import md5

from .functions import *
from .compilers import Compilers

logger = logging.getLogger("sttb-logger")

class Worker():

  def __init__(self, theConfig, workerName):

    self.theConfig    = theConfig
    self.workerName   = workerName.strip()
    self.theCompilers = Compilers(self.theConfig)
    self.theJobs      = []
    self.libDepend    = []

    self.gitHash      = theConfig.gitHash
    self.gitRef       = theConfig.gitRef
    self.jobsDir      = theConfig.jobsDir

    self.addCompiler  = self.theCompilers.addCompiler

    return

  def setCurrentHash(self, gitHash):
    self.gitHash = gitHash.strip()
    logger.info("Current git hash is: %s" % self.gitHash)
    return

  def setLibDependencies(self, libDepend):
    self.libDepend = libDepend
    logger.info("Libraries: %s" % " ".join(libDepend))
    return

  def addJob(self, jobName, buildCompiler, buildType, buildFlags, testFlags=None):
    if self.theCompilers.checkCompiler(buildCompiler) == False:
      logger.warning("Skipping job with compiler %s for flags %s" % (buildCompiler, buildFlags))
      return
    if buildType not in ["Release","Debug"]:
      logger.warning("Skipping job with unknown build type %s for flags %s" % (buildType, buildFlags))
      return
    cVersion = self.theCompilers.getVersion(buildCompiler)
    theJob   = BuildJob(self.theConfig, self.workerName, jobName, buildCompiler, cVersion, buildType, buildFlags, testFlags)
    self.theJobs.append(theJob)
    return

  def writeJobFiles(self):

    workDir = path.join(self.jobsDir,self.workerName,self.gitHash)
    if not path.isdir(workDir):
      mkdir(workDir)

    jobNo = 1

    shName = "Step_%04d_Checkout.sh" % jobNo
    shPath = path.join(workDir, shName)
    with open(shPath, mode="w+") as shFile:
      shFile.write("#!/bin/bash\n")
      shFile.write("cd $STTB_REPO\n")
      shFile.write("git remote update\n")
      shFile.write("if [ ! -d \"$STTB_WDIR/%s\" ]; then\n" % self.gitHash)
      shFile.write("  mkdir $STTB_WDIR/%s\n" % self.gitHash)
      shFile.write("  git clone $STTB_REPO $STTB_WDIR/%s\n" % self.gitHash)
      shFile.write("fi\n")
      shFile.write("cd $STTB_WDIR/%s\n" % self.gitHash)
      shFile.write("git fetch origin %s:tmpbranch\n" % self.gitRef)
      shFile.write("git checkout --detach %s\n" % self.gitHash)
      shFile.write("if [ -d \"SixTrack\" ]; then\n")
      shFile.write("  cd SixTrack\n")
      shFile.write("  ./buildLibraries.sh\n")
      shFile.write("else\n")
      for libDep in self.libDepend:
        shFile.write("  ./buildLibraries.sh %s\n" % libDep)
      shFile.write("fi\n")

    for aJob in self.theJobs:
      jobNo += 1
      aJob.writeJobFile(workDir, jobNo, len(self.theJobs))

    jobNo += 1
    shName = "Step_%04d_Cleanup.sh" % jobNo
    shPath = path.join(workDir, shName)
    with open(shPath, mode="w+") as shFile:
      shFile.write("#!/bin/bash\n")
      shFile.write("cd $STTB_WDIR\n")
      shFile.write("rm -rf %s/\n" % self.gitHash)

    return

# END Class Worker

class BuildJob():

  def __init__(self, theConfig, workerName, jobName, buildCompiler, compVersion, buildType, buildFlags, testFlags):

    self.jobName       = jobName.strip()
    self.workerName    = workerName
    self.buildCompiler = buildCompiler
    self.compVersion   = compVersion
    self.buildType     = buildType
    self.buildFlags    = sorted(buildFlags.split())
    self.testFlags     = testFlags

    self.gitHash       = theConfig.gitHash
    self.gitTime       = theConfig.gitTime
    self.gitMsg        = theConfig.gitMsg
    self.gitRef        = theConfig.gitRef
    self.jobsDir       = theConfig.jobsDir

    if self.testFlags is not None:
      self.buildFlags.append("BUILD_TESTING")

    self.buildOpt  = ("%s %s %s" % ( self.buildCompiler, self.buildType.strip(), " ".join(self.buildFlags))).strip()
    self.buildKey  = md5((self.workerName+"_"+self.jobName+"_"+self.gitHash+"_"+self.buildOpt).encode("utf-8")).hexdigest()
    self.buildName = "Build_"+self.buildKey

    if self.testFlags is None:
      logger.info("Added build job '%s'" % self.buildOpt)
    else:
      logger.info("Added build job '%s' with tests '%s'" % (self.buildOpt,self.testFlags))

    return

  def writeJobFile(self, jobDir, jobNo, nJobs):
    shName = "Step_%04d_Build_%s.sh" % (jobNo, self.buildKey)
    bldLog = "Build_%s.log" % self.buildKey
    tstLog = "Test_%s.xml" % self.buildKey
    shPath = path.join(jobDir, shName)
    with open(shPath, mode="w+") as shFile:
      shFile.write("#!/bin/bash\n")
      shFile.write("\n")
      shFile.write("BDIR=%s\n" % self.buildName)
      shFile.write("WDIR=$STTB_WDIR/%s\n" % self.gitHash)
      shFile.write("BLOG=$(pwd)/%s\n" % bldLog)
      shFile.write("TLOG=$(pwd)/%s\n" % tstLog)
      shFile.write("\n")
      shFile.write("cd $WDIR\n")
      shFile.write("if [ -d \"$BDIR\" ]; then\n")
      shFile.write("  rm -rf $BDIR\n")
      shFile.write("fi\n")
      shFile.write("mkdir $BDIR\n")
      shFile.write("cd    $BDIR\n")
      shFile.write("\n")
      shFile.write("echo \"## BEGIN BuildLog\" > $BLOG\n")
      shFile.write("echo \"# JobName         : %s\" >> $BLOG\n" % self.jobName)
      shFile.write("echo \"# BuildName       : %s\" >> $BLOG\n" % self.buildName)
      shFile.write("echo \"# BuildCompiler   : %s\" >> $BLOG\n" % self.buildCompiler)
      shFile.write("echo \"# BuildType       : %s\" >> $BLOG\n" % self.buildType)
      shFile.write("echo \"# BuildFlags      : %s\" >> $BLOG\n" % (" ".join(self.buildFlags)).strip())
      shFile.write("echo \"# CompilerVersion : %s\" >> $BLOG\n" % self.compVersion)
      shFile.write("echo \"# GitRef          : %s\" >> $BLOG\n" % self.gitRef)
      shFile.write("echo \"# GitHash         : %s\" >> $BLOG\n" % self.gitHash)
      shFile.write("echo \"# GitTime         : %s\" >> $BLOG\n" % self.gitTime)
      shFile.write("echo \"# GitMessage      : %s\" >> $BLOG\n" % self.gitMsg)
      shFile.write("echo \"# WorkerName      : %s\" >> $BLOG\n" % self.workerName)
      shFile.write("echo \"# WorkerHost      : $(hostname | head -n1)\" >> $BLOG\n")
      shFile.write("echo \"# WorkerOS        : $(uname -o)\" >> $BLOG\n")
      shFile.write("echo \"# WorkerArch      : $(uname -m)\" >> $BLOG\n")
      shFile.write("echo \"# KernelName      : $(uname -s)\" >> $BLOG\n")
      shFile.write("echo \"# KernelRelease   : $(uname -r)\" >> $BLOG\n")
      shFile.write("echo \"# KernelVersion   : $(uname -v)\" >> $BLOG\n")
      shFile.write("echo \"# BuildStart      : $(date +%s%N)\" >> $BLOG\n")
      shFile.write("cmake .. %s\n" % self._assembleCMakeFlags())
      shFile.write("echo \"# CMakeStatus     : $?\" >> $BLOG\n")
      shFile.write("make -j$STTB_BCPU\n")
      shFile.write("echo \"# MakeStatus      : $?\" >> $BLOG\n")
      shFile.write("echo \"# BuildEnd        : $(date +%s%N)\" >> $BLOG\n")
      if self.testFlags is not None:
        shFile.write("\n")
        shFile.write("echo \"# TestStart       : $(date +%s%N)\" >> $BLOG\n")
        shFile.write("ctest %s -T Test -j$STTB_TCPU\n" % self.testFlags)
        shFile.write("echo \"# TestStatus      : $?\" >> $BLOG\n")
        shFile.write("echo \"# TestEnd         : $(date +%s%N)\" >> $BLOG\n")
        shFile.write("cp Testing/*/Test.xml $TLOG\n")

      shFile.write("\n")
      shFile.write("cd $WDIR\n")
      shFile.write("rm -rf $BDIR\n")
      shFile.write("echo \"## END BuildLog\" >> $BLOG\n")

    return

  def _assembleCMakeFlags(self):
    theFlags  = "-G \"Unix Makefiles\" "
    theFlags += "-DCMAKE_Fortran_COMPILER=%s " % self.buildCompiler
    theFlags += "-DCMAKE_BUILD_TYPE=%s "       % self.buildType
    for jobFlag in self.buildFlags:
      if jobFlag == "": continue
      if jobFlag[0] == "-":
        theFlags += "-D%s=OFF " % jobFlag[1:]
      else:
        theFlags += "-D%s=ON " % jobFlag
    return theFlags.strip()

# END Class BuildJob
