import os
import pickle

def save(object, path):
    """ Saves object to path. Wraps pickle for consolidated codebase. """
    file = open(path, "wb")
    pickle.dump(object, file, pickle.HIGHEST_PROTOCOL)
    print(f"Object successfully saved to {path}.")

def load(path):
    """ Loads object from path. Wraps pickle for consolidated codebase. """
    file = open(path, "rb")
    object = pickle.load(file)
    return object

def delete_folder(folderPath):
    """ Deletes folderPath and contents """
    if os.path.exists(folderPath):
        for file in os.listdir(folderPath):
            os.remove(f'{folderPath}/{file}')
        os.rmdir(folderPath)
