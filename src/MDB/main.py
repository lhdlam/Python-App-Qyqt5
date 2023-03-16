import logging
from logging.handlers import TimedRotatingFileHandler
from math import prod
import os

from cmd_menus import createArgParser
from enum import IntEnum
from APICaller import APICaller
from APIRequests import GetItemInfoRequest, GetItemTextRequest
from APIRequests import GetPictureRequest
from APIRequests import GetItemTextQueryFields
from Utils import LoadProductListSingleSheet
from validateFileCSV import validateFileCSV
from Product import Product
from config import ConfigSMartTool
import csv
import base64
from CSVDefine import CSVDefine

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)

# fileHandler = logging.FileHandler("csvtools.log")
rotationHandler = TimedRotatingFileHandler('csvtools.log', 
                                   when='midnight', encoding='utf-8',
                                   backupCount=10)
rotationHandler.setFormatter(formatter)

logger.addHandler(rotationHandler)


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


def load_custom_version(product: Product, versions=[]):
    jancode = product.shn_cd

    # Download text data
    customVersionPath = product.getCustomVersionPath()
    customVersionFilename = "{0}.current".format(jancode)
    customVersionFullPath = os.path.join(
        customVersionPath, customVersionFilename)

    currentVersionName = 'update_latest'
    if os.path.isfile(customVersionFullPath):
        with open(customVersionFullPath) as fp:
            currentVersionName = fp.readline().strip()

    currentVersion = {}
    if (currentVersionName == 'update_latest'):
        currentVersion = max(versions, lambda x: x['upd_date'])
    else:
        cust_add_date, cust_upd_date = currentVersionName.split(',')
        for version in versions:
            if (
                (version['add_date'] == cust_add_date) and
                (version['upd_date'] == cust_upd_date)
            ):
                currentVersion = version
                break

    if (not currentVersion):
        currentVersion = max(versions, lambda x: x['upd_date'])

    return currentVersion


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


def Download(args):
    logger.info("Configuration")
    logger.info("Default from_date :{0}".format(
        ConfigSMartTool.APIConfig['from_date']))
    absPath = os.path.abspath(args.path)
    logger.info("Abs path :{0}".format(absPath))

    # Download
    logger.debug("Download")
    productListExcelFile = args.products
    logger.info("Product list file :{0}".format(productListExcelFile))

    # Load product list
    productList = LoadProductListSingleSheet(
        productListExcelFile, args.sheet-1)
    logger.info("Number of product :{0}".format(len(productList)))

    # Set storage path
    for product in productList:
        product: Product = product
        product.storagePath = absPath

    # For each product
    apiCaller = APICaller()
    apiCaller.authen()
    download_result_list = []
    for product in productList:
        product: Product = product
        # product.describe()

        # If existing and not overwrite, skip
        logger.debug("Product path :{0}".format(product.getBasePath()))
        if product.isExistingData():
            if not args.overwrite:
                logger.info(
                    "{0} Existing, skip download cause overwrite option".format(product.shn_cd))
                download_result_list.append([product.shn_cd, "SKIPPED"])
                continue
            else:
                logger.info(
                    "{0} Existing, still download : ".format(product.shn_cd))
                download_result = download_product(
                    product=product, apiCaller=apiCaller, 
                    isUpdateVersionOnly=args.update_version_only)
                download_result_list.append([product.shn_cd, download_result])
        else:
            logger.info(" {0} New downloading".format(product.shn_cd))
            download_result = download_product(
                product=product, apiCaller=apiCaller,
                isUpdateVersionOnly=args.update_version_only
                )
            download_result_list.append([product.shn_cd, download_result])

    if args.report != None:
        with open(args.report, 'w', encoding='UTF8') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(["jan", "result"])
            csvWriter.writerows(download_result_list)


def Text_Data_Validation(args):
    # Text data validation
    logger.debug("Text_Data_Validation")
    print("Validate data CSV")
    data = validateFileCSV()
    print(data)
    print("Successfully!")

def csv_process_adjust(newTextData):
    # gtin_cd
    if not newTextData["gtin_cd"]:
        newTextData["gtin_cd"] = "0"
    if not newTextData["next_gtin_cd"]:
        newTextData["next_gtin_cd"] = "0"

def csv_process_product(product: Product):
    csvResultFullPath = product.getCSVProcessFullPath()
    logger.info("{0} Process CSV to :{0}".format(
        product.shn_cd, csvResultFullPath))

    # Make sure directory is existing
    product.makeProcessTextDirectory()

    # Load original CSV
    orgTextData = {}
    with open(product.getTextDataFullPath(), encoding='utf8', newline='') as orgCSVFile:
        reader = csv.DictReader(orgCSVFile)
        for row in reader:
            orgTextData = row
            break

    # Create new CSV data
    newTextData = {}

    for field in CSVDefine.NewFormatFields:
        fieldID, _, _, fieldDefaultValue = field
        newTextData[fieldID] = fieldDefaultValue

    for field in CSVDefine.NewFormatFields:
        fieldID, _, _, _ = field
        # Mapping  MDB -> NewFormat (same field name)
        if (fieldID in orgTextData):
            newTextData[fieldID] = orgTextData[fieldID]

    # Mapping MDB -> NewFormat (by Master Table )
    for unitField in CSVDefine.UnitMap:
        newFieldName, orgFieldName = unitField
        if (orgTextData[orgFieldName] != ''):
            newTextData[newFieldName] = CSVDefine.UnitNames[orgTextData[orgFieldName]]
        else:
            newTextData[newFieldName] = ''

    # Mapping MDB -> New format (different field)
    for field in CSVDefine.Org2NewFormat:
        newFieldName, orgFieldName = field
        newTextData[newFieldName] = orgTextData[orgFieldName]

    csv_process_adjust(newTextData)

    # Load 3 fields from Excel
    logger.debug("{0} price {1}".format(product.shn_cd, product.price))
    newTextData["price"] = None
    if (product.price):        
        priceInt = 0
        try:
            priceInt = int(float(product.price))
        except:
            logger.warning("Invalid price value of {0}".format(product.shn_cd))

        newTextData["price"] = str(priceInt)

    logger.debug("{0} new price {1}".format(product.shn_cd, newTextData["price"]))
    newTextData["department_name"] = product.department_name
    newTextData["tax_rate_kbn"] = "2"

    with open(csvResultFullPath, 'w', encoding='UTF8', newline='') as f:
        csvWriter = csv.writer(f)
        row1 = [field[1] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row1)
        row2 = [field[2] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row2)
        row3 = [field[0] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row3)

        dataRow = []
        for field in CSVDefine.NewFormatFields:
            fieldID, _, _, _ = field
            dataRow.append(newTextData[fieldID])
        csvWriter.writerow(dataRow)


def Text_Data_Process(args):
    logger.info("Configuration")
    logger.info("Default from_date :{0}".format(
        ConfigSMartTool.APIConfig['from_date']))
    absPath = os.path.abspath(args.path)
    logger.info("Abs path :{0}".format(absPath))

    # Download
    logger.debug("Text_Data_Process")
    productListExcelFile = args.products
    logger.info("Product list file :{0}".format(productListExcelFile))

    # Load product list
    productList = LoadProductListSingleSheet(
        productListExcelFile, args.sheet - 1)
    logger.info("Number of product :{0}".format(len(productList)))

    # Set storage path
    for product in productList:
        product: Product = product
        product.storagePath = absPath

    # For each product
    for product in productList:
        product: Product = product
        # product.describe()

        # If existing and not overwrite, skip
        logger.debug("CSV org path :{0}".format(product.getTextDataFullPath()))
        if product.isExistingTextData():
            logger.debug("CSV result path :{0}".format(
                product.getCSVProcessFullPath()))
            if product.isExistingCSVProcessResult():
                if not args.overwrite:
                    logger.info("{0} Existing, skip csv processing cause overwrite option".format(
                        product.shn_cd))
                    continue
                else:
                    logger.info(
                        "{0} Existing, still csv processing ".format(product.shn_cd))
                    csv_process_product(product=product)
            else:
                logger.info(
                    "{0} New text data processing".format(product.shn_cd))
                csv_process_product(product=product)
        else:
            logger.info("{0} No text data available".format(product.shn_cd))


def Item_Info(args):
    print("Search Item: API GetItemInfor")
    # data = callApiGetItemInfo()
    # print(data)
    print("Successfully!")


def Validate_file_csv(args):
    print("Validate data CSV")
    data = validateFileCSV()
    print(data)
    print("Successfully!")

def getTextResult(product : Product):
    logger.info("{0} Load processed text".format(product.shn_cd))
    

def Export(args):
    logger.info("Export")
    logger.info("Default from_date :{0}".format(
        ConfigSMartTool.APIConfig['from_date']))
    absPath = os.path.abspath(args.path)
    logger.info("Abs path :{0}".format(absPath))

    # Download
    logger.debug("Text_Data_Process")
    productListExcelFile = args.products
    logger.info("Product list file :{0}".format(productListExcelFile))

    # Load product list
    productList = LoadProductListSingleSheet(
        productListExcelFile, args.sheet - 1)
    logger.info("Number of product :{0}".format(len(productList)))

    # Set storage path
    for product in productList:
        product: Product = product
        product.storagePath = absPath

    # For each product
    textResultList = []
    for product in productList:
        product: Product = product
        # product.describe()

        # If existing and not overwrite, skip
        if (product.isExistingData()):
            if (product.isExistingCSVProcessResult()):
                if (product.isExistingImageProcessResult()):
                    textResult = getTextResult(product)
                    textResultList.append(textResult)
                else:
                    logger.warning("No image process result available".format(product.shn_cd))
            else:
                logger.warning("{0} no text process result available".format(product.shn_cd))
        else:
            logger.warning("{0} No product folder available".format(product.shn_cd))

    # Write out to CSV
    with open(args.file) as f:
        csvWriter = csv.writer(f)
        
        # Write header
        row1 = [field[1] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row1)
        row2 = [field[2] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row2)
        row3 = [field[0] for field in CSVDefine.NewFormatFields]
        csvWriter.writerow(row3)

        # Write content
        csvWriter.writerows(textResultList)

class Mode(IntEnum):
    DOWNLOAD = 1
    TEXT_DATA_VALIDATION = 2
    TEXT_DATA_PROCESS = 3
    ITEM_INFO = 4
    EXPORT = 5


if __name__ == '__main__':
    parser = createArgParser()
    args = parser.parse_args()

    # Product path
    print(args)
    print("Product path : ", args.path)
    print("Product list file :", args.products)
    print("Path type: ", args.path_type)
    print("Run mode :", args.mode)
    print("Overwrite :", args.overwrite)
    print("Sheet number:", args.sheet)

    if args.mode == Mode.DOWNLOAD:
        Download(args)
    elif args.mode == Mode.TEXT_DATA_VALIDATION:
        Text_Data_Validation(args)
    elif args.mode == Mode.TEXT_DATA_PROCESS:
        Text_Data_Process(args)
    elif args.mode == Mode.ITEM_INFO:
        Item_Info(args)
    elif args.mode == Mode.EXPORT:
        Export(args)
    else:
        print("Nothing")
