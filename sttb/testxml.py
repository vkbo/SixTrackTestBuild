# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - TestXML Class
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from os   import path
from lxml import etree

# from .functions import *

logger = logging.getLogger("sttb-logger")

class TestXML():

  def __init__(self, xmlFile):

    self.xmlFile = xmlFile
    self.testRes = {}

    if not path.isfile(xmlFile):
      logger.error("File not dound: %s" % xmlFile)
      return

    self._parseXML()

    # print(self.testRes)

    return

  def getTestCount(self):
    nTest = 0
    nPass = 0
    nFail = 0
    for testName in self.testRes.keys():
      nTest += 1
      if self.testRes[testName]["Status"] == "passed":
        nPass += 1
      elif self.testRes[testName]["Status"] == "failed":
        nFail += 1
    return nTest, nPass, nFail

  def _parseXML(self):

    inXML = etree.parse(self.xmlFile)
    xRoot = inXML.getroot()

    for xChild in xRoot:
      if xChild.tag == "Testing":
        for xItem in xChild:
          if xItem.tag != "Test":
            continue
          tName   = "Unknown"
          tResult = {
            "Status"     : xItem.attrib["Status"],
            "Completion" : "Unknown",
            "RunTime"    : 0.0,
            "Lables"     : [],
          }
          for xEntry in xItem:
            if xEntry.tag == "Name":
              tName = xEntry.text
            elif xEntry.tag == "Results":
              for xResult in xEntry:
                if xResult.tag == "NamedMeasurement":
                  if xResult.attrib["name"] == "Completion Status":
                    for xValue in xResult:
                      if xValue.tag == "Value":
                        tResult["Completion"] = xValue.text
                  elif xResult.attrib["name"] == "Execution Time":
                    for xValue in xResult:
                      if xValue.tag == "Value":
                        tResult["RunTime"] = float(xValue.text)*1e3
            elif xEntry.tag == "Labels":
              for xLabel in xEntry:
                tResult["Lables"].append(xLabel.text)
          self.testRes[tName] = tResult

    return

# END Class TestXML
