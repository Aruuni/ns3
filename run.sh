#!/bin/bash


PROTOCOLS="TcpCubic TcpBbr TcpBbr3"
BANDWIDTHS="10"
DELAYS="5 10 15 20 25 30 35 40 45"
RUNS="1 2 3 4 5"
QMULTS="1 2 4"
FLOWS="2"

for bw in $BANDWIDTHS
do
    for del in $DELAYS
    do
        for qmult in $QMULTS
        do
            for flow in $FLOWS
            do
                for protocol in $PROTOCOLS
                do
                    for run in $RUNS
                    do
                        # delay is ( 2.5 x 4 ) + ( botlink x 2 ) 
                        ./ns3 run "scratch/SimulatorScript.cc --stopTime=200 --flowStartOffset=100 --appendFlow=$protocol --queueBDP=$qmult --botLinkDelay=$del --p2pLinkDelay=2.5  --path=fairnessafter100secs/bw$bw/delay$del/qmult$qmult/flows$flow/$protocol/run$run --seed=$run"
                    done
                done
            done
        done
    done
done




