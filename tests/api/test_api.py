import time
import pytest
from api.api_helper import APIHelper


class TestProductAPI:
    """
    Test Suite: E-Commerce Product & Customer API
    Site: https://jsonplaceholder.typicode.com
    Simulates product catalogue and customer REST operations.
    """

    # ── TC01: Get single product ─────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_product(self):
        api = APIHelper()
        response = api.get_product(1)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    # ── TC02: Get all products ───────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_products(self):
        api = APIHelper()
        response = api.get_all_products()

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), \
            "Expected list of products"
        assert len(data) > 0, \
            "Product catalogue should not be empty"

    # ── TC03: Create product listing ─────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_product(self):
        api = APIHelper()
        response = api.create_product(
            "Wireless Headphones",
            "Noise-cancelling over-ear headphones"
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Wireless Headphones"
        assert "id" in data, "Expected ID in response"

    # ── TC04: Update product details ─────────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_product(self):
        api = APIHelper()
        response = api.update_product(
            1,
            "Wireless Headphones - Updated",
            "Updated product description"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Wireless Headphones - Updated"

    # ── TC05: Delete product ─────────────────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_product(self):
        api = APIHelper()
        response = api.delete_product(1)

        assert response.status_code == 200

    # ── TC06: Invalid product returns 404 ────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_invalid_product_returns_404(self):
        api = APIHelper()
        response = api.get_product(99999)

        assert response.status_code == 404

    # ── TC07: API response time under 3 seconds ──────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_api_response_time(self):
        api = APIHelper()
        start = time.time()
        response = api.get_product(1)
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 3.0, \
            f"Response too slow: {duration:.2f}s"

    # ── TC08: Product response has required fields ────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_product_response_schema(self):
        api = APIHelper()
        response = api.get_product(1)

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert "userId" in data

    # ── TC09: Get single customer ─────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_customer(self):
        api = APIHelper()
        response = api.get_customer(1)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "email" in data
        assert "username" in data

    # ── TC10: Get all customers ───────────────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_all_customers(self):
        api = APIHelper()
        response = api.get_all_customers()

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), \
            "Expected list of customers"
        assert len(data) > 0, \
            "Customer list should not be empty"
