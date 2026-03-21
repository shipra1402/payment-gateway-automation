import time
import pytest
from api.api_helper import APIHelper
from db.db_helper import DBHelper


class TestAPI:
    """
    Test Suite: REST API validation
    Site: https://jsonplaceholder.typicode.com
    """

    # ── TC01: Get single user ────────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_user(self):
        api = APIHelper()
        response = api.get_user(1)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    # ── TC02: Get all users ──────────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_users(self):
        api = APIHelper()
        response = api.get_all_users()

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Expected list response"
        assert len(data) > 0, "Expected non-empty list"

    # ── TC03: Create user ────────────────────────────────
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_user(self):
        api = APIHelper()
        response = api.create_user("Shipra", "QA Engineer")

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Shipra"
        assert "id" in data, "Expected ID in response"

    # ── TC04: Update user ────────────────────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_user(self):
        api = APIHelper()
        response = api.update_user(1, "Shipra Updated", "Senior QA")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Shipra Updated"

    # ── TC05: Delete user ────────────────────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_user(self):
        api = APIHelper()
        response = api.delete_user(1)

        assert response.status_code == 200

    # ── TC06: Invalid user returns 404 ───────────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_invalid_user_returns_404(self):
        api = APIHelper()
        response = api.get_user(9999)

        assert response.status_code == 404

    # ── TC07: Response time under 3 seconds ──────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_api_response_time(self):
        api = APIHelper()
        start = time.time()
        response = api.get_user(1)
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 3.0, \
            f"Response too slow: {duration:.2f}s"

    # ── TC08: Response has required fields ───────────────
    @pytest.mark.api
    @pytest.mark.regression
    def test_user_response_schema(self):
        api = APIHelper()
        response = api.get_user(1)

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "email" in data
        assert "username" in data


class TestDatabase:
    """
    Test Suite: MySQL DB transaction validation
    """

    # ── TC01: Insert and verify SUCCESS transaction ───────
    @pytest.mark.db
    @pytest.mark.smoke
    def test_insert_and_verify_transaction(self, db_connection):
        db = DBHelper(db_connection)
        order_id = "ORD_DB_001"

        db.insert_transaction(
            order_id=order_id,
            amount=500.00,
            payment_method="UPI",
            status="SUCCESS"
        )

        txn = db.get_transaction(order_id)
        assert txn["status"] == "SUCCESS"
        db.delete_transaction(order_id)

    # ── TC02: Insert FAILED transaction ──────────────────
    @pytest.mark.db
    @pytest.mark.regression
    def test_failed_transaction_recorded(self, db_connection):
        db = DBHelper(db_connection)
        order_id = "ORD_DB_002"

        db.insert_transaction(
            order_id=order_id,
            amount=999.00,
            payment_method="CARD",
            status="FAILED"
        )

        txn = db.get_transaction(order_id)
        assert txn["status"] == "FAILED", \
            f"Expected FAILED, got: {txn['status']}"
        db.delete_transaction(order_id)

    # ── TC03: Duplicate order ID raises exception ─────────
    @pytest.mark.db
    @pytest.mark.regression
    def test_duplicate_order_id(self, db_connection):
        db = DBHelper(db_connection)
        order_id = "ORD_DB_DUP"

        db.insert_transaction(
            order_id=order_id,
            amount=100.00,
            payment_method="UPI",
            status="SUCCESS"
        )

        with pytest.raises(Exception):
            db.insert_transaction(
                order_id=order_id,
                amount=200.00,
                payment_method="UPI",
                status="SUCCESS"
            )

        db.delete_transaction(order_id)