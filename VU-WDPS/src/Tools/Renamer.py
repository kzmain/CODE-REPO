import glob
import os


def rename_file_at_location(path, old_prefix, new_prefix, file_type):
    files = glob.glob(path + "/" + old_prefix + "*" + file_type)
    for file in files:
        os.rename(file, file.replace(old_prefix, new_prefix))

