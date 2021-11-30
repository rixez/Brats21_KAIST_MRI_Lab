# Winning submission to the 2021 Brain Tumor Segmentation Challenge

This repo contains the codes and pretrained weights for the winning submission to the 2021 Brain Tumor Segmentation Challenge by KAIST MRI Lab Team.
The code was developed on top of the excellent [nnUNet library](https://github.com/MIC-DKFZ/nnUNet). Please refer to the original repo for the installation, usages, and common Q&A

## Inference with docker image
You can run the inference with the docker image that we submitted to the competition by following these instructions:

1. Install `docker-ce` and `nvidia-container-toolkit` ([instruction](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html))
2. Pull the docker image from [here](https://hub.docker.com/r/rixez/brats21nnunet)
3. Gather the data you want to infer on in one folder. The naming of the file should follow the convention: `BraTS2021_ID_<contrast>.nii.gz` with `contrast` being `flair, t1, t1ce, t2`
4. Run the command: ```docker run -it --rm --gpus device=0 --name nnunet -v "/your/input/folder/":"/input" -v "/your/output/folder/":"/output" rixez/brats21nnunet ```, replacing `/your/input/folder` and `/your/output/folder` with the absolute paths to your input and output folder.
5. You can find the prediction results in the specified output folder.

The docker container was built and verified with Pytorch 1.9.1, Cuda 11.4 and a RTX3090. It takes about 4GB of GPU memory for inference with the docker container. The provided docker image might not work with different hardwares or cuda version. In that case, you can try running the models from the command line.

## Inference with command line
If you want to run the model without docker, first, download the models from [here](https://drive.google.com/file/d/1yWgD1JlEocXRWVMAYOa7YKtQLEhDjhIx/view?usp=sharing). Extract the files and put the models in the `RESULTS_FOLDER` that you set up with nnUNet.
Then run the following commands:
```
nnUNet_predict -i <input_folder> -o <output_folder1> -t <TASK_ID> -m 3d_fullres -tr nnUNetTrainerV2BraTSRegions_DA4_BN_BD --save_npz
nnUNet_predict -i <input_folder> -o <output_folder2> -t <TASK_ID> -m 3d_fullres -tr nnUNetTrainerV2BraTSRegions_DA4_BN_BD_largeUnet_Groupnorm --save_npz
nnUNet_ensemble -f <output_folder1> <output_folder2> -o <final_output_folder>
```
You need to specify the options in `<>`. `TASK_ID` is 500 for the pretrained weights but you can change it depending on the task ID that you set with your installation of nnUNet. To get the results that we submitted, you need to additionally apply post-processing threshold for of 200 and convert the label back to BraTS convention. You can check this [file](nnunet/dataset_conversion/Task500_BraTS_2021.py) as an example.

## Training with the model
You can train the models that we used for the competition using the command:
```
nnUNet_train 3d_fullres nnUNetTrainerV2BraTSRegions_DA4_BN_BD <TASK_ID> <FOLD> --npz # BL config
nnUNet_train 3d_fullres nnUNetTrainerV2BraTSRegions_DA4_BN_BD_largeUnet_Groupnorm <TASK_ID> <FOLD> --npz # BL + L + GN config
```

