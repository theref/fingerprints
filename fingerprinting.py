import sys
from os import getlogin
import axelrod as axl

user = getlogin()
turns = int(sys.argv[1])
repetitions = [5, 10, 50, 100]
probes = [axl.TitForTat, axl.TitFor2Tats, axl.TwoTitsForTat, axl.Bully,
          axl.PSOGambler]
col_maps = ['seismic', 'PuOr']
file_types = ['.png', '.pdf']
interpolations = ['none', 'None', 'bicubic', 'bessel']

if __name__ == "__main__":
    if user = 'James':
        for rep in repetitions[0]:
            for probe in probes[0]:
                for strategy in axl.strategies[0]:
                    path = '~/Projects/fingerprint/images/{}/{}/{}/'.format(turns, rep, probe)
                    af = axl.AshlockFingerprint(strategy, probe)
                    data = af.fingerprint(turns=turns, repetitions=rep, step=0.01)

    if user = 'c1304586':
        for rep in repetitions:
            for probe in probes:
                for strategy in axl.strategies:
                    path = '/scratch/c1304586/images/{}/{}/{}/'.format(turns, rep, probe)
                    af = axl.AshlockFingerprint(strategy, probe)
                    data = af.fingerprint(turns=turns, repetitions=rep, step=0.01)
