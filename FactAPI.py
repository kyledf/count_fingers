import requests


class FactAPI:
    def __init__(self, number):
        self.number = number
        url = f"https://numbersapi.p.rapidapi.com/{self.number}/trivia"
        querystring = {"fragment": "true", "json": "true"}
        headers = {
            "X-RapidAPI-Key": "165bd3c90bmsh9b4ca13cccf62fep1adbb4jsn1d1be4386948",
            "X-RapidAPI-Host": "numbersapi.p.rapidapi.com"
        }
        self.response = requests.get(url, headers=headers, params=querystring)

    def get_fact(self):
        return self.response.json().get("text")
