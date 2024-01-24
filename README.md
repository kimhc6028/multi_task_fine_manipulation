# multi_task_fine_manipulation
Project Page: https://sites.google.com/view/multi-task-fine

Paper: https://arxiv.org/abs/2401.07603

Complementary Data Builder for the Multi-Task Fine Manipulation Dataset. This tool enhances the data available from the Multi-Task Fine Manipulation Dataset and is designed for use in conjunction with the dataset described in our accompanying paper. Additionally, it includes a feature to convert video data from MP4 format to HDF5 format, facilitating more efficient data handling and analysis.

## Usage
1) Download the dataset from https://sites.google.com/view/multi-task-fine and place it under 'downloaded_dataset'.
2) Convert the downloaded dataset, which consists of mp4 and h5 files, into an h5 file:
 ```
python h5_build.py
```

## Data Description
After the conversion process, you will find the HDF5 files in the 'h5_dataset' directory. The contents of these HDF5 files are as follows:

| Key                | Shape              | DataType | Description                                             |
|--------------------|--------------------|----------|---------------------------------------------------------|
| `desc`             | (1,)               | S42      | Language description                                    |
| `gaze`             | (length, 4)        | float32  | Human gaze ([left x, left y, right x, right y])         |
| `head_state`       | (length, 2)        | float32  | Camera joint state (fixed)                              |
| `left_foveated_img`| (length, 320, 360, 3) | uint8 | Left foveated vision                                    |
| `left_global_img`  | (length, 144, 256, 3) | uint8 | Left global vision                                      |
| `right_foveated_img`| (length, 320, 360, 3) | uint8 | Right foveated vision                                   |
| `right_global_img` | (length, 144, 256, 3) | uint8 | Right global vision                                     |
| `left_dual`        | (length,)          | int64   | Dual-action label of left robot arm                     |
| `left_hstate`      | (length, 7)        | float32 | Joint states of left controller (i.e., human)           |
| `left_state`       | (length, 7)        | float32 | Joint states of left robot arm                          |
| `right_dual`       | (length,)          | int64   | Dual-action label of right robot arm                    |
| `right_hstate`     | (length, 7)        | float32 | Joint states of right controller                        |
| `right_state`      | (length, 7)        | float32 | Joint states of right robot arm                         |


The language description can be retrieved as a string using the following code snippet: 
```f['desc'][0].decode()```.

The term "length" in the dataset refers to the length of each episode, with the data frequency set at 5Hz.

For calculating the forward kinematics of robot joint states, the Denavit-Hartenberg (DH) parameters for the UR5 robot can be utilized. Detailed DH parameters for UR5 are available in the [Universal Robots DH Parameters documentation](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/). For practical implementation, the [ikfastpy library on GitHub](https://github.com/andyzeng/ikfastpy) can be used to simplify this computation.

You can build the robot used in this research by following [this document](https://docs.google.com/document/d/1T3YJK7IVRwcna9iGkYi1mRSvquYTrXzVz6xZdrMhdac/edit?usp=share_link).

## Citation

If you use our dataset in your research, please cite our paper:
```
@article{kim2024multi,
  title={Multi-task robot data for dual-arm fine manipulation},
  author={Kim, Heecheol and Ohmura, Yoshiyuki and Kuniyoshi, Yasuo},
  journal={arXiv preprint arXiv:2401.07603},
  year={2024}}
```
