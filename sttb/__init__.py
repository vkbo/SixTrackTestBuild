# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Test Builds - INIT
 =============================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from sttb.config   import Config
from sttb.worker   import Worker
from sttb.database import BuildsDB

logger = logging.getLogger("tbsixtrack")

__all__ = ["Worker","Config","BuildsDB"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2018, Veronica Berglyd Olsen, CERN (BE-ABP-HSS)"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2019"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Perpetual Development"
__url__        = ""
