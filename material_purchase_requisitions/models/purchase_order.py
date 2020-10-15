# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Requisitions',
        copy=False
    )
    project_id = fields.Many2one("project.project", string="Project", store=True)
    job_id = fields.Many2one("project.task", string="Job order", store=True)
    cost_sheet_id = fields.Many2one("job.costing.sheet", "Cost Sheet")
    is_drop_shipping = fields.Boolean("Drop Ship")

    def button_confirm(self):
        for order in self:
            if order.is_drop_shipping:
                project = order.project_id
                code = ''
                for c in (project.name).split():
                    code = code + c[0]
                warehouse = self.env['stock.warehouse'].search([("name", "=", project.name),
                                                                ("company_id", "=", order.company_id.id),
                                                                ("code", "=", code)])
                if not warehouse:
                    warehouse = self.env['stock.warehouse'].create({'name': project.name,
                                                                    'company_id': order.company_id.id or self.env[
                                                                        'res.company']._company_default_get(
                                                                        'odoo_job_costing_management').id,
                                                                    'code': code})

                picking_type_obj = self.env["stock.picking.type"].search([("warehouse_id", "=", warehouse.id),
                                                                          ("code", "=", "incoming"),
                                                                          ("company_id", "=", order.company_id.id)])
                order.picking_type_id = picking_type_obj.id
            print("order printed in custom confirm button ::>>> 20 line ::>>", order)
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True

    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.create(res)
                else:
                    picking = pickings[0]
                moves = order.order_line._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                moves._action_assign()
                picking.message_post_with_view('mail.message_origin_link',
                                               values={'self': picking, 'origin': order},
                                               subtype_id=self.env.ref('mail.mt_note').id)
        return True


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_requisition_line_id = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisitions Line',
        copy=False
    )
