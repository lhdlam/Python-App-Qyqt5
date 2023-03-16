from asyncio.log import logger
import glob
import os
import csv
import math

class Product:
    """
    Product class

    Attributes
    ----------
    shn_cd : str
        Product JAN
    price : str
        Consider as string
    department_name : str

    """

    def __init__(self, row):
        """
        Constructor

        Parameters
        ----------
        row : str
            Record from Product List file

        """
        self.shn_cd = None
        self.price = None
        self.department_name = None
        self.storagePath = None
        for col in row:
            setattr(self, col, str(row[col]))

        if (self.shn_cd):
            self.shn_cd = str(math.trunc(float(self.shn_cd))).zfill(13)
            # if (self.shn_cd.isnumeric()):
            #     self.shn_cd = "{0:.0}".format(self.shn_cd).zfill(13)
            # else:
            #     self.shn_cd = "{0:.0}".format(self.shn_cd).zfill(13)

    def __eq__(self, __o: object) -> bool:
        if (isinstance(__o, Product)):
            return self.shn_cd == __o.shn_cd

    def getBasePath(self):
        return os.path.join(self.storagePath, self.shn_cd)

    def getImageDataPath(self):
        return os.path.join(self.storagePath, self.shn_cd)

    def getTextDataPath(self):
        return os.path.join(self.storagePath, self.shn_cd)

    def getTextDataFullPath(self):
        return os.path.join(self.getTextDataPath(), "{0}.csv".format(self.shn_cd))
    
    def getVersionDataFullPath(self):
        return os.path.join(self.getTextDataPath(), "{0}.version".format(self.shn_cd))

    def getInfoDataPath(self):
        return os.path.join(self.storagePath, self.shn_cd)


    def getCustomVersionPath(self):
        return os.path.join(self.storagePath, self.shn_cd)

    def getTextValidationPath(self):
        return os.path.join(self.getBasePath(),"validation")

    def getTextProcessPath(self):
        return os.path.join(self.getBasePath(),"process_1")

    def getImageProcessPath(self):
        return os.path.join(self.getBasePath(),"process_2")

    def describe(self):
        """
        Print summary
        """
        print("shc_cd :{0}, price :{1}, department_name :{2}, storage path :{3}".format(
            self.shn_cd,
            self.price,
            self.department_name,
            self.storagePath
        )
        )

    def isExistingData(self):
        return os.path.isdir(self.getBasePath())

    def getCSVProcessFullPath(self):
        return os.path.join(
                self.getTextProcessPath(),
                "{0}.csv".format(self.shn_cd)
                )

    def getImagesProcessFullPaths(self):
        # Get all file with pattern :{JAN}_*_0.PNG
        return glob.glob(
            os.path.join(
                self.getImageProcessPath(),
                "{0}_*_0.PNG".format(self.shn_cd)
            )
        )

    def isExistingTextData(self):
        return os.path.isfile(
            self.getTextDataFullPath()
        )

    def isExistingCSVProcessResult(self):
        return os.path.isfile(
            self.getCSVProcessFullPath()
        )
    
    def isExistingImageProcessResult(self):
        return (len(self.getImagesProcessFullPaths()) > 0)

    def makeDirectory(self):
        if (not os.path.isdir(self.getBasePath())):
            os.makedirs(self.getBasePath())

    def deleteDirectoryIfEmpty(self):
        if (len(os.listdir(self.getBasePath())) == 0):
            os.rmdir(self.getBasePath())

    def makeProcessTextDirectory(self):
        if (not os.path.isdir(self.getTextProcessPath())):
             os.makedirs(self.getTextProcessPath())
             
    def __str(self):
        return "Product(jan={0}, price={1}, department_name={2})".format(self.shn_cd, self.price, self.department_name)