# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: l10n_hr_base
#    Author: Goran Kliska
#    mail:   goran.kliska(AT)slobodni-programi.hr
#    Copyright: Slobodni programi d.o.o., Zagreb
#                  http://www.slobodni-programi.hr
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

from osv import osv, fields 

class l10n_hr_base_nkd(osv.osv):
    _name = 'l10n_hr_base.nkd'
    _description = 'NKD - Nacionalna klasifikacija djelatnosti'
    _columns = {
        'code': fields.char('Code', size=16, required=True, select=1),
        'name': fields.char('Name', size=128, required=True),
    }
l10n_hr_base_nkd()
