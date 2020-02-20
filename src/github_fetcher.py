import requests
import json
import pprint
from datetime import datetime as dt
from time import mktime
import time


def fetch(repo_name, repo_owner, n=5, auth=None, output_filepath=None):
    """ Fetch some relevant information for the latest open issues on GitHub
        for the repository specified.

        Keyword args:
            repo_name: The name of the repository from where to fetch issues
            repo_owner: The name of the repository we want to fetch issues
            n: The number of issues to be retrieved
            auth: token for authentication
            output_filepath: folder where to serialize the retrieved issues
    """

    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/issues'

    if not auth:
        with open('../misc/git_token', 'r') as api_token_file:
            auth = api_token_file.readline()
    headers = {'Authorization': 'token ' + auth}
    issues_request = requests.get(url + '?state=open', headers=headers)
    issues = issues_request.json()
    issues_info = {}

    for issue in issues:
        iid = issue['id']
        issues_info[iid] = {}
        issues_info[iid]['author_username'] = issue['user']['login']
        issues_info[iid]['repository_url'] = issue['repository_url']
        issues_info[iid]['issue_number'] = issue['number']
        issues_info[iid]['title'] = issue['title']
        issues_info[iid]['body'] = issue['body']
        label_names = [l['name'] for l in issue['labels']]
        issues_info[iid]['labels'] = label_names
        issues_info[iid]['number_of_comments'] = issue['comments']
        date_to_strp = time.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        issues_info[iid]['created_at'] = dt.fromtimestamp(mktime(date_to_strp))

        issues_info[iid]['reactions'] = {}
        reactions_url = url + '/' + str(issue['number']) + '/reactions'
        headers['Accept'] = 'application/vnd.github.squirrel-girl-preview+json'
        reactions_request = requests.get(reactions_url, headers=headers)
        reactions = reactions_request.json()

        reactions_summary = {'total_count': 0,
                             '+1': 0,
                             '-1': 0,
                             'laugh': 0,
                             'heart': 0,
                             'hooray': 0}

        for reaction in reactions:
            reactions_summary['total_count'] += 1

            # there are some reactions we are not interested, don't save them
            if reaction['content'] in reactions_summary.keys():
                reactions_summary[reaction['content']] += 1

        issues_info[iid]['reactions'] = reactions_summary


    if output_filepath:
        with open(output_filepath + '/' + repo_owner+'_'+repo+'.json') as dump_file:
            json.dump(issues_info, dump_file)
        pass
    else:
        pprint.pprint(issues_info, width=60)


if __name__ == '__main__':
    owner = 'rust-lang'
    repo = 'rust'
    num_issues = 400

    fetch(repo, owner, n=num_issues, output_filepath='data')

