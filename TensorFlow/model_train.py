import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image
import matplotlib.pyplot as plt

def build_cnn_encoder( input_dims=[ (128,128,3), (256,256,3)], 
                        layer_sizes=[ (16,16,16), (32,32) ],
                        combined_layers = [32,32,32], 
                        dropout=0.25,  output_dim=(128,128,3) ):

    assert(len(input_dims)==len(layer_sizes))
    inputs = []
    layerx = []

    for i in range(len(input_dims)):
        inputs.append( tf.keras.Input(shape=input_dims[i], name='input_{}'.format(i)) )

        for j in range(len(layer_sizes[i])):
            if j >= 1:
                layerx[i] = layers.Conv2D(layer_sizes[i][j], kernel_size=4, padding="same", activation=layers.LeakyReLU())(layerx[i])
            else:
                layerx.append(layers.Conv2D(layer_sizes[i][j], kernel_size=4, padding="same", activation=layers.LeakyReLU())(inputs[i]))
            layerx[i] = layers.BatchNormalization(momentum=0.75)(layerx[i]) 
    

    # combine the models
    c = layers.Add()(layerx)

    for i in range(0,len(combined_layers)):
        c = layers.Conv2D(combined_layers[i],kernel_size=3, padding="same", activation=layers.LeakyReLU())(c)
        c = layers.BatchNormalization(momentum=0.5)(c)
        #if i == 0: c = layers.Dropout(dropout)(c)
        
    output = layers.Conv2D(3, kernel_size=3, name='encoder_output', padding="same", activation='linear')(c)

    return tf.keras.Model(inputs=inputs, outputs=output, name='encoder')

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
    
    # preprocess inputs + outputs
    # subtract average? 

    encoder.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), 
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']
    )

    history = encoder.fit(
        [X0,X1,X2,X3],
        y,
        epochs=50, 
        batch_size=8,
        shuffle=True,
        validation_split=0.1,
    )

    encoder.save_weights("encoder_weights.h5")

    
    # Plot training & validation loss values
    f,ax = plt.subplots(1)
    ax.plot(np.log2(history.history['loss']))
    ax.plot(np.log2(history.history['val_loss']))
    ax.set_ylabel('Loss')
    ax.set_xlabel('Training Epoch')
    ax.legend(['Train', 'Test'], loc='upper left')
    plt.show()
