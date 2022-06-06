import giphy_client as gc
from giphy_client.rest import ApiException
from random import randint
import requests
from tkinter import *
from app import predicted_emotion

root = Tk()
root.title('GIF')

# create an instance of API class
api_instance = gc.DefaultApi()
api_key = "0hxf7PZVWF9wIzz6IipsQqdDYKSVj8Ww"
q = predicted_emotion     # search query term or phrase
fmt = "gif"               # used to indicate the expected response format, default is Json

try:
    # Search Endpoint
    response = api_instance.gifs_search_get(api_key,q,limit=1,offset=randint(1,10),rating='pg',fmt=fmt)
    gif_id = response.data[0]
    gif_url = gif_id.images.downsized.url
except ApiException:
    print("Exception when calling DefaultApi->gifs_search_get: %s\n"%e)

# download the GIF
with open('test.gif','wb') as f:
    f.write(requests.get(gif_url).content)

# animated GIF consists of number of frames in single file, we have to specify each frame in Tkinter 
frames = []
i = 0
while True:   #  Add frames until out of range
    try:
        frames.append(PhotoImage(file='test.gif', format = 'gif -index %i' %(i)))
        i = i + 1
    except TclError:
        break

def update(ind):    # Display and loop the GIF
    if ind >= len(frames):
        ind = 0
    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    root.after(100, update, ind)

label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
