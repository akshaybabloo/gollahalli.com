---
title: Retrieving User Repositories Using Github Api With Little Help of Python 3
date: 2018-06-30T11:20:32+12:00
draft: false
categories: ["Tutorial"]
tags: ["Python-3"]
description: "How to retrieve GitHub users repository? If thats the question you have, then this blog post is for you."
---

There are different ways to retrieve user repositories; one such is using Python libraries, but they usually need your API keys even though your repository is public. We could do this by using GitHub's API v3 HTTP request.

For example, to retrieve my public libraries I would use https://api.github.com/users/akshaybabloo/repos, this returns a JSON array; we just have to use the Python's json library to get the desired key-value pairs (in Python's terminology - Dictionary).

## Code

Lets build a custom iterator for the class GitHubRepo.

```python
class GitHubRepo:
    def __init__(self):
          response = urlopen(DEFAULT_BASE_URL) # Open the url
          data = response.read().decode("utf-8") # Encode the content as UTF-8

            self.data = json.loads(data)  # Load the JSON list
            self.index = len(self.data)  # Get the length of the JSOn list
            del response  # Delete unused variable (Optional)
            del data  # Delete unused variable (Optional)

    def __iter__(self):
        """
        Creating an iterator, which returns itself.
        """
        return self

    def __next__(self):
        """
        Continues the loop until the index reaches 0.
        """
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]
```

iter and next are the built-in iterator types.

You are essentially making the GitHubRepo object loopable, for example, let us consider the following snippet:

```
>>> x = [1, 2, 3]
>>> y = iter(x)
>>> next(y)
1
>>> next(y)
2
>>> next(y)
3
>>> next(y)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Once there are no more indexes to reach, the program raises a StopIteration exception and exits. The above terminal code can be written as:

```python
x = [1, 2, 3]
for y in x:
    print(y)

# 1
# 2
# 3
```

GitHub JSON structure
The next thing you should know is the structure of the JSON Objects that is requested from GitHub.

```json
{
    "id": 66637386,
    "name": "Abies",
    "full_name": "akshaybabloo/Abies",
    "owner": {
      "login": "akshaybabloo",
      "id": 7360286,
      "avatar_url": "https://avatars.githubusercontent.com/u/7360286?v=3",
      "gravatar_id": "",
      "url": "https://api.github.com/users/akshaybabloo",
      "html_url": "https://github.com/akshaybabloo",
      "followers_url": "https://api.github.com/users/akshaybabloo/followers",
      "following_url": "https://api.github.com/users/akshaybabloo/following{/other_user}",
      "gists_url": "https://api.github.com/users/akshaybabloo/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/akshaybabloo/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/akshaybabloo/subscriptions",
      "organizations_url": "https://api.github.com/users/akshaybabloo/orgs",
      "repos_url": "https://api.github.com/users/akshaybabloo/repos",
      "events_url": "https://api.github.com/users/akshaybabloo/events{/privacy}",
      "received_events_url": "https://api.github.com/users/akshaybabloo/received_events",
      "type": "User",
      "site_admin": false
    },
    "private": false,
    "html_url": "https://github.com/akshaybabloo/Abies",
    "description": ":evergreen_tree: A Django based all-in-one web creator.",
    "fork": false,
    "url": "https://api.github.com/repos/akshaybabloo/Abies",
    "forks_url": "https://api.github.com/repos/akshaybabloo/Abies/forks",
    "keys_url": "https://api.github.com/repos/akshaybabloo/Abies/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/akshaybabloo/Abies/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/akshaybabloo/Abies/teams",
    "hooks_url": "https://api.github.com/repos/akshaybabloo/Abies/hooks",
    "issue_events_url": "https://api.github.com/repos/akshaybabloo/Abies/issues/events{/number}",
    "events_url": "https://api.github.com/repos/akshaybabloo/Abies/events",
    "assignees_url": "https://api.github.com/repos/akshaybabloo/Abies/assignees{/user}",
    "branches_url": "https://api.github.com/repos/akshaybabloo/Abies/branches{/branch}",
    "tags_url": "https://api.github.com/repos/akshaybabloo/Abies/tags",
    "blobs_url": "https://api.github.com/repos/akshaybabloo/Abies/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/akshaybabloo/Abies/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/akshaybabloo/Abies/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/akshaybabloo/Abies/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/akshaybabloo/Abies/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/akshaybabloo/Abies/languages",
    "stargazers_url": "https://api.github.com/repos/akshaybabloo/Abies/stargazers",
    "contributors_url": "https://api.github.com/repos/akshaybabloo/Abies/contributors",
    "subscribers_url": "https://api.github.com/repos/akshaybabloo/Abies/subscribers",
    "subscription_url": "https://api.github.com/repos/akshaybabloo/Abies/subscription",
    "commits_url": "https://api.github.com/repos/akshaybabloo/Abies/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/akshaybabloo/Abies/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/akshaybabloo/Abies/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/akshaybabloo/Abies/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/akshaybabloo/Abies/contents/{+path}",
    "compare_url": "https://api.github.com/repos/akshaybabloo/Abies/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/akshaybabloo/Abies/merges",
    "archive_url": "https://api.github.com/repos/akshaybabloo/Abies/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/akshaybabloo/Abies/downloads",
    "issues_url": "https://api.github.com/repos/akshaybabloo/Abies/issues{/number}",
    "pulls_url": "https://api.github.com/repos/akshaybabloo/Abies/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/akshaybabloo/Abies/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/akshaybabloo/Abies/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/akshaybabloo/Abies/labels{/name}",
    "releases_url": "https://api.github.com/repos/akshaybabloo/Abies/releases{/id}",
    "deployments_url": "https://api.github.com/repos/akshaybabloo/Abies/deployments",
    "created_at": "2016-08-26T09:56:00Z",
    "updated_at": "2016-12-28T20:13:49Z",
    "pushed_at": "2016-11-24T12:07:57Z",
    "git_url": "git://github.com/akshaybabloo/Abies.git",
    "ssh_url": "git@github.com:akshaybabloo/Abies.git",
    "clone_url": "https://github.com/akshaybabloo/Abies.git",
    "svn_url": "https://github.com/akshaybabloo/Abies",
    "homepage": "https://abies.herokuapp.com/",
    "size": 2079,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "JavaScript",
    "has_issues": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "open_issues_count": 0,
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master"
  },
...
```

Once you know what information you want from the JSON Object, just call by its key, for example, using the same **GitHubRepo** class we could do the following:

```python
repo = GitHubRepo()
for data in repo:
    print(data['name'])

# In my case it will print:
#
# Ruby-notes
# RemindMe
# Python3-notes
# Python-QT-5-Tutorial
# Python-opengl-notes
# Python-CUDA
# PyMark
# php-mysql-notes
# NeuroRehab
# Maven-notes
# Machine-Learning
# JMark
# JCal
# JavaScript-Tutorial
# JavaFX
# Java-JDBC-notes
# GUpdater
# GearVR-UnrealEngine4
# EmoWin
# Emotiv-Matlab
# EmoPy
# EEGRotor-VE
# Dotfiles
# CV
# CPP-Notes
# Cognionics-LabStreamingLayer-Matlab
# Casper
# C-notes
# Auro
# Abies
```
