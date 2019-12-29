# 3D Material Synthesis
Estimate surface normals from a single view using multiple light sources and artificial intelligence.

## Generate Training Data with Unity 

4 point sources are placed around a scene to mimic LEDs on a tripod-like structure

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

OUTPUT: 1 image 480 x 320 px corresponding to a normal map (a grayscale image)

```
glob images
format training set
cross-val for testing
create NN architecture
start training
view model error vs training epoch
view side by side comparison of predicted normal map
create unity side by side comparison with a moving light source
```

## Real World Application
We are working on building a tripod light structure using a bluetooth controlled arduino and some LED strips in order to mimic our Unity simulation. A mobile app will allow you to run through the lighting sequence on your phone and capture data in the real world similar to how it was set up in Unity. This will allow one to create photo-realistic materials using their cellphone camera and an easy to build light stand. 

## Use Cases
- Create photo-realistic textures for motion pictures and video games
- Estimate a height map from geostationary satellite images by integrating the normal map. Images must be taken hours apart while the sun is at different angles. The algorithm needs to be retrained using a directional light source which takes into account your latitude on the Earth

### License
This software is intended strictly for educational purposes. Please cite this work if you use any of these algorithms for your project. Licensing fees may apply for any use beyond educational purposes, please contact support@digitaldream.io for more information