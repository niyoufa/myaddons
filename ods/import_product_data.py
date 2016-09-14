#coding=utf-8

import pdb
import sys,os
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
import libs
import libs.xmlrpc_lib as xmlrpclib
import libs.mongo_lib as mongolib
import libs.utils as utils

def import_product_template_data(*args, **options):
    coll = mongolib.get_coll("goods")

    # good_list = coll.find()
    good_list = [{
        "_id" : "570506cd988c7d3d1919a087",
        "drp2" : "5.0",
        "drp1" : "10.0",
        "is_new" : 0,
        "on_sale_flag" : 0,
        "cost" : 50,
        "specs" : "5kg/箱",
        "unit" : "箱",
        "goods_type" : "normal",
        "sku" : "14173",
        "goods_desc" : "<p><img src='http://www.jonthons.com/images/14173_03.png'></p><img src='http://www.jonthons.com/images/14173_04.png'></p><img src='http://www.jonthons.com/images/14173_05.png'></p><img src='http://www.jonthons.com/images/14173_06.png'></p><img src='http://www.jonthons.com/images/14173_07.png'></p><img src='http://www.jonthons.com/images/14173_08.png'></p><img src='http://www.jonthons.com/images/14173_10.png'></p><img src='http://www.jonthons.com/images/14173_11.png'></p><img src='http://www.jonthons.com/images/14173_12.png'></p><img src='http://www.jonthons.com/images/14173_13.png'></p><img src='http://www.jonthons.com/images/14173_14.png'></p>",
        "goods_thumb" : "http://www.jonthons.com/images/14173_02.png",
        "sort" : 0,
        "box_name" : "tag测试",
        "goods_name" : "鱿鱼头",
        "tags" : [
            "57848d23988c7d24cc51dde9"
        ],
        "start_time" : 0,
        "sales" : 1,
        "shop_price" : 55.56,
        "market_price" : 85,
        "goods_img" : "http://www.jonthons.com/images/14173_01.png",
        "add_time" : "2016-04-06 20:53:33",
        "country" : "阿根廷",
        "favorite" : 100,
        "end_time" : 0,
        "is_hot" : 0,
        "discount_rule" : "",
        "stock" : 9,
        "goods_summary" : "",
        "least_num" : 5,
        "most_num" : 10,
        "goods_brief_backup" : "5kg",
        "goods_brief" : "5kg/箱"
    }]

    for good in good_list:
        sku = good["sku"]

        product_template_obj = {
            "name": good.get("goods_name"),
            "_id" : unicode(good.get("_id","")),
            "drp2" : good.get("drp2",""),
            "drp1" : good.get("drp1",""),
            "is_new" : good.get("is_new",""),
            "on_sale_flag" : bool(good.get("on_sale_flag",0)),
            "cost": good.get("cost",0.0),
            "specs": good.get("specs",""),
            "unit": good.get("unit",""),
            "goods_type": good.get("goods_type",""),
            "sku": good.get("sku",""),
            "goods_desc": good.get("goods_desc"),
            "goods_thumb": good.get("goods_thumb",""),
            "sort": good.get("sort",0),
            "box_name": good.get("box_name",""),
            "goods_name": good.get("goods_name",""),
            "tags": str(good.get("tags","")),
            "start_time": good.get("start_time"),
            "sales": good.get("sales",0),
            "shop_price": good.get("shop_price",0.0),
            "market_price": good.get("market_price",0.0),
            "goods_img": good.get("goods_img",""),
            "add_time": good.get("add_time",""),
            "country": good.get("阿根廷",""),
            "favorite": good.get("favorite",0),
            "end_time": good.get("end_time"),
            "is_hot": good.get("is_hot",0),
            "discount_rule": good.get("discount_rule",""),
            "stock": good.get("stock",0),
            "goods_summary": good.get("goods_summary",""),
            "least_num": good.get("least_num",0),
            "most_num": good.get("most_num",0),
            "goods_brief_backup": good.get("goods_brief_backup",""),
            "goods_brief": good.get("goods_brief","")
        }
        query_params = dict(
            sku=sku,
        )
        xmlrpcclient = xmlrpclib.get_xmlrpcclient("ProductTemplate")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], product_template_obj)
        else:
            utils.load_obj(xmlrpcclient, product_template_obj)

if __name__ == "__main__":
    import_product_template_data()
