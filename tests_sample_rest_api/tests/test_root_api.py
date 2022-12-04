from ..testcase import client


class TestRoot():

    def test_read_root(self):
        response = client.get("/v1/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Pyfolio API V1!"}
