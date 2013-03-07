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
from tools.translate import _

class account_journal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'posting_policy':fields.selection([
                                           ('contra', 'Contra (debit<->credit)'),
                                           ('storno', 'Storno (-)'),
                                           ],
                                         'Storno or Contra', size=16, required=True,
                                         help="Contra doesn't allow negative posting by swaping credit and debit side. Storno allows minus postings."),
        'refund_journal_id':fields.many2one('account.journal', 'Invoice refund journal',),
                }
    _defaults = {'posting_policy': 'storno', }

account_journal()


class account_move_line(osv.osv):
    _inherit = "account.move.line"
    _sql_constraints = [
        #('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in accounting entry !'),
        ('credit_debit2', 'CHECK (abs(credit+debit)>=0)', 'Wrong credit or debit value in accounting entry !'),
    ]

account_move_line()

class account_model_line(osv.osv):
    _inherit = "account.model.line"
    _sql_constraints = [
        #('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in model (Credit Or Debit Must Be "0")!'),
        ('credit_debit2', 'CHECK (abs(credit+debit)>=0)', 'Wrong credit or debit value in model (Credit + Debit Must Be greater "0")!'),
    ]
account_model_line()

#TODO this or abs(this) functionality
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




