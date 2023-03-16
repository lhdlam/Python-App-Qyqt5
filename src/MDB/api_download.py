import logging
import os
from .APICaller import APICaller
from .APIRequests import GetItemInfoRequest, GetItemTextRequest
from .APIRequests import GetPictureRequest
from .APIRequests import GetItemTextQueryFields
from .Utils import LoadProductListSingleSheet
from .Product import Product
from .config import ConfigSMartTool
import csv
import base64

# import sys
# sys.path.append('D:\\Scropper\\python_app')
# import run

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

# def Download(path, products, sheet):
    
  
  
#     logger.info("Configuration")
#     logger.info("Default from_date :{0}".format(
#         ConfigSMartTool.APIConfig['from_date']))
#     absPath = os.path.abspath(path)
#     logger.info("Abs path :{0}".format(absPath))

#     # Download
#     logger.debug("Download")
#     productListExcelFile = products
#     logger.info("Product list file :{0}".format(productListExcelFile))

#     # Load product list
#     productList = LoadProductListSingleSheet(
#         productListExcelFile, sheet-1)
#     logger.info("Number of product :{0}".format(len(productList)))

#     # Set storage path
#     for product in productList:
#         product: Product = product
#         product.storagePath = absPath

#     # For each product
#     apiCaller = APICaller()
#     apiCaller.authen()
#     download_result_list = []
#     for product in productList:
#         print("qqqq")
#         product: Product = product
#         # product.describe()
#         # If existing and not overwrite, skip
#         logger.debug("Product path :{0}".format(product.getBasePath()))
#         if product.isExistingData():
#             logger.info(
#                 "{0} Existing, still download : ".format(product.shn_cd))
#             download_result = download_product(
#                 product=product, apiCaller=apiCaller)
#             download_result_list.append([product.shn_cd, download_result])
#         else:
#             logger.info(" {0} New downloading".format(product.shn_cd))
#             download_result = download_product(
#                 product=product, apiCaller=apiCaller,
#                 )
#             download_result_list.append([product.shn_cd, download_result])

#     # if args.report != None:
#     #     with open(args.report, 'w', encoding='UTF8') as f:
#     #         csvWriter = csv.writer(f)
#     #         csvWriter.writerow(["jan", "result"])
#     #         csvWriter.writerows(download_result_list)

def download_product(product: Product, 
            apiCaller: APICaller, 
            isUpdateVersion=False,
            isUpdateVersionOnly=False
            ):
    product.makeDirectory()    
    result = ""
    product_version_info_list = download_version_info(
        product=product, apiCaller=apiCaller)
    if (len(product_version_info_list) > 0):
        # Create folder if has some data
        if (isUpdateVersionOnly == True):
            result = "OK"
        else:
            text_data = download_text(
                product=product, apiCaller=apiCaller, isUpdateVersion=isUpdateVersion)
            if ("errors" not in text_data):
                download_result = download_image(product=product, apiCaller=apiCaller,
                                                text_data=text_data)
                if ("errors" in download_result):
                    result = download_result["errors"]
                else:
                    result = "OK"
            else:
                result = text_data["errors"]
    else:
        logger.info("{0} was not found".format(product.shn_cd))
        result = "NOT FOUND"

    product.deleteDirectoryIfEmpty()
    return result
  

def download_version_info(product: Product, apiCaller: APICaller):
    jancode = product.shn_cd
    logger.info("{0} search".format(jancode))

    # Download info data
    infoDataSavePath = product.getInfoDataPath()
    infoFilename = "{0}.version".format(jancode)
    infoDataFullPath = os.path.join(infoDataSavePath, infoFilename)

    getItemInfoRequest = GetItemInfoRequest(
        jans=[jancode], from_date=ConfigSMartTool.APIConfig['from_date'])
    queryResults = apiCaller.GetItemInfo(getItemInfoRequest)

    errors = queryResults.get('errors', None)
    versions = []
    if (errors == None):
        resultList = queryResults['data']['GetItemInfo']

        if (len(resultList) <= 0):
            logger.error("{0} No item info available".format(jancode))
            return versions

        with open(infoDataFullPath, 'w', encoding='UTF8', newline='') as f:
            csvWriter = csv.writer(f)
            for indx, ItemInfo in enumerate(resultList):
                rowData = []
                rowData.append(jancode)
                rowData.append(indx + 1)
                logger.debug(ItemInfo)
                rowData.append(ItemInfo['add_date'])
                rowData.append(ItemInfo['upd_date'])
                if (indx == 0):
                    rowData.append('Latest')
                else:
                    rowData.append('')

                versions.append({
                    'add_date': ItemInfo['add_date'],
                    'update_date': ItemInfo['upd_date']
                })
                csvWriter.writerow(rowData)
            logger.info("{0} Write version file {1}".format(
                jancode, infoDataFullPath))
    else:
        logger.error("{0} API Error :{1}".format(jancode, errors))

    return versions



def download_text(product: Product, apiCaller: APICaller, isUpdateVersion=False):
    jancode = product.shn_cd
    logger.info("{0} download text".format(jancode))

    # Download text data
    textDataSavePath = product.getTextDataPath()
    textFilename = "{0}.csv".format(jancode)
    textDataFullPath = os.path.join(textDataSavePath, textFilename)

    result = {}

    getTextDataRequest = GetItemTextRequest(
        jans=[jancode], from_date=ConfigSMartTool.APIConfig['from_date'])
    queryResults = apiCaller.GetItemText(getTextDataRequest)
    if (queryResults is not {}):
        logger.debug("queryResults")
        errors = queryResults.get('errors', None)
        if (errors == None):
            resultList = queryResults['data']['GetItemText']
            if (len(resultList) > 0):
                if (isUpdateVersion):  # Update version
                    versionFullPath = product.getVersionDataFullPath()
                    with open(versionFullPath, 'w', encoding='UTF8', newline='') as f:
                        csvWriter = csv.writer(f)
                        csvWriter.writerow(["add_date", "upd_date"])
                        for revison in resultList:
                            rowData = []
                            rowData.append(revison["add_date"])
                            rowData.append(revison["upd_date"])
                            csvWriter.writerow(rowData)
                        logger.info("{0} Write versions {1}".format(
                            jancode, versionFullPath))

                # Load custom version
                result = resultList[0]  # Latest version

            if (not result):
                logger.error("{0} No text data available".format(jancode))
                result["errors"] = "NO TEXT DATA"
                return

            with open(textDataFullPath, 'w', encoding='UTF8', newline='') as f:
                csvWriter = csv.writer(f)
                # Write header
                csvWriter.writerow(GetItemTextQueryFields)
                # Write data
                rowData = []
                for textField in GetItemTextQueryFields:
                    rowData.append(result[textField])
                csvWriter.writerow(rowData)
                logger.info("{0} Write csv {1}".format(jancode, textFilename))
        else:
            logger.error("{0} API Error :{1}".format(jancode, errors))
            result["errors"] = "API ERROR :{0}".format(errors)
    else:
        logger.error("No text data available")
        result["errors"] = "No text data available"

    return result


Image_Men_No = {
    "0": "01",
    "45": "07",
    "90": "03",
    "135": "08",
    "180": "20",
    "225": "09",
    "270": "22",
    "315": "13",
    "TOP": "02",
    "BOTTOM": "21",
    "UPPER": "65",
}


def download_image(product: Product, apiCaller: APICaller, text_data):
    jancode = product.shn_cd
    logger.info("{0} download image".format(jancode))

    result = {}

    if not text_data:
        logger.error("{0}: No image data avaliable".format(jancode))
        result["errors"] = "NO IMAGE DATA AVAILABLE"
        return result

    mkr_pv_cd = text_data['mkr_pv_cd']
    logger.info("{0} mkr_pv_cd :{1}".format(jancode, mkr_pv_cd))

    imageDataSavePath = product.getImageDataPath()
    isFrontImage = False
    for img_men in Image_Men_No:
        img_men_no_val = Image_Men_No[img_men]
        imageFileName = "{0}_{1}_{2}.JPG".format(jancode, mkr_pv_cd, img_men)
        imageDataSaveFullPath = os.path.join(imageDataSavePath, imageFileName)
        getPictureDataRequest = GetPictureRequest(
            jan=jancode,
            mkr_pv_cd=mkr_pv_cd,
            img_men_no=img_men_no_val
        )
        logger.info("{0} Download image {1}".format(jancode, imageFileName))
        queryResults = apiCaller.GetPicture(getPictureDataRequest)
        errors = queryResults.get('errors', None)
        if (errors == None):
            resultList = queryResults['data']['GetPicture']
            if (len(resultList) > 0):
                result = resultList[0]  # Latest version
            else:
                logger.error("{0} no image data".format(jancode))
                result["img_men"] = "NO IMAGE DATA"
                continue
            imgdata = base64.b64decode(result['img_image'])
            with open(imageDataSaveFullPath, 'wb') as f:
                f.write(imgdata)
                logger.info("{0} Write image {1}".format(
                    jancode, imageFileName))

            if (img_men == "0"):
                isFrontImage = True
        else:
            logger.error("{0} API Error :{1}".format(jancode, errors))
            result[img_men] = "API Error :{0}".format(errors)

    if (isFrontImage == False):
        result["errors"] = "NO Front Image"

    return result
