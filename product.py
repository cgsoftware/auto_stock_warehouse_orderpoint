# -*- encoding: utf-8 -*-

import netsvc
import pooler, tools
import math

from tools.translate import _

from osv import fields, osv


class product_product(osv.osv):
    _inherit='product.product'
    
    def check_orderpoint(self,cr,uid,product_ids,context):
      
      if product_ids:
        for product in self.pool.get('product.product').browse(cr,uid,[product_ids]):

          company = product.product_tmpl_id.company_id
          location_id = company.location_id.id
          #import pdb;pdb.set_trace()
          ids_orderpoint = self.pool.get('stock.warehouse.orderpoint').search(cr,uid,[ ('product_id', '=', product.id), ('location_id', '=', location_id)])
          if not ids_orderpoint:
            orderpoint = {
                          'warehouse_id':company.warehouse_id.id,
                          'location_id':company.location_id.id,
                          'product_id':product.id,
                          'product_uom':product.product_tmpl_id.uom_id.id,
                          'product_min_qty':company.product_min_qty,
                          'product_max_qty':company.product_max_qty,
                         
                          }
            ids_orderpoint = self.pool.get("stock.warehouse.orderpoint").create(cr,uid,orderpoint)
            
      return True
    
    def create(self, cr, uid, data, context=None):
      res = super(product_product, self).create(cr, uid, data, context) 
      
      ok = self.check_orderpoint(cr,uid,res,context)
      return   res 
            
    def write(self, cr, uid, ids, vals, context=None):
      res = super(product_product, self).write(cr, uid, ids, vals, context=context)
      #import pdb;pdb.set_trace()
      for product_id in ids:
        ok = self.check_orderpoint(cr,uid,product_id,context)
      return res            
 

product_product()

class company(osv.osv):
    _inherit = 'res.company'
    _columns = {
                'product_min_qty': fields.float('Min Quantity', required=False,
                                                help="When the virtual stock goes belong the Min Quantity, OpenERP generates "\
                                                "a procurement to bring the virtual stock to the Max Quantity."),
                'product_max_qty': fields.float('Max Quantity', required=False,
                                                help="When the virtual stock goes belong the Max Quantity, OpenERP generates "\
                                                "a procurement to bring the virtual stock to the Max Quantity."),
                'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse', required=False),
                'location_id': fields.many2one('stock.location', 'Location', required=False),
                                                
    }

company()