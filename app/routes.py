import logging
from flask import jsonify
from flask import Flask, Response, request
from app.services import bitbucket_service
from app.services import github_service

app = Flask("user_profiles_api")

@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    logging.info("Health Check!")
    return Response("All Good!", status=200)

@app.route("/api/v1/version-control-info", methods=["GET"]) 
def version_control_info():
    """
    Endpoint to get aggregate github and bitbucket data
    """
    logging.info("Aggregating Results")
    github_org = request.args.get('github_org')
    bitbucket_team = request.args.get('bitbucket_team')
    
    github_response = github_service.github_service(github_org)
    bitbucket_response = bitbucket_service.bitbucket_service(bitbucket_team)

    return jsonify(github_response.serialize(), bitbucket_response.serialize())
