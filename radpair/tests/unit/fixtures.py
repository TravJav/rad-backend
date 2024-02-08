from faker import Faker

Faker.seed(4321)
faker = Faker()
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3MDQ5NDU5NjksImV4cCI6MTczNjQ4MTk2OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.dgnEVHT-uQd-X8PjYHuAZxeKh-PVxRY95ApAdbENDhw"
jwt = {"Authorization": "Bearer {}".format(access_token)}


def mock_jwt_required(realm):
    return jwt



def expected_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }


def bad_headers():
    return {
        "Content-Type": "application/json",
        "host": faker.company_suffix(),
        "Authorization": "Bearer {}".format(access_token),
    }
