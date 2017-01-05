#!/bin/bash

echo $1
echo $2
echo $3

OLD=ARRAY_STRING
TASKNUMBER=NUMBEROFTASKS
cat job_processing/sbatch_innuca.template | sed "s#$OLD#$1#1" > sbatch_innuca.sh
cat sbatch_innuca.sh | sed "s#$TASKNUMBER#$2#1" > sbatch_innuca_final.sh

sbatch --array=0-$2 --ntasks=1 --cpus-per-task=1 sbatch_innuca.sh