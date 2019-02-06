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
#  Set up Worker
##

theWorker = Worker(theConfig, "Worker1")
theWorker.addCompiler("gfortran", "--version")
theWorker.setLibDependencies(["naff"])

##
#  Add the Jobs
##

theWorker.addJob("Standard Single", "gfortran", "Release", "-64BITM -CRLIBM 32BITM",  None)
theWorker.addJob("Standard Double", "gfortran", "Release", "",                        "-L fast")
theWorker.addJob("Standard Quad",   "gfortran", "Release", "-64BITM -CRLIBM 128BITM", None)

theWorker.writeJobFiles()

# theJobs = JobsWrapper(theConfig, theCompilers)
# theJobs.setCurrentHash(gitHash)
# theJobs.addJob("Standard Single",   "-64BITM -CRLIBM 32BITM",  ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Standard Double",   "",                        ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Standard Quad",     "-64BITM -CRLIBM 128BITM", ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Round Up",          "-ROUND_NEAR ROUND_UP",    ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Round Down",        "-ROUND_NEAR ROUND_DOWN",  ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Round Zero",        "-ROUND_NEAR ROUND_ZERO",  ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Checkpoint/Restart", "CR",                     ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("No SingleTrackFile", "-STF",                   ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("libArchive Support", "LIBARCHIVE",             ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("BOINC Support",      "CR BOINC LIBARCHIVE",    ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Fortran I/O",        "FIO",                    ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("HDF5",               "HDF5",                   ["gfortran"],                  ["Release","Debug"])
# theJobs.addJob("Beam-Gas",           "BEAMGAS",                ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Fluka Coupling",     "FLUKA",                  ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addJob("Merlin Scattering",  "MERLINSCATTER",          ["gfortran","ifort","nagfor"], ["Release","Debug"])

# theJobs.addTest("-L 'fast|medium'",  "",                       ["gfortran","ifort","nagfor"], ["Release"])
# theJobs.addTest("-L 'fast'"       ,  "",                       ["gfortran","ifort","nagfor"], ["Debug"])
# theJobs.addTest("-L 'fast'",         "FIO",                    ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addTest("-L 'fast'",         "-STF",                   ["gfortran","ifort","nagfor"], ["Release","Debug"])
# theJobs.addTest("-L 'fast|medium'",  "CR",                     ["gfortran","ifort","nagfor"], ["Release"])
# theJobs.addTest("-L 'fast'",         "CR BOINC LIBARCHIVE",    ["gfortran","ifort","nagfor"], ["Release"])

# theJobs.writeJobFiles()
