from odoo import models,fields,api,_
from odoo.exceptions import Warning
class AdvanceButtonPayment(models.TransientModel):
    _inherit = 'sale.advance.payment'
    def gen_sale_advance_payment(self):
        for record in self:
            if record.total_amount < record.advance_amount or record.advance_amount == 0.00:
                raise Warning(_('Please enter valid advance payment amount..!'))
            if record.advance_amount + record.paid_payment > record.total_amount:
                raise Warning(_('Please No Advance payment because the Payment Amount and Paid Amount is bigger than total Amount..'))
            payment_data = {
				'currency_id':record.currency_id.id,
				'payment_type':'inbound',
				'partner_type':'customer',
				'partner_id':record.partner_id.id,
				'amount':record.advance_amount,
				'journal_id':record.journal_id.id,
				'payment_date':record.payment_date,
				'communication':record.sale_order_id.name,
				'payment_method_id':record.payment_method_id.id
			}
            account_payment_id = self.env['account.payment'].create(payment_data)
            account_payment_id.post()
            if record.currency_id != record.company_id.currency_id:
                amount_currency = record.advance_amount
                advance_amount = record.currency_id._convert(record.advance_amount, record.company_id.currency_id, record.company_id, record.payment_date)
                currency_id = record.currency_id
            else:
                advance_amount = abs(self._compute_payment_amount(record.currency_id, record.journal_id, record.payment_date))
                amount_currency = 0.0
                currency_id = record.company_id.currency_id
            if account_payment_id.state == 'posted':
                record.sale_order_id.write({'payment_history_ids':[(0,0,{
					'name': record.name,
					'payment_date': record.payment_date,
					'partner_id': record.partner_id.id,
					'journal_id': record.journal_id.id,
					'payment_method_id': record.payment_method_id.id,
					'amount_currency': amount_currency,
					'currency_id': currency_id.id,
					'advance_amount': advance_amount,
					'total_amount': record.total_amount})]})
                
            action_vals = {
				'name': _('Advance Payment'),
				'domain': [('id', 'in', account_payment_id.ids), ('state', '=', 'posted')],
				'view_type': 'form',
				'res_model': 'account.payment',
				'view_id': False,
				'type': 'ir.actions.act_window',
			}
            if len(account_payment_id) == 1:
                    action_vals.update({'res_id': account_payment_id[0].id, 'view_mode': 'form'})
            return action_vals
				
			
                
                    
                
							
	


				
				
	
				
                
	