import axelrod as axl
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
import pandas as pd
import numpy as np
from collections import namedtuple
import tempfile


Point = namedtuple('Point', 'x y')


def create_points(step):
    """Creates a set of Points over the unit square.
    A Point has coordinates (x, y). This function constructs points that are
    separated by a step equal to `step`. The points are over the unit
    square which implies that the number created will be (1/`step` + 1)^2.
    Parameters
    ----------
    step : float
        The separation between each Point. Smaller steps will produce more
        Points with coordinates that will be closer together.
    Returns
    ----------
    points : list
        of Point objects with coordinates (x, y)
    """
    num = int((1 / step) // 1) + 1

    points = []
    for x in np.linspace(0, 1, num):
        for y in np.linspace(0, 1, num):
            points.append(Point(x, y))

    return points


def create_jossann(point, probe):
    """Creates a JossAnn probe player that matches the Point.
    If the coordinates of point sums to more than 1 the parameters are
    flipped and subtracted from 1 to give meaningful probabilities. We also
    use the Dual of the probe. This is outlined further in [Ashlock2010]_.
    Parameters
    ----------
    point : Point
    probe : class
        A class that must be descended from axelrod.strategies
    Returns
    ----------
    joss_ann: Joss-AnnTitForTat object
        `JossAnnTransformer` with parameters that correspond to `point`.
    """
    x, y = point

    if isinstance(probe, axl.Player):
        init_args = probe.init_args
        probe = probe.__class__
    else:
        init_args = ()

    if x + y >= 1:
        joss_ann = DualTransformer()(
            JossAnnTransformer((1 - x, 1 - y))(probe))(*init_args)
    else:
        joss_ann = JossAnnTransformer((x, y))(probe)(*init_args)
    return joss_ann


def create_probes(probe, points):
    """Creates a set of probe strategies over the unit square.
    Constructs probe strategies that correspond to points with coordinates
    (x, y). The probes are created using the `JossAnnTransformer`.
    Parameters
    ----------
    probe : class
        A class that must be descended from axelrod.strategies.
    points : list
        of Point objects with coordinates (x, y)
    Returns
    ----------
    probes : list
        A list of `JossAnnTransformer` players with parameters that
        correspond to point.
    """
    probes = [create_jossann(point, probe) for point in points]
    return probes


def create_edges(strategies, points):
    """Creates a set of edges for a spatial tournament.
    Constructs edges that correspond to `points`.
    Parameters
    ----------
    points : list
        of Point objects with coordinates (x, y)
    Returns
    ----------
    edges : list of tuples
        A list containing tuples of length 2.
    """
    num_strategies = len(strategies)
    edges = []
    for i in range(num_strategies):
        e = [(i, index + num_strategies) for index, point in enumerate(points)]
        edges += e
    return edges


def create_test_df(strategies):
    points = create_points(step=0.25)
    probes = create_probes(axl.TitForTat, points)
    edges = create_edges(strategies, points)
    tournament_players = strategies + probes
    spatial_tournament = axl.SpatialTournament(tournament_players, edges=edges)
    results = spatial_tournament.play()

    with tempfile.NamedTemporaryFile() as temp:
        results.write_summary(temp.name)
        training_df = pd.read_csv(temp.name)

    return training_df


def clean_test_df(training_df):
    training_df = training_df[training_df.Name != 'Dual Joss-Ann Tit For Tat']
    training_df = training_df[training_df.Name != 'Joss-Ann Tit For Tat']
    training_df.drop('Rank', axis=1, inplace=True)
    training_df['Median_score'] = training_df['Median_score'] / 5
    return training_df


def create_large_df(small_df):
    orig_columns = small_df.columns
    A_columns = [i + '_A' for i in orig_columns]
    B_columns = [i + '_B' for i in orig_columns]
    new_df_A = small_df.copy()
    new_df_B = small_df.copy()
    new_df_A.columns = A_columns
    new_df_B.columns = B_columns

    overall_df = pd.DataFrame()
    length = len(small_df.index)
    for x in range(length):
        for y in range(length):
            line = pd.concat([new_df_A.iloc[x], new_df_B.iloc[y]])
            overall_df = overall_df.append(line, ignore_index=True)

    overall_df['Equivalent'] = overall_df['Name_A'] == overall_df['Name_B']
    overall_df['Equivalent'] = overall_df['Equivalent'].astype(int)
    overall_df['CC_rate_r'] = (overall_df[['CC_rate_A', 'CC_rate_B']].min(axis=1) /
                               overall_df[['CC_rate_A', 'CC_rate_B']].max(axis=1))

    overall_df['CD_rate_r'] = (overall_df[['CD_rate_A', 'CD_rate_B']].min(axis=1) /
                               overall_df[['CD_rate_A', 'CD_rate_B']].max(axis=1))

    overall_df['DC_rate_r'] = (overall_df[['DC_rate_A', 'DC_rate_B']].min(axis=1) /
                               overall_df[['DC_rate_A', 'DC_rate_B']].max(axis=1))

    overall_df['DD_rate_r'] = (overall_df[['DD_rate_A', 'DD_rate_B']].min(axis=1) /
                               overall_df[['DD_rate_A', 'DD_rate_B']].max(axis=1))


    overall_df['CC_to_C_r'] = (overall_df[['CC_to_C_rate_A', 'CC_to_C_rate_B']].min(axis=1) /
                               overall_df[['CC_to_C_rate_A', 'CC_to_C_rate_B']].max(axis=1))

    overall_df['CD_to_C_r'] = (overall_df[['CD_to_C_rate_A', 'CD_to_C_rate_B']].min(axis=1) /
                               overall_df[['CD_to_C_rate_A', 'CD_to_C_rate_B']].max(axis=1))

    overall_df['DC_to_C_r'] = (overall_df[['DC_to_C_rate_A', 'DC_to_C_rate_B']].min(axis=1) /
                               overall_df[['DC_to_C_rate_A', 'DC_to_C_rate_B']].max(axis=1))

    overall_df['DD_to_C_r'] = (overall_df[['DD_to_C_rate_A', 'DD_to_C_rate_B']].min(axis=1) /
                               overall_df[['DD_to_C_rate_A', 'DD_to_C_rate_B']].max(axis=1))



    overall_df['Cooperation_rating_r'] = (overall_df[['Cooperation_rating_A',
                                                      'Cooperation_rating_B']].min(axis=1) /
                                          overall_df[['Cooperation_rating_A',
                                                      'Cooperation_rating_B']].max(axis=1))

    overall_df['Initial_C_rate_r'] = (overall_df[['Initial_C_rate_A',
                                                  'Initial_C_rate_B']].min(axis=1) /
                                      overall_df[['Initial_C_rate_A',
                                                  'Initial_C_rate_B']].max(axis=1))

    overall_df['Median_score_r'] = (overall_df[['Median_score_A', 'Median_score_B']].min(axis=1) /
                                    overall_df[['Median_score_A', 'Median_score_B']].max(axis=1))

    overall_df['Wins_r'] = (overall_df[['Wins_A', 'Wins_B']].min(axis=1) /
                            overall_df[['Wins_A', 'Wins_B']].max(axis=1))

    overall_df.drop(['Name_A', 'Name_B', 'CC_rate_A', 'CC_rate_B', 'CD_rate_A',
                     'CD_rate_B', 'DC_rate_A', 'DC_rate_B', 'DD_rate_A',
                     'CC_to_C_rate_A', 'CC_to_C_rate_B', 'CD_to_C_rate_A',
                     'CD_to_C_rate_B', 'DC_to_C_rate_A', 'DC_to_C_rate_B',
                     'DD_to_C_rate_A', 'DD_to_C_rate_B',
                     'DD_rate_B', 'Cooperation_rating_A', 'Cooperation_rating_B',
                     'Initial_C_rate_A', 'Initial_C_rate_B', 'Median_score_A',
                     'Median_score_B', 'Wins_A', 'Wins_B'], axis=1, inplace=True)

    overall_df.fillna(1, inplace=True)

    return overall_df
