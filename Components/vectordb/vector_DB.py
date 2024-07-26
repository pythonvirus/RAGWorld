from abc import ABC, abstractmethod
class VectorDB(ABC):

    @abstractmethod    
    def add_document(self):
        pass

    @abstractmethod
    def create_client(self):
        pass

    @abstractmethod
    def create_database(self):
        pass
        