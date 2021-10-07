"""all imports"""

import os 
#for creating and removing directories

import sys
from numpy.lib.function_base import append
#for using the python interpreter

import tensorflow as tfl
#machine learning library

import numpy as np
#for math operations

from typing import List, Tuple

from tensorflow._api.v2 import compat, nn
from tensorflow._api.v2.compat import v1
from tensorflow.python.client.session import Session
from tensorflow.python.ops.gen_array_ops import expand_dims
from tensorflow.python.ops.gen_random_ops import truncated_normal
from tensorflow.python.ops.gen_state_ops import Variable
from tensorflow.python.ops.nn_ops import atrous_conv2d
from tensorflow.python.training.checkpoint_management import latest_checkpoint
from tensorflow.python.training.saver import Saver
#to use for data storage

from dataloader_iam import Batch
#supporting python files

from word_beam_search import WordBeamSearch

class types_Decoder : 
    wordBsearch=2
    Bsearch=1
    Best_Path=0

    #This class defines the autoencoder decoder types for tfl

    tflv1 = tfl.compat.v1


class TF_Model:

    def __init__(self,
                clist: List[str],
                dcode_type: str = types_Decoder.Best_path,
                restore: bool = False,
                dump: bool = False) -> None: 

    #defines constructor and paramaters to be parsed into the various layers
    #constructor also initalize class self
        self.dump = dump
        self.clist = clist
        self.dcode_type = dcode_type
        self.restore = restore
        self.ainsID = 0

        #if normalization, batch or population is used
        self.train_status = tfl.compact.v1.placeholder(tfl.bool, name='train_status')

        #input training data (input images) loaded previously
        self.input_images= tfl.compact.v1.placeholder(tfl.float32,shape=(None,None,None))
        
        #define neural net layer types
        self.convnn
        self.reccurnn
        self.ctemporalc

        #setup the training optimizer for the neural network
        self.trained_bat = 0
        self.update_oper = tfl.compat.v1.get_collection(tfl.compat.v1.GraphKeys.UPDATE_OPS)
        with tfl.control_dependencies(self.update_oper):
            self.optimizer=tfl.compat.v1.train.AdamOptimizer().minimize(self.loss)
        
        
        #initialize tensorflow, setup tensorflow session (sess)
        self.sess, self.saver = self.tfl_setup()

        #Creating the CNN Layer
        def convnn(self):
            
            convnn_in4Dim = tfl.expand_dims(input=self.input_images, axis=3)

            #Parameters for CNN layers
            kernelV = [5,5,3,3,3]
            FeatureV = [1,32,64,128,128,256]
            strideV = pool_values=[(2,2)(2,2)(1,2)(1,2)(1,2)]
            n_layers = len(strideV)

  
            pool=convnn_in4Dim

            n = 0
            while n < n_layers :
                kernel = tfl.Variable(
                    tfl.random.truncated_normal(kernelV[n],kernelV[n],FeatureV[n],FeatureV[n+1],
                    stddev=0.1))
                convol = tfl.nn.conv2d(input = pool, filters = kernel, padding = 'SAME', strides = (1, 1, 1, 1))
                convol_norm = tfl.compat.v1.layers.batch_normalization(convol, training=self.train_status)
                av_relu = tfl.nn.relu(convol_norm)
                pool=tfl.nn.max_pool2d(input=av_relu,ksize=(1,pool_values[n][0],pool_values[n][1],1,padding='VALID')
                n=+1
            self.convnn_out4Dim = pool


            #Creating the RNN Layer

        def reccurnn(self):

            self.recurnn_in3dim = tfl.squeeze(self.convnn_out4Dim, axis=[2])

            #initializing RNN cells (2 rnn layers)

            n_Hidden = 256
            cells = [tfl.compat.v1.nn.rnn_cell.LSTMCell(num_units=num_hidden, state_is_tuple=true) for range(2)]

            #assembling RNN Cells for bidirectional function
            RNN_Stack = tfl.compat.v1.nn.rnn_cell.MultiRNNCell(cells, state_is_tuple=True)
            
            (fow,bac), _ = tfl.compat.v1.nn.bidirectional_dynamic_rnn(cell_fw=RNN_Stack, cell_bw=RNN_Stack, dtype=recurnn_in3dim.dtype)

            conc = tf.expand_dims(tf.concat([fow,bac], 2) 2)
            
            #character outputs 
            
            kernel = tfl.Variable(tfl.random.truncated_normal([1,1,N_Hidden*2,len(self.clist)+1,stddev=0.1]))
            self.recurnn_out3Dim = tfl.squeeze(tfl.nn.atrous_conv2d(value = conc,filters=kernel,rate=1,padding='SAME'),axis=[2])
            
            

        def ctemporalc(self):
            self.ctcin3d = tf.transpose(self.recurnn_out3Dim,[1,0,2])

            self.gttexts=tfl.SparseTensor(tfl.compat.v1.placeholder(tf.int64, shape=[None, 2]),
                                        tfl.compat.v1.placeholder(tf.int32, [None]),
                                        tfl.compat.v1.placeholder(tf.int64, [2]))

            self.seq_length = tfl.compat.v1.placeholder(tfl.int32, [None])

            self.loss = tfl.reduce_mean(
                input_tensor=tfl.compat.v1.nn.ctc_loss(labels=self.gttexts,inputs=self.ctcin3d,
                                                       sequence_length=self.seq_length,
                                                       ctc_merge_repeated=True)
            )

            self.saved_ctc_input= tfl.compat.v1.placeholder(tf.float32,
                                                        shape=[None, None, len(self.clist) + 1])
            
            self.loss_per_element = tfl.compat.v1.nn.ctc_loss(labels=self.gttexts, inputs=self.saved_ctc_input,
                                                         seqlength=self.seq_length, ctc_merge_repeated=True)

            
            if self.dcode_type == DecoderType.BestPath:
                self.decoder = tfl.nn.ctc_greedy_decoder(inputs=self.ctcin3d, seqlength=self.seq_length)  
            elif self.dcode_type == DecoderType.BeamSearch:
                self.decoder = tfl.nn.ctc_beam_search_decoder(inputs=self.ctcin3d, seqlength=self.seq_length,
                                                         beam_width=50)
            
            
            elif self.dcode_type == DecoderType.WordBeamSearch:
                characters=''.join(self.clist)
                word_characters=open('../model/wordCharList.txt').read().splitlines()[0]
                corpus=open('../data/corpus.txt').read()

                self.decoder = WordBeamSearch(50, 'Words', 0.0, corpus.encode('utf8'), characters.encode('utf8'),
                                          word_characters.encode('utf8'))
        
                self.wbs_input=tfl.nn.softmax(self.ctcin3d, axis=2)

        def tfl_setup(self) -> Tuple[tfl.compat.v1.Session, tfl.compat.v1.train.Saver]:

            #initialise tensorflow session
            sess = tfl.compat.v1.Session()

            #saving tensorflow model to a file
            saver = tfl.compat.train.Saver(max_to_keep=1)
            mod_directory = '.../model/'

            #check if there is a previously saved tensorflow model
            snaps_newest = tfl.train.latest_checkpoint(mod_directory)

            if self.restore and not snaps_newest:
                raise Exception('No model found in /model/')
            
            #load model if saved model is found in /model/
            if snaps_newest:
                print('Latest snapshot loaded')
                saver.restore(sess, snaps_newest)
            else:
                print('Init with new values')
                sess.run(tfl.compat.v1.global_variables_initialier())
            
            return sess, saver


        #Placing ground truth texts into sparse tensor for ctc loss.
        def tensor_sparse(self, texts: List[str]) -> Tuple[List[List[int]], List[int], List[int]]:

            values = []
            indices= []
            shape = [len(texts), 0]
            
            for batch_member, text in enumerate(texts):

                label_str = [self.clist.index(c) for c in text]
                if len(label_str) > shape[1]:
                   shape[1] = len(label_str)
                
                for a, label in enumerate(label_str):
                    indices.append([batch_member, a])
                    values.append(label)  

            return indices, values, shape
            
            
     def Decoder_txt_output(self,Batch_S:int,out_ctc:tuple):->List[str]
         
        #takes ctc layer output and extracts text

        if self.dcode_type == types_Decoder.wordBsearch:
            str_Label = out_ctc

        else:
            decoded = out_ctc[0][0]

            str_Label = [[] for _ in range(Batch_S)]
            
            for (idx, idx2d) in enumerate(decoded.indices):
                label = decoded.values[idx]
                batch_element = idx2d[0]
                label_strs[batch_element].append(label)
            #the tuple is returned.
            #first elemnt = sparse tensor

        return [''.join([self.clist[c] for c in labelStr]) for labelStr in label_strs]
 
