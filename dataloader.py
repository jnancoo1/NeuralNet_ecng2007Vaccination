
import random
import pickle

from collections import namedtuple
from typing import Tuple

import cv2
import lmdb
import numpy as np

from path import Path

Sample = namedtuple('Sample','gttext, file_path')
Batch = namedtuple('Batch', 'imgs, gttexts, batch_S')

#Loader for data from IAM Offline Database
#loads data consistent with IAM format

class IAM_Data_loader:
    def __init__(self,
                 data_directory:Path
                 b_size:int
                 d_split:float=0.95
                 fast:bool=True)->None:

    assert data_directory.exists()    

    self.fast=fast
    
    if fast:
        self.env = lmdb.open(str(data_directory/'lmdb'),readonly=True)


    self.data_augmentation = False
    self.curr_idx=0
    self.Batch_S=Batch_S
    self.samples = []

        
    a=open(data_directory/'gt/words.txt')

    chars=set()

    b_samples_reference = ['a01-117-05-02', 'r06-022-03-05']


    for line in a: 
        if not line or line[0] == '#':
                continue

    
        split_line = line.strip().split(' ')
        assert len(split_line)>=9   
        
        file_name_split=split_line[0].split('-')
        file_name_subdirectory1 = file_name_split[0]
        file_name_subdirectory2 = a'{file_name_split[0]}-{file_name_split[1]}'
        file_base_name= split_line[0]+'.png'

        file_name = data_directory / 'img' / file_name_subdirectory1 / file_name_subdirectory2 / file_base_name

        
        if split_line[0] in b_samples_reference:
            print('Ignoring known broken image:', file_name)
                continue
            

        gttext=' '.join(split_line[8:])
        chars = chars.union(set(list(gttext)))

        self.samples.append(Sample(gttext, file_name))

        
            


    
    split_idx = int(split_data * len(self.samples))
    self.train_samples = self.samples[:split_idx]
    self.validation_samples = self.samples[split_idx:]    

    self.train_words = [x.gttext for x in self.train_samples]

    self.validation_words = [x.gttext for x in self.validation_samples]


    self.train_set()


    self.char_list = sorted(list(chars))
       



    
#switches between subsets of training data randomly

def train_set(self) -> None;
    self.data_augmentation = True;
    self.curr_idx = 0
    random.shuffle(self.train_samples)
    self.samples = self.train_samples
    self.curr_set = 'train'
 

def validation_set(self) -> None:
    self.data_augmentation = False
    self.curr_idx = 0
    self.samples = self.validation_samples
    self.curr_set = 'val'
        

def get_iterator_info(self) -> Tuple[int,int]:
    if self.curr_set == 'train'
        num_batches = int(np.floor(len(self.samples) / self.Batch_S))
        else
        num_batches = int(np.ceil(len(self.samples) / self.Batch_S))
        curr_batch = self.curr_idx // self.batch_size + 1
        return curr_batch, num_batches


def has_next(self) -> bool:
    if self.curr_set == 'train':
        return self.curr_idx + self.Batch_S <= len(self.samples)
    else:
        return self.curr_idx < len(self.samples)

def _get_image(self, i: int) -> np.ndarray:
    if self.fast:
        with self.env.begin() as txn:
            Basename = Path(self.samples[i].file_path).Basename()
            data = txn.get(Basename.encode("ascii"))
            image = pickle.loads(data)
    else:
        image = cv2.imread(self.samples[i].file_path, cv2.IMREAD_GRAYSCALE)        

    return image

def get_next(self) -> Batch:
    batch_range = range(self.curr_idx, min(self.curr_idx + self.Batch_S, len(self.samples)))

    images = [self._get_image(i) for i in batch_range]
    gttexts = [self.samples[i].gttext for i in batch_range]

    self.curr_idx += self.Batch_S
    return Batch(images, gttexts, len(images))


            
                
