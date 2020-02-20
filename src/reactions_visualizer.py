import json
import matplotlib.pyplot as plt
import os
import numpy as np

# data structure to collect the necessary info for the viz
counters = {'total_reactions':
            {'+1': 0, '-1': 0, 'heart': 0, 'hooray': 0, 'laugh': 0},
            'comment_reactions': {},
            'comment_reactions_avg': {},
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

        comments_n = issue['number_of_comments']
        if comments_n not in counters['comment_reactions']:
            counters['comment_reactions'][comments_n] = [sum(issue['reactions'].values())]
        else:
            counters['comment_reactions'][comments_n].append(sum(issue['reactions'].values()))

    counters['total_reactions']['+1'] += counters['repos_reactions'][repo]['+1']
    counters['total_reactions']['-1'] += counters['repos_reactions'][repo]['-1']
    counters['total_reactions']['heart'] += counters['repos_reactions'][repo]['heart']
    counters['total_reactions']['hooray'] += counters['repos_reactions'][repo]['hooray']
    counters['total_reactions']['laugh'] += counters['repos_reactions'][repo]['laugh']

    for comments_n, reacts in counters['comment_reactions'].items():
        counters['comment_reactions_avg'][comments_n] = sum(reacts)/len(reacts)

# x_ticks_labels = list(counters['total_reactions'].keys())
# x = range(len(x_ticks_labels))
# y = list(counters['total_reactions'].values())
# plt.bar(x, y)
# plt.xticks(x, x_ticks_labels)
# plt.title('Total reactions')
# plt.show()



x_ticks_labels = list(counters['comment_reactions'].keys())
x = range(len(x_ticks_labels))
y = list(counters['comment_reactions_avg'].values())
plt.bar(x, y)
plt.xticks(x, x_ticks_labels, rotation=90)
plt.title('Average reactions by comment')
plt.show()



x = np.arange(len(x_ticks_labels))
width = .1  # the width of the bars

fig, ax = plt.subplots()
y = {}
offsets = [-.25, -.15, .15, .25]
i=0

for repo in counters['repos_reactions'].keys():
    y[repo] = list(counters['repos_reactions'][repo].values())
    rects = ax.bar(x + offsets[i], y[repo], width, label=repo)
    i += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Total')
ax.set_title('Breakdown by repository')
ax.set_xticks(x)
ax.set_xticklabels(x_ticks_labels)
ax.legend()
plt.show()
