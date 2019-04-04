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

xDebian10.addJob("Performance GNU",   "gfortran", "Release", "", "-E prob")
xDebian10.addJob("Performance Intel", "ifort",    "Release", "", "-E prob")
xDebian10.addJob("Performance NAG",   "nagfor",   "Release", "", "-E prob")

xDebian10.writeJobFiles()
