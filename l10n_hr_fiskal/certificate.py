import os, time
from M2Crypto import BIO, Rand, SMIME, EVP, RSA, X509, ASN1
from osv import fields, osv, orm
from tools.translate import _

class certificate(osv.osv):
    _inherit = "crypto.certificate"

    def _get_cert_selection(self,cursor,user_id, context=None):
        return (('fina_demo','Fina Demo Certifiacte'),
                ('fina_prod','Fina Production Certificate'),
                ('personal','Personal Certificate'),
<<<<<<< HEAD
                ('other','Other types')
               )
=======
<<<<<<< HEAD
                ('other','Other types')
               )
=======
                ('other','Other types ->TODO')
               )

>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
    
    _columns = {
        'company_id':fields.many2one('res.company','Tvrtka',help='Cerificate is used for this company only.'),
        'group_id': fields.many2one('res.groups', 'User group', select=True, help='Users who use the certificate.'),
        'cert_type':fields.selection(_get_cert_selection,'Certificate Use'),
        'pfx_certificate':fields.binary('Certificate', help='Original Pfx File.')
        
    }
    _defaults = {
         'state': 'draft',
         'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'crypto.certificate', context=c),
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
        
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
    }
    


