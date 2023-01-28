import os
import shutil
import pickle


cwd=os.getcwd()
list_of_input_img=os.listdir(os.path.join(cwd, "multi_channel_images"))

#getting the lattice type name corresponding to each file
modded_list=[file_name[8:].lstrip("0123456789")[:-4] for file_name in list_of_input_img]

out_dir=os.path.join(cwd, "sep_multi_channel_images")

counter_dict={}
file_name_mapper={}


print(modded_list)
i=0
for name in modded_list:
    if name in os.listdir(out_dir):
        #this dictionary counts the image generated for each lattice type
        counter_dict[name]+=1
        shutil.copy(os.path.join(cwd, "multi_channel_images", list_of_input_img[i]), os.path.join(out_dir, name, list_of_input_img[i][8:].lstrip("0123456789")[:-4]+f" ({counter_dict[name]}).png"))

        #this dictionary keeps the names of the original zip file and the output 4 channel image.
        file_name_mapper[list_of_input_img[i][8:][:-4]+".zip"]=list_of_input_img[i][8:].lstrip("0123456789")[:-4]+f" ({counter_dict[name]}).png"

    #if a new type is encountered, creates new directory and new entry in counter_dict
    else:
        os.mkdir(os.path.join(out_dir, name))
        counter_dict[name]=1
        shutil.copy(os.path.join(cwd, "multi_channel_images", list_of_input_img[i]), os.path.join(out_dir, name, list_of_input_img[i][8:].lstrip("0123456789")[:-4]+f" ({counter_dict[name]}).png"))
        file_name_mapper[list_of_input_img[i][8:][:-4]+".zip"]=list_of_input_img[i][8:].lstrip("0123456789")[:-4]+f" ({counter_dict[name]}).png"

    i+=1

#dumps the mapper dictionary into a pickle file so that it can be used later
with open('file_name_mapper.pickle', 'wb') as handle:
    pickle.dump(file_name_mapper, handle, protocol=pickle.HIGHEST_PROTOCOL)