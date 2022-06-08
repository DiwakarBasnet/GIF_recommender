# GIF_recommender
Haar Cascade algorithm detects face in the image or live feed, crops it and then sends it to our CNN model which detects emotion.
Model is trained on <a href="https://www.kaggle.com/datasets/msambare/fer2013">FER-2013<a> dataset on kaggle. Dataset consists of 7 classes, the training set consists of 28,709 examples and the test set consists of 3,589 examples.
  The detected emotion is used as key to search for a gif using <a href="https://developers.giphy.com/docs/api/">giphy api<a>, the api then sends a gif to be displayed.
