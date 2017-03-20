import numpy as np
import pandas as pd
from itertools import product
from axelrod.strategies.memoryone import MemoryOnePlayer
from AshlockTournament import build_ashlock_tournament, create_ashlock_tournament_df, combine_dfs


def create_epsilon_vectors(epsilon):
    """Will return all 16 possible vectors for a given epsilon
    """
    options = [epsilon, -epsilon]
    epsilon_vectors = product(options, repeat=4)
    return epsilon_vectors


def deviate_vector(original, epsilon_vector):
    """For an original vector, return the new vector where min/max
    values are limited to 0/1 respectively
    """
    new_vector = np.array(original) + np.array(epsilon_vector)
    new_vector = new_vector.clip(0, 1)
    return new_vector


def create_deviated_vectors(original, epsilon):
    """For an original vector and value of epsilon, return all
    16 m_epsilon vectors.
    """
    epsilon_vectors = create_epsilon_vectors(epsilon)
    deviated_vectors = (deviate_vector(original, e) for e in epsilon_vectors)
    return deviated_vectors


def results_df_for_epsilon(vector, epsilon):
    """Run ashlock tournament for all 16 vectors and build the results df
    """
    deviated_vectors = create_deviated_vectors(vector, epsilon)
    strats = [MemoryOnePlayer(v) for v in deviated_vectors]
    ashlock_tourn = build_ashlock_tournament(strats)
    ash_tourn_df = create_ashlock_tournament_df(ashlock_tourn, None)
    return ash_tourn_df


def comparison_df_for_vector(vector, epsilons, path=None):
    """for range of epsilons, create big dataframe that compares
    with original vector
    """
    vector_ash_tourn = build_ashlock_tournament([MemoryOnePlayer(vector)])
    vector_ash_tourn_df = create_ashlock_tournament_df(vector_ash_tourn)

    epsilons_dfs = {e: results_df_for_epsilon(vector, e) for e in epsilons}
    comparison_dfs = [combine_dfs(vector_ash_tourn_df, epsilons_dfs[e], e) for e in epsilons]
    concat_df = pd.concat(comparison_dfs)

    if path is None:
        return concat_df
    else:
        with open(path, 'a') as f:
            concat_df.to_csv(f, header=f.tell() == 0, index=False)


def create_main_compare_df(vectors, epsilons):
    """for range of starting vectors and epsilons, create the large
    comparison df
    """
    comparisons = [comparison_df_for_vector(v, epsilons) for v in vectors]
    return pd.concat(comparisons)
