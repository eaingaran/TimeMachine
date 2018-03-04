import datetime
import logging
import os
from shutil import copyfile

from utilities import Path


def archive_file(file, scenario_name, archive_file_type):
    try:
        if not os.path.exists(os.path.join(os.path.join(os.path.join(os.path.join(Path.get_base_path(), "Archive"),
                                                                     scenario_name), str(datetime.date.today())),
                                           archive_file_type)):
            os.mkdir(os.path.join(os.path.join(os.path.join(os.path.join(Path.get_base_path(), "Archive"),
                                                            scenario_name), str(datetime.date.today())),
                                  archive_file_type))
        head, tail = os.path.split(Path.get_base_path() + file)
        copyfile(Path.get_base_path() + file,
                 os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(Path.get_base_path(),
                                                                     "Archive"), scenario_name),
                                                        str(datetime.date.today())), archive_file_type), tail))
    except Exception as e:
        logging.error("archive failed", e)
