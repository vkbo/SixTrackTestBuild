# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - Database Class
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging
import pymysql.cursors

from os import path, mkdir

from .functions import *

logger = logging.getLogger("sttb-logger")

class BuildsDB():

  def __init__(self, theConfig, dbConfig, archiveDir=None):

    self.theConfig = theConfig
    self.dbConfig  = dbConfig
    self.dbConn    = None
    self.dbCursor  = None
    try:
      self.dbConn = pymysql.connect(**self.dbConfig, cursorclass=pymysql.cursors.DictCursor)
    except Exception:
      endExec("Could not connect to MySQL database on host '%s'" % self.dbConfig["host"])
    else:
      logger.info("Connect to MySQL database on host '%s'" % self.dbConfig["host"])
      self.dbCursor = self.dbConn.cursor()

    return

  def importResults(self, workerName, buildLog=False, testLog=False):
    return

# END Class BuildsDB
