import cv2
from IPython.display import display
import matplotlib.cm as cm
import os
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# 모델 불러오기
model = tf.keras.models.load_model('acc_07099.h5')

font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 0, 0)

# CAM을 보고싶은 data path
CAM_path = "./test_CAM/"

# output CAM 저장 위치
save_path = "./output_CAM/"

data_dir = CAM_path
# data_list = os.listdir("./oven_data_collection/")

# list of label
data_list = ['blouse',
             'hoodie',
             't_shirt']


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.layers[0].inputs], [model.layers[0].get_layer(last_conv_layer_name).output, model.layers[0].output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def display_gradcam(img_path, heatmap, alpha=0.8):
    res = 512
    # Load the original image
    raw_img = Image.open(img_path)
    raw_img = raw_img.resize((224, 224), Image.LANCZOS)
    img = np.array(raw_img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = tf.keras.preprocessing.image.img_to_array(jet_heatmap)

    #     jet_heatmap = np.zeros((img.shape[0], img.shape[1], 3))

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img

    superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img)

    #     plt.figure(figsize=(5, 5))
    #     plt.imshow(superimposed_img)
    #     plt.show()

    img = np.expand_dims(img, axis=0)
    pred_res = model.predict(img)
    pred_res = np.argmax(pred_res)

    return superimposed_img, pred_res


for class_name in data_list:
    if not os.path.exists(save_path + class_name):
        os.makedirs(save_path + class_name)
    for i, img in enumerate(os.listdir(data_dir + class_name)):
        loaded = Image.open(data_dir + class_name + "/" + img)
        raw_img = loaded.resize((224, 224), Image.LANCZOS)
        raw_img = np.array(raw_img)
        raw_img = np.expand_dims(raw_img, axis=0)

        heatmap = make_gradcam_heatmap(raw_img, model, "multiply_18")

        res, pred_res = display_gradcam(data_dir + class_name + "/" + img, heatmap)
        res = np.array(res)
        pred_res = data_list[pred_res]
        print(pred_res)

        cv2.putText(res, pred_res, (10, 15), fontFace=font, fontScale=0.5, color=color, thickness=2)
        plt.figure(figsize=(5, 5))
        plt.imshow(res)
        plt.show()
        save_dir = save_path + class_name + "/" + img
        cv2.imwrite(save_dir, cv2.cvtColor(res, cv2.COLOR_RGB2BGR))

