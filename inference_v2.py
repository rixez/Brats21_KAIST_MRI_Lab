import os
import numpy as np
import torch
from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.dataset_conversion.Task500_BraTS_2021 import apply_threshold_to_folder
from nnunet.dataset_conversion.Task032_BraTS_2018 import convert_labels_back_to_BraTS_2018_2019_convention
import shutil

def main():
    input_folder = '/input'
    output_folder = '/output'

    tmp_input_folder = '/tmp_input'
    tmp_output_folder = '/tmp_output'
    maybe_mkdir_p(tmp_input_folder)
    os.system("export RESULTS_FOLDER=/usr/local/bin/trained_models/")
    #convert raw data to nnunet format
    contrast_to_number = {'t1':'0000', 't1ce':'0001','t2':'0002','flair':'0003'}
    for p in subfiles(input_folder, join=False):
        tokens = p.split('_')
        patient_id = tokens[0] + "_" + tokens[1]
        contrast = tokens[-1].split('.')[0]
        shutil.copy(join(input_folder, p), join(tmp_input_folder, patient_id + "_" + contrast_to_number[contrast] + ".nii.gz"))

    #run nnunet inference
    tmp_output_folder_BL = join(tmp_output_folder,'raw_output_1')
    tmp_output_folder_BL_L_GN = join(tmp_output_folder,'raw_output_2')
    tmp_output_folder_ensemble = join(tmp_output_folder,'ensemble')
    os.system("nnUNet_predict -i {} -o {} -t 500 -m 3d_fullres -tr nnUNetTrainerV2BraTSRegions_DA4_BN_BD --save_npz".format(tmp_input_folder, tmp_output_folder_BL))
    os.system("nnUNet_predict -i {} -o {} -t 500 -m 3d_fullres -tr nnUNetTrainerV2BraTSRegions_DA4_BN_BD_largeUnet_Groupnorm --save_npz".format(tmp_input_folder, tmp_output_folder_BL_L_GN))
    os.system("nnUNet_ensemble -f {} {} -o {}".format(tmp_output_folder_BL,tmp_output_folder_BL_L_GN,tmp_output_folder_ensemble))
    apply_threshold_to_folder(tmp_output_folder_ensemble, join(tmp_output_folder, 'pp_output'), 200, 2)
    convert_labels_back_to_BraTS_2018_2019_convention(join(tmp_output_folder,'pp_output'), join(tmp_output_folder,'pp_output_converted'))

    for p in subfiles(join(tmp_output_folder,'pp_output_converted'), join=False):
        patient_id = p.split('_')[1].split('.')[0]
        shutil.copy(join(tmp_output_folder,'pp_output_converted',p),join(output_folder,patient_id + ".nii.gz"))

if __name__ == '__main__':
    main()