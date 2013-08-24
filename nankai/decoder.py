# -*- coding: utf-8  -*-
import Image
import ImageFilter

import math

# VectorCompare was taken from http://www.boyter.org/decoding-captchas/

class VectorCompare:
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.iteritems():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word):
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))



def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

class Decoder:
    save_path = '.'
    sample_path = 'sample'
    char_base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    vector_base = []
    vector_machine = VectorCompare()
    def __init__(self, p=''):
        self.save_path = p
        self.build_base()

    def build_base(self):
        for item in self.char_base:
            m = Image.open('%s/%s.bmp'%(self.sample_path, item))
            self.vector_base.append({item: buildvector(m)})
            

    def tryWholeFile(self, f):
        result = []
        src = Image.open(f)    
        img_pieces = crop(transform_whole(src))
        for i, img in enumerate(img_pieces):
            dst = transform_single(img)
            r = self.try_match(dst)
            result.append(r)
        return result

    def fix_minor(self, guess):
        if guess[0][0] < 0.6:
            if guess[0][1] == '3':
                return '2'
            elif guess[0][1] == '5':
                return '9'
            else:
                return guess[0][1]
        else:
            return guess[0][1]

    def try_match(self, one):
        guess = []
        for image in self.vector_base:
            for x, y in image.iteritems():
                guess.append( ( self.vector_machine.relation(y, buildvector(one) ), x) )
        guess.sort(reverse=True)
        # return self.fix_minor(guess)
        return guess[0][1]

def remove_bg(img):
    bg_color = img.getpixel((0, 0))

    def replace_bg(point):
        # compare with bg_color or use value 150
        return abs(point - bg_color) > 50 and 255

    return img.point(replace_bg, '1')

def resize_to_single(img):
    return img.resize((7, 11))

def try_split(img):
    img_size = img.size
    pix = img.load()
    is_this_empty_line = False
    is_last_empty_line = False
    border = []
    for x in range(img_size[0]):
        for y in range(img_size[1]):
            is_this_empty_line = True
            if pix[x, y] != 0:
                is_this_empty_line = False
                break

        if is_this_empty_line and (not is_last_empty_line):
            border.append(x)
        is_last_empty_line = is_this_empty_line

    grid = []
    for i in range(len(border) - 1):
        grid.append( (border[i], 0, border[i+1], 20) )
    return grid

def crop(img):
    result = []
    for item in try_split(img):
        result.append(remove_border(img.crop(item)))
    return result

    # return [ remove_border(img.crop((0, 0, 20, 20))),
    #         remove_border(img.crop((20, 0, 30, 20))), 
    #         remove_border(img.crop((30, 0, 43, 20))), 
    #         remove_border(img.crop((45, 0, 60, 20))) ]

def resize(img):
    return img.resize((hash_size+1, hash_size), Image.ANTIALIAS)

def decolor(img):
    return img.convert("L")

def remove_border(img):
    box = img.getbbox()
    return img.crop(box)

def transform_whole(img):
    return remove_bg(decolor(img))

def transform_single(img):
    return resize_to_single(img)

def save(img, name, save_path='.'):
    img.save('%s/%s.bmp'%(save_path, name), 'bmp')

