turns = [50, 100, 250, 500, 1000]
repetitions = [10, 50, 100, 200]
command = """#!/bin/bash
#PBS -q workq
#PBS -N T{}-R{}
#PBS -o out.txt
#PBS -e err.txt
#PBS -l select=1:ncpus=16:mpiprocs=16
#PBS -l place=scatter:excl
#PBS -l walltime=60:00:00
#PBS -P PR350

export MPLBACKEND="agg"

/home/c1304586/anaconda3/envs/fingerprint/bin/python /home/c1304586/fingerprints/fingerprinting.py {} {}
"""

if __name__ == "__main__":
    for t in turns:
        for r in repetitions:
            filename = 'pbs/T{}-R{}.pbs'.format(t, r)
            with open(filename, "w") as text_file:
                text_file.write(command.format(t, r, t, r))
