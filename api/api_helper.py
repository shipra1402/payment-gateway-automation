import requests

class APIHelper:

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        url = f"{self.BASE_URL}/users/{user_id}"

        response = requests.get(url)
        return response

    def create_user(self, name, job):
        url = f"{self.BASE_URL}/users"

        payload = {
            "name": name,
            "job": job
        }

        response = requests.post(url, json=payload)
        return response