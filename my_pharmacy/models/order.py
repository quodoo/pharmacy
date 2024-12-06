from odoo import api, models, fields
import requests, base64

class Order(models.Model):
    _name = 'pharmacy.order'
    _description = 'Pharmacy Order'


    code = fields.Integer('Code')
    stock_id = fields.Many2one('pharmacy.stock', string='Stock')
    pharmacie = fields.Many2one(related='stock_id.pharmacie_id', string='Pharmacy', store=True)
    medicament = fields.Many2one(related='stock_id.medicament_id', string='Medicine', store=True)
    orderBookDate = fields.Datetime('Book Date')
    schedule_cancel_date = fields.Datetime('Scheduled Cancel Date', readonly=True)
    orderState = fields.Selection(
        [('booked', 'Booked'),
        ('canceled', 'Canceled'),
        ('paid', 'Paid')],
        'State', default="booked")


    def make_booked(self):
        self.ensure_one()
        self.orderState = 'booked'
    
    def make_canceled(self):
        self.ensure_one()
        self.orderState = 'canceled'
    
    def make_paid(self):
        self.ensure_one()
        if self.stock_id and self.stock_id.quantity > 0:
            self.stock_id.quantity -= 1
            self.orderState = 'paid'
        else:
            self.make_canceled()



    def cancel_overdue_orders(self):
        overdue_orders = self.search([('orderState', '=', 'booked'), ('schedule_cancel_date', '<=', fields.Datetime.now())])

        for order in overdue_orders:
            order.make_canceled()
