import pytest
from starlette.testclient import TestClient

from app import app

client = TestClient(app)


# def test_user_sync_e2e(uow):
#     data = {
#         "username": "DGPARK",
#         "password": "ktc1234!",
#         "service_name": "27809"
#     }
#     headers = {
#         "X-Internal-Secret": "test-test-test"  # 여기에 인증용 시크릿 키 넣기
#     }
#
#     response = client.post(
#         "/api/v1/sync/user",
#         json=data,
#         headers=headers
#     )
#     print(response.json())
