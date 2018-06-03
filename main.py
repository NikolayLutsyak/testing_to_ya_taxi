import numpy as np
import pandas as pd
from scipy import stats
from collections import defaultdict

def normal_confidence_interval(mean, std, alpha=0.05):
    z_alpha = stats.norm.ppf(1 - alpha/2)
    return [mean - z_alpha * std, mean + z_alpha * std]

def binomial_std(p, n):
    return np.sqrt(p * (1 - p) / n)

def main(filename='log.txt', max_num_line=100000, alpha=0.05):
    with open(filename, 'r') as infile:
        queries = []
        for num_line, line in enumerate(infile):
            if num_line == max_num_line:
                break
            line = line.strip().split(',')
            queries.append({
                "Type": line[1],
                "mobile": int(line[2])
            })

    queries = pd.DataFrame(queries)
    queries_info = queries.groupby('Type').agg(['mean', 'count'])

    conf_intervals = []
    for mean, n in queries_info.values:
        std = binomial_std(mean, n)
        conf_intervals.append(normal_confidence_interval(mean, std, alpha))
    conf_intervals = pd.DataFrame(np.array(conf_intervals), 
                                    index=queries_info.index, 
                                    columns=['low', 'high'])
    conf_intervals['mean'] = queries_info.iloc[:, 0]
    conf_intervals.to_csv('confident_intervals.csv')

    index_proba = queries_info.loc['/index', ('mobile', 'mean')]
    test_proba = queries_info.loc['/test', ('mobile', 'mean')]
    diff = index_proba - test_proba
    diff_std = np.sqrt((index_proba + test_proba - diff ** 2) / 
                        queries['mobile'].sum())
    diff_conf_interval = normal_confidence_interval(diff, diff_std, alpha)
    equal = diff_conf_interval[0] <= 0 <= diff_conf_interval[1]
    with open('check_index_test_equal.txt', 'w') as out:
        out.write(("The percentages of '/index' and '/test' mobile queries is {}"
                   "equal with a significance level of {}%.\n{}% confidence"
                   " interval for difference: ({:.3f}, {:.3f})\n").format(
            "" if equal else "not ", int(alpha * 100), int((1-alpha)*100), 
            diff_conf_interval[0], diff_conf_interval[1]))
        
if __name__ == '__main__':
    main()