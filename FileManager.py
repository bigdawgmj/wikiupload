""" Manages Wiki Files """
import os
import pdb

class FileManager:
    """ Gets files for the program in order to upload to google drive """
    def __init__(self, path):
        """ Init FileManager """
        self.path = path

    def get_files_after_date(self, date_str):
        """ Gets a file after a date string """
        path_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        filter_files = []
        # pdb.set_trace()
        for f in path_files:
            if date_str < f and 'diary' not in f:
                filter_files.append(f)
        return filter_files