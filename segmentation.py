import opts as opt
import os
import shutil

from mrcnn.my_inference import predict_images
from mrcnn.preprocess_images import preprocess_images
from mrcnn.convert_to_image import convert_to_image, convert_to_imagej

if opt.output_directory != '' and not os.path.isdir(opt.output_directory):
    os.mkdir(opt.output_directory)

if os.path.isdir(opt.output_directory):
    if len(os.listdir(opt.output_directory)) > 0:
        print ("ERROR: Make sure that the output directory to save masks to is empty.")
    else:
        preprocessed_image_directory = opt.output_directory + "/preprocessed_images/"
        preprocessed_image_list = opt.output_directory + "/preprocessed_images_list.csv"
        rle_file = opt.output_directory + "/compressed_masks.csv"
        output_mask_directory = opt.output_directory + "/masks/"
        output_imagej_directory = opt.output_directory + "/imagej/"

        # Preprocess the images
        if opt.verbose:
            print ("\nPreprocessing your images...")
        preprocess_images(opt.input_directory,
                          preprocessed_image_directory,
                          preprocessed_image_list,
                          verbose = opt.verbose)

        if opt.verbose:
            print ("\nRunning your images through the neural network...")
        predict_images(preprocessed_image_directory,
                       preprocessed_image_list,
                       rle_file,
                       rescale = opt.rescale,
                       scale_factor = opt.scale_factor,
                       verbose = opt.verbose)

        if opt.save_masks == True:
            if opt.verbose:
                print("\nSaving the masks...")
            
            if opt.output_imagej == True:
                convert_to_image(rle_file,
                                 output_mask_directory,
                                 preprocessed_image_list,
                                 rescale=opt.rescale,
                                 scale_factor=opt.scale_factor,
                                 verbose = opt.verbose)
                
                convert_to_imagej(output_mask_directory,
                                  output_imagej_directory)
            else:
                convert_to_image(rle_file,
                                 output_mask_directory,
                                 preprocessed_image_list,
                                 rescale=opt.rescale,
                                 scale_factor=opt.scale_factor,
                                 verbose = opt.verbose)

        os.remove(preprocessed_image_list)
        
        if not opt.save_preprocessed:
            shutil.rmtree(preprocessed_image_directory)

        if not opt.save_compressed:
            os.remove(rle_file)

        if not opt.save_masks:
            shutil.rmtree(output_mask_directory)


