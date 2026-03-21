import requests


class APIHelper:

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        """GET single user by ID"""
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.get(url)
        return response

    def get_all_users(self):
        """GET all users — list validation"""
        url = f"{self.BASE_URL}/users"
        response = requests.get(url)
        return response

    def create_user(self, name, job):
        """POST create new user"""
        url = f"{self.BASE_URL}/posts"
        payload = {
            "name": name,
            "job": job,
            "userId": 1
        }
        response = requests.post(url, json=payload)
        return response

    def update_user(self, user_id, name, job):
        """PUT update existing user"""
        url = f"{self.BASE_URL}/posts/{user_id}"
        payload = {
            "name": name,
            "job": job
        }
        response = requests.put(url, json=payload)
        return response

    def delete_user(self, user_id):
        """DELETE user by ID"""
        url = f"{self.BASE_URL}/posts/{user_id}"
        response = requests.delete(url)
        return response