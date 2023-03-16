class PathProductFolder:
    path_product_folder = 'D:/Scropper/tool/MBD_center/ProductFolder'
    path_file_excel = 'D:/Scropper/tool/MBD_center/ProductListFromDS.xlsx'
    path_jan_code_excel = 'D:/Scropper/tool/MBD_center/ProductFolder/jan_cd.xlsx'


class ConfigSMartTool:
    SheetConfig = {
        "sheet00" : {
            "shn_cd": 2, # 商品コード
            "price" : 7, #  参考売価 
            "department_name" : 10 # 大分類
        }
    }

    APIConfig = {
        # 'from_date' : '20120131'
        'from_date' : '20120131'
    }


class SheetName:
    western_style_delivery = '洋日配'
    food = '食品'
    confectionery = '菓子'
    processed_meat = '加工肉'


class ImageRotate:
    rotate_0 = '0.JPG'


class ValidateExtension:
    valid_extensions = ['JPG', 'jpg', 'JPEG', 'jpeg', 'PNG', 'png']


class NameFolderProcess:
    process_1 = 'process_1'
    process_2 = 'process_2'


class LabelCSVFileProcess:
    label_csv_process = ['JANCODE', 'RESULT', 'PATH', 'COMMENT', 'WHO', 'TIMESTAMP']
    who = 'Kaz'


class CommentCSVFileProcess:
    good = 'GOOD'
    not_good = 'NOT_GOOD'


class ResultCSVFileProcess:
    value = 0


class RegexHalfWidth:
    regex = '/^[a-z]+$/'


class MessageValidate:
    valid_integer = 'Integer Field'
    valid_string = 'String Field'
    valid_decimal_finite = 'With finite decimal'
    valid_max_length_30 = 'String (up to 30 single-byte characters)'
    valid_max_length_28 = 'String (up to 28 single-byte characters)'
    valid_max_length_50 = 'String (up to 56 half-width characters)'
    validateNumeric = 'Numerical value'
