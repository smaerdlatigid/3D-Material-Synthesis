import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image
import matplotlib.pyplot as plt

from model_train import build_cnn_encoder

if __name__ == "__main__":
    images = glob.glob("train/UnitySamples/*normal.png")
    img = Image.open(images[0])

    encoder = build_cnn_encoder( 
        input_dims=[(img.size[1],img.size[0],3)]*4, 
        layer_sizes=[ (8,8,8) ]*4,
        combined_layers = [8,8,8], 
        output_dim=(img.size[1],img.size[0],3)
    )

    encoder.summary()

    try:
        encoder.load_weights("encoder_weights.h5")
    except:
        print('load weights failed')

    try:
        tf.keras.utils.plot_model(encoder, to_file='encoder.png', show_shapes=True, show_layer_names=False)
    except:
        pass

    X0 = np.zeros( (10, img.size[1], img.size[0], 3), dtype=np.float16 )
    X1 = np.zeros( (10, img.size[1], img.size[0], 3), dtype=np.float16 )
    X2 = np.zeros( (10, img.size[1], img.size[0], 3), dtype=np.float16 )
    X3 = np.zeros( (10, img.size[1], img.size[0], 3), dtype=np.float16 )
    y = np.zeros( (10, img.size[1], img.size[0], 3), dtype=np.float16 )
    
    j = 0
    for i in np.random.choice(np.arange(len(images)),10):
        y[j] = np.asarray(Image.open(images[i]))
        X0[j] = np.asarray(Image.open(images[i].replace('_normal','_color1')))
        X1[j] = np.asarray(Image.open(images[i].replace('_normal','_color2')))
        X2[j] = np.asarray(Image.open(images[i].replace('_normal','_color3')))
        X3[j] = np.asarray(Image.open(images[i].replace('_normal','_color4')))
        j += 1
    
    output = encoder.predict([X0,X1,X2,X3])

    f,ax = plt.subplots(7,4,figsize=(5,7))
    for i in range(7):
        ax[i,0].imshow(X0[i].astype(int))
        ax[i,1].imshow(y[i].astype(int))
        ax[i,2].imshow(output[i].astype(int))
        ax[i,3].imshow((y[i]-output[i]).astype(int) )
        
        ax[i,0].get_yaxis().set_visible(False)
        ax[i,0].get_xaxis().set_visible(False)
        ax[i,1].get_yaxis().set_visible(False)
        ax[i,1].get_xaxis().set_visible(False)
        ax[i,2].get_yaxis().set_visible(False)
        ax[i,2].get_xaxis().set_visible(False)
        ax[i,3].get_yaxis().set_visible(False)
        ax[i,3].get_xaxis().set_visible(False)

    ax[0,0].set_title("Input")
    ax[0,1].set_title("Truth")
    ax[0,2].set_title("Predction")
    ax[0,3].set_title("Residual")
    plt.tight_layout()
    plt.show()