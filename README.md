# Coding Challenge App

A skeleton flask app to use for a coding challenge. Something

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code
```
python -m run or flask run
```

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```

```
curl -i "http://127.0.0.1:5000/version-control-info?github_org=<GITHUB_ORG>&bitbucket_team=<BITBUCKET_TEAM>"
```

## Running Tests

```
python3 -m unittest discover .
```

## What'd I'd like to improve on...

Better handle query params
    - account for missing parameters.

Improve error handling around nested API calls.

Use ENVs or Consts for important static variables i.e. API urls.

Add tests more tests
    - when an error occurs, no team/repos/watchers when making API calls.
    - different user inputs for the query parameters.

Add error handling tests around api.
    - add specifics, like returning a better message depending on what the error was i.e. 404, 401 etc.

Make async.
    - needs to better handle multiple requests.

## Other Questions

● How do you handle versions of external APIs - are some versions better suited to solve our problem?

    Each external dependency is its own service which can have different functions that handle the different versions of the API and they can be interchanged as needed even combined. Current versions seemed to have what we needed for the most part.

● How do you/would you handle a failed network call to Github/Bitbucket?

    Catch the error and display a meaningful message to the user.
    ○ What do you return to the client?
        A default object with an error message. Code can fail in either the Bitbucket API or Github API but user might still want to see the results for one of the APIs.

● Which REST verbs and URI structure makes the most sense?

    GET makes the most sense since we are retrieving information for an external dependency not publishing or deleting. In terms of URI, query parameters make the most sense since they make it easy to make the parameters optional in the future in case we want to expand, sort or data in the future.

● How efficient is your code?

    Fairly efficient in terms of time complexity, iterating only once over the list of repos in the team. Space complexity can probably use some simplification to not store some values in variables. Makes it easy for now though so it's easier to understand.
