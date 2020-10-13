# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    require_foc = fields.Boolean('FOC')
    delivery_type = fields.Selection([('pickup', 'Pickup'), ('delivery', 'Delivery')], string="Delivery Type", required=True)
    choose_warehouse = fields.Many2one('stock.location', string="Outlet")
    order_location = fields.Many2one('stock.warehouse', string="Ordering Location", required=True)

    # @api.onchange('delivery_type')
    # def change_delivery_type(self):
    #     slip = self.env['stock.picking']
    #     if slip:
    #         slip.delivery_type = self.delivery_type

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # manufacture = self.env['mrp.production'].search([('origin', '=', self.name)])
        # if manufacture:
        #     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', self.order_location.code)
        #     manufacture.write({'shortt_name': self.order_location.code,
        #                        })
        new_location = self.env.ref('stock.stock_location_inter_wh')
        stock_location = self.env.ref('stock.stock_location_stock')
        if self.delivery_type == "pickup":
            for i in self.order_line:
                print('neeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',new_location.usage)
                print('neeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',stock_location.name)
                print('neeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',stock_location.usage)
                move_vals = ({
                    'name': 'New Location',
                    'location_id': stock_location.id,
                    'location_dest_id': new_location.id,
                    'product_id': i.product_id.id,
                    'product_uom': i.product_id.uom_id.id,
                    'product_uom_qty': i.product_uom_qty
                    # 'picking_type_id': self.env.ref('stock.picking_type_in').id,
                })
                move_ids = self.env['stock.move'].create(move_vals)
                # print("<<<<<", move_ids)
                vals = {
                    'note': 'Stock Issued',
                    'location_id': stock_location.id,
                    'location_dest_id': new_location.id,
                    'product_id': i.product_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                    'move_lines': [(6, 0, move_ids.ids)],
                }
                print(",,,,,,,", vals)
                picking = self.env['stock.picking'].create(vals)
                picking.origin = self.name
                picking.state = 'confirmed'
                move_vals1 = ({
                    'name': 'New Location',
                    'location_id': new_location.id,
                    'location_dest_id': self.choose_warehouse.id,
                    'product_id': i.product_id.id,
                    'product_uom': i.product_id.uom_id.id,
                    'product_uom_qty': i.product_uom_qty
                })
                move_ids1 = self.env['stock.move'].create(move_vals1)
                # print("<<<<<", move_ids)
                vals1 = {
                    'note': 'Stock Received',
                    'location_id': new_location.id,
                    'location_dest_id': self.choose_warehouse.id,
                    'product_id': i.product_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                    'move_lines': [(6, 0, move_ids1.ids)],
                }
                print(",,,,,,,", vals1)
                picking1 = self.env['stock.picking'].create(vals1)
                picking1.origin = self.name
                picking1.state = 'confirmed'
                result = self.env['stock.picking'].search([('origin', '=', self.name), ('picking_type_id.name', '=',
                                                                                        'Delivery Orders')])
                if result:
                    print('operationnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', result.picking_type_id.name)
                    print('operationnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', result.picking_type_id.name)
                    print('oldddddddddddddddddd', result.location_id)
                    print('choose_warehouse', self.choose_warehouse.id)
                    result.update({'delivery_type': self.delivery_type,
                                'location_id': self.choose_warehouse.id})
                    print('newwwwwwwwwwwwwwwww', result.location_id)
        delivery = self.env['stock.picking'].search([('origin', '=', self.name)])
        if delivery:
            delivery.update({'delivery_type': self.delivery_type,
                           })

        return res


class deliveryNotification(models.Model):
    _inherit = 'stock.picking'

    delivery_type = fields.Char(string='Delivery Type', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('issued', 'Stock Issued'),
        ('received', 'Stock Recieved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    # sale_ref = fields.Many2one('sale.order')

    def button_issue(self):
        picking = self.env['stock.picking'].search([('origin', '=', self.origin), ('picking_type_id.name', '=',
                                                                                'Internal Transfers'), ('note', '=',
                                                                                                        'Stock Issued')])
        if picking:
            for j in picking:
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.origin)
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.note)
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.move_ids_without_package.product_uom_qty)
                for i in j.move_ids_without_package:
                    i.quantity_done = i.product_uom_qty
                    picking.write({'state': "done"})
        return self.write({"state": "issued"})

    def button_receive(self):
        picking_recived = self.env['stock.picking'].search([('origin', '=', self.origin), ('picking_type_id.name', '=',
                                                                                   'Internal Transfers'), ('note', '=',
                                                                                                           'Stock Received')])
        if picking_recived:
            for j in picking_recived:
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.origin)
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.note)
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', j.move_ids_without_package.product_uom_qty)
                for a in j.move_ids_without_package:
                    a.quantity_done = a.product_uom_qty
                    picking_recived.write({'state': "done"})
        return self.write({"state": "received"})
