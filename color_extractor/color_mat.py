import pandas as pd
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline  

'''
Notes
-------------------------
myfunc(*tuple) expands a tuple
'''

df = pd.read_csv(r"C:\Users\Dhiraj\Desktop\Color Recommeder\color_extractor\file.csv", header=None, 
                 names=["id", "color1","color2","color3","color4","color5","color6","color7","color8"])

similar_mat = df.iloc[:,1:].astype(str)

def hextorgb(hex):
    try:
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
    except:
        return hex
    
#Converting HEX to RGB
similar_mat= similar_mat.applymap(hextorgb)

def rgbtohex(rgb):
    try:
        r = '#%02x%02x%02x' % rgb
        return r
    except:
        return rgb

#Converting RGB to HEX
similar_mat= similar_mat.applymap(rgbtohex)

#Checking unique Values
Y = similar_mat.values
Y = Y.flatten()
unique = np.unique(Y)

#Drop nan from unique array
unique = unique[:-1]

#Converting numpy array back to RGB
unique = pd.Series(unique)
unique = unique.apply(hextorgb)

diff_mat = np.zeros((len(unique),len(unique)))

#Finding difference between each element
for i in range(0, len(unique)):
    COMPARE_LEN = 20
    #Comparing only within a limit of +-COMPARE_LEN
    low = i - COMPARE_LEN;
    high = i + COMPARE_LEN;
    if(i < COMPARE_LEN):
        low = 0
    if(i > len(unique)-COMPARE_LEN):
        high = len(unique)
        
    for j in range(low, high):
        
        color1_rgb = sRGBColor(*unique[i], is_upscaled=True)
        color2_rgb = sRGBColor(*unique[j], is_upscaled=True)
        
        # Convert from RGB to Lab Color Space
        color1_lab = convert_color(color1_rgb, LabColor)
        color2_lab = convert_color(color2_rgb, LabColor)
        
        #Finding the difference
        diff_mat[i,j] = delta_e_cie2000(color1_lab, color2_lab)


# 0 Non similar and 1 is for similar
diff_mat[diff_mat > 4 ] = 0

'''
diff_mat = pd.DataFrame(diff_mat)
diff_mat.to_csv("diff_mat.csv", sep='\t')
'''

#Plotting Color Patches
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_facecolor('black')
rect1 = matplotlib.patches.Rectangle((-200,-100), 200, 200, color='#FEFEFE')
rect2 = matplotlib.patches.Rectangle((-0,-100), 200, 200, color='#FFFFFF')
ax.add_patch(rect1)
ax.add_patch(rect2)
plt.xlim([-400, 400])
plt.ylim([-400, 400])
plt.show()


#Useful resources
#https://snapower-opencv.tumblr.com/post/101669832648/color-difference-between-2-colors-using-python
#https://en.wikipedia.org/wiki/Color_difference#CIELAB_Delta_E*
#http://hanzratech.in/2015/01/16/color-difference-between-2-colors-using-python.html
#https://codereview.stackexchange.com/questions/128493/dynamic-colour-binning-grouping-similar-colours-in-images