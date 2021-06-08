
# Common class used to combine both Github and Bitbucket into a common ground response
class VCInfo:

    def __init__(self, error_message = None, source = None, original_repo_count = None, forked_repo_count = None, watchers = None, languages = None, repo_topics = None):
        if error_message != None:
            self.error = error_message
        else:
            self.error = None
        self.source = source
        self.total_public_repos_original = original_repo_count
        self.total_public_repos_forked = forked_repo_count
        self.total_watchers = watchers
        self.languages = languages
        self.languages_count = len(languages) if languages != None else 0
        self.repo_topics = repo_topics
        self.repo_topics_count = len(repo_topics) if repo_topics != None else 0

    # JSON format serializer
    def serialize(self):
        return {"source": self.source,
                "error": self.error,
                "total_public_repos_original": self.total_public_repos_original,
                "total_public_repos_forked": self.total_public_repos_forked,
                "total_watchers": self.total_watchers,
                "languages": self.languages,
                "languages_count": self.languages_count,
                "repo_topics": self.repo_topics,
                "repo_topics_count": self.repo_topics_count }