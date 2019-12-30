# 3D Material Synthesis
Estimate high resolution surface normals from a single view using multiple light sources and artificial intelligence.

## Generate Training Data with Unity 

4 light sources are placed around a scene to mimic LEDs on a tripod-like structure

![](Figures/Screenshot.png)

The lights turn on individually and a screenshot is captured for each. These four images are input into a convolutional neural network in order to estimate a normal map.

![](Figures/animation.gif)

A labeled data set is created with the simulated images and their corresponding normal map. The normal map encodes information about how bumpy or curved the surface is so that light can interact with it in a realistic manner. More information about normal maps be found here: https://docs.unity3d.com/Manual/StandardShaderMaterialParameterNormalMap.html

![](Figures/NormalSurface.png)

Here is the difference between a surface with and without a normal map while being illuminated with a directional light at 45 degrees 

![](Figures/normal_anim.gif)

## Finding Textures Online

The training data is composed of high resolution textures with normals from sources like https://www.substance3d.com/

A web crawler is created to find training data on websites that provide free textures
- https://3dtextures.me 
- https://cc0textures.com/
- https://www.cgbookcase.com/
- https://texturehaven.com/textures/

To use the script follow: 
```
python webscrape.py --BASE_URL https://3dtextures.me/ --PATTERN https://drive 
```

To download folders from a list of google drive links use: 

    python gdrive_download.py --file download_links.txt --dir train

Format the data and then import the directory `train/Textures/` into Unity

    python format_data.py   

Use the script `ScreenCapture.cs` within Unity to generate training samples for a CNN. The training data is augmented within Unity to account for different perspectives & small distortions (e.g. warps, rotations, translations and cropping). Set the file path before running the "TrainingSamples" scene. Ignore all moments Unity tries to conver the texture type to a normal map. The normal map will be set to the albedo/base map to generate a ground truth label and gets renders in a wierd manner if set to a normal map in the texture settings. 

![](Figures/unity_training.gif)

## Machine learning model 

INPUT: 4 images 480 x 320 corresponding to light from 4 different angles

OUTPUT: 1 image 480 x 320 px corresponding to a normal map

![](Figures/texture_anim.gif)

The architecture of the neural network is rather simple consisting of only a few convolutional layers. The neural network doesn't have to be super complex or require many layers because the input data is so similar to the output.

*image of neural network architecture 

Training was done by optimizing for the mean squared error using Adam with a batch size of 8 images. The neural network was trained with 1500 samples for 20 epochs on a GTX 1070 (total training time ~1 hour).

![](Figures/normal_training.png)

*color0, truth, prediction, residual mosaic 

The model is built with TensorFlow 2.0

```python
from PIL import Image
import matplotlib.pyplot as plt
from model_train import build_cnn_encoder

if __name__ == "__main__":

    img = np.asarray(Image.open("test.jpg"))

    encoder = build_cnn_encoder( 
        input_dims=[(img.size[1],img.size[0],3)]*4, 
        layer_sizes=[ (8,8,8) ]*4,
        combined_layers = [8,8,8], 
        output_dim=(img.size[1],img.size[0],3)
    )

    encoder.load_weights("encoder_weights.h5") 
    output = encoder.predict([X0,X1,X2,X3])
    
```

* show unity comparison

## Real World Application

We are working on building a tripod light structure using a bluetooth controlled arduino and some LED strips in order to mimic our Unity simulation. A mobile app will allow you to run through the lighting sequence on your phone and capture data in the real world similar to how it was set up in Unity. This will allow one to create photo-realistic materials using their cellphone camera and an easy to build light stand. 

* Show picture of 2x4 and LED strip

## Use Cases
- Create photo-realistic textures for motion pictures and video games
- Estimate a height map from geostationary satellite images by integrating the normal map. Images must be taken hours apart while the sun is at different angles. The algorithm needs to be retrained using a directional light source with the correct geometry based on your location

![]() 

Image from the HiRISE instrument on the Mars Reconaissence Orbiter

### License
This software is intended strictly for educational purposes. Please cite this work if you use any of these algorithms for your project. Licensing fees may apply for any use beyond educational purposes, please contact support@digitaldream.io for more information

### Outstanding Research & Development
- Optimize CNN
    - architecture
    - number of inputs
    - merge layer

- improve texture rendering 
    - higher resolution
    - curate textures for training
    - include height map as vertex displacement
    - simulate LED bar