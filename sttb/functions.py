"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import subprocess

logger = logging.getLogger("sttb-logger")

def endExec(errMsg = None):
  if errMsg is None:
    logger.info("All done! Exiting ...")
    exit(0)
  else:
    logger.error(errMsg)
    logger.critical("Exiting with status 1")
    exit(1)

# Wrapper function for system calls
def sysCall(callStr):
  sysP = subprocess.Popen([callStr], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  stdOut, stdErr = sysP.communicate()
  return stdOut.decode("utf-8"), stdErr.decode("utf-8"), sysP.returncode

# Command line output wrapper
def logWrap(outTag, stdOut, stdErr, exCode):
  outLns = stdOut.split("\n")
  errLns = stdErr.split("\n")
  for outLn in outLns:
    if outLn.strip() == "": continue
    logger.debug("%s> %s" % (outTag, outLn))
  if exCode is not 0:
    for errLn in errLns:
      if errLn.strip() == "": continue
      logger.error("%s> %s" % (outTag, errLn))
    logger.error("%s> Exited with code %d" % (outTag, exCode))
    exit(1)

def cmakeSixReturn(stdOut, stdErr):
  outLns = stdOut.split("\n")
  errLns = stdErr.split("\n")
  bPath  = ""
  if len(outLns) > 1:
    tmpData = outLns[-2].split()
    if len(tmpData) > 0:
      bPath = tmpData[-1]
  return bPath

def ctestReturn(stdOut, stdErr):
  outLns  = stdOut.split("\n")
  tFailed = ""
  if len(outLns) <= 2:
    logger.debug("CTEST> %s" % outLns[-1])
  else:
    atSum  = False
    atFail = False
    for outLn in outLns:
      outLn = outLn.strip()
      if outLn == "":
        atSum = True
        continue
      if not atSum:
        continue
      if not outLn == "":
        logger.debug("CTEST> %s" % outLn.strip())
      if outLn.strip() == "The following tests FAILED:":
        atFail = True
        continue
      if atFail:
        splFail = outLn.split()
        if len(splFail) == 4:
          if splFail[3] == "(Failed)":
            tFailed += splFail[2]+", "
    if atFail:
      tFailed = tFailed[:-2]
  return tFailed
