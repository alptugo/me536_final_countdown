import cv2
import os
import numpy as np

prev_name=""
layer_counter=0

multi_channel_img=np.empty((48,48,4))
multi_channel_list=[]
multi_image_path=os.path.join(os.getcwd(), "output_example")


#checks for 4 of the same named images (with different slice numbers). When it finds one image, it saves it to a channel
#of a 4 channel image. When 4 is complete, the image is saved to a .png file.
for file in os.listdir(multi_image_path):
    if file.split(".")[0]==prev_name:
        multi_channel_list.append(cv2.imread(os.path.join(multi_image_path, file), cv2.IMREAD_GRAYSCALE))
        layer_counter+=1
        if layer_counter==4:
            print(os.path.join(os.getcwd(), "multi_channel_images", file.split(".")[0]+".png"))
            S_values=[[np.linalg.svd(layer, compute_uv=False)[0],i] for layer, i in zip(multi_channel_list, range(4))]

            #sorts according to their singular values.
            sorted_indexes=[mem[1] for mem in sorted(S_values)]

            i=0
            for index in sorted_indexes:
                multi_channel_img[:,:,i]=multi_channel_list[index]
                i+=1

            cv2.imwrite(os.path.join(os.getcwd(), "multi_channel_images", file.split(".")[0]+".png"), multi_channel_img)
            layer_counter=0
            S_values, multi_channel_list=[], []
    else:
        layer_counter=0
        S_values, multi_channel_list=[], []
        multi_channel_list.append(cv2.imread(os.path.join(multi_image_path, file), cv2.IMREAD_GRAYSCALE))
        layer_counter += 1
        prev_name=file.split(".")[0]