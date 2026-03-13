"""
Pytest test suite for the A&D Supply Chain Platform.
Tests the database schema, FastAPI endpoints, and SQL sanitization logic.
"""
import sqlite3
import os
import sys
import pytest

# Ensure imports work from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDatabaseSchema:
    """Validates the SQLite database schema and seed data integrity."""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Seed the database before tests."""
        from backend.db_init import init_db
        init_db()
        self.db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "supply_chain.db"
        )

    def test_database_exists(self):
        assert os.path.exists(self.db_path), "Database file should exist after init"

    def test_suppliers_table_has_rows(self):
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM Suppliers").fetchone()[0]
        conn.close()
        assert count >= 3, "Suppliers table should have at least 3 seed rows"

    def test_parts_table_has_rows(self):
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM Parts").fetchone()[0]
        conn.close()
        assert count >= 3, "Parts table should have at least 3 seed rows"

    def test_work_orders_table_has_rows(self):
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM WorkOrders").fetchone()[0]
        conn.close()
        assert count >= 3, "WorkOrders table should have at least 3 seed rows"

    def test_supplier_location_column_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("PRAGMA table_info(Suppliers)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        assert "location" in columns, "Suppliers table must include a location column"

    def test_seattle_supplier_exists(self):
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT name FROM Suppliers WHERE location = 'Seattle'"
        ).fetchall()
        conn.close()
        assert len(rows) >= 1, "At least one supplier should be located in Seattle"


class TestSQLSanitization:
    """Validates the clean_sql() preprocessing function."""

    def test_strips_sql_query_prefix(self):
        from rag.nlp_agent import clean_sql
        raw = 'SQLQuery: SELECT * FROM Suppliers'
        assert clean_sql(raw) == 'SELECT * FROM Suppliers'

    def test_strips_markdown_code_block(self):
        from rag.nlp_agent import clean_sql
        raw = '```sql\nSELECT * FROM Parts\n```'
        assert clean_sql(raw) == 'SELECT * FROM Parts'

    def test_passes_clean_sql_through(self):
        from rag.nlp_agent import clean_sql
        raw = 'SELECT name FROM Suppliers WHERE location = "Seattle"'
        assert clean_sql(raw) == raw


class TestFastAPIEndpoints:
    """Tests the FastAPI application endpoints."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        from backend.db_init import init_db
        init_db()
        from fastapi.testclient import TestClient
        from backend.main import app
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_schema_endpoint(self):
        response = self.client.get("/api/schema")
        assert response.status_code == 200
        data = response.json()
        assert "schema" in data
        assert "Suppliers" in data["schema"]
        assert "Parts" in data["schema"]
        assert "WorkOrders" in data["schema"]

    def test_docs_list_endpoint(self):
        response = self.client.get("/api/docs")
        assert response.status_code == 200
        assert "docs" in response.json()

    def test_chat_with_fake_key(self):
        response = self.client.post("/api/chat", json={
            "prompt": "List all suppliers",
            "api_key": "fake-key-for-testing"
        })
        assert response.status_code == 200
        assert "Simulated Response" in response.json()["response"]
