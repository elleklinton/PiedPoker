import pickle

class FileHandler:
    OUTPUT_DIR = 'lookup_table/out/'

    @staticmethod
    def save(o: object, fp: str):
        """
        Saves the object o to the filepath fp inside the lookup_table/out/* directory
        :param o: The object to save
        :type o: object
        :param fp: The filepath to save the object to
        :type fp: str
        """
        with open(FileHandler.OUTPUT_DIR + fp, 'wb') as file:
            pickle.dump(o, file)



    @staticmethod
    def load(fp: str) -> dict:
        """
        Loads the object at filepath fp from the lookup_table/out/* directory
        :param fp: Filepath of object to retrieve
        :type fp: str
        :return: Object contained at filepath
        :rtype: object
        """
        with open(FileHandler.OUTPUT_DIR + fp, 'rb') as file:
            return pickle.load(file)
