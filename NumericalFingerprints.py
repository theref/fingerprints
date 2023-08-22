import axelrod as axl
strats = [axl.TitForTat, axl.WinStayLoseShift, axl.AntiTitForTat, axl.Cooperator, axl.Defector, axl.Cycler('CD'), axl.GoByMajority(75)]
for s in strats:
    probe = axl.TitForTat
    af = axl.AshlockFingerprint(s, probe)
    data = af.fingerprint(turns=500, repetitions=200, step=0.01, processes=0)
    p = af.plot()
    p.savefig(f'/scratch/c1304586/img/{s.name}-Numerical.pdf')
