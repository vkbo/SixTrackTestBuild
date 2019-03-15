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
xDebian10.setLibDependencies(["naff","boinc","hdf5","pythia"])

# gfortran release
xDebian10.addJob("Standard Single",       "gfortran", "Release", "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "gfortran", "Release", "",                        "-E prob")
xDebian10.addJob("Standard Quad",         "gfortran", "Release", "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "gfortran", "Release", "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "gfortran", "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "gfortran", "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "gfortran", "Release", "-STF",                    "-L fast")
xDebian10.addJob("Fortran I/O",           "gfortran", "Release", "FIO",                     "-L fast")
xDebian10.addJob("Checkpoint/Restart",    "gfortran", "Release", "CR",                      "-E prob")
xDebian10.addJob("BOINC Support",         "gfortran", "Release", "CR BOINC LIBARCHIVE",     "-E prob")
xDebian10.addJob("HDF5 Support",          "gfortran", "Release", "HDF5",                    "-L fast")
xDebian10.addJob("Pythia Support",        "gfortran", "Release", "PYTHIA",                  "-L fast")
xDebian10.addJob("Beam-Gas Support",      "gfortran", "Release", "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "gfortran", "Release", "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "gfortran", "Release", "MERLINSCATTER",           None)

# gfortran debug
xDebian10.addJob("Standard Single",       "gfortran", "Debug",   "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "gfortran", "Debug",   "",                        "-L fast")
xDebian10.addJob("Standard Quad",         "gfortran", "Debug",   "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "gfortran", "Debug",   "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "gfortran", "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "gfortran", "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "gfortran", "Debug",   "-STF",                    None)
xDebian10.addJob("Fortran I/O",           "gfortran", "Debug",   "FIO",                     None)
xDebian10.addJob("Checkpoint/Restart",    "gfortran", "Debug",   "CR",                      None)
xDebian10.addJob("BOINC Support",         "gfortran", "Debug",   "CR BOINC LIBARCHIVE",     None)
xDebian10.addJob("HDF5 Support",          "gfortran", "Debug",   "HDF5",                    None)
xDebian10.addJob("Pythia Support",        "gfortran", "Debug",   "PYTHIA",                  None)
xDebian10.addJob("Beam-Gas Support",      "gfortran", "Debug",   "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "gfortran", "Debug",   "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "gfortran", "Debug",   "MERLINSCATTER",           None)

# ifort release
xDebian10.addJob("Standard Single",       "ifort",    "Release", "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "ifort",    "Release", "",                        "-E prob")
xDebian10.addJob("Standard Quad",         "ifort",    "Release", "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "ifort",    "Release", "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "ifort",    "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "ifort",    "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "ifort",    "Release", "-STF",                    "-L fast")
xDebian10.addJob("Fortran I/O",           "ifort",    "Release", "FIO",                     "-L fast")
xDebian10.addJob("Checkpoint/Restart",    "ifort",    "Release", "CR",                      "-E prob")
xDebian10.addJob("BOINC Support",         "ifort",    "Release", "CR BOINC LIBARCHIVE",     "-E prob")
xDebian10.addJob("Pythia Support",        "ifort",    "Release", "PYTHIA",                  "-L fast")
xDebian10.addJob("Beam-Gas Support",      "ifort",    "Release", "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "ifort",    "Release", "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "ifort",    "Release", "MERLINSCATTER",           None)

# ifort debug
xDebian10.addJob("Standard Single",       "ifort",    "Debug",   "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "ifort",    "Debug",   "",                        "-L fast")
xDebian10.addJob("Standard Quad",         "ifort",    "Debug",   "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "ifort",    "Debug",   "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "ifort",    "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "ifort",    "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "ifort",    "Debug",   "-STF",                    None)
xDebian10.addJob("Fortran I/O",           "ifort",    "Debug",   "FIO",                     None)
xDebian10.addJob("Checkpoint/Restart",    "ifort",    "Debug",   "CR",                      None)
xDebian10.addJob("BOINC Support",         "ifort",    "Debug",   "CR BOINC LIBARCHIVE",     None)
xDebian10.addJob("Pythia Support",        "ifort",    "Debug",   "PYTHIA",                  None)
xDebian10.addJob("Beam-Gas Support",      "ifort",    "Debug",   "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "ifort",    "Debug",   "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "ifort",    "Debug",   "MERLINSCATTER",           None)

# nagfor release
xDebian10.addJob("Standard Single",       "nagfor",   "Release", "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "nagfor",   "Release", "",                        "-E prob")
xDebian10.addJob("Standard Quad",         "nagfor",   "Release", "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "nagfor",   "Release", "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "nagfor",   "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "nagfor",   "Release", "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "nagfor",   "Release", "-STF",                    "-L fast")
xDebian10.addJob("Fortran I/O",           "nagfor",   "Release", "FIO",                     "-L fast")
xDebian10.addJob("Checkpoint/Restart",    "nagfor",   "Release", "CR",                      "-E prob")
xDebian10.addJob("BOINC Support",         "nagfor",   "Release", "CR BOINC LIBARCHIVE",     "-E prob")
xDebian10.addJob("Pythia Support",        "nagfor",   "Release", "PYTHIA",                  "-L fast")
xDebian10.addJob("Beam-Gas Support",      "nagfor",   "Release", "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "nagfor",   "Release", "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "nagfor",   "Release", "MERLINSCATTER",           None)

# nagfor debug
xDebian10.addJob("Standard Single",       "nagfor",   "Debug",   "-64BITM -CRLIBM 32BITM",  None)
xDebian10.addJob("Standard Double",       "nagfor",   "Debug",   "",                        "-L fast")
xDebian10.addJob("Standard Quad",         "nagfor",   "Debug",   "-64BITM -CRLIBM 128BITM", None)
xDebian10.addJob("Round Up",              "nagfor",   "Debug",   "-ROUND_NEAR ROUND_UP",    None)
xDebian10.addJob("Round Down",            "nagfor",   "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("Round Zero",            "nagfor",   "Debug",   "-ROUND_NEAR ROUND_DOWN",  None)
xDebian10.addJob("No SingleTrackFile",    "nagfor",   "Debug",   "-STF",                    None)
xDebian10.addJob("Fortran I/O",           "nagfor",   "Debug",   "FIO",                     None)
xDebian10.addJob("Checkpoint/Restart",    "nagfor",   "Debug",   "CR",                      None)
xDebian10.addJob("BOINC Support",         "nagfor",   "Debug",   "CR BOINC LIBARCHIVE",     None)
xDebian10.addJob("Pythia Support",        "nagfor",   "Debug",   "PYTHIA",                  None)
xDebian10.addJob("Beam-Gas Support",      "nagfor",   "Debug",   "BEAMGAS",                 None)
xDebian10.addJob("Fluka Support",         "nagfor",   "Debug",   "FLUKA",                   None)
xDebian10.addJob("MerlinScatter Support", "nagfor",   "Debug",   "MERLINSCATTER",           None)

xDebian10.writeJobFiles()
