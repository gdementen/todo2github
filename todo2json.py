"""
convert a simple TODO text file to GitHub's issue json format
"""
import json


def choose(msg, letters, default=None):
    choices_str = ' (%s) ' % '/'.join(c.capitalize() if c == default else c
                                      for c in letters)
    answer = None
    if default is not None:
        letters = ('',) + tuple(letters)
    while answer not in letters:
        if answer is not None:
            print("answer should be %s, or <return>"
                  % ', '.join(repr(l) for l in letters))
        answer = raw_input(msg + choices_str).lower()
    return default if answer == '' else answer


def convert(inpath, outpath, assignee=None, milestone=None):
    with open(inpath) as f:
        lines = f.read().splitlines()

    pos = 0
    numlines = len(lines)
    issues = []
    while pos < numlines:
        line = lines[pos]
        if line.startswith('- '):
            issue_text = line[2:]
            while True:
                if pos + 1 >= numlines:
                    break
                nextline = lines[pos + 1]
                if nextline.isspace():
                    nextline = ''
                if not nextline:
                    if not issue_text.endswith('\n'):
                        issue_text += '\n'
                    issue_text += '\n'
                    pos += 1
                elif nextline.startswith('  '):
                    nextline = nextline[2:]
                    indent = len(nextline) - len(nextline.lstrip(' '))
                    keywords = ('>>> ', 'def ', '* ', '- ', '? ', '-> ')
                    usekeyword = any(nextline.startswith(kw) for kw in keywords)
                    if indent > 0 or usekeyword:
                        toadd = '\n' + nextline
                    else:
                        if issue_text[-1].isspace():
                            toadd = nextline
                        else:
                            toadd = ' ' + nextline
                    issue_text += toadd
                    pos += 1
                else:
                    break
            issue_text = issue_text.rstrip()
            print "\n", issue_text
            initial = choose('bug or enhancement?', ('b', 'e'), 'e')
            label = {'b': 'bug', 'e': 'enhancement'}[initial]
            issue = {
                'title': issue_text.splitlines()[0],
                'body': issue_text,
                'labels': [label]
            }
            if assignee is not None:
                issue['assignee'] = assignee
            if milestone is not None:
                issue['milestone'] = milestone
            issues.append(issue)
        pos += 1

    with open(outpath, 'w') as f:
        json.dump(issues, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    from sys import argv

    convert(*argv[1:])
