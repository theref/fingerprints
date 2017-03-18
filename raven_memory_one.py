import itertools
import numpy as np
from Memory_One import comparison_df_for_vector
from joblib import Parallel, delayed


if __name__ == '__main__':
    q_num = 11
    original_vectors = itertools.product(np.linspace(0, 1, q_num), repeat=4)

    path = '/scratch/c1304586/memory_one.csv'
    epsilons = [0.01, 0.025, 0.05, 0.1, 0.25]

    for v in original_vectors:
        comparison_df_for_vector(v, epsilons, path)

    Parallel(n_jobs=16)(delayed(comparison_df_for_vector)(v, epsilons, path)
                        for v in original_vectors)

    parallelizer = Parallel(n_jobs=16)
    tasks_iterator = (delayed(comparison_df_for_vector)(v, epsilons, path)
                      for v in original_vectors)
    result = parallelizer(tasks_iterator)
