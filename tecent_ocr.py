import base64
import json

import cv2
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


class TecentOcr:
    def __init__(self):
        f = open('config.json', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        params = json.loads(text)
        self.cred = credential.Credential(params['SecretId'], params['SecretKey'])
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "ocr.tencentcloudapi.com"

        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        self.client = ocr_client.OcrClient(self.cred, "ap-shanghai", self.clientProfile)

    def identify(self, img):
        image = cv2.imencode('.jpg', img)[1]
        base64_code = str(base64.b64encode(image))[2:-1]
        req = models.GeneralBasicOCRRequest()
        params = '{"ImageBase64":"%s"}' % base64_code
        req.from_json_string(params)

        resp = self.client.GeneralBasicOCR(req)
        print(resp.to_json_string())
        return resp


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]

    return image_code


if __name__ == "__main__":
    ocr = TecentOcr()
    ocr.identify(cv2.imread("02.jpg"))
