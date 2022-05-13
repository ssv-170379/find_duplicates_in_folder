import os
import hashlib


class ScanDirForDuplicates:
    blocksize = 65536  # chunk size for hashing big files

    def __init__(self, path: str) -> None:
        """
        Scan directory for duplicates - files with equal content.
        Result dictionary (hash + list of os.DirEntry) stored in self.duplicates attribute.
        Formatted  output is also available via print(instance) command.
        See the example in the end of this module below the class code.

        :param path: string with absolute path to the directory.
        """
        self.path = path
        self._file_list = self.scan_for_files()  # get list of files
        self._duplicates_size = self.find_duplicates_size()  # get files with non-unique size
        self.duplicates = self.find_duplicates_hash()  # get files with non-unique hash

    def __str__(self):  # formatted result output
        if not self.duplicates:
            return f'No duplicates found in {self.path}.'

        output = [f'Found duplicates in {self.path}.\n']
        for hash, files in d.duplicates.items():
            record = f'hash: {hash}\n' \
                     f'size: {files[0].stat().st_size} bytes\n' \
                     f'files: {", ".join([dir_entry.name for dir_entry in files])}\n' \
                     f'{"-" * 80}'
            output.append(record)
        return '\n'.join(output)

    def scan_for_files(self) -> [os.DirEntry]:
        data = os.scandir(self.path)
        return [e for e in data if e.is_file() and not e.is_symlink()]  # filter out dirs and symlinks

    @staticmethod
    def remove_unique(d: dict) -> dict:
        return {key: val for key, val in d.items() if len(val) > 1}  # return only multiple-value items (i.e. duplicates)

    def find_duplicates_size(self) -> dict:
        by_size = {}  # group files by size
        for i in range(len(self._file_list)):
            size = self._file_list[i].stat().st_size
            if size not in by_size:
                by_size[size] = [self._file_list[i]]
            else:
                by_size[size].append(self._file_list[i])
        return self.remove_unique(by_size)  # return only groups of files with duplicated size

    def get_hash(self, entry) -> str:
        hasher = hashlib.blake2s()
        with open(entry.path, 'rb') as f:
            buf = f.read(self.blocksize)
            while len(buf):
                hasher.update(buf)
                buf = f.read(self.blocksize)
        return hasher.hexdigest()

    def find_duplicates_hash(self) -> dict:
        by_hash = {}  # group files by hash
        for files in self._duplicates_size.values():  # process files with duplicated size
            for entry in files:
                file_hash = self.get_hash(entry)
                if not file_hash in by_hash:
                    by_hash[file_hash] = [entry]
                else:
                    by_hash[file_hash].append(entry)
        return self.remove_unique(by_hash)  # return only groups of files with duplicated hash


if __name__ == '__main__':
    path = '/bin'
    d = ScanDirForDuplicates(path)
    print(d)
