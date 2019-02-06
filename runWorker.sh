#!/bin/bash

JDIR=/scratch/SixTrackTestBuilds/sync/jobs/Debian10

while true; do

  export STTB_REPO=/scratch/SixTrackTestBuilds/repo/SixTrack.git
  export STTB_WDIR=/scratch/Temp
  export STTB_BCPU=8
  export STTB_TCPU=8

  if ls $JDIR/*/ 1> /dev/null 2>&1; then
    for BDIR in $JDIR/*/; do
      BDIR=${BDIR%*/}
      cd $BDIR
      if ls *.sh 1> /dev/null 2>&1; then
        echo ""
        echo " Running Jobs: ${BDIR##*/}"
        echo "========================================================"
        echo ""
        for JFILE in `ls -v Step_*.sh`; do
          echo ">> Starting: $JFILE <<"
          echo ""
          chmod +x $JFILE
          ./$JFILE
          unlink $JFILE
          echo ""
          echo ">> Finished: $JFILE <<"
          echo ""
        done
      fi
    done
  fi

  echo "Sleeping for 60 seconds ..."
  sleep 60

done