Small one-file scripts, written with learning purposes.

scan_dir_for_duplicates.py
        Scan directory for duplicates - files with equal content.
        Result dictionary (hash + list of os.DirEntry) stored in self.duplicates attribute.
        Formatted  output is also available via print(instance) command.
        See the example in the end of this module below the class code.

        :param path: string with absolute path to the directory.