from scipy.stats import pearsonr, spearmanr, kendalltau


test_dict = {'pearson': pearsonr,
                     'spearman': spearmanr,
                     'kendall': kendalltau
                     }
