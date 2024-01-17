# multi_task_fine_manipulation
Project Page: https://sites.google.com/view/multi-task-fine

Paper: https://arxiv.org/abs/2401.07603

Complementary Data Builder for the Multi-Task Fine Manipulation Dataset. This tool enhances the data available from the Multi-Task Fine Manipulation Dataset and is designed for use in conjunction with the dataset described in our accompanying paper. Additionally, it includes a feature to convert video data from MP4 format to HDF5 format, facilitating more efficient data handling and analysis

## Usage
1) Download the dataset from https://sites.google.com/view/multi-task-fine and place it under 'downloaded_dataset'
2) Convert the downloaded dataset, which consists of mp4 and h5 files, into an h5 file. ```python h5_build.py```

## Citation

If you use our dataset in your research, please cite our paper:
```
@inproceedings{kim2024multi,
  author = {Kim, Heecheol and Ohmura, Yoshiyuki and Kuniyoshi, Yasuo},
  title  = {Multi-task robot data for dual-arm fine manipulation},
  booktitle = {arXiv},
  year  = {2024}}
```
