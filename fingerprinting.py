import sys
import os
import csv
import axelrod as axl

# user = os.getlogin()
turns = int(sys.argv[1])
repetitions = [5, 10, 50, 100]
probes = [axl.TitForTat, axl.TitFor2Tats, axl.TwoTitsForTat, axl.Bully,
          axl.PSOGambler]
col_maps = ['seismic', 'PuOr']
file_types = ['png', 'pdf']
interpolations = ['none', 'None', 'bicubic', 'bessel']


def write_to_file(data, directory):
    filename = directory + 'results.csv'
    os.makedirs(directory)
    with open(filename, 'w') as textfile:
        w = csv.writer(textfile)
        for key, value in data.items():
            row = (key[0], key[1], value)
            w.writerow(row)


if __name__ == "__main__":
    # if user == 'James':
    #     for rep in repetitions[:1]:
    #         for probe in probes[:1]:
    #             for strategy in axl.strategies[:1]:
    #                 af = axl.AshlockFingerprint(strategy, probe)
    #                 data = af.fingerprint(turns=turns, repetitions=rep, step=0.01)
    #                 for cmap in col_maps:
    #                     for intpl in interpolations:
    #                         for ftype in file_types:
    #                             p = af.plot(col_map=cmap, interpolation=intpl)
    #                             directory = '/Users/James/Projects/fingerprints/images/'
    #                             directory += '{}/{}/{}/'.format(turns, rep, probe.__name__)
    #                             write_to_file(data, directory)
    #                             directory += '{}/{}/'.format(cmap, intpl)
    #                             if not os.path.exists(directory):
    #                                 os.makedirs(directory)
    #                             directory += '{}.{}'.format(strategy.__name__, ftype)
    #                             p.savefig(directory)

    # if user == 'c1304586':
    for rep in repetitions:
        for probe in probes:
            for strategy in axl.strategies:
                af = axl.AshlockFingerprint(strategy, probe)
                data = af.fingerprint(turns=turns, repetitions=rep, step=0.01, processes=0)
                for cmap in col_maps:
                    for intpl in interpolations:
                        for ftype in file_types:
                            p = af.plot(col_map=cmap, interpolation=intpl)
                            directory = '/scratch/c1304586/fingerprints/images/'
                            directory += '{}/{}/{}/'.format(turns, rep, probe.__name__)
                            write_to_file(data, directory)
                            directory += '{}/{}/'.format(cmap, intpl)
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            directory += '{}.{}'.format(strategy.__name__, ftype)
                            p.savefig(directory)
