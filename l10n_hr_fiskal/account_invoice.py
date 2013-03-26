# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: l10n_hr_fiskal
#    Author: Davor Bojkić
#    mail:   bole@dajmi5.com
#    Copyright (C) 2012- Daj Mi 5, 
#                  http://www.dajmi5.com
#    Contributions: Hrvoje ThePython - Free Code!
#                   Goran Kliska (AT) Slobodni Programi
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import uuid 

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
import pooler
from fiskal import *
import tools


class account_invoice(osv.Model):
    _inherit = "account.invoice"
    _columns = {
<<<<<<< HEAD
                'vrijeme_izdavanja': fields.datetime("Vrijeme", readonly=True),
=======
                'vrijeme_izdavanja': fields.datetime("Date", readonly=True),
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
                'fiskal_user_id'   : fields.many2one('res.users', 'Fiskalizirao', help='Fiskalizacija. Osoba koja je potvrdila racun'),
                'zki': fields.char('ZKI', size=64, readonly=True),
                'jir': fields.char('JIR',size=64 , readonly=True),
                'uredjaj_id':fields.many2one('fiskal.uredjaj', 'Naplatni uredjaj', help ="Naplatni uređaj na kojem se izdaje racun"),
                'prostor_id':fields.many2one('fiskal.prostor', 'Poslovni prostor', help ="Poslovni prostor u kojem se izdaje racun"),
<<<<<<< HEAD
                'fiskal_log_ids':fields.one2many('fiskal.log','invoice_id','Logovi poruka', help="Logovi poslanih poruka prema poreznoj upravi"),
=======
=======
"""
#TODOfrom fiskal import *
import pooler
#TODO
class account_invoice(osv.Model):
    _inherit = "account.invoice"
    _columns = {
                'zki': fields.char('ZKI', size=64, readonly=True),
                'jir': fields.char('JIR',size=64 , readonly=True),
                'pprostor_id':fields.many2one('l10n.hr.pprostor', 'Pos. Prostor', help ="Pos. prostor u kojem se izdaje racun"),
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
                'nac_plac':fields.selection((
                                             ('G','GOTOVINA'),
                                             ('K','KARTICE'),
                                             ('C','CEKOVI'),
                                             ('T','TRANSAKCIJSKI RACUN'),
                                             ('O','OSTALO')
                                             ),
                                            'Nacin placanja', required=True)   
               }
    _defaults = {
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
                 #'pprostor_id':'1',
                 'nac_plac':'T' # TODO : postaviti u bazi pitanje kaj da bude default!
                 }

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'vrijeme_izdavanja':False,
            'fiskal_user_id':False,
            'zki':False,
            'jir': False,
            #'uredjaj_id': False,
            #'prostor_id': False,
            #'nac_plac': False,
        })
        return super(account_invoice, self).copy(cr, uid, id, default, context)
       
    def button_fiscalize(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for invoice in self.browse( cr, uid, ids, context):
            self.fiskaliziraj(cr, uid, invoice.id, context=context)

    def get_fiskal_taxes(self, cr, uid, invoice, a, context=None):
        res=[]
        
        def get_factory(val):
            fiskal_type = val.get('fiskal_type',False) 
            
            if fiskal_type=='pdv':      tns = {'tns': (a.racun.Pdv.Porez , 'tns:Porez')     , 'fields': ('Stopa' ,'Osnovica', 'Iznos') }  
            elif fiskal_type=='pnp':    tns = {'tns': (a.racun.Pnp.Porez , 'tns:Porez')     , 'fields': ('Stopa' ,'Osnovica', 'Iznos') }
            elif fiskal_type=='ostali': tns = {'tns': (a.racun.OstaliPor.Porez, 'tns:Porez'), 'fields': ('Naziv','Stopa' ,'Osnovica', 'Iznos') }
            elif fiskal_type=='naknade':tns = {'tns': (a.racun.Naknade, 'tns:Naknada'), 'fields': ('NazivN', 'IznosN') }

            elif fiskal_type=='oslobodenje':  tns = {'tns': (a.racun.IznosOslobPdv),   'value': 'Osnovica' }
            elif fiskal_type=='ne_podlijeze': tns = {'tns': (a.racun.IznosNePodlOpor), 'value': 'Osnovica' }
            elif fiskal_type=='marza':        tns = {'tns': (a.racun.IznosMarza),      'value': 'Osnovica' }
            else  :tns={}
            place = tns.get('tns',False)
            if not place:
                return False
            if len(place) > 1:      
                porez = a.client2.factory.create(place[1])
                place[0].append(porez)
            else:    
                porez = place[0]

            if tns.get('fields',False):
                for field in tns['fields']:
                    porez[field] = val[field]
                   
            if tns.get('value',False):
                tns['tns'][0] = val[field]

            return tns
        
        for tax in invoice.tax_line:
            if not tax.tax_code_id:
                continue # TODO special cases without tax code, or with base tax code without tax if found
            val={ 'tax_code': tax.tax_code_id.id,
                  'fiskal_type': tax.tax_code_id.fiskal_type,
                  'Naziv': tax.tax_code_id.name,
                  'Stopa': tax.tax_code_id.fiskal_percent,
                  'Osnovica': fiskal_num2str(tax.base_amount),
                  'Iznos': fiskal_num2str(tax.tax_amount),
                  'NazivN': tax.tax_code_id.name,
                 }
            res.append(val)
            #TODO group and sum by fiskal_type and Stopa hmmm then send 1 by one into factory... 
            get_factory(val)            
        return res


    def fiskaliziraj(self, cr, uid, id, context=None):
        """ Fiskalizira jedan izlazni racun
        """
        if context is None:
            context = {}
        prostor_obj= self.pool.get('fiskal.prostor')
                    
        invoice= self.browse(cr, uid, [id])[0]
        
        #tko pokusava fiskalizirati?
        if not invoice.fiskal_user_id:
            self.write(cr, uid, [id], {'fiskal_user_id':uid})

        if not invoice.fiskal_user_id:
            self.write(cr, uid, [id], {'fiskal_user_id':uid})
            
        invoice= self.browse(cr, uid, [id])[0] #refresh

        #TODO - posebna funkcija za provjeru npr. invoice_fiskal_valid()
<<<<<<< HEAD
        if not invoice.fiskal_user_id.oib:
=======
        if not invoice.fiskal_user_id.OIB:
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
            raise osv.except_osv(_('Error'), _('Neispravan OIB korisnika!'))
        
        wsdl, cert, key = prostor_obj.get_fiskal_data(cr, uid, company_id=invoice.company_id.id)
        if not wsdl:
            return False
        a = Fiskalizacija()
        a.set_start_time()

        a.init('Racun', wsdl, cert, key)
        
        start_time=a.time_formated()
        a.t = start_time['datum'] 
        a.zaglavlje.DatumVrijeme = start_time['datum_vrijeme'] #TODO UTC -> Europe/Zagreb 
        a.zaglavlje.IdPoruke = str(uuid.uuid4())
        
        dat_vrijeme = invoice.vrijeme_izdavanja
        if not dat_vrijeme:
            dat_vrijeme = start_time['datum_vrijeme']
            self.write(cr, uid, [id], {'vrijeme_izdavanja': start_time['time_stamp'].strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT) })
        
        if not invoice.company_id.fina_certifikat_id:
            pass #TODO Error
        if invoice.company_id.fina_certifikat_id.cert_type == 'fina_prod':
           a.racun.Oib = invoice.company_id.partner_id.vat[2:]  # npr"57699704120"
        elif invoice.company_id.fina_certifikat_id.cert_type == 'fina_demo':
           a.racun.Oib = invoice.uredjaj_id.prostor_id.spec[2:]  #OIB IT firme 
        else:
            pass #TODO Error
                   
         
        a.racun.DatVrijeme = dat_vrijeme #invoice.vrijeme_izdavanja
        a.racun.OznSlijed = invoice.prostor_id.sljed_racuna #'P' ## sljed_racuna

        #dijelovi broja racuna
        BrojOznRac, OznPosPr, OznNapUr = invoice.number.rsplit('/',2)
        BrOznRac = ''
        for b in ''.join([x for x in BrojOznRac[::-1]]): #reverse
            if b.isdigit() :BrOznRac += b                #
            else: break                                  #break on 1. non digit
        BrOznRac = BrOznRac[::-1].lstrip('0')    #reverse again and strip leading zeros

        a.racun.BrRac.BrOznRac = BrOznRac
        a.racun.BrRac.OznPosPr = OznPosPr
        a.racun.BrRac.OznNapUr = OznNapUr
        
        a.racun.USustPdv = invoice.prostor_id.sustav_pdv and "true" or "false"
        if invoice.prostor_id.sustav_pdv:
            self.get_fiskal_taxes(cr, uid, invoice, a, context=context)
        
        a.racun.IznosUkupno = fiskal_num2str(invoice.amount_total)
        
        a.racun.NacinPlac = invoice.nac_plac
        a.racun.OibOper = invoice.fiskal_user_id.oib[2:]  #"57699704120"
        
        if not invoice.zki:
            a.racun.NakDost = "false"  ##TODO rutina koja provjerava jel prvi puta ili ponovljeno sranje!
            a.izracunaj_zastitni_kod() #start_time['datum_racun'])
            self.write(cr,uid,id,{'zki':a.racun.ZastKod})
        else :
            a.racun.NakDost = "true"
            a.racun.ZastKod = invoice.zki
<<<<<<< HEAD
=======
=======
                 'pprostor_id':'1',
                 'nac_plac':'T' # TODO : postaviti u bazi pitanje kaj da bude default!
                 }
       
    
    def button_fiscalize(self, cr, uid, id, context=None):
        if context is None:
            context = {}
            
        invoice= self.browse(cr,uid,id,context=context)[0]
        
        a = Fiskalizacija()
        start_time=a.time_formated()
        
        a.t = start_time['datum'] 
        a.zaglavlje.DatumVrijeme = start_time['datum_vrijeme']
        a.zaglavlje.IdPoruke = str(uuid.uuid4())
        
        poslao = "Račun :" + invoice.number +"\n"
        poslao=poslao +"StartTime : "+ start_time['datum_vrijeme']+ "\n"
        
        a.racun.Oib = "57699704120" #ucitaj ! OIB korisnika
        poslao=poslao + "OIB Organizacije : " +"\n"
        
        
        
        
        a.racun.DatVrijeme = start_time['datum_vrijeme']
        poslao=poslao + "Datum na računu :" + start_time['datum_racun'] + "\n"
        
        a.racun.OznSlijed = invoice.pprostor_id.sljed_racuna #'P' ## sljed_racuna
        poslao= poslao + "Sljed racuna oznaka : " + a.racun.OznSlijed + "\n"
        
        
        ## e ovoo je zajebani dio..
        ## lako je stavit sufiks na IRA broj krug., ali kad ima vise prostora 
        ## brojevi se moraju generirati shodno pos jed. i napl. uredj.
        
        
            
        a.racun.BrRac.BrOznRac = '1' #invoice.number #'1'
        a.racun.BrRac.OznPosPr = invoice.pprostor_id.oznaka_pp #'TESTIRAMO' ## name!pazi! nesmije imati razmake u nazivu.
        a.racun.BrRac.OznNapUr = '1'  ## nisam siguran odkud ovo da zvadim pa ostavim zasada 1!!!
        a.porez = a.client2.factory.create('tns:Porez')
        
        pdv="false"
        if invoice.pprostor_id.sustav_pdv:
            pdv="true"
                    
        a.racun.USustPdv = pdv #'true'  ## sustav_pdv
        poslao = poslao + "U sustavu PDV : " + pdv + "\n" 
        ### TODO : zbrojiti sve pojedine poreze i grupirati i kaj ako nije u sustavu pdv?
        
        
        poslao = poslao + "Stopa poreza : hardcode 25.00 \n" 
        a.porez.Stopa = "25.00" #"25.00"
        
        osnovica=str(invoice.amount_untaxed)
        if osnovica[-2]==".":
            osnovica=osnovica+"0"
        a.porez.Osnovica = osnovica #"100.00"
        poslao = poslao + "Osnovica : " + osnovica + "\n" 
        
        porez=str(invoice.amount_tax)
        if porez[-2]==".":
            porez=porez + "0"
        poslao = poslao + "Iznos poreza : " + porez + "\n" 
        a.porez.Iznos = porez #"25.00"
        a.racun.Pdv.Porez.append(a.porez)
        
        iznos=str(invoice.amount_total) 
        if iznos[-2]=='.':  # ovo sam dodao ako slučajno iznos završava na 0  da ne vrati gresku radi druge decimale!
                            # npr 75,00 prikze kao 75.0 ! pa dodam samo jednu nulu da prodje :)
            iznos=iznos+'0'
        a.racun.IznosUkupno = iznos # "125.00" #
        poslao = poslao + "Iznos ukupno : " + iznos + "\n" 
        
        a.racun.NacinPlac = invoice.nac_plac
        poslao = poslao + "Način Plaćanja : " + invoice.nac_plac + "\n"
        if not invoice.user_id.vat: 
            zk=self.write(cr,uid,id,{'zki':'Ovaj korisnik nema unešen OIB! izdavanje ZKI nije moguće'})
            return
        else:  a.racun.OibOper = invoice.user_id.vat[2:] #"57699704120"
        ## PAZI : ne dozvoliti dalje ako nije unešen OIB operatera!
        if not invoice.zki:
            a.racun.NakDost = "false"  ##TODO rutina koja provjerava jel prvi puta ili ponovljeno sranje!
            poslao="Slanje: 1.\n" + poslao + "\n"
        else :
            a.racun.NakDost ="true"
            poslao="Ponovljeno slanje \n" + poslao + "\n"
        
        a.izracunaj_zastitni_kod(start_time['datum_racun'])
        zk=self.write(cr,uid,id,{'zki':a.racun.ZastKod})
        
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
        
        odgovor_string=a.posalji_racun()
        odgovor_array = odgovor_string[0]
        # ... sad tu ima odgovor.Jir
        if odgovor_array==500 : 
            g = odgovor_string[1]
            odgovor= g.Greske.Greska
            zk=self.write(cr,uid,id,{'jir':'došlo je do greške!'})
            pass
        else :
            b=odgovor_string[1]
            jir=b.Jir
            odgovor = "JIR - " + jir
            zk=self.write(cr,uid,id,{'jir':jir})
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638

        """
        poslao = "Račun :" + invoice.number +"\n"
        poslao = poslao +"StartTime : "+ start_time['datum_vrijeme']+ "\n"
        poslao = poslao + "OIB Organizacije : " +"\n"
        poslao = poslao + "Datum na računu :" + start_time['datum_racun'] + "\n"
        poslao = poslao + "Sljed racuna oznaka : " + a.racun.OznSlijed + "\n"
        poslao = poslao + "U sustavu PDV : " + pdv + "\n" 
        poslao = poslao + "Stopa poreza : hardcode 25.00 \n" 
        poslao = poslao + "Osnovica : " + osnovica + "\n" 
        poslao = poslao + "Iznos ukupno : " + iznos + "\n" 
        poslao = poslao + "Iznos poreza : " + porez + "\n" 
        poslao = poslao + "Način Plaćanja : " + invoice.nac_plac + "\n"
        if not invoice.zki:
            poslao="Slanje: 1.\n" + poslao + "\n"
        else :
            poslao="Ponovljeno slanje \n" + poslao + "\n"
        """
<<<<<<< HEAD
=======
=======
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
        stop_time=a.time_formated()
        
        ##ovo sam dodao samo da vidim vrijeme odaziva...
        t_obrada=stop_time['time_stamp']-start_time['time_stamp']
        time_ob='%s.%s s'%(t_obrada.seconds, t_obrada.microseconds)
        ################################################
<<<<<<< HEAD

        """
=======
<<<<<<< HEAD

        """
=======
        
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
        values={
                'name':uuid.uuid4(),
                'type':'racun',
                'sadrzaj':poslao,
                'timestamp':stop_time['time_stamp'], 
                'time_obr':time_ob,
                'origin_id':invoice.id,
                'odgovor': odgovor
                }
        return self.pool.get('l10n.hr.log').create(cr,uid,values,context=context)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
        """
account_invoice()


    
<<<<<<< HEAD
=======
=======
    
account_invoice()
"""
>>>>>>> 253bacc248c06453424ca891b6f2c2264b0f6315
>>>>>>> 87fa7789f88249193a4f15d6b932d67bcffcf638
