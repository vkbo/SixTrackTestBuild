# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from .functions import sysCall, logWrap

logger = logging.getLogger("sttb-logger")

class Compilers():

  def __init__(self, theConfig):
    self.theCompilers = {}
    return

  def addCompiler(self, compilerExec, versionCommand):

    cName = compilerExec.strip()
    cVers = versionCommand.strip()
    self.theCompilers[cName] = {}
    self.theCompilers[cName]["versionCommand"] = cVers

    stdOut, stdErr, exCode = sysCall("%s %s" % (cName, cVers))
    tmpLn = (stdOut+stdErr).split("\n")
    self.theCompilers[cName]["compilerVersion"] = tmpLn[0]
    if exCode == 0:
      self.theCompilers[cName]["compilerOK"] = True
      logger.info("Using compiler: %s" % tmpLn[0])
    else:
      self.theCompilers[cName]["compilerOK"] = False
      logger.error("There is a problem with the %s compiler" % cName)
      logWrap("COMPILER",stdOut,stdErr,exCode)

    return

  def checkCompiler(self, compilerName):
    if compilerName in self.theCompilers.keys():
      return self.theCompilers[compilerName]["compilerOK"]
    return False


# END Class Compiler
