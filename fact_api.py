import requests


class FactAPI:
    def __init__(self):
        self.querystring = {"fragment": "true", "json": "true"}
        self.headers = {
            "X-RapidAPI-Key": "165bd3c90bmsh9b4ca13cccf62fep1adbb4jsn1d1be4386948",
            "X-RapidAPI-Host": "numbersapi.p.rapidapi.com"
        }

    def get_fact(self, number):
        url = f"https://numbersapi.p.rapidapi.com/{number}/trivia"
        response = requests.get(url, headers=self.headers, params=self.querystring)
        # if text is over 120 characters long, get a new fact
        while len(response.json().get("text")) > 120:
            response = requests.get(url, headers=self.headers, params=self.querystring)
        return response.json().get("text")
