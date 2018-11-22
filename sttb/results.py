# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging
import socket

from os import path

logger = logging.getLogger("tbsixtrack")

class Results():

  def __init__(self, theConfig, gitHash):

    self.gitHash    = gitHash.strip()
    self.resultPath = theConfig.resultPath
    self.resultFile = path.join(self.resultPath, self.gitHash+".dat")

    self._checkFile()

    return

  def _checkFile(self):
    if path.isfile(self.resultFile):
      pass
    else:
      with open(self.resultFile,mode="w+") as rFile:
        rFile.write("# SixTrack Test Build System\n")
        rFile.write("#"*80+"\n")
      self.writeLine("HostName",socket.gethostname())
    return

  def writeLine(self, theName, theValue, fmt=None):
    with open(self.resultFile,mode="a") as rFile:
      if fmt is not None:
        rFile.write(("%-32s : "+fmt+"\n") % (theName, theValue))
      elif isinstance(theValue, int):
        rFile.write("%-32s : %12d\n" % (theName, theValue))
      elif isinstance(theValue, float):
        rFile.write("%-32s : %23.17e\n" % (theName, theValue))
      else:
        rFile.write("%-32s : %s\n" % (theName, str(theValue)))
    return

# END Class Results
