#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - DB Data Import
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

# Get the pasword from a file
with open("/scratch/SixTrackTestBuilds/dbPassword.txt","r") as pwFile:
  passWord = pwFile.read().strip()

# Options are those taken by the PyMySQL connector
dbConfig = {
  "host":     "localhost",
  "user":     "sttb_master",
  "password": passWord,
  "database": "sixtrack_build",
  "port":     3306
}

theDB = BuildsDB(theConfig, dbConfig, archiveDir="/scratch/SixTrackTestBuilds/archive")

theDB.importResults(workerName="Debian10", buildLog=True, testLog=False)
