import requests
import logging
from flask.globals import request
from flask.wrappers import Response
from app.models import version_control_info
# api calls to bitbucket so that info can be retrieved

# returns an object with selected information from bitbucket api call, takes in the bitbucket team name
def bitbucket_service(team):
    try:
        logging.info("Calling Bitbucket API for team: %s" %(team))
        response = requests.get('https://bitbucket.org/api/2.0/repositories/%s' %(team))
        data = response.json()
        response.raise_for_status()
    except:
        # check for errors calling Bitbucket API, if error occured return a object with error message
        logging.error("Failed to call Bitbucket API for team: %s" %(team))
        return version_control_info.VCInfo(source="Bitbucket", error_message=('Failed to reach Bitbucket'))

    total_watchers = 0
    total_public_repos = 0
    languages_used = set()

    # Check if values key exists, values is the object containing repos, if not there return empty object
    # with error message
    if 'values' in data:
        repos = data['values']
    else: 
        return version_control_info.VCInfo(source="Bitbucket", error_message=('No repos are available'))

    # iterate through each repo look for respective key and condition, update the variable in question
    for repo in repos: 
        if 'is_private' in repo and repo['is_private'] == False:
            total_public_repos += 1
            # Main API call has no watchers/followers info, so need to call the watchers url for each repo, 
            # then tally the watchers from each request
            if 'links' in repo: 
                if 'watchers' in repo['links']:
                    if 'href' in repo['links']['watchers']:
                        total_watchers += getWatchers(repo['links']['watchers']['href'])
            if 'language' in repo:
                languages_used.add(repo['language'])
    
    # Bitbucket has no topic or fork vs original data
    return version_control_info.VCInfo(None, "Bitbucket", total_public_repos, None, total_watchers,
     list(languages_used), None)

# makes call to watchers api for repo and retrives the total watchers as an int if none are found, returns 0
def getWatchers(url):
    response = requests.get(url)
    data = response.json()

    if 'size' in data: 
        return data['size']
    else: 
        return 0