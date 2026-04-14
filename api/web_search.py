import requests

class WebSearchAPI:
    def wikipedia(self, query):
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query}"
        return requests.get(url).json()

    def github(self, query):
        url = f"https://api.github.com/search/repositories?q={query}"
        return requests.get(url).json()

    def pypi(self, package):
        url = f"https://pypi.org/pypi/{package}/json"
        return requests.get(url).json()

    def youtube_future(self, query):
        return {
            "status": "future implementation",
            "provider": "youtube"
        }

    def bing_future(self, query):
        return {
            "status": "future implementation",
            "provider": "bing"
        }
