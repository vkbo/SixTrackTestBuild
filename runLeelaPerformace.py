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
xDebian10.setLibDependencies(["naff","boinc"])

# gfortran
xDebian10.addJob("Standard Double",    "gfortran", "Release", "",                    "-E prob")
xDebian10.addJob("Checkpoint/Restart", "gfortran", "Release", "CR",                  "-E prob")
xDebian10.addJob("BOINC Support",      "gfortran", "Release", "CR BOINC LIBARCHIVE", "-E prob")
xDebian10.addJob("Standard Double",    "gfortran", "Debug",   "",                    "-L fast")

# ifort
xDebian10.addJob("Standard Double",    "ifort",    "Release", "",                    "-E prob")
xDebian10.addJob("Checkpoint/Restart", "ifort",    "Release", "CR",                  "-E prob")
xDebian10.addJob("BOINC Support",      "ifort",    "Release", "CR BOINC LIBARCHIVE", "-E prob")
xDebian10.addJob("Standard Double",    "ifort",    "Debug",   "",                    "-L fast")

# nagfor
xDebian10.addJob("Standard Double",    "nagfor",   "Release", "",                    "-E prob")
xDebian10.addJob("Checkpoint/Restart", "nagfor",   "Release", "CR",                  "-E prob")
xDebian10.addJob("BOINC Support",      "nagfor",   "Release", "CR BOINC LIBARCHIVE", "-E prob")
xDebian10.addJob("Standard Double",    "nagfor",   "Debug",   "",                    "-L fast")

xDebian10.writeJobFiles()
