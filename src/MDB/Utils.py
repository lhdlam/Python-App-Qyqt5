import logging
from .config import ConfigSMartTool
import pandas as pd
from .Product import Product

logger = logging.getLogger('Utils')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)

def LoadProductListSingleSheet(productListExcelFilePath: str, sheet_index=0) -> list:
    """
    Load product list from first sheet.

    Parameters
    ----------
    productListExcelFilePath : str
        Path to product list file (Excel)
    
    Returns
    -------
    productList : list
        List of Product object
    """
    # Load 1st sheet as Product list
    df = pd.read_excel(productListExcelFilePath, sheet_name = sheet_index, header=0)

    # Print somes record
    df.head()
    
    # Load only some columns
    cols = list(ConfigSMartTool.SheetConfig["sheet00"].values())
    print(cols)
    cols = [val - 1 for val in cols]
    logger.info(cols)
    df2 = df.iloc[:, cols]
    df2.head()

    # Set cols name
    colNames = list(ConfigSMartTool.SheetConfig["sheet00"].keys())
    logger.info(colNames)
    df3 = df2.set_axis(colNames, axis='columns')

    # Get records list
    rowList = df3.to_dict('records')
    productList = []
    for row in rowList:
        newProduct = Product(row)
        if newProduct in productList:
            logger.warning("Duplicated, skipped, {0}".format(newProduct.shn_cd))
            continue
        productList.append(newProduct)

    return productList

if __name__ == '__main__':
    sampleFile = "ProductFolder/jan_cd.xlsx"
    productList = LoadProductListSingleSheet(sampleFile)
    for product in productList:
        product.describe()