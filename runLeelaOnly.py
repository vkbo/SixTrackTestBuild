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
  logLevel = "debug"
)
theConfig.gitCheckout(sys.argv)

##
#  Debian Linux, 64 BIT
##

xDebian10 = Worker(theConfig, "Debian10")
xDebian10.addCompiler("gfortran", "--version")
xDebian10.setLibDependencies(["naff"])

xDebian10.addJob("Standard Double",           "gfortran", "Release", "",   "-L fast")
xDebian10.addJob("Checkpoint/Restart Double", "gfortran", "Release", "CR", "-L fast")

xDebian10.writeJobFiles()