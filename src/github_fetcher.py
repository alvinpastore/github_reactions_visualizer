import requests
import json
import pprint


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

    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/issues?state=open'

    if not auth:
        with open('../misc/git_token', 'r') as api_token_file:
            auth = api_token_file.readline()
    headers = {'Authorization': 'token ' + auth}

    print('Accessing ' + url)

    r = requests.get(url, headers=headers)
    json_info = r.json()

    # TODO iterate up to n issues and populate issues_info

    # dummy
    issues_info = {
        "author_username": 'STRING',
        "reactions": {
            "total_count": 'INT',
            "+1": 'INT',
            "-1": 'INT',
            "laugh": 'INT',
            "confused": 'INT',
            "heart": 'INT',
            "hooray": 'INT'
        },
        "repository_url": 'STRING',
        "issue_number": 'INT',
        "title": 'STRING',
        "body": 'STRING',
        "labels": 'LIST[STRING]  Just label names',
        "number_of_comments": 'INT',
        "created_at": 'TIMESTAMP',
        }

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

