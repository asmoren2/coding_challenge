import requests
import logging
from flask.wrappers import Response
from app.models import version_control_info

# Service that makes api calls to Github so that info can be retrieved for specified organization

# returns an object with selected information from Github api call, takes in the Github Org name
def github_service(github_org):
    try:
        logging.info("Calling Github API for org: %s" %(github_org))
        response = requests.get('https://api.github.com/orgs/%s/repos' %(github_org))
        repos = response.json()
        response.raise_for_status()
    except:
        # check for errors calling Github API, if error occured return a object with error message
        logging.error("Failed to call Github API for org: %s" %(github_org))
        return version_control_info.VCInfo(source="Github", error_message=('Failed to reach Github'))

    public_repos_count = 0
    forked_repos_count = 0
    total_watcher_count = 0
    languages_used = set()
    topics = []

    # iterate through each repo look for respective key and condition, update the variable in question
    for repo in repos:
        if 'private' in repo and repo['private'] == False:
            if 'fork' in repo and repo['fork'] == False:
                public_repos_count += 1
            else: 
                forked_repos_count += 1
            if 'language' in repo and repo['language']:
                languages_used.add(repo['language'])
        if 'watchers_count' in repo and repo['watchers_count']:
             total_watcher_count += repo['watchers_count']
        if 'topics' in repo:
             topics.extend(repo['topics'])

    # remove duplicates from the topics list
    unique_topics = set(topics)

    return version_control_info.VCInfo(None, "Github", public_repos_count, forked_repos_count,
     total_watcher_count, list(languages_used), list(unique_topics))
