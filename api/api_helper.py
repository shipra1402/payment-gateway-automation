import requests


class APIHelper:
    """
    API Helper for e-commerce REST API tests.
    Site: https://jsonplaceholder.typicode.com
    Simulates product, order, and user API operations.
    """

    BASE_URL = "https://jsonplaceholder.typicode.com"

    # ── PRODUCTS ─────────────────────────────────────────

    def get_product(self, product_id):
        """GET single product by ID"""
        url = f"{self.BASE_URL}/posts/{product_id}"
        return requests.get(url)

    def get_all_products(self):
        """GET all products — catalogue listing"""
        url = f"{self.BASE_URL}/posts"
        return requests.get(url)

    def create_product(self, title, body):
        """POST create new product listing"""
        url = f"{self.BASE_URL}/posts"
        payload = {
            "title": title,
            "body": body,
            "userId": 1
        }
        return requests.post(url, json=payload)

    def update_product(self, product_id, title, body):
        """PUT update existing product details"""
        url = f"{self.BASE_URL}/posts/{product_id}"
        payload = {
            "title": title,
            "body": body,
            "userId": 1
        }
        return requests.put(url, json=payload)

    def delete_product(self, product_id):
        """DELETE product by ID"""
        url = f"{self.BASE_URL}/posts/{product_id}"
        return requests.delete(url)

    # ── USERS ────────────────────────────────────────────

    def get_customer(self, customer_id):
        """GET single customer by ID"""
        url = f"{self.BASE_URL}/users/{customer_id}"
        return requests.get(url)

    def get_all_customers(self):
        """GET all customers"""
        url = f"{self.BASE_URL}/users"
        return requests.get(url)
