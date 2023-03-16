# API Login
import csv
import datetime
import logging
import os

import pandas as pd
import requests

from callAPI_requests import query_item_text, query_item_info
from config import PathProductFolder, MessageValidate
from validateField import *

logging.basicConfig(filename='./logs.log',
                    filemode='a+',
                    level=logging.WARNING,
                    format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')


def validateFileCSV():
    response = requests.post('https://gql.mdbc.co.jp/auth', headers={'Authorization': 'RFNDOjAwMDAwMDpzbWFydA=='},
                             verify=False)
    data_login = response.json()

    # API GraphQL
    url = 'https://gql.mdbc.co.jp/graphql'
    header = {
        'Authorization': data_login.get('token'),
    }
    path_directory = PathProductFolder.path_product_folder
    jan_code_file = PathProductFolder.path_jan_code_excel
    df = pd.read_excel(jan_code_file)

    jan_code_list = []
    data_jan_from_file = df.values.tolist()
    for jan in data_jan_from_file:
        for item in jan:
            jan_code_list.append(item)

    result = []
    for jan_code in jan_code_list:
        variables_item = {'jan': str(jan_code)}
        # Item Info
        response_item_info_json = requests.post(url, headers=header,
                                                json={'query': query_item_info, 'variables': variables_item},
                                                verify=False)
        if not response_item_info_json:
            continue
        # Item Text
        response_item_text_json = requests.post(url, headers=header,
                                                json={'query': query_item_text, 'variables': variables_item},
                                                verify=False)
        data_get_item_text = response_item_text_json.json()
        if data_get_item_text:
            validate = responseValidate(data_get_item_text['data']['GetItemText'][0])
            if validate:
                result.append({
                    'JAN': jan_code,
                    'response': validate
                })
    logging.warning('Validate Field : %s', result)


def responseValidate(dict_data):
    res_data = {}
    shn_cd = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_cd')))
    if shn_cd:
        res_data['shn_cd'] = shn_cd

    mkr_pv_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('mkr_pv_cd')))
    if mkr_pv_cd:
        res_data['mkr_pv_cd'] = mkr_pv_cd

    pkg_dsn_kbn = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('pkg_dsn_kbn')))
    if pkg_dsn_kbn:
        res_data['pkg_dsn_kbn'] = pkg_dsn_kbn

    shn_cd_sbt = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('shn_cd_sbt')))
    if shn_cd_sbt:
        res_data['shn_cd_sbt'] = shn_cd_sbt

    shiyousyo_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('shiyousyo_cd')))
    if shiyousyo_cd:
        res_data['shiyousyo_cd'] = shiyousyo_cd

    gtin_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('gtin_cd')))
    if gtin_cd:
        res_data['gtin_cd'] = gtin_cd

    next_gtin_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('next_gtin_cd')))
    if next_gtin_cd:
        res_data['next_gtin_cd'] = next_gtin_cd

    next_itm_ken = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('next_itm_ken')))
    if next_itm_ken:
        res_data['next_itm_ken'] = next_itm_ken

    mkr_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('mkr_cd')))
    if mkr_cd:
        res_data['mkr_cd'] = mkr_cd

    d_mkr_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('d_mkr_cd')))
    if d_mkr_cd:
        res_data['d_mkr_cd'] = d_mkr_cd

    brn_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('brn_cd')))
    if brn_cd:
        res_data['brn_cd'] = brn_cd

    sub_brn_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('sub_brn_cd')))
    if sub_brn_cd:
        res_data['sub_brn_cd'] = sub_brn_cd

    sei_shn_mei = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('sei_shn_mei')))
    if sei_shn_mei:
        res_data['sei_shn_mei'] = sei_shn_mei

    shn_mei = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_mei')))
    if shn_mei:
        res_data['shn_mei'] = shn_mei

    # chua tim thay field trong file excel
    shn_mei_l = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_mei_l')))
    if shn_mei_l:
        res_data['shn_mei_l'] = shn_mei_l

    # chua tim thay field trong file excel
    shn_mei_s = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_mei_s')))
    if shn_mei_s:
        res_data['shn_mei_s'] = shn_mei_s

    rece_mei = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('rece_mei')))
    if rece_mei:
        res_data['rece_mei'] = rece_mei

    sei_shn_mei_kana = checkValidate(MessageValidate.valid_string,
                                     validateStringField(dict_data.get('sei_shn_mei_kana')))
    if sei_shn_mei_kana:
        res_data['sei_shn_mei_kana'] = sei_shn_mei_kana

    shn_mei_lkana = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_mei_lkana')))
    if shn_mei_lkana:
        res_data['shn_mei_lkana'] = shn_mei_lkana

    shn_mei_skana = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('shn_mei_skana')))
    if shn_mei_skana:
        res_data['shn_mei_skana'] = shn_mei_skana

    kikaku = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('kikaku')))
    if kikaku:
        res_data['kikaku'] = kikaku

    kikaku_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('kikaku_tani')))
    if kikaku_tani:
        res_data['kikaku_tani'] = kikaku_tani

    irisu = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('irisu')))
    if irisu:
        res_data['irisu'] = irisu

    iri_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('iri_tani')))
    if iri_tani:
        res_data['iri_tani'] = iri_tani

    nairyo = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('nairyo')))
    if nairyo:
        res_data['nairyo'] = nairyo

    nairyo_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('nairyo_tani')))
    if nairyo_tani:
        res_data['nairyo_tani'] = nairyo_tani

    zyuryo = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('zyuryo')))
    if zyuryo:
        res_data['zyuryo'] = zyuryo

    zyuryo_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('zyuryo_tani')))
    if zyuryo_tani:
        res_data['zyuryo_tani'] = zyuryo_tani

    kokeiryo = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('kokeiryo')))
    if kokeiryo:
        res_data['kokeiryo'] = kokeiryo

    kokeiryo_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('kokeiryo_tani')))
    if kokeiryo_tani:
        res_data['kokeiryo_tani'] = kokeiryo_tani

    bun_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('bun_cd')))
    if bun_cd:
        res_data['bun_cd'] = bun_cd

    o_bun_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('o_bun_cd')))
    if o_bun_cd:
        res_data['o_bun_cd'] = o_bun_cd

    syuzei_kbn = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('syuzei_kbn')))
    if syuzei_kbn:
        res_data['syuzei_kbn'] = syuzei_kbn

    j_dai_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('j_dai_cd')))
    if j_dai_cd:
        res_data['j_dai_cd'] = j_dai_cd

    j_cyu_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('j_cyu_cd')))
    if j_cyu_cd:
        res_data['j_cyu_cd'] = j_cyu_cd

    j_syo_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('j_syo_cd')))
    if j_syo_cd:
        res_data['j_syo_cd'] = j_syo_cd

    j_sai_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('j_sai_cd')))
    if j_sai_cd:
        res_data['j_sai_cd'] = j_sai_cd

    gpc = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('gpc')))
    if gpc:
        res_data['gpc'] = gpc

    w_size = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('w_size')))
    if w_size:
        res_data['w_size'] = w_size

    h_size = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('h_size')))
    if h_size:
        res_data['h_size'] = h_size

    d_size = checkValidate(MessageValidate.valid_decimal_finite, validateDecimaFiniteField(dict_data.get('d_size')))
    if d_size:
        res_data['d_size'] = d_size

    # chua tim thay field trong file excel
    size_tani = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('size_tani')))
    if size_tani:
        res_data['size_tani'] = size_tani

    # inner_pkg_cd <=> nai_youki_cd
    nai_youki_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('nai_youki_cd')))
    if nai_youki_cd:
        res_data['nai_youki_cd'] = nai_youki_cd

    # outer_pkg_cd <=> gai_youki_cd
    gai_youki_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('gai_youki_cd')))
    if gai_youki_cd:
        res_data['gai_youki_cd'] = gai_youki_cd

    # Itemtype_cd <=> sbt_betu_kbn
    sbt_betu_kbn = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('sbt_betu_kbn')))
    if sbt_betu_kbn:
        res_data['sbt_betu_kbn'] = sbt_betu_kbn

    # image_pkg_lvl <=> pkg_lvl: chua tim thay field trong file excel
    pkg_lvl = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('pkg_lvl')))
    if pkg_lvl:
        res_data['pkg_lvl'] = pkg_lvl

    pb_nb_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('pb_nb_cd')))
    if pb_nb_cd:
        res_data['pb_nb_cd'] = pb_nb_cd

    # channel_cd <=> han_cha:  chua tim thay field trong file excel
    han_cha = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('han_cha')))
    if han_cha:
        res_data['han_cha'] = han_cha

    # item_life_days <=> syomi_kikan
    syomi_kikan = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('syomi_kikan')))
    if syomi_kikan:
        res_data['syomi_kikan'] = syomi_kikan

    # mkr_price <=> kibo_uri_kin
    kibo_uri_kin = checkValidate(MessageValidate.valid_decimal_finite,
                                 validateDecimaFiniteField(dict_data.get('kibo_uri_kin')))
    if kibo_uri_kin:
        res_data['kibo_uri_kin'] = kibo_uri_kin

    # mkr_price_cd <=> kibo_uri_kbn
    kibo_uri_kbn = checkValidate(MessageValidate.valid_decimal_finite,
                                 validateDecimaFiniteField(dict_data.get('kibo_uri_kbn')))
    if kibo_uri_kbn:
        res_data['kibo_uri_kbn'] = kibo_uri_kbn

    # info_st_date <=> koukai_st_date
    koukai_st_date = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('koukai_st_date')))
    if koukai_st_date:
        res_data['koukai_st_date'] = koukai_st_date

    # info_ed_date <=> koukai_ed_date
    koukai_ed_date = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('koukai_ed_date')))
    if koukai_ed_date:
        res_data['koukai_ed_date'] = koukai_ed_date

    # mkr_item_st_date <=> mkr_uri_st_date
    mkr_uri_st_date = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('mkr_uri_st_date')))
    if mkr_uri_st_date:
        res_data['mkr_uri_st_date'] = mkr_uri_st_date

    # mkr_item_ed_date <=> mkr_uri_ed_date
    mkr_uri_ed_date = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('mkr_uri_ed_date')))
    if mkr_uri_ed_date:
        res_data['mkr_uri_ed_date'] = mkr_uri_ed_date

    itf_cd = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('itf_cd')))
    if itf_cd:
        res_data['itf_cd'] = itf_cd

    # b_item_num <=> b_irisu
    b_irisu = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('b_irisu')))
    if b_irisu:
        res_data['b_irisu'] = b_irisu

    b_w_size = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('b_w_size')))
    if b_w_size:
        res_data['b_w_size'] = b_w_size

    b_h_size = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('b_h_size')))
    if b_h_size:
        res_data['b_h_size'] = b_h_size

    b_d_size = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('b_d_size')))
    if b_d_size:
        res_data['b_d_size'] = b_d_size

    # c_item_num <=> c_irisu
    c_irisu = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('c_irisu')))
    if c_irisu:
        res_data['c_irisu'] = c_irisu

    c_w_size = checkValidate(MessageValidate.validateNumeric, validateNumeric(dict_data.get('c_w_size')))
    if c_w_size:
        res_data['c_w_size'] = c_w_size

    c_h_size = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('c_h_size')))
    if c_h_size:
        res_data['c_h_size'] = c_h_size

    c_d_size = checkValidate(MessageValidate.valid_integer, validateIntegerField(dict_data.get('c_d_size')))
    if c_d_size:
        res_data['c_d_size'] = c_d_size

    # image_code <=> sam_get_route : chua tim thay validate trong file excel
    sam_get_route = checkValidate(MessageValidate.valid_string, validateStringField(dict_data.get('sam_get_route')))
    if sam_get_route:
        res_data['sam_get_route'] = sam_get_route

    return res_data


def checkValidate(message, actionValidateField):
    res_message = None
    if actionValidateField is False:
        res_message = message
    return res_message
