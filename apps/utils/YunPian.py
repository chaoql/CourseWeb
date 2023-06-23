import requests


def send_single_sms(apikey, code, mobile):
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    # 报备通过的短信模板
    text = "".format(code)

    res = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        "text": text,
    })
    return res
