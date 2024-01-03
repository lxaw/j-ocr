import os
from torch.utils.data import Dataset
from PIL import Image

class OcrDataset(Dataset):
    def __init__(self,img_folder,dataframe,transform):
        # dataframe has columns
        # path, label, character
        self.dataframe = dataframe
        self.transform = transform

        self.img_folder = img_folder
    
    def __len__(self):
        return len(self.dataframe)
    
    def __getitem__(self,idx):
        img_path = os.path.join(self.img_folder,self.dataframe.iloc[idx]['path'])
        label = self.dataframe.iloc[idx]['label']

        # load and preprocess image
        img = Image.open(img_path).convert('L') # convert to grayscale
        if self.transform:
            img = self.transform(img)
        
        return {
            'imgs':img,
            'labels':label
        }
