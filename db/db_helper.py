import pymysql
import logging

logger = logging.getLogger(__name__)


class DBHelper:
    """
    Handles all MySQL operations for Payment Gateway tests.
    Used to INSERT, SELECT, UPDATE and verify transaction data.
    """

    def __init__(self, connection):
        self.conn   = connection
        self.cursor = connection.cursor()

    # ── INSERT a new transaction record ─────────────────
    def insert_transaction(self, order_id, amount,
                               payment_method, status="PENDING"):
        sql = """
            INSERT INTO transactions
                (order_id, amount, payment_method, status)
            VALUES
                (%s, %s, %s, %s)
        """
        self.cursor.execute(sql, (order_id, amount,
                                   payment_method, status))
        self.conn.commit()
        logger.info(f"Inserted transaction: {order_id}")
        return self.cursor.lastrowid   # returns new row ID

    # ── GET transaction by order_id ──────────────────────
    def get_transaction(self, order_id):
        sql = "SELECT * FROM transactions WHERE order_id = %s"
        self.cursor.execute(sql, (order_id,))
        return self.cursor.fetchone()   # returns dict or None

    # ── UPDATE status after payment captured ─────────────
    def update_status(self, order_id, status, txn_id=None):
        sql = """
            UPDATE transactions
            SET    status = %s,
                   transaction_id = %s
            WHERE  order_id = %s
        """
        self.cursor.execute(sql, (status, txn_id, order_id))
        self.conn.commit()
        logger.info(f"Updated {order_id} → {status}")

    # ── VERIFY — assert status matches expected ──────────
    def verify_payment_status(self, order_id, expected_status):
        txn = self.get_transaction(order_id)
        assert txn is not None, \
            f"Transaction '{order_id}' not found in DB"
        assert txn["status"] == expected_status, \
            f"Expected '{expected_status}', got '{txn['status']}'"
        logger.info(f"✅ DB verified: {order_id} = {expected_status}")
        return txn

    # ── GET all transactions (for reporting) ─────────────
    def get_all_transactions(self):
        sql = "SELECT * FROM transactions ORDER BY created_at DESC"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # ── DELETE test data after test (cleanup) ────────────
    def delete_transaction(self, order_id):
        sql = "DELETE FROM transactions WHERE order_id = %s"
        self.cursor.execute(sql, (order_id,))
        self.conn.commit()
        logger.info(f"Deleted test data: {order_id}")