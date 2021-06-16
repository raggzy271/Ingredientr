# import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
import os
from . import args
import pickle
from . import model
from torchvision import transforms
from .utils import output_utils
from PIL import Image
import time
import requests
from io import BytesIO
import random
from collections import Counter


data_dir = '../data'

# code will run in gpu if available and if the flag is set to True, else it will run on cpu
use_gpu = False
device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu'


# code below was used to save vocab files so that they can be loaded without Vocabulary class
#ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'final_recipe1m_vocab_ingrs.pkl'), 'rb'))
#ingrs_vocab = [min(w, key=len) if not isinstance(w, str) else w for w in ingrs_vocab.idx2word.values()]
#vocab = pickle.load(open(os.path.join(data_dir, 'final_recipe1m_vocab_toks.pkl'), 'rb')).idx2word
#pickle.dump(ingrs_vocab, open('../demo/ingr_vocab.pkl', 'wb'))
#pickle.dump(vocab, open('../demo/instr_vocab.pkl', 'wb'))

########## ADDED ABSOLUTE PATHS (REMOVE LATER) ########################

ingrs_vocab = pickle.load(open('D:/Computer Man 3/Deep Learning/Ingredientr/Home/inverse_cooking_model/data/ingr_vocab.pkl', 'rb'))
vocab = pickle.load(open('D:/Computer Man 3/Deep Learning/Ingredientr/Home/inverse_cooking_model/data/instr_vocab.pkl', 'rb'))

ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)
output_dim = instrs_vocab_size


print (instrs_vocab_size, ingr_vocab_size)


t = time.time()
import sys; sys.argv=['']; del sys
args = args.get_parser()
args.maxseqlen = 15
args.ingrs_only=False
model = model.get_model(args, ingr_vocab_size, instrs_vocab_size)
# Load the trained model parameters

########## ADDED ABSOLUTE PATHS (REMOVE LATER) ########################

# model_path = os.path.join(data_dir, 'modelbest.ckpt')
model_path = 'D:/Computer Man 3/Deep Learning/Ingredientr/Home/inverse_cooking_model/data/modelbest.ckpt'

model.load_state_dict(torch.load(model_path, map_location=map_loc))
model.to(device)
model.eval()
model.ingrs_only = False
model.recipe_only = False
print ('loaded model')
print ("Elapsed time:", time.time() -t)


transf_list_batch = []
transf_list_batch.append(transforms.ToTensor())
transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406), 
                                              (0.229, 0.224, 0.225)))
to_input_transf = transforms.Compose(transf_list_batch)

greedy = [True, False, False, False]
beam = [-1, -1, -1, -1]
temperature = 1.0
numgens = len(greedy)

def getIngredients(use_urls, imageFileName):
    show_anyways = False #if True, it will show the recipe even if it's not valid
    # image_folder = os.path.join(data_dir, 'demo_imgs')
    image_folder = "D:/Computer Man 3/Deep Learning/Ingredientr/Home/inverse_cooking_model/data/demo_imgs"

    if not use_urls:
        demo_imgs = os.listdir(image_folder)
        random.shuffle(demo_imgs)

    demo_urls = ['https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/12/9/0/FNK_Cheesecake_s4x3.jpg.rend.hgtvcom.826.620.suffix/1387411272847.jpeg',
                'https://www.196flavors.com/wp-content/uploads/2014/10/california-roll-3-FP.jpg']

    demo_files = demo_urls if use_urls else demo_imgs


    for img_file in demo_files:
        
        if use_urls:
            response = requests.get(img_file)
            image = Image.open(BytesIO(response.content))
        elif img_file == imageFileName:
            image_path = os.path.join(image_folder, img_file)
            image = Image.open(image_path).convert('RGB')
        else:
            continue
        
        transf_list = []
        transf_list.append(transforms.Resize(256))
        transf_list.append(transforms.CenterCrop(224))
        transform = transforms.Compose(transf_list)
        
        image_transf = transform(image)
        image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)
        
        # plt.imshow(image_transf)
        # plt.axis('off')
        # plt.show()
        # plt.close()
        
        # num_valid = 1
        for i in range(numgens):
            with torch.no_grad():
                outputs = model.sample(image_tensor, greedy=greedy[i], 
                                    temperature=temperature, beam=beam[i], true_ingrs=None)
                
            ingr_ids = outputs['ingr_ids'].cpu().numpy()
            recipe_ids = outputs['recipe_ids'].cpu().numpy()
                
            outs, valid = output_utils.prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)

            return outs
            
            # if valid['is_valid'] or show_anyways:
                
                # print ('RECIPE', num_valid)
                # num_valid+=1
                #print ("greedy:", greedy[i], "beam:", beam[i])
        
                # BOLD = '\033[1m'
                # END = '\033[0m'
                # print (BOLD + '\nTitle:' + END,outs['title'])

                # print (BOLD + '\nIngredients:'+ END)
                # print (', '.join(outs['ingrs']))

                # print (BOLD + '\nInstructions:'+END)
                # print ('-'+'\n-'.join(outs['recipe']))

                # print ('='*20)

            # else:
            #     pass
                # print ("Not a valid recipe!")
                # print ("Reason: ", valid['reason'])