class GetItemInfoRequest:
    jans = []
    acquired_items = []
    def __init__(self, jans : list, from_date:str="20200131", acquired_items: list=["shn_cd"]):
        self.jans = jans
        self.from_date = from_date
        self.acquired_items = acquired_items

class GetItemInfoRequestSearchJICFS:
    def __init__(self,
        from_date:str="20200131",
        jicfs_dai_cd=None, jicfs_cyu_cd=None, 
        jicfs_syo_cd=None, jicfs_sai_cd=None):
        self.from_date = from_date
        self.jicfs_dai_cd = jicfs_dai_cd
        self.jicfs_cyu_cd = jicfs_cyu_cd
        self.jicfs_syo_cd = jicfs_syo_cd
        self.jicfs_sai_cd = jicfs_sai_cd
class GetItemTextRequest:
    jans = []
    acquired_items = []
    def __init__(self, jans : list, from_date:str="20200131", acquired_items: list=["shn_cd"]):
        self.jans = jans
        self.from_date = from_date
        self.acquired_items = acquired_items

class GetPictureRequest:
    acquired_items = []
    def __init__(self, 
    jan:str, 
    mkr_pv_cd:str, img_men_no:str="01", img_gazou_syurui:str="10",
    acquired_items=["shn_cd"]):
        self.jan = jan
        self.mkr_pv_cd = mkr_pv_cd
        self.img_men_no = img_men_no
        self.img_gazou_syurui = img_gazou_syurui
        self.acquired_items = acquired_items

# Get Item Info
GetItemInfoFields = [
            'shn_cd',
            'mkr_pv_cd',
            'sei_shn_mei',
            'pkg_dsn_kbn',
            'pkg_lvl',
            'koukai_flg',
            'add_date',
            'upd_date'
]

query_item_info = """ query{{
         GetItemInfo(from_date: "{from_date}",jan: [{jans}], pkg_dsn_kbn: ["1"], pkg_lvl: ["0"]) {{
            {fields}
        }}
    }}
"""

def MakeGetItemInfoQuery(from_date:str, jans:list):
    # Quote with 2 double quotes
    janStrList = list(map(lambda x: '"' + x + '"', jans))
    print(janStrList)
    
    # Join its by comma
    jansStr = ','.join(janStrList)

    # Retrive fields
    fields = '\n'.join(GetItemInfoFields)
    return query_item_info.format(
        from_date=from_date, 
        jans=jansStr,
        fields=fields
        )

# Get Item Info
GetItemInfoFields1 = [
            'shn_cd',
            'mkr_pv_cd',
            'sei_shn_mei',
            'shn_mei',
            'pkg_dsn_kbn',
            'j_dai_cd',
            'j_cyu_cd',
            'j_syo_cd',
            'j_sai_cd',
            'pkg_lvl',
            'koukai_flg',
            'add_date',
            'upd_date']

query_item_info_1 = """ query
    {{
         GetItemInfo(
            from_date: "{from_date}",
            jicfs_dai_cd: "{jicfs_dai_cd}",
            jicfs_cyu_cd: "{jicfs_cyu_cd}",
            jicfs_syo_cd: "{jicfs_syo_cd}",
            jicfs_sai_cd: "{jicfs_sai_cd}",
            pkg_dsn_kbn: ["1"], pkg_lvl: ["0"])
            {{
                {fields}
            }}
    }}
"""

def MakeGetItemInfoQuery1(from_date:str, 
                jicfs_dai_cd=None, jicfs_cyu_cd=None, 
                jicfs_syo_cd=None, jicfs_sai_cd=None):

    # Retrive fields
    fields = '\n'.join(GetItemInfoFields1)
    return query_item_info_1.format(
        from_date=from_date, 
        jicfs_dai_cd="{0:1d}".format(jicfs_dai_cd) if jicfs_dai_cd is not None else "",
        jicfs_cyu_cd="{0:1d}".format(jicfs_cyu_cd) if jicfs_cyu_cd is not None else "",
        jicfs_syo_cd="{0:02d}".format(jicfs_syo_cd) if jicfs_syo_cd is not None else "",
        jicfs_sai_cd="{0:02d}".format(jicfs_sai_cd) if jicfs_sai_cd is not None else "",
        fields=fields
        )

GetItemTextQueryFields = [
    "shn_cd",
    "mkr_pv_cd",
    "pkg_dsn_kbn",
    "shn_cd_sbt",
    "shiyousyo_cd",
    "gtin_cd",
    "next_gtin_cd",
    "next_itm_ken",
    "mkr_cd",
    "d_mkr_cd",
    "mkr_mei",
    "brn_cd",
    "sub_brn_cd",
    "sei_shn_mei",
    "shn_mei",
    "shn_mei_l",
    "shn_mei_s",
    "rece_mei",
    "sei_shn_mei_kana",
    "shn_mei_lkana",
    "shn_mei_skana",
    "kikaku",
    "kikaku_tani",
    "irisu",
    "iri_tani",
    "nairyo",
    "nairyo_tani",
    "zyuryo",
    "zyuryo_tani",
    "kokeiryo",
    "kokeiryo_tani",
    "bun_cd",
    "o_bun_cd",
    "syuzei_kbn",
    "j_dai_cd",
    "j_cyu_cd",
    "j_syo_cd",
    "j_sai_cd",
    "gpc",
    "w_size",
    "h_size",
    "d_size",
    "size_tani",
    "nai_youki_cd",
    "gai_youki_cd",
    "sbt_betu_kbn",
    "pkg_lvl",
    "pb_nb_cd",
    "han_cha",
    "syomi_kikan",
    "kibo_uri_kin",
    "kibo_uri_kbn",
    "koukai_st_date",
    "koukai_ed_date",
    "mkr_uri_st_date",
    "mkr_uri_ed_date",
    "itf_cd",
    "b_irisu",
    "b_w_size",
    "b_h_size",
    "b_d_size",
    "c_irisu",
    "c_w_size",
    "c_h_size",
    "c_d_size",
    "sam_get_route",
    "add_date",
    "upd_date"
]
GetItemTextQuery = """ query{{
         GetItemText(jan: [{jans}], from_date: "{from_date}",pkg_dsn_kbn: ["1"], pkg_lvl: ["0"]) {{
             {fields}
        }}
    }}
"""

def MakeGetItemTextQuery(from_date:str, jans:list):
    # Quote with 2 double quotes
    janStrList = list(map(lambda x: '"' + x + '"', jans))
    # Join its by comma
    jansStr = ','.join(janStrList)
    # Retrive fields
    fields = '\n'.join(GetItemTextQueryFields)
    return GetItemTextQuery.format(
        from_date=from_date, 
        jans=jansStr,
        fields=fields
        )

# GET image

query_image_info = """ query{{
        GetPicture(jan: "{jan}", img_men_no: "{img_men_no}", mkr_pv_cd: "{mkr_pv_cd}" , img_gazou_syurui: "{img_gazou_syurui}") {{
            msdbm0900_shn_cd
            msdbm0900_mkr_pv_cd
            img_image
            img_gazou_syurui
            img_men_no
        }}
    }}
"""

def MakeGetPictureQuery(jan:str, img_men_no:str, mkr_pv_cd:str, img_gazou_syurui:str):
    return query_image_info.format(
        jan=jan, 
        img_men_no=img_men_no, 
        mkr_pv_cd=mkr_pv_cd, 
        img_gazou_syurui=img_gazou_syurui
        )