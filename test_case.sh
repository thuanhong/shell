#!/bin/sh
echo "======================History======================="
history
history 1
history 5
history 1000
history hahff 10
history 10 dfjsdfs
echo "=======================globbing====================="
ls *
ls s*
ls s?
ls -l sd[ajsnajnjfnbgst]?
echo "=======================titde expand================="
echo ~
echo ~-
echo ~+
cd ~/Downloads
cd ~-
cd ~/shell
echo "=======================param expand=================="


