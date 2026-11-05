import requests
from frontend.config import BASE_URL


class ApiClient:
    def __init__(self):
        self.token = None
        self.user = None

    def _h(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def post(self, path, **kw):
        return requests.post(BASE_URL + path, headers=self._h(), **kw)

    def get(self, path, **kw):
        return requests.get(BASE_URL + path, headers=self._h(), **kw)

    def put(self, path, **kw):
        return requests.put(BASE_URL + path, headers=self._h(), **kw)

    def delete(self, path, **kw):
        return requests.delete(BASE_URL + path, headers=self._h(), **kw)


api = ApiClient()
