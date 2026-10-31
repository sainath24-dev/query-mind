import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert data["project"] == "QueryMind"
        assert data["status"] == "online"


@pytest.mark.asyncio
async def test_schema_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/schema")
        assert res.status_code == 200
        data = res.json()
        table_names = [t["name"] for t in data["tables"]]
        assert "students" in table_names
        assert "departments" in table_names
        assert "marks" in table_names
        assert "attendance" in table_names
        assert len(data["relationships"]) > 0


@pytest.mark.asyncio
async def test_dashboard_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/dashboard")
        assert res.status_code == 200
        data = res.json()
        assert data["total_students"] >= 5000
        assert data["total_departments"] == 10
        assert data["total_faculty"] >= 100
        assert data["average_cgpa"] > 0
        assert len(data["department_distribution"]) == 10


@pytest.mark.asyncio
async def test_query_top_students():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/query", json={"question": "Who are the top 10 students by CGPA?"})
        assert res.status_code == 200
        data = res.json()
        assert data["intent"] == "TOP_N"
        assert data["status"] == "SUCCESS"
        assert data["row_count"] == 10
        assert len(data["rows"]) == 10
        assert "SELECT" in data["sql"]
        assert data["execution_time_ms"] > 0
        assert len(data["explanation"]) > 0


@pytest.mark.asyncio
async def test_query_department_count():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/query", json={"question": "How many students are enrolled in each department?"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "SUCCESS"
        assert data["row_count"] == 10
        assert data["visualization"]["can_visualize"] is True
        assert data["visualization"]["recommended_chart"] == "bar"


@pytest.mark.asyncio
async def test_query_unanswerable():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/query", json={"question": "What is the average salary of employees?"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_answerable"] is False
        assert "salary information" in data["explanation"].lower()


@pytest.mark.asyncio
async def test_query_security_rejection_delete():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/query", json={"question": "Delete all students."})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] in ["ERROR", "UNANSWERABLE"] or "prohibited" in data["explanation"].lower() or "rejected" in data["explanation"].lower()


@pytest.mark.asyncio
async def test_query_security_rejection_drop():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/query/validate", json={"sql": "DROP TABLE students;"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_safe"] is False
        assert "DROP" in data["error_message"]
