from openerp.osv import fields, osv
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),
    ('active','Active'),
    ('expired','Expired'),
    ('req_delete','Request For Delete'),
    ('delete','Deleted')
]

class rdm_customer_coupon(osv.osv):
    _name = 'rdm.customer.coupon'
    _description = 'Redemption Customer Coupon'
    
    def process_expired(self, cr, uid, context=None):
        _logger.info('Start Customer Coupon Process Expired')
        now = datetime.now().strftime('%Y-%m-%d')
        sql_req = "UPDATE rdm_customer_coupon SET state='expired' WHERE expired_date < '" + now + "' AND state='active'" 
        cr.execute(sql_req)
        _logger.info('End Customer Coupon Process Expired')
        return True    
    
    def add_coupon(self, cr, uid, values, context=None):
        trans_data = {}
        trans_data.update({'customer_id': values.get('customer_id')})
        trans_data.update({'trans_id': values.get('trans_id')})
        trans_data.update({'trans_type': values.get('trans_type')})
        trans_data.update({'coupon': values.get('coupon')})
        trans_data.update({'customer_id': values.get('customer_id')})
        trans_data.update({'expired_date': values.get('expired_date')})
        trans_id = self.create(cr, uid, trans_data, context=context)
        expired_date = values.get('expired_date')
        for i in range (0,values.get('coupon')):
            self.pool.get('rdm.customer.coupon.detail').add_coupon_detail(cr, uid, trans_id, expired_date, context=context)
            
            
    _columns = {
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),
        'trans_id': fields.integer('Transaction ID', readonly=True),        
        'trans_type': fields.selection([('promo','Promotion'),('point','Point'),('reward','Reward'),('reference','Reference'),('member','New Member')], 'Transaction Type'),        
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
    
    def add_coupon_detail(self, cr, uid, trans_id, expired_date, context=None):
        trans_data = {}
        trans_data.update({'customer_coupon_id': trans_id})
        coupon_code = self.pool.get('ir.sequence').get(cr, uid, 'rdm.customer.coupon.sequence')
        trans_data.update({'coupon_code': coupon_code})
        trans_data.update({'expired_date': expired_date})
        self.create(cr, uid, trans_data, context=context)
        
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
