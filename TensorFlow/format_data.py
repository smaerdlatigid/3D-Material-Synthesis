from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import glob 
import os

def contains(string,keys):
    for k in keys:
        if k.lower() in string.lower():
            return True
    return False

if __name__ == "__main__":
    dirs = glob.glob("train/*/")
    COLOR_KEYS = ['color']
    NORMAL_KEYS = ['norm', 'normal', 'nrm', 'nrml']
    IGNORE_KEYS = ['fabric', 'cloth', 'floor']
    SAVE_DIR = "train\\Textures\\"
    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)

    stds = []
    tn = 0
    for d in dirs:

        imgs = []
        types = ("*.jpg", "*.jpeg", "*.png")
        for t in types:
            tmp = glob.glob(d+t)
            if tmp: imgs.extend(tmp)
        
        data = {}
        for i in imgs:            
            if not contains(i, IGNORE_KEYS):
                try:
                    if contains(i,NORMAL_KEYS):
                        data['normal'] = np.asarray(Image.open(i))
                    elif contains(i, COLOR_KEYS):
                        data['color'] = np.asarray(Image.open(i))
                except:
                    pass

        if len(data) == 2:
            if np.std(data['normal'][:,:,0]) > 15:
                stds.append(np.std(data['normal'][:,:,0]))
                                
                normal = Image.fromarray(data['normal'])
                normal.save(SAVE_DIR+"Texture_{}_normal.png".format(tn)) 
                normal.close()

                color = Image.fromarray(data['color'])
                color.save(SAVE_DIR+"Texture_{}_color.png".format(tn))   
                color.close()         
                tn += 1
    