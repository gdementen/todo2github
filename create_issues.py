"""
create issues on GitHub
"""

import requests
import json


def upload(fpath, repo, user=None, password=None):
    """
    repo is a fully-qualified repository name. eg liam2/liam2
    """
    with open(fpath) as f:
        issues = json.load(f)
    assert isinstance(issues, list)
    url = 'https://api.github.com/repos/%s/issues' % repo
    if password is not None:
        if user is None:
            user = repo.split('/')[0]
        auth = (user, password)
    else:
        auth = None
    for issue in issues:
        r = requests.post(url, json.dumps(issue), auth=auth)
        if r.ok:
            d = json.loads(r.text or r.content)
            print "issue %d created at %s" % (d['number'], d['created_at'])

if __name__ == '__main__':
    from sys import argv

    upload(*argv[1:])
