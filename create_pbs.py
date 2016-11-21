turns = [10, 50, 100, 250, 500]
command = """#!/bin/bash
#PBS -q workq
#PBS -N Turns-{}
#PBS -o out.txt
#PBS -e err.txt
#PBS -l select=1:ncpus=16:mpiprocs=16
#PBS -l place=scatter:excl
#PBS -l walltime=60:00:00
#PBS -P PR350

python /home/C1304586/fingerprints/fingerprinting.py {}
"""

if __name__ == "__main__":
    for t in turns:
        filename = 'pbs/Turns-{}.pbs'.format(t)
        with open(filename, "w") as text_file:
            text_file.write(command.format(t, t))
