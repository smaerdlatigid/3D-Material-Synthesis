# PhotoMaterialSynthesis
Estimate normal, height and occlusion maps from photographs with artificial intelligence.

## Creating a data set
Download high resolution textures with normals, height or occlusion maps (e.g. https://www.substance3d.com/, https://gendosplace.artstation.com/store/6l1g/texture-pack-volume-1 )

Augment the images to account for different perspectives, small distortions (e.g. warps, rotations, translations and cropping) 

Create a web scraper to download texture packs
1. Follow the instructions here to set up the gdrive python library: https://developers.google.com/drive/api/v3/quickstart/python
