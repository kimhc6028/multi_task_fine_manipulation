import os
import cv2
import h5py
from tqdm import tqdm
import numpy as np
import shutil
import zipfile


def unzip_files(zip_dataset_path, extract_dataset_path):
    for root, dirs, files in os.walk(zip_dataset_path):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dataset_path)
                    # Check and remove the __MACOSX folder if it exists
                    macosx_path = os.path.join(extract_dataset_path, '__MACOSX')
                    if os.path.exists(macosx_path):
                        shutil.rmtree(macosx_path)


def check_dataset_lengths(h5_file):
    lengths = [h5_file[key].shape[0] for key in h5_file if key != 'desc']
    return all(length == lengths[0] for length in lengths)


def process_video_to_h5(mp4_path, h5_file, left_key, right_key):
    cap = cv2.VideoCapture(mp4_path)
    left_frames = []
    right_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        mid_point = frame.shape[1] // 2
        left_frame = frame[:, :mid_point]
        right_frame = frame[:, mid_point:]

        left_frames.append(left_frame)
        right_frames.append(right_frame)

    cap.release()

    left_frames_np = np.array(left_frames)
    right_frames_np = np.array(right_frames)

    for key in h5_file:
        if key != 'desc' and h5_file[key].shape[0] != len(left_frames_np):
            print(f"Video length mismatch for {mp4_path} compared to dataset '{key}' in H5 file.")
            return False

    h5_file.create_dataset(left_key, data=left_frames_np)
    h5_file.create_dataset(right_key, data=right_frames_np)
    return True


def process_h5_files(zip_dataset_path, extract_dataset_path, h5_dataset_path):
    unzip_files(zip_dataset_path, extract_dataset_path)
    h5_files = []

    for root, dirs, files in os.walk(extract_dataset_path):
        for file in files:
            if file.endswith('.h5'):
                h5_files.append(os.path.join(root, file))

    for h5_file_path in tqdm(h5_files, desc="Processing .h5 files"):
        base_filename = os.path.splitext(os.path.basename(h5_file_path))[0]
        global_mp4_file = base_filename + '_global.mp4'
        foveated_mp4_file = base_filename + '_foveated.mp4'

        global_mp4_path = os.path.join(os.path.dirname(h5_file_path), global_mp4_file)
        foveated_mp4_path = os.path.join(os.path.dirname(h5_file_path), foveated_mp4_file)

        if os.path.exists(global_mp4_path) and os.path.exists(foveated_mp4_path):
            relative_path = os.path.relpath(os.path.dirname(h5_file_path), extract_dataset_path)
            dest_folder = os.path.join(h5_dataset_path, relative_path)
            os.makedirs(dest_folder, exist_ok=True)
            dest_h5_file_path = os.path.join(dest_folder, os.path.basename(h5_file_path))

            if os.path.exists(dest_h5_file_path):
                with h5py.File(dest_h5_file_path, 'r') as processed_file:
                    if all(key in processed_file for key in ['left_global_img', 'right_global_img', 'left_foveated_img', 'right_foveated_img']):
                        continue  # Skip this file as it has already been processed

            print(h5_file_path)
            with h5py.File(h5_file_path, 'r') as h5_file:
                if not check_dataset_lengths(h5_file):
                    print(f"Dataset length mismatch in file {h5_file_path}")
                    return
                print(dest_h5_file_path)

                with h5py.File(dest_h5_file_path, 'w') as new_h5_file:
                    global_length_result = process_video_to_h5(global_mp4_path, new_h5_file, 'left_global_img', 'right_global_img')
                    foveated_length_result = process_video_to_h5(foveated_mp4_path, new_h5_file, 'left_foveated_img', 'right_foveated_img')

                    if not global_length_result or not foveated_length_result:
                        os.remove(dest_h5_file_path)
                        return

                    for key in h5_file:
                        new_h5_file.create_dataset(key, data=h5_file[key], compression='lzf')


zip_dataset_path = 'downloaded_dataset'
extract_dataset_path = 'extracted_dataset'
h5_dataset_path = 'h5_dataset'

process_h5_files(zip_dataset_path, extract_dataset_path, h5_dataset_path)

