from openerp.osv import fields, osv

class rdm_customer_coupon(osv.osv):
    _name = 'rdm.customer.coupon'
    _description = 'Redemption Customer Coupon'
    _columns = {
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),
        'trans_id': fields.integer('Transaction ID', readonly=True),        
        'trans_type': fields.selection([('promo','Promotion'),('point','Point'),('reference','Reference'),('member','New Member')], 'Transaction Type'),        
        'coupon': fields.integer('Coupon #', required=True),        
        'expired_date': fields.date('Expired Date', required=True),
        'customer_coupon_detail_ids': fields.one2many('rdm.customer.coupon.detail','customer_coupon_id','Coupon Codes'),
        'deleted': fields.boolean('Deleted'),
    }        
    
    _defaults = {
        'coupon': lambda *a: 0,
        'deleted': lambda *a: False,
    }
    
rdm_customer_coupon()

class rdm_customer_coupon_detail(osv.osv):
    _name = 'rdm.customer.coupon.detail'
    _description = 'Redemption Customer Coupon Detail'
    _columns = {
        'customer_coupon_id': fields.many2one('rdm.customer.coupon','Customer Coupon'),
        'coupon_code': fields.char('Coupon Code', size=10, required=True),
        'expired_date': fields.date('Expired Date', required=True),
    }

rdm_customer_coupon_detail()
