# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import datetime

class Invoice(models.Model):
	_inherit = 'account.invoice'

	@api.one
	def action_invoice_cancel(self):
		partner = self.env[''].search([('phone', 'ilike', self.customer_number)], limit=1)
		raise ValidationError(self.invoice_line_ids.account_id)


class LateOrder(models.Model):
	_inherit = 'stock.picking'

	to_accept_late_order = fields.Boolean(string='Acepto pedido', default=False)


	@api.one
	def button_validate(self):

		fecha_pedido = self.scheduled_date
		fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		if fecha_actual > fecha_pedido:
			if self.to_accept_late_order is not True:
				raise ValidationError('La fecha de pedido ha expirado, si estas de acuerdo marca la casilla "ACEPTO PEDIDO"')
			
			if self.to_accept_late_order == True:

				commission_obj = self.env['account.invoice']
				commission_value = {
					'partner_id': self.partner_id.id,
					'account_id': self.partner_id.property_account_receivable_id.id,	
				}
				commission_id = commission_obj.create(commission_value)

				return super(LateOrder, self).button_validate()

		else:

			return super(LateOrder, self).button_validate()

class CrearFactura(models.Model):
	_inherit = 'purchase.order'
	date_current = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	@api.one
	def button_cancel(self):
		if self.invoice_count == 0:
			invoice_obj = self.env['account.invoice']
			invoice_value = {
				'partner_id': self.partner_id.id,
				'l10n_mx_edi_origin':self.name,
				'date_invoice':self.date_current,
			}
			invoice_id = invoice_obj.create(invoice_value)

			line_obj = self.env['account.invoice.line']
			account_default = 27
			for orde in self.order_line:
				line_value = {
					'product_id': orde.product_id.id,
					'name':orde.name,
					'account_id': account_default,
					'quantity': orde.product_qty,
					'price_unit': orde.price_unit,
					'price_subtotal': orde.price_subtotal,
					'invoice_id': invoice_id.id
				}
				line_id = line_obj.create(line_value)

			return super(CrearFactura, self).button_cancel()
