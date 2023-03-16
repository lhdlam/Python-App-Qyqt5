from json import JSONDecodeError
from .APIRequests import GetItemInfoRequest
from .APIRequests import GetItemInfoRequestSearchJICFS
from .APIRequests import GetItemTextRequest
from .APIRequests import GetPictureRequest
from .APIRequests import MakeGetItemInfoQuery 
from .APIRequests import MakeGetItemInfoQuery1
from .APIRequests import MakeGetItemTextQuery 
from .APIRequests import MakeGetPictureQuery 

import requests
import urllib3
urllib3.disable_warnings()

import logging

logger = logging.getLogger('APICaller')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)

class APICaller:
    __token = ""
    def __init__(self):
        logger.info("Initialize a API Caller")

    def request_data(url, headers, query):
        response_text = requests.post(url, headers=headers, json={"query": query}, verify=False)
        return response_text.json()

    def executeQuery(self, query):
        header = {"Authorization": self.__token,}
        url = "https://gql.mdbc.co.jp/graphql"
        
        response_json = requests.post(url, headers=header, json={"query": query}, verify=False)

        result = {}
        try:
            result = response_json.json()
        except JSONDecodeError as jde:
            # print("Exception : {0}".format(jde))
            result['errors'] = response_json.reason
            logger.error(response_json.reason)

        return result

    def authen(self):
        # API Login
        logger.debug("Authen")
        response_text = requests.post('https://gql.mdbc.co.jp/auth', headers={'Authorization': 'RFNDOjAwMDAwMDpzbWFydA=='},
                                verify=False)
        data_login = response_text.json()
        
        self.__token = data_login.get('token')
        
        return data_login.get('token')

    def GetItemInfo(self, request: GetItemInfoRequest):
        logger.debug("GetItemInfo")
        
        jans = request.jans
        from_date = request.from_date

        query = MakeGetItemInfoQuery(from_date=from_date, jans=jans)
        
        logger.debug("Query : " + query)

        queryResults = self.executeQuery(query) 

        return queryResults
        
    def GetItemInfoByJICFS(self, request: GetItemInfoRequestSearchJICFS):
        logger.debug("GetItemInfo")
        
        from_date = request.from_date
        jicfs_dai_cd = request.jicfs_dai_cd
        jicfs_cyu_cd = request.jicfs_cyu_cd
        jicfs_syo_cd = request.jicfs_syo_cd
        jicfs_sai_cd = request.jicfs_sai_cd

        query = MakeGetItemInfoQuery1(from_date=from_date,
                                    jicfs_dai_cd=jicfs_dai_cd,
                                    jicfs_cyu_cd=jicfs_cyu_cd,
                                    jicfs_syo_cd=jicfs_syo_cd,
                                    jicfs_sai_cd=jicfs_sai_cd)
        
        logger.debug("Query : " + query)

        queryResults = self.executeQuery(query) 

        return queryResults

    def GetItemText(self, request: GetItemTextRequest):
        logger.debug("GetItemText")

        jans = request.jans
        from_date = request.from_date

        query = MakeGetItemTextQuery(from_date=from_date, jans=jans)
        
        logger.debug("Query : " + query)

        queryResults = self.executeQuery(query) 

        return queryResults

    def GetPicture(self, request: GetPictureRequest):
        logger.debug("GetPicture")

        jan = request.jan
        mkr_pv_cd = request.mkr_pv_cd
        img_men_no = request.img_men_no
        img_gazou_syurui = request.img_gazou_syurui

        query = MakeGetPictureQuery(
            jan=jan, mkr_pv_cd=mkr_pv_cd, 
            img_men_no=img_men_no, img_gazou_syurui=img_gazou_syurui
        )
        
        logger.debug("Query : " + query)

        queryResults = self.executeQuery(query) 

        return queryResults

if __name__ == '__main__':
    sampleCaller = APICaller()
    # Authen
    token = sampleCaller.authen()
    print("Token : ", token)

    #Search
    # getItemInfoRequest = GetItemInfoRequest(from_date='20000101')
    # getItemInfoRequestSearchJICFS = GetItemInfoRequestSearchJICFS(
    #         from_date='20000101',
    #         jicfs_dai_cd=1,
    #         jicfs_cyu_cd=1,
    #         jicfs_syo_cd=1,
    #         jicfs_sai_cd=17,
    #         )
    # queryResults = sampleCaller.GetItemInfoByJICFS(getItemInfoRequestSearchJICFS)
    # # print(queryResults)
    # if (len(queryResults['data']['GetItemInfo'])) > 0:
    #     print("Number of result :{0}".format(len(queryResults['data']['GetItemInfo'])))
    #     mkr_pv_cd = queryResults['data']['GetItemInfo'][0]['mkr_pv_cd']
    #     # for indx, ItemInfo in enumerate(queryResults['data']['GetItemInfo']):
    #     #     print("JAN = {0}, Add date = {1}, Update date = {2}, mkr_pv_cd = {3}".format(
    #     #         ItemInfo['shn_cd'],
    #     #         ItemInfo['add_date'],
    #     #         ItemInfo['upd_date'],
    #     #         ItemInfo['mkr_pv_cd']
    #     #         ))
    # else:
    #     print("No data available")

    # Get Item Info
    getItemInfoRequest = GetItemInfoRequest(jans=["4903110301592"], from_date='20000101')
    queryResults = sampleCaller.GetItemInfo(getItemInfoRequest)
    print(queryResults)

    # Get Text data
    # getTextDataRequest = GetItemTextRequest(jans=["4903110301592"], from_date='20220101')
    # queryResults = sampleCaller.GetItemText(getTextDataRequest)
    # print(queryResults)

    # Get Image data
    # getPictureDataRequest = GetPictureRequest(
    #     jan="4903110301592",mkr_pv_cd='mdbautos11100'
    #     )
    # queryResults = sampleCaller.GetPicture(getPictureDataRequest)
    # print(queryResults)
    # base64Image = queryResults['data']['GetPicture'][0]['img_image']
    # print(len(base64Image))

    # import base64
    # imgdata = base64.b64decode(base64Image)
    # with open("image.jpg", 'wb') as f:
    #     f.write(imgdata)