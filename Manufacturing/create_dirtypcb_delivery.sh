#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"
set -e

rm -f $1_DIRTYPCB.ZIP
cp $1-F_Cu.gbr TOP_COPPER.GTL
cp $1-B_Cu.gbr BTM_COPPER.GBL
cp $1-F_Mask.gbr TOP_MASK.GTS
cp $1-B_Mask.gbr BTM_MASK.GBS
cp $1-F_SilkS.gbr TOP_SILK.GTO
cp $1-B_SilkS.gbr BTM_SILK.GBO
cp $1-Edge_Cuts.gbr BRD_EDGE.GBR
cp $1.drl BRD_DRILL.TXT
zip -m $1_DIRTYPCB.ZIP TOP_COPPER.GTL BTM_COPPER.GBL TOP_MASK.GTS BTM_MASK.GBS TOP_SILK.GTO BTM_SILK.GBO BRD_EDGE.GBR BRD_DRILL.TXT
