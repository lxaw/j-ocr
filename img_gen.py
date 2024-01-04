######
# Code to generate training images
# Note that all transformations are to occur on the model side
#

import re
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class ImgGen:
    def __init__(self,corpus,folder_path,font_paths,font_size):
        self.corpus = corpus
        self.folder_path = folder_path
        # a list
        self.font_paths = font_paths
        self.font_size = font_size
    
    def generate_random_hiragana(n):
        hiragana_pattern = re.compile('[\u3041-\u3096]')
        return ''.join([random.choice(hiragana_pattern.findall(chr(random.randint(0x3041, 0x3096)))) for _ in range(n)])

    ##
    # generate an img file based on text
    # args: 
    # text: str
    # file_name: str
    # img_size: 2-tuple
    # font_path: str
    # font_size: int
    def gen_img(self,text,file_name,img_size,font_path,font_size,add_furi=False):
        
        font = ImageFont.truetype(font_path,font_size)
        
        furigana_font_size = font_size//2

        # init position for text
        initial_position = ((img_size[0] - font_size) // 2, (img_size[1] - len(text) * font_size) // 2 - 15)

        # randomize position by slightly adding
        # todo
        position = initial_position

        # create the img
        color = "white"

        img = Image.new("RGB",img_size,color)

        draw = ImageDraw.Draw(img)

        # draw the text
        draw.text(position,text,font=font,fill='black')

        # apply furigana randomly
        if add_furi:
            # each char has about 2 furigana
            furigana_txt = self.generate_random_hiragana(2)
            furigana_x,furigana_y = position
            furigana_x += font_size
            furigana_y += 5 # to do: remove magic number
            for furigana_char in furigana_txt:
                draw.text((furigana_x,furigana_y),furigana_char,font=font,fill='black')
                furigana_y += furigana_font_size

        # save img
        img.save(file_name)
    
    def run(self):
        # read txt file, make imgs
        with open(self.corpus,'r') as file:
            file_content = file.read()
            num_files = len(file_content)
            for i,text in enumerate(file_content):
                padded_file_name = f"{i:04d}.jpg"
                file_path = os.path.join(self.folder_path,padded_file_name)
                for font_path in self.font_paths:
                    # one without furi
                    self.gen_img(text,file_path,(50,50),font_path,self.font_size,False)
                    # one with furi
                    self.gen_img(text,file_path,(50,50),font_path,self.font_size,True)


if __name__ == "__main__":
    img_folder = "imgs/"
    corpus = './corpus.txt'

    img_gen = ImgGen(corpus,img_folder)
    img_gen.run()