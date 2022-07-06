import os 

class FilePath():
    def __init__(self, fichier):
        self.ficher = str(fichier)
        
    def __str__(self):
        absPath = os.path.abspath(__file__)
        pthDir1 = os.path.dirname(absPath)
        pthDir2 = os.path.dirname(pthDir1)
        fchPath = os.path.join(pthDir2, self.ficher)
        return (fchPath)