import requests


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

    print('Accessing ' + url)

    r = requests.get(url, headers=headers)

    print(r.status_code)
    print(r.headers['content-type'])
    print(r.encoding)
    print(r.text)
    print(r.json())


if __name__ == '__main__':
    owner = 'rust-lang'
    repo = 'rust'
    fetch(repo, owner)

