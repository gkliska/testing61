# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: account_storno
#    Author: Goran Kliska
#    mail:   gkliskaATgmail.com, 
#    Copyright (C) 2011- Slobodni programi d.o.o., Zagreb www.slobodni-programi.hr
#    Contributions: 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv, orm
import time
from openerp.tools import float_compare
from openerp.tools.translate import _
import decimal_precision as dp

class account_journal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'posting_policy':fields.selection([
                                           ('contra', 'Contra (debit<->credit)'),
                                           ('storno', 'Storno (-)'),
                                           ],
                                          'Storno or Contra', size=16, required=True,
                                           help="Storno allows minus postings, Refunds are posted on the same joural/account * (-1).\n"
                                                "Contra doesn't allow negative posting. Refunds are posted by swaping credit and debit side."
                                        ),
        'refund_journal_id':fields.many2one('account.journal', 'Refund journal',
                                           help="Journal for refunds/returns from this journal. Leave empty to use same journal for normal and refund/return postings.",
                                            ),
                }
    _defaults = {'posting_policy': 'storno', 
                }


class account_move_line(osv.osv):
    _inherit = "account.move.line"
    #Original constraints
    #_sql_constraints = [
    #('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in accounting entry !'),
    #('credit_debit2', 'CHECK (credit+debit>=0)', 'Wrong credit or debit value in accounting entry !'),
    #]

    # credit_debit1 is valid constraint. Clear message   
    # credit_debit2 is replaced with dummy constraint that is always true.   

    _sql_constraints = [
        ('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in accounting entry! Either credit or debit must be 0.00.'),
        ('credit_debit2', 'CHECK (abs(credit+debit)>=0)', 'Wrong credit or debit value in accounting entry !'),
    ]

    def _check_contra_minus(self, cr, uid, ids, context=None):
        """ This is to restore credit_debit2 check functionality, for contra journals 
        """
        for l in self.browse(cr, uid, ids, context=context):
            if l.journal_id.posting_policy == 'contra':
                if not (l.debit * l.credit) >= 0.0:
                    return False
        return True

    def _check_storno_tax(self, cr, uid, ids, context=None):
        """For Storno accounting Tax/Base amount is always == (debit + credit)
           Still trying to find the case where it is not.
           Maybe for contra check is abs(tax_amount) = abs(debit + credit) ???     
        """
        for l in self.browse(cr, uid, ids, context=context):
            if l.journal_id.posting_policy == 'storno' and l.tax_code_id:
                if float_compare((l.debit + l.credit), l.tax_amount, precision_digits = 2) != 0:   #precision_digits=dp.get_precision('Account')[1]) 
                    return False
        return True

    _constraints = [
        (_check_contra_minus, _('Negative credit or debit amount is not allowed for "contra" journal policy.'), ['journal_id']),
        (_check_storno_tax, _('Invalid tax amount. Tax amount can be 0.00 or equal to (Credit + Debit).'), ['journal_id']),
    ]


class account_model_line(osv.osv):
    _inherit = "account.model.line"
    _sql_constraints = [
        ('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in model! Either credit or debit must be 0.00.'),
        ('credit_debit2', 'CHECK (abs(credit+debit)>=0)', 'Wrong credit or debit value in accounting entry !'),
    ]




#Trigger example 
#For Storno accounting Tax/Base amount always == debit + credit   
"""
        cr.execute('''
                CREATE OR REPLACE FUNCTION debit_credit2tax_amount() RETURNS trigger AS
                $debit_credit2tax_amount$
                BEGIN
                   NEW.tax_amount := CASE when NEW.tax_code_id is not null
                                           then coalesce(NEW.credit, 0.00)+coalesce(NEW.debit, 0.00)
                                           else 0.00
                                      END;
                   RETURN NEW;
                END;
                $debit_credit2tax_amount$ LANGUAGE plpgsql;

                ALTER FUNCTION debit_credit2tax_amount() OWNER TO %s;

                DROP TRIGGER IF EXISTS move_line_tax_amount ON account_move_line;
                CREATE TRIGGER move_line_tax_amount BEFORE INSERT OR UPDATE ON account_move_line
                    FOR EACH ROW EXECUTE PROCEDURE debit_credit2tax_amount();
        '''%(tools.config['db_user'],))

"""