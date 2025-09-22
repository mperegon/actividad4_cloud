from abc import ABC, abstractmethod

class FileStorageInterface(ABC):
    @abstractmethod
    def put_file(self, local_path:str,remote_identifier: str):
        pass
    @abstractmethod
    def get_file(self, rmeote_path: str, local_folder: str):
        pass
    @abstractmethod
    def rmeove_file(self,remote_path: str):
        pass