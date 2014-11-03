from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

class rdm_customer(osv.osv):    
    _inherit = "rdm.customer"
    
    def get_coupons(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {}
        sql_req= "SELECT sum(c.coupon) as total FROM rdm_customer_coupon c WHERE (c.customer_id=" + str(id) + ")"        
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res:
            total_coupons = sql_res['total']
        else:
            total_coupons = 0
        #return {'value':{'':total_coupons}}
        res[id] = total_coupons    
        return res         
        
    _columns = {
        'coupon': fields.function(get_coupons, type="integer", string='Coupons'),
        #'coupon': fields.integer('Coupons'),                     
        'customer_coupon_ids': fields.one2many('rdm.customer.coupon','customer_id','Coupons',readonly=True)    
    }
    
rdm_customer()