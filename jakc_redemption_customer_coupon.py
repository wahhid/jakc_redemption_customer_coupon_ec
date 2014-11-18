from openerp.osv import fields, osv

AVAILABLE_STATES = [
    ('draft','New'),
    ('active','Active'),
    ('expired','Expired'),
    ('deleted','Deleted'),    
]

class rdm_customer_coupon(osv.osv):
    _name = 'rdm.customer.coupon'
    _description = 'Redemption Customer Coupon'
    
    def batch_expired_date(self, cr, uid, context=None):
        sql_req = "UPDATE rdm.customer.coupon SET state='expired' WHERE expired_date=now()"
        cr.execute(sql_req)
        return True    
    
    _columns = {
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),
        'trans_id': fields.integer('Transaction ID', readonly=True),        
        'trans_type': fields.selection([('promo','Promotion'),('point','Point'),('reference','Reference'),('member','New Member')], 'Transaction Type'),        
        'coupon': fields.integer('Coupon #', required=True),        
        'expired_date': fields.date('Expired Date', required=True),
        'customer_coupon_detail_ids': fields.one2many('rdm.customer.coupon.detail','customer_coupon_id','Coupon Codes'),
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),
    }        
    
    _defaults = {
        'coupon': lambda *a: 0,
        'state': lambda *a: 'active',
    }
    
rdm_customer_coupon()

class rdm_customer_coupon_detail(osv.osv):
    _name = 'rdm.customer.coupon.detail'
    _description = 'Redemption Customer Coupon Detail'
    _columns = {
        'customer_coupon_id': fields.many2one('rdm.customer.coupon','Customer Coupon'),
        'coupon_code': fields.char('Coupon Code', size=10, required=True),
        'expired_date': fields.date('Expired Date', required=True),
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),
    }

    _defaults = {    
        'state': lambda *a: 'active',
    }    

rdm_customer_coupon_detail()
