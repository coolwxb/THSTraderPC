import base64
import urllib
import requests

API_KEY = "G2Y3k7G8k3vsndpaV53mpBzp"
SECRET_KEY = "u1OZ3tFrfFgw7Fc2OfO1VtkhWCZuKUlG"


def baidu_ocr(payload):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\605588.png",True) 方法获取
    payload=f'image={payload}&detect_direction=false&paragraph=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    print(baidu_ocr(
        'iVBORw0KGgoAAAANSUhEUgAAAcIAAAAeCAIAAAAw8YnyAAAIrUlEQVR4nO2cP2%2BjThPHJ5hzIvZl2FIipXBDeRLdIbmxRF7AFqkeCgp3zgsInQsKuhS8ACO5seQS6UoaipMSCb%2BMtRKCya%2Fgj7HNgh3HF9%2Bj%2BSjNLTvLztoM35ld34UkSYAgCPKv8fPnz9%2B%2Ff5%2FDXYRTTwJBEOT%2Fm4tfv3599xwQBEH%2BYS4wqUcQBDkGTOoRBEGOAsMogiDIUQhyHLCIVl2SzbfATLiWchywN1Mu%2FzOiANRdMjfe59ay%2BcbYkrElW08gMYNl3lgafA2vQ6PhBtRd5q4lZpD3r12KOqdOshS7U93bkEZ7LwV1mVvpMr%2F%2FYQb5PAOWsW1NXRbUznKnQ2mwBlNodpC6bC8anK52cD34zjzLTuzepMYQOUMEbzVT2g7natd4zR%2FI7ceSPkRg%2FRj52yaOJukQNYYP6i69fkshEiESIdkEZPO9P7siRCJEUiwwvO2YwuvQaJjfNWJBLJddc5NiPoy%2FFP6kFaoRL5ydYikA0nC8tNUDDeU4sD8spWkp%2FiLUZV5%2FppAUreSgGTBW42BlB9l8KgZTLDC8T0T1Eo5GNtDnAHOd7KDxnhGug7IZ2B1L4czTH%2FXKwytWCKH16DQbImfIhSRJELssmZLtCCKbb0%2FwozeqyvvlOHiAniZSdzl8ueqNBEgH0cG286gxbxNNrL6rHAdeMt654yaxyyLQJf73l9eBb0gjNhSUnni7nnZiBq9GF0Kr5AURBiyqebo3HDzRUmTt4k3w2p9dVXwKHEPqLm0obsdbCurWhq982vpO9KAus2G3uQbZDLzr8a5F1v54E3j9mdLbfQs1dqibz%2Fc7uDlQw7DlywcZImeBAAAydELhD2Typ9CenrHaUaNLFsQyxK6XjDUR5HjYaY%2FhPU0qVYjtoZCLI4loIkDssorEVr5bgSV%2B2xeDRrZaVqMtS5GyOFUsBbRSQcf7U6wWAMDplsIXe7WvGY5hctOB%2BbQI2eJ0DupgVw7nGkyxwtBSCIfDnl3qVuW%2B8l0fMpW1iT%2Fq1d%2BgsUMd3%2B6gfNOB%2BbRodqZzUAccWSmbQzWXogcZImeCwJbMi2Am5O96Uc8ffn0Oc709z3vOdYnoIizAp4kKsc2WzEvGPdEZXRIiEXJlhS3rXqzUDJskd%2F3V4hmKamZ1skwTFcRpzfec14HXLseBHUM38gZCmgXPoWU9ipMZGF7%2BksiWQtTI5chPi4xFHSN2S%2FVHf3RJNBH%2BzlIcYJhcd%2FcbIOX2urt4Lua5Z6FUtfevG8p3%2Fe7iGYpC4BeX%2BuhALcecXT7lYGcY7D1TnoO3%2B38Q9MHozse52j7AEDkXBCIRIpVzxoGbPZm2CqqdTPOoqjkATptoIjhtQiSii3N9Sy6t%2Bk9vJekaURC1TItto9rvcC8RIhGlDcbrzr5DxOw4rFGsvA41hr7Yy7UhdZeMJVNyOfLBH%2F2wrHYhMzfSZ6dNyA944u8U%2FYWl4MMxbL38Wff589KqGYEO1BAGQfboyzed9ZWagLNTOkxFnaNx9J1qP8H9V9Uyy7N3mb1WcdVdPuUgzO6JvjC8rRfEoQ6Gmx9EyJ%2Fj1qtgT0PkbNgtfE61ct4a2xtJfSHHYncgpN8omoXdV6MLXWitM9nanDQs9mR8cbyZeFJ3yew4L1ZWwOvQaAiQ7WLbKpRce4cJuFVb5IxFFIRRrzr85ZxwKerhGK6ub9d9bq9X%2FAHoQA1nj9r9rP%2B0vRVug%2F5l5bjQus%2FnORp%2FUYpKXcZsNbR4NdOs1%2BccXDz74GiEKFbH3keWchzsbn4QHJFZIaj3M0TOB4EteS9lP0tRy39pOEjMIFLV9FRNBOWwuwAfACB29zh1VFBWTNRd2mqpWLkDr0OjYUaqH5W2rqTZNwCsDC9Kc%2FPyUjiaRIgwKPJlmqhZ2bTMCZfiIGoMw5fqBZHNoTofj3zwR%2BOF8WTKt9ddUAc03Qo%2F0Z7Gl2irTIYqpDaGHu%2BgP%2BoRoi8OEtA1Dm6IzNIc6wU1xxA5JwQiTQd5%2BLhNuqFwk512TMwgbc9rgjTK1Kic9LsQWldbOsuftMIOyDRiLAL9kv8NFyazVvd6XQQsFJNsvtlqy1K4trwOjYY5sZvXQG0vlY0bW0nZUqy32iK1OBqV1lW3tPnJlqIJnuHWnlI8UGHxXBlG6YNRbI04GulN7obqXNfBfnju1YenQ%2FAns7Asro7XVrIZNMtQgC9z0NFqt6J4Dm5tDdGBCqUi7Ub3zfY9DZFzQgBwtOxAjHzzAQsYaZLysioOVKbcmG9sKChppPDFXlpDlOOgrOB8YQaRZ4NOihM21dvT%2FqQVqqtMo9HIVlvWo5hum4QVBzATM8giO68Dp30XUSMS0UUI2wop1Oj6wHy2FEUVdWtfft7e1uanWgoexVJwDZ2pCHm7bK7UsF0ldWQzsNX1tgYAdT1joWuO82h17M%2FtA1VvZPuTWagO83m6TcVM2Qzqj7rLd%2F3uOomuG%2BebHXSmc8jbS5pz08GqLTKOIXLGCEXFU46fDEgfRX90SbQNCfM8uiS90tZz%2BjuZJ7hPw0Qm31770AKIB5mG5SezvthTWv10f9z%2BKKvI7SNWO3GH16HREACyWGZ%2FWOMtgSaMrQ%2B74kdE2Y%2BjslPu06Ri8JMtRQM8Q6etWNnZA8%2B40HtVBwbogwFWntamZ9zzs4n%2BqKfM%2Bt5nfqrEmWc2IGOM2Z09VGQzXcNrOClwDg46mmJBOlPPWOhVfss3nYqMfQ9D5Ly4kKT%2Fucvhy9U9vHvXLfIIgRfV5V1hWxkn3lBQ0ueTRsyOIWwrxeOatkDtmfPvITGLo%2BxynLlZnjlAdoR%2BkuSLwCkUpD7O22SasH9yKTJkM%2FCMbsUh9OKK8jL0jD3y8KoxzoBmB7ev4HF35HDwP8pDEAQ5CvwfnhAEQY4CwyiCIMhRYBhFEAQ5CgyjCIIgR4FhFEEQ5CgwjCIIghwFhlEEQZCjwDCKIAhyFBhGEQRBjgLDKIIgyFFgGEUQBDmK%2FwC4%2BHS5b1DZwAAAAABJRU5ErkJggg%3D%3D'))

