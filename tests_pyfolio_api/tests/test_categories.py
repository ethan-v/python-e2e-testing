from faker import Faker
from pytest_schema import schema, Or
from ..testcase import client

fake = Faker()

caregory = {
    "id": int,
    "title": str,
    "slug": str,
    "icon": Or(None, str),
    "image": Or(None, str),
    "description": Or(None, str),
    "is_active": bool,
    "created_at": Or(None, str),
    "updated_at": Or(None, str),
}

category_detail_structure = {
    "message": Or(None, str),
    "data": caregory
}

category_list_structure = {
    "message": Or(None, str),
    "data": {
        "total": int,
        "limit": int,
        "skip": int,
        "total_page": int,
        "next_page_link": Or(None, str),
        "items": [
            caregory
        ]
    }
}



class TestCategoryApi:

    def test_read_category_list(self):
        response = client.get("/v1/categories")
        data = response.json()
        assert response.status_code == 200
        assert schema(category_list_structure) == data
