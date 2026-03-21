import pytest
from api.api_helper import APIHelper
from db.db_helper import DBHelper


class TestAPI:

    def test_get_user(self):
        api = APIHelper()
        response = api.get_user(1)

        assert response.status_code == 200

        data = response.json()
        assert data["id"] == 1


    def test_create_user_api(self):
        api = APIHelper()
        response = api.create_user("Shipra", "QA")

        assert response.status_code == 201

        data = response.json()
        assert data["name"] == "Shipra"


    def test_invalid_user_returns_404(self):
        api = APIHelper()
        response = api.get_user(9999)

        assert response.status_code == 404


# 🔥 Separate DB tests (VERY IMPORTANT)

class TestDatabase:

    @pytest.mark.db
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