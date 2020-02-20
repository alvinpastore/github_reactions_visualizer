import json
import matplotlib.pyplot as plt
import os

# data structure to collect the necessary info for the viz
counters = {'total_reactions':
            {'+1': 0, '-1': 0, 'heart': 0, 'hooray': 0, 'laugh': 0},
            'comment_reactions': {},
            'repos_reactions': {},
            'most_inf': {}}

# load data
for f in os.listdir("../data"):
    # drop .json from filename and use as repo name
    repo = f.split('.')[0]
    print('Counting reactions from ' + repo)

    with open('../data/' + f, 'r') as issues_file:
        issues = json.load(issues_file)

    counters['repos_reactions'][repo] = {'+1': 0, '-1': 0, 'heart': 0, 'hooray': 0, 'laugh': 0}

    for iid, issue in issues.items():

        counters['repos_reactions'][repo]['+1'] += issue['reactions']['+1']
        counters['repos_reactions'][repo]['-1'] += issue['reactions']['-1']
        counters['repos_reactions'][repo]['heart'] += issue['reactions']['heart']
        counters['repos_reactions'][repo]['hooray'] += issue['reactions']['hooray']
        counters['repos_reactions'][repo]['laugh'] += issue['reactions']['laugh']

    counters['total_reactions']['+1'] += counters['repos_reactions'][repo]['+1']
    counters['total_reactions']['-1'] += counters['repos_reactions'][repo]['-1']
    counters['total_reactions']['heart'] += counters['repos_reactions'][repo]['heart']
    counters['total_reactions']['hooray'] += counters['repos_reactions'][repo]['hooray']
    counters['total_reactions']['laugh'] += counters['repos_reactions'][repo]['laugh']

print('a')


plt.bar(counters['total_reactions'].keys(), counters['total_reactions'].values(), width=10, color='g')
