import torch
import os
from . import args
import pickle
from . import model
from torchvision import transforms
from .utils import output_utils
from PIL import Image
import time

use_gpu = False
device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu'

data_dir = os.path.join(os.getcwd(), 'Home\\inverse_cooking_model\\data')
ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'ingr_vocab.pkl'), 'rb'))
vocab = pickle.load(open(os.path.join(data_dir, 'instr_vocab.pkl'), 'rb'))

ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)
output_dim = instrs_vocab_size

t = time.time()
import sys; sys.argv=['']; del sys
args = args.get_parser()
args.maxseqlen = 15
args.ingrs_only=False
model = model.get_model(args, ingr_vocab_size, instrs_vocab_size)

model_path = os.path.join(data_dir, 'modelbest.ckpt')

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

def getRecipe(imageFileName):
    image_folder = os.path.join(os.getcwd(), 'media')
    image_path = os.path.join(image_folder, imageFileName)
    image = Image.open(image_path).convert('RGB')
        
    transf_list = []
    transf_list.append(transforms.Resize(256))
    transf_list.append(transforms.CenterCrop(224))
    transform = transforms.Compose(transf_list)
    
    image_transf = transform(image)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    for i in range(numgens):
        with torch.no_grad():
            outputs = model.sample(image_tensor, greedy=greedy[i], 
                                temperature=temperature, beam=beam[i], true_ingrs=None)
            
        ingr_ids = outputs['ingr_ids'].cpu().numpy()
        recipe_ids = outputs['recipe_ids'].cpu().numpy()
            
        outs = output_utils.prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)[0]
        
        return outs