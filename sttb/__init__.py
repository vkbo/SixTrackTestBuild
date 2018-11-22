# -*- coding: utf-8 -*
"""SixTrack Test Builds

  SixTrack Tools - SixTrack Test Builds
 =======================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging

from sttb.compilers import Compilers
from sttb.config    import Config
from sttb.jobs      import JobsWrapper
from sttb.results   import Results

logger = logging.getLogger("tbsixtrack")

__all__ = ["Compilers","Config","JobsWrapper","Results"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2018, Veronica Berglyd Olsen, CERN (BE-ABP-HSS)"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2018"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Perpetual Development"
__url__        = ""
