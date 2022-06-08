import giphy_client as gc
from giphy_client.rest import ApiException
from random import randint
import requests

def GIF(pred):
    # create an instance of API class
    api_instance = gc.DefaultApi()
    api_key = "0hxf7PZVWF9wIzz6IipsQqdDYKSVj8Ww"
    q = pred                  # search query term or phrase
    fmt = "gif"               # used to indicate the expected response format, default is Json
    try:
        # Search Endpoint
        response = api_instance.gifs_search_get(api_key,q,limit=1,offset=randint(1,10),rating='pg',fmt=fmt)
        gif_id = response.data[0]
        gif_url = gif_id.images.downsized.url
    except ApiException:
        print("Exception when calling DefaultApi->gifs_search_get\n")

    # download the GIF
    with open('test.gif','wb') as f:
        f.write(requests.get(gif_url).content)
