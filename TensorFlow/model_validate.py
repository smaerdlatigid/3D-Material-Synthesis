import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image
import matplotlib.pyplot as plt

from model_train import build_cnn_encoder

if __name__ == "__main__":
    filepath = "train\\UnitySamples\\"
    images = glob.glob(filepath+"*normal.png")
    # determine image size + aloc arrays
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

    tf.keras.utils.plot_model(encoder, to_file='encoder.png', show_shapes=True, show_layer_names=False)

    dude()
    print('loading data...')
    X0 = np.zeros( (len(images), img.size[1], img.size[0], 3), dtype=np.float16 )
    X1 = np.zeros( (len(images), img.size[1], img.size[0], 3), dtype=np.float16 )
    X2 = np.zeros( (len(images), img.size[1], img.size[0], 3), dtype=np.float16 )
    X3 = np.zeros( (len(images), img.size[1], img.size[0], 3), dtype=np.float16 )
    y = np.zeros( (len(images), img.size[1], img.size[0], 3), dtype=np.float16 )
    
    for i in range(len(images)):
        y[i] = np.asarray(Image.open(images[i]))
        X0[i] = np.asarray(Image.open(images[i].replace('_normal','_color0')))
        X1[i] = np.asarray(Image.open(images[i].replace('_normal','_color1')))
        X2[i] = np.asarray(Image.open(images[i].replace('_normal','_color2')))
        X3[i] = np.asarray(Image.open(images[i].replace('_normal','_color3')))
    
    output = model.predict([X0,X1,X2,X3])

    # TODO side by side comparison
    f,ax = plt.subplots(1,2)
    ax[0].imshow(output[0].astype(int))
    ax[0].set_title("Predicted")
    ax[1].imshow(y[0].astype(int))
    ax[1].set_title("Ground Truth")
    plt.show()