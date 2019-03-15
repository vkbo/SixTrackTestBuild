#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import sys
import logging
from sttb import *

logger = logging.getLogger("sttb-logger")

theConfig = Config(
  workDir  = "/scratch/SixTrackTestBuilds",
  jobsDir  = "/scratch/SixTrackTestBuilds/sync/jobs",
  logLevel = "info"
)
theConfig.gitCheckout(sys.argv)

##
#  Debian Linux, 64 BIT
##

xDebian10 = Worker(theConfig, "Debian10")
xDebian10.addCompiler("gfortran", "--version")
xDebian10.addCompiler("ifort",    "--version")
xDebian10.addCompiler("nagfor",   "-V")
xDebian10.setLibDependencies(["naff"])

xDebian10.addJob("Standard Double",           "gfortran", "Release", "",   "-L fast")
xDebian10.addJob("Checkpoint/Restart Double", "gfortran", "Release", "CR", "-L fast")
xDebian10.addJob("Standard Double",           "ifort",    "Release", "",   "-L fast")
xDebian10.addJob("Checkpoint/Restart Double", "ifort",    "Release", "CR", "-L fast")
xDebian10.addJob("Standard Double",           "nagfor",   "Release", "",   "-L fast")
xDebian10.addJob("Checkpoint/Restart Double", "nagfor",   "Release", "CR", "-L fast")

xDebian10.writeJobFiles()

##
#  Windows 10, 32 BIT
##

win10_32 = Worker(theConfig, "Win10_MINGW32")
win10_32.addCompiler("gfortran", "--version")
win10_32.setLibDependencies(["naff"])

win10_32.addJob("Standard Double",           "gfortran", "Release", "-64BIT 32BIT",    "-L fast -E Check")
win10_32.addJob("Checkpoint/Restart Double", "gfortran", "Release", "-64BIT 32BIT CR", "-L fast -E Check")

win10_32.writeJobFiles()

##
#  Windows 10, 64 BIT
##

win10_64 = Worker(theConfig, "Win10_MINGW64")
win10_64.addCompiler("gfortran", "--version")
win10_64.setLibDependencies(["naff"])

win10_64.addJob("Standard Double",           "gfortran", "Release", "",   "-L fast -E Check")
win10_64.addJob("Checkpoint/Restart Double", "gfortran", "Release", "CR", "-L fast -E Check")

win10_64.writeJobFiles()
