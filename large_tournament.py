import numpy as np
import axelrod as axl
from MachineLearning import create_test_df, clean_test_df, create_large_df


strategies = [i() for i in axl.strategies]
strategies = list(np.repeat(strategies, 5))
test_df = create_test_df(strategies)
cleaned_test_df = clean_test_df(test_df)
training_df = create_large_df(cleaned_test_df)
training_df.to_csv('/scratch/c1304586/large_data.csv')
