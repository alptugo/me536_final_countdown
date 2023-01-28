import cv2
import numpy as np
import numpy.linalg as linalg
import os
from scipy.ndimage.measurements import center_of_mass
import zipfile
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import pdist
from sklearn.cluster import KMeans

display_on=False


log=open("log.txt", "w")



def rectangler(img, x,y,size):
    '''A function to get a rectengular slice of an ndarray.'''
    return img[x:x+size, y:y+size]



def pattern_catcher(slice, kernel_size, x, y, z=0):
    '''This is a function for detecting a repeating pattern in a given binary image (slicec). Kernel size is the size
    of the square repeating element. z is used for debugging and can be omitted. If a pattern is found,
    output is
    New image: the detected pattern filtered from the image and
    Kernel: repeating square shaped ndarray.
    else if there is no pattern
    False, False is returned'''

    #how many times will we move kernel
    translation_time=int(slice.shape[0]/kernel_size)-1
    is_kernel=False

    #starting with empty matrix for the pattern
    prev_rec=np.zeros(kernel_size)

    #starting with empty matrix for the filtered image
    new_image=np.zeros(slice.shape)

    #looping through x and y dimensions
    for i in range(translation_time):
        for k in range(translation_time):
            rec=rectangler(slice, x+i*kernel_size, y+k*kernel_size, kernel_size)

            #if the content of a square, the one beside it and the one beside and below it are the same, and if it is
            #not full black or full white, we have a pattern!
            if linalg.norm(prev_rec-rec)<np.sqrt(0.5) and not np.array_equal(rec,np.zeros((kernel_size, kernel_size))) and not np.array_equal(rec, np.ones((kernel_size,kernel_size))*255):
                new_image[x+i*kernel_size:x+(i+1)*kernel_size, y+k*kernel_size:y+(k+1)*kernel_size]=rec
                is_kernel=True
                kernel=rec
            else:
                pass

            prev_rec=rec
            z+=1
    if is_kernel:
        return new_image, kernel
    else:
        return False, False




zip_name_list=[]
#lists the names of files that end with .zip on the .\images folder
for file in os.listdir(os.path.join(os.getcwd(), "images")):
    if file.endswith(".zip"):
        zip_name_list.append(file)


zip_name_counter=1
#loops through every zip file, which each contains a lot of images
for zip_name in zip_name_list:
    path=os.path.join(os.getcwd(), "images", zip_name)
    imgzip = zipfile.ZipFile(path)
    inflist = imgzip.infolist()
    S_array = "undetermined"
    indice_map=[]
    i, kernel_container_counter=1, 0
    tiled_list=[]

    #loops trough every image in a zip file
    for f in inflist:
        ifile = imgzip.read(f)
        #reads a single image as grayscale
        slice = cv2.imdecode(np.frombuffer(ifile, np.uint8), cv2.IMREAD_GRAYSCALE)

        #displays the image read
        if display_on:
            cv2.imshow("original", slice)
            cv2.waitKey(0)
        x,y=0,0
        z=0
        kernel_size=12


        #checks for patterns in the image
        new_image, kernel=pattern_catcher(slice, kernel_size,x,y,z)

        #if there is a pattern in the image, new_image produced is not of type Boolean but instead of numpy.ndarray
        if type(new_image)==np.ndarray:


            count=np.count_nonzero(new_image)
            #check if there is enough pattern to bother
            if count>kernel_size*4:

                #tiles the patter 4x4 for the generation of a new image. This way, even the kernel is cropped from
                #different sections, singular values are the same for same patterns.
                tiled=np.tile(kernel, (4,4))
                tiled_list.append(tiled)

                #performs SVD to acquire said singular values
                _,S,_=linalg.svd(tiled)
                S.shape=(1, S.shape[0])
                if type(S_array)==type(" "):
                    S_array=S
                else:
                    S_array = np.append(S_array, S, axis=0)

                #counts the number of kernel found and slice number
                indice_map.append([kernel_container_counter, i])

                #shows the 4x4 tile if display is on
                if display_on:
                    cv2.imshow("abc", tiled)
                    cv2.waitKey(0)
                kernel_container_counter+=1
        i+=1

    #if no pattern is catched, type of S_array is kept string, and a log is kept.
    if type(S_array)==type(" "):
        log.writelines(f"I couldn't get any texture {zip_name}")
        continue

    #Creates a distance matrix from the biggest singular values of each immage
    distance_matrix = pairwise_distances(S_array, metric='euclidean')

    #if there are less than 4 slice with pattern data, there is not enough texture for lattice
    if distance_matrix.shape[0]<4:
        log.writelines(f"I couldn't get enough textures for {zip_name}")
        continue


    #In order to accurately show data on a small form, most dissimilar 4 slice are to be selected. For this clustering
    #is performed on the data.
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(distance_matrix)

    # gets the indices of the elements in each cluster
    cluster_indices = [np.where(kmeans.labels_ == i)[0] for i in range(4)]

    #the indices of slices inside the clusters are also sorted in-cluster, so that on the resulting 4 images,
    #Same type of tiles can correspond to same order.
    sorted_cluster_indices=[]
    if cluster_indices:
        for cluster in cluster_indices:
            if cluster.shape[0]>1:

                S_values = [[np.linalg.svd(tiled_list[layer], compute_uv=False)[0], cluster[i]] for layer, i in zip(cluster, range(cluster.shape[0]))]
                sorted_in_cluster_indices = np.array([mem[1] for mem in sorted(S_values)])
            elif cluster.shape[0]==1:
                sorted_in_cluster_indices=cluster
            else:
                sorted_in_cluster_indices=np.empty((0,1))
            sorted_cluster_indices.append(sorted_in_cluster_indices)
    print(sorted_cluster_indices)

    #picks the first tile out of each cluster. If there isn't 4 cluster, it returns to the first cluster
    selected_elements=[]
    repeater_index=0
    same_cluster_index=1
    if cluster_indices:
        for cluster in cluster_indices:
            if cluster.shape[0]>0:
                selected_elements.append(cluster[0])
            else:
                if len(cluster_indices[repeater_index])>same_cluster_index:
                    selected_elements.append(cluster_indices[repeater_index][same_cluster_index])
                else:
                    repeater_index+=1
                    same_cluster_index=1

                same_cluster_index+=1

        #save the selected 4 images with their slice names
        dis_mem_arr=np.array(selected_elements)
        for i in range(len(tiled_list)):
            if i in selected_elements:
                cv2.imwrite(f".\\output_example\\texture_{zip_name}_{indice_map[i][1]}.png", tiled_list[i])
                print(f"i saved /output_example/texture_{zip_name}_{indice_map[i][1]}.png")

    print(f"I am on {zip_name_counter} out of {len(zip_name_list)}")
    zip_name_counter+=1
log.close()