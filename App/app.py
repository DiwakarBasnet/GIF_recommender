import tkinter as tk                 # for GUI
from tkinter import W, filedialog    # offers a set of dialogs while working with files
from PIL import ImageTk, Image       # Python Imaging Library adds image processing capabilities
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2

# model selection
model = tf.keras.models.model_from_json(open("Model/model.json","r").read())
model.load_weights("Model/model.h5")
face_haar_cascade = cv2.CascadeClassifier("Model/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

live_tab = False
after_id = 0

# model prediction on image
def emotion(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.4, 5)    # 1.4 and 5 are scaleFactor and minNeighbors
    for (x,y,w,h) in faces_detected:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
        roi_gray = gray_img[y:y+w,x:x+h]        # cropping region i.e face area from image
        roi_gray = cv2.resize(roi_gray,(48,48))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis = 0)
        img_pixels /= 255
        predictions = model.predict(img_pixels)
        max_index = np.argmax(predictions[0])
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        predicted_emotion = emotions[max_index]
        cv2.putText(img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    resized_img = img
    return resized_img     # sends back the original image

# resize image
def image_resize(im, inter = cv2.INTER_AREA):
    h, w, c = im.shape
    if w > h:
        r = 600 / W
    else:
        r = 480 / h
    width = int(im.shape[1] * r)
    height = int(im.shape[0] * r)
    dim = (width, height)
    resized = cv2.resize(im, dim)
    return resized

def load_splash():
    global img
    for img_display in frame.winfo_children():
        img_display.destroy()
    img = Image.open("App/assets/hehe.png")
    basewidth = 600
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1] * float(wpercent))))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel_image = tk.Label(frame, image=img).pack()

# load image when Select Image button is pressed
def load_img():
    global img, img_data
    for img_display in frame.winfo_children():         # .winfo_children() --> gets list of all child widgets
        img_display.destroy()
    img_data = filedialog.askopenfilename(initialdir="/", title="Choose Image", filetypes=(("all files", "*.*"), ("png files", "*.png")))
    img = cv2.imread(img_data)
    img = emotion(img)
    img = image_resize(img)
    b,g,r = cv2.split(img)             # splits image into 3 channels
    img = cv2.merge((r,g,b))           # cv2 reads image in BGR while model reads in RGB format
    im = Image.fromarray(img)          # saves img in .jpeg format
    img = ImageTk.PhotoImage(image=im) # displays image
    file_name = img_data.split('/')
    panel = tk.Label(frame, text=str(file_name[len(file_name) -1]).upper()).pack()
    panel_image = tk.Label(frame, image=img).pack()    # tk.Label --> implements a display box for text or images

# capture images from live webcam
def live_img():
    global img, img_data, after_id
    for img_display in frame.winfo_children():
        img_display.destroy()
    _, cam_img = cap.read()
    img = emotion(cam_img)
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    im = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=im)
    panel = tk.Label(frame, text="Live Cam").pack()
    panel_image = tk.Label(frame, image=img).pack()
    after_id = frame.after(10, live_img)     # after 10 ms calls live_img function

# setup for webcam live feature
def live_setup():
    global live_tab, after_id
    if live_tab:
        load_splash()
        live_btn_text.set("Live")
        frame.after_cancel(after_id)
        live_tab = False
    else:
        live_btn_text.set("Stop")
        live_img()
        live_tab = True


root = tk.Tk()                    # initializes tkinter interpreter and creates root window 
root.title('EMOTIONS')            # title bar
root.resizable(False, False)      # can the windows be resized

canvas = tk.Canvas(root, height=480, width=600, bg='white')   # creates window canvas
canvas.pack()                                                 # organizes widgets in blocks before placing them in parent widget

frame = tk.Frame(root, bg='white')                            # groups and organizes other widgets
frame.place(relwidth=1, relheight=1, relx=0, rely=0)          # places widgets in specific position in parent widget

img_btn = tk.Button(root, text = 'Select Image', padx=35, pady=10, command=load_img)
img_btn.pack(side = tk.LEFT)
live_btn_text = tk.StringVar()         # variable holds a string data which can be retrived
live_btn_text.set("Live")
live_btn = tk.Button(root, textvariable = live_btn_text, padx=35, pady=10, command=live_setup)
live_btn.pack(side = tk.RIGHT)

load_splash()
root.mainloop()            # needed for tkinter files
