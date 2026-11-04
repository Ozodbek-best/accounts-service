"""Tests for the Accounts service"""
import unittest
from service import app
from service.models import db

BASE_URL = "/accounts"
ACCOUNT = {
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St",
    "phone_number": "555-1234",
}


class TestAccountService(unittest.TestCase):
    """Account service tests"""

    def setUp(self):
        app.config["TESTING"] = True
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_create_account(self):
        """It should create an Account"""
        resp = self.client.post(BASE_URL, json=ACCOUNT)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["name"], ACCOUNT["name"])

    def test_create_bad_data(self):
        """It should not create an Account with missing data"""
        resp = self.client.post(BASE_URL, json={"name": "no email"})
        self.assertEqual(resp.status_code, 400)

    def test_list_accounts(self):
        """It should list all Accounts"""
        self.client.post(BASE_URL, json=ACCOUNT)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

    def test_read_account(self):
        """It should read an Account"""
        created = self.client.post(BASE_URL, json=ACCOUNT).get_json()
        resp = self.client.get(f"{BASE_URL}/{created['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["email"], ACCOUNT["email"])

    def test_read_not_found(self):
        """It should not read an Account that does not exist"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, 404)

    def test_update_account(self):
        """It should update an Account"""
        created = self.client.post(BASE_URL, json=ACCOUNT).get_json()
        created["name"] = "Jane Doe"
        resp = self.client.put(f"{BASE_URL}/{created['id']}", json=created)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Jane Doe")

    def test_update_not_found(self):
        """It should not update an Account that does not exist"""
        resp = self.client.put(f"{BASE_URL}/0", json=ACCOUNT)
        self.assertEqual(resp.status_code, 404)

    def test_delete_account(self):
        """It should delete an Account"""
        created = self.client.post(BASE_URL, json=ACCOUNT).get_json()
        resp = self.client.delete(f"{BASE_URL}/{created['id']}")
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get(f"{BASE_URL}/{created['id']}")
        self.assertEqual(resp.status_code, 404)
