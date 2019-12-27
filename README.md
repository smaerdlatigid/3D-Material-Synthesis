# 3D Material Synthesis
Estimate surface normals from a single view using multiple light sources and artificial intelligence.

## Generate Training Data with Unity 
4 point sources are placed around a scene to mimic LEDs on a tripod-like structure

![](Screenshot.png)

The lights turn on individually and a screenshot is captured for each. These four images are input into a convolutional neural network in order to estimate a normal map.

![](animation.gif)

The "ground truth" value for the images is a normal map. The normal map encodes information about how bumpy or curved the surface is so that light can interact with it in a photorealistic way.

![](NormalSurface.png)

## Finding Textures Online

The training data is composed of high resolution textures with normals from sources like https://www.substance3d.com/ or https://3dtextures.me) 

Web scraper to search for training data from

Augment the images to account for different perspectives & small distortions (e.g. warps, rotations, translations and cropping) 

create latent space animation?

DCGAN to latent space, interpolation between textures, run textures through map estimator

- `webscrape.py`

afterwards run gdrive_download.py --file download_links.txt --dir train

Sift through the data set

Create a sample blender scene and render training images from different perspectives?

## Machine learning model 

Common practice of augmenting your images to produce larger training data sets (e.g. Augmentor)
4 image input, simulating LEDs at different angles

LSTM video feed to single image output

More free textures: 
    https://cc0textures.com/
    https://www.cgbookcase.com/
    https://texturehaven.com/textures/


