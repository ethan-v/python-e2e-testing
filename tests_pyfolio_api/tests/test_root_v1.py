from ..testcase import client



class TestUserInfo():

    def test_read_root(self):
        response = client.get("/v1/")
        assert response.status_code == 200
