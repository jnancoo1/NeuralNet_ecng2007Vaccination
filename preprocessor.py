import cv2
import numpy as np
from dataloader import Batch

import random
from typing import Tuple


class preprocessor:
    
    def __init__(self
                image_size: Tuple[int,int],
                padding: int = 0,
                dynamic_width: bool = False,
                line_mode: bool = False)
        
        assert not (dynamic_width and data_augmentation)
        assert not (padding > 0 and not dynamic_width)

        self.image_size = image_size
        self.padding = padding
        self.dynamic_width = dynamic_width
        self.data_augmentation = data_augmentation
        self.line_mode = line_mode
        

@staticmethod

def shorten_label(Txt:str,maximum_text_length:int)->str:

    cost=0

    for a in range(len(Txt)):
        if  a!=0 and Txt[a]==Txt[a-1]:
            cost= cost+2
        
        else:
            cost=cost+1
                
        if maximum_text_length > cost:
            return Txt[:a]

        
    return Txt
                


def _simulate_text_line(self, batch: Batch) -> Batch:
        
    default_word_sep = 30
    default_n_words = 5

    res_images = []
    res_gttexts = []

    for a in range(batch.Batch_S):
        n_words = random.randint(1,8) if self.data_augmentation else default_n_words
   
        curr_gt = ' '.join([batch.gttexts[(a+b) % batch.Batch_S] for b in range(n_words)])
        res_gttexts.append(curr_gt)
            
        sel_images = []
        word_seps = [0]
        h = 0
        w = 0
            
        for b in range(n_words):
            curr_sel_image = batch.images[(a+b) % batch.Batch_S]
            curr_word_sep = random.randint(20, 50) if self.data_augmentation else default_word_sep
            h = max(h, curr_sel_image.shape[0])
            w += curr_sel_image.shape[1]
            sel_images.append(curr_sel_image)
    
            if b + 1 < n_words:
                w += curr_word_sep
                word_seps.append(curr_word_sep)

            target = np.ones([h,w], np.uint8) * 255
            
        x = 0
        for curr_sel_image, curr_word_sep in zip(sel_images, word_seps):
            x += curr_word_sep
            y = (h - curr_sel_image.shape[0]) // 2
            target[y:y + curr_sel_image.shape[0]:, x:x + curr_sel_image.shape[1]] = curr_sel_image
            x += curr_sel_image.shape[1]
                
            res_images.append(target)
            
    return Batch(res_images, res_gttexts, batch.Batch_S)        
        

  
def process_image(self,image:np.ndarray)-> np.ndarray:

    if image is None:
        image=np.zeroes(self.img_size[::-1])
    
    
    image=image.astype(np.float)
    
    if self.data_augmentation:
        
        if random.random<0.25:
            def random_odd():
                return random.randint(1, 3) * 2 + 1
            
            img=cv2.GaussianBlur(image, (random_odd(), random_odd()), 0)
            
        if random.random<=0.24:
            img = cv2.dilate(image, np.ones((3, 3)))

        if random.random() < 0.25:
            img = cv2.erode(image, np.ones((3, 3)))
                
        
        height,width=image.shape              


        t_height,t_width=self.image_size

        f=min(t_width / width, t_height / height)

        fx=f*np.random.uniform(0.75,1.05)
        fy=f*np.random.uniform(0.75,1.05)

        txc = (t_width - width * fx) / 2
        tyc = (t_height - height * fy) / 2


        freedom_x = max((t_width - fx * width) / 2, 0)

        freedom_y = max((t_height - fy * height) / 2, 0)
 
        tx = txc + np.random.uniform(-freedom_x, freedom_x)
        ty = tyc + np.random.uniform(-freedom_y, freedom_y)

        ty = tyc + np.random.uniform(-freedom_y, freedom_y)

        if random.random <0.5:
            image = image * (0.25 + random.random() * 0.75)
    
        if random.random() < 0.1:
            image = 255 - image  
  
        if random.random() < 0.25:
            image = np.clip(image + (np.random.random(img.shape) - 0.5) * random.randint(1, 25), 0, 255)

    else:
        if self.dynamic_width:
            t_height=self.image_size[1]
            height,width=image.shape

            f=t_height/height
            t_width=int(f*width+self.padding)
            t_width = t_width + (4 - t_width) % 4
            tx = (t_width - width * f) / 2
            ty = 0
        
        else:
            t_width, t_height = self.image_size
            height, width = image.shape
            f = min(t_width / width, t_height / height)
            tx = (t_width - width * f) / 2
            ty = (t_height - height * f) / 2


        M = np.float32([[f, 0, tx], [0, f, ty]])
        target = np.ones([t_height, t_width]) * 255
        image = cv2.warpAffine(image, M, dsize=(t_width, t_height), dst=target, borderMode=cv2.BORDER_TRANSPARENT)
    image= cv2.transpose(image)

    image=image/255-0.5

    return image



def batch_processing(self, batch: Batch) -> Batch:
        if self.line_mode:
            batch = self._simulate_text_line(batch)
        
        res_imgs = [self.process_image(img) for img in batch.imgs]
        max_text_length = res_imgs[0].shape[0] // 4
        res_gttexts = [self.shorten_label(gttext, max_text_length) for gttext in batch.gttexts]
        return Batch(res_imgs, res_gttexts, batch.batch_S)

def main():
    import matplotlib.pyplot as plot

    image = cv2.imread('../data/test.png',cv2.IMREAD_GREYSCALE)
    image_augmentation = preprocessor((256,32),data_augmentation = True).process_image(image)
    plot.subplot(121)
    plot.imshow(image, cmap='gray')
    plot.subplot(122)
    plot.imshow(cv2.transpose(image_augmentation) + 0.5, cmap='gray', vmin=0, vmax=1)
    plot.show()


if __name__ == '__main__':
    main()
