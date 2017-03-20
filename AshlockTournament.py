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


def build_ashlock_tournament(strategies):
    """For a list of strategies, build the ashlock tournament but do not play.
    """
    points = create_points(step=0.25)
    probes = create_probes(axl.TitForTat, points)
    edges = create_edges(strategies, points)
    tournament_players = strategies + probes
    spatial_tournament = axl.SpatialTournament(tournament_players, edges=edges)
    return spatial_tournament


def create_ashlock_tournament_df(ashlock_tournament, p=None, p_bar=False):
    """For an ashlock tournament, build the results dataframe.
    This includes, removing all Dual/Joss-Ann lines, and
    standardising median score.
    """
    results = ashlock_tournament.play(processes=p, progress_bar=p_bar)

    with tempfile.NamedTemporaryFile() as temp:
        results.write_summary(temp.name)
        results_df = pd.read_csv(temp.name)

    results_df = results_df[results_df.Name != 'Dual Joss-Ann Tit For Tat']
    results_df = results_df[results_df.Name != 'Joss-Ann Tit For Tat']
    results_df.drop('Rank', axis=1, inplace=True)
    results_df['Median_score'] = results_df['Median_score'] / 5

    return results_df


def combine_dfs(df_1, df_2, epsilon=None):
    column_names = df_1.columns
    A_columns = [i + '_A' for i in column_names]
    B_columns = [i + '_B' for i in column_names]
    df_A = df_1.copy()
    df_B = df_2.copy()
    df_A.columns = A_columns
    df_B.columns = B_columns

    combination_df = pd.DataFrame()
    for x in range(len(df_A.index)):
        for y in range(len(df_B.index)):
            line = pd.concat([df_A.iloc[x], df_B.iloc[y]])
            combination_df = combination_df.append(line, ignore_index=True)

    r_columns = [i + '_r' for i in column_names[1:]]
    for c_name in zip(r_columns, A_columns[1:], B_columns[1:]):
        combination_df[c_name[0]] = (combination_df[[c_name[1], c_name[2]]].min(axis=1) /
                                     combination_df[[c_name[1], c_name[2]]].max(axis=1))

    combination_df.drop(['CC_rate_A', 'CC_rate_B', 'CD_rate_A',
                         'CD_rate_B', 'DC_rate_A', 'DC_rate_B', 'DD_rate_A',
                         'CC_to_C_rate_A', 'CC_to_C_rate_B', 'CD_to_C_rate_A',
                         'CD_to_C_rate_B', 'DC_to_C_rate_A', 'DC_to_C_rate_B',
                         'DD_to_C_rate_A', 'DD_to_C_rate_B',
                         'DD_rate_B', 'Cooperation_rating_A',
                         'Cooperation_rating_B', 'Initial_C_rate_A',
                         'Initial_C_rate_B', 'Median_score_A', 'Median_score_B',
                         'Wins_A', 'Wins_B'], axis=1, inplace=True)

    if epsilon is not None:
        combination_df['Epsilon'] = epsilon

    combination_df.fillna(1, inplace=True)

    return combination_df
