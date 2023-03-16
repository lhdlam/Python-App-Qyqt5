# GetItemText
query_item_text = """ query($jan: String!){
             GetItemText(from_date: "20190625",jan: [$jan]) {
                shn_cd
                mkr_pv_cd
                pkg_dsn_kbn
                shn_cd_sbt
                shiyousyo_cd
                gtin_cd
                next_gtin_cd
                next_itm_ken
                mkr_cd
                d_mkr_cd
                brn_cd
                sub_brn_cd
                sei_shn_mei
                shn_mei
                shn_mei_l
                shn_mei_s
                rece_mei
                sei_shn_mei_kana
                shn_mei_lkana
                shn_mei_skana
                kikaku
                kikaku_tani
                irisu
                iri_tani
                nairyo
                nairyo_tani
                zyuryo
                zyuryo_tani
                kokeiryo
                kokeiryo_tani
                bun_cd
                o_bun_cd
                syuzei_kbn
                j_dai_cd
                j_cyu_cd
                j_syo_cd
                j_sai_cd
                gpc
                w_size
                h_size
                d_size
                size_tani
                nai_youki_cd
                gai_youki_cd
                sbt_betu_kbn
                pkg_lvl
                pb_nb_cd
                han_cha
                syomi_kikan
                kibo_uri_kin
                kibo_uri_kbn
                koukai_st_date
                koukai_ed_date
                mkr_uri_st_date
                mkr_uri_ed_date
                itf_cd
                b_irisu
                b_w_size
                b_h_size
                b_d_size
                c_irisu
                c_w_size
                c_h_size
                c_d_size
                sam_get_route
                add_date
                upd_date
            }
        }
    """

# Get Item Info
query_item_info = """ query($jan: String!){
         GetItemInfo(from_date: "20190625",jan: [$jan]) {
            shn_cd
            mkr_pv_cd
            pkg_dsn_kbn
            pkg_lvl
            koukai_flg
            add_date
            upd_date
        }
    }
"""

# GET image

query_image_info_0 = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "01", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """
query_image_info_90 = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "03", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """
query_image_info_180 = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "20", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """
query_image_info_270 = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "22", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """
query_image_info_top = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "02", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """
query_image_info_upper = """ query($mkr_pv_cd: String!, $jan: String!){
            GetPicture(jan: $jan, img_men_no: "65", mkr_pv_cd: $mkr_pv_cd , img_gazou_syurui: "10") {
                msdbm0900_shn_cd
                msdbm0900_mkr_pv_cd
                img_image
                img_gazou_syurui
                img_men_no
            }
        }
    """