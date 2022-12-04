from ..testcase import client


class TestRoot():

    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
