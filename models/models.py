# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import datetime

class LateOrder(models.Model):
	_inherit = 'stock.picking'

	to_accept_late_order = fields.Boolean(string='Acepto pedido', default=False)
	@api.one
	def action_cancel(self):
		raise ValidationError(self.purchase_id.product_id.name)
	@api.one
	def button_validate(self):

		fecha_pedido = self.scheduled_date
		fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		if fecha_actual > fecha_pedido:
			if self.to_accept_late_order is not True:
				raise ValidationError('La fecha de pedido ha expirado, si estas de acuerdo marca la casilla "ACEPTO PEDIDO"')
			
			if self.to_accept_late_order == True:
				invoice_obj = self.env['account.invoice']
				invoice_value = {
					'partner_id': self.purchase_id.partner_id.id,
					'reference': self.purchase_id.partner_ref,
					'origin':self.name,
					'date_invoice': fecha_actual,
					'type': 'in_invoice'
				}
				invoice_id = invoice_obj.create(invoice_value)

				line_obj = self.env['account.invoice.line']
				account_default = 27
				for orde in self.purchase_id.order_line:
					line_value = {
						'product_id': orde.product_id.id,
						'name':orde.name,
						'account_id': account_default,
						'quantity': orde.product_qty,
						'price_unit': orde.price_unit,
						'price_subtotal': orde.price_subtotal,
						'invoice_id': invoice_id.id,
					}
				line_id = line_obj.create(line_value)
				return super(LateOrder, self).button_validate()
		else:
			return super(LateOrder, self).button_validate()

"""class CrearFactura(models.Model):
	_inherit = 'purchase.order'
	date_current = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	@api.one
	def crear_factura(self):
		if self.invoice_count == 0:
			invoice_obj = self.env['account.invoice']
			invoice_value = {
				'partner_id': self.partner_id.id,
				'reference': self.partner_ref,
				'l10n_mx_edi_origin':self.name,
				'date_invoice':self.date_current,
				'type': 'in_invoice',
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
			if invoice_obj:
					raise ValidationError('La factura se creo correctamente')"""
