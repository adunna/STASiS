from clarifai.client import ClarifaiApi
import os
import json

os.environ["CLARIFAI_APP_ID"] = "s_ssv1QnDN2gzvtEJduA6kvwdC8M3vgh7DfC6DzP"
os.environ["CLARIFAI_APP_SECRET"] = "iW0F_LuIgCt4oOotl6RGyVhSiEe2ExQcw67bi3rZ"

clarifai_api = ClarifaiApi()

def clarifai_req(img):
    res = clarifai_api.tag_images(img)
    return json.dumps(res, sort_keys=True, indent=2, separators=(',', ':'))

def clarifai_b64(b64str):
    res = clarifai_api.tag_image_urls("data:image/png;base64," + b64str)
    return json.dumps(res, sort_keys=True, indent=2, separators=(',', ':'))
