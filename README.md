# me536_final_countdown
This is term project for ME536 Design of Intelligent Machine course. It tries to get lattice types classified from STL slice images.

A slide that explains the topic can be found [here](
https://docs.google.com/presentation/d/10Uo8F_Dm4h35ygELFrS2dK_oo3cB4Kviv31DtEW7o00/edit?usp=sharing).

I started to work with generic STL data from [Princeton Benchmark for 3D Mesh Segmentation](https://www.kaggle.com/datasets/herimor/princeton-benchmark-for-3d-mesh-segmentation]).

Then, by using the nTopology(.ntop) file found on the root directory and the generator.py file, I systematicaly generated image slices for 14 types of lattice on 400 different mesh.

Using pattern_catcher_2.py, I acquired texture of images. By clustering according to their singular values, I reduced the number of slices to 4 per STL part.

Using channel_maker_2.py, I merged those 4 images into a single 4 channel image. Also I sorted the images according to their singular values.

Using lattice_separetor.py, I made new directories for each type of lattice. I placed 4 channel images into directories with proper indicing. Also I gave a maping from slice .zip file to these separeted 4 channel images. This mapping can be found on file_name_mapper.pickle file. It is used by the colab file as well.

Colab file contains the CNN and autoencoders used. I contains it's own explanations as well.


