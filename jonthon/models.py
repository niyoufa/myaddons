# -*- coding: utf-8 -*-
import pdb
from openerp.osv import fields, osv

class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'
    _order = "create_date desc"

    _columns = {
        '_id': fields.char('ObjectId'),
        'drp2': fields.char(),
        'drp1': fields.char(),
        'is_new': fields.integer('新品'),
        'on_sale_flag': fields.boolean('特价商品'),
        'cost': fields.integer('成本'),
        'specs': fields.char('规格'),
        'unit': fields.char('单位'),
        'goods_type': fields.char('商品类型'),
        'sku': fields.char('商品码'),
        'goods_desc':fields.char("商品描述"),
        'goods_thumb':fields.char("图片"),
        'sort':fields.integer(),
        'box_name':fields.char("大类名称"),
        'goods_name':fields.char('小类名称'),
        'tags':fields.char(),
        'start_time':fields.integer(),
        'sales':fields.integer('销售量'),
        'shop_price':fields.float('售价'),
        'market_price':fields.float('市场价'),
        'goods_img':fields.char(),
        'add_time':fields.char(),
        'country':fields.char('国家'),
        'favorite':fields.integer('关注度'),
        'end_time':fields.integer(),
        'is_hot':fields.integer(),
        'discount_rule':fields.char(),
        'stock':fields.integer(),
        'goods_summary':fields.char(),
        'least_num':fields.integer(),
        'most_num':fields.integer(),
        'goods_brief_backup':fields.char(),
        'goods_brief':fields.char(),
    }