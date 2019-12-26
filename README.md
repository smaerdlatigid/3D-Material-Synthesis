# 3D Material Synthesis
Estimate normal, height and occlusion maps from photographs with artificial intelligence.

## Training Data
Download high resolution textures with normals, height or occlusion maps (e.g. https://www.substance3d.com/)

Web scraper to search for training data from https://3dtextures.me

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

