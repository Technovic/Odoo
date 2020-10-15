# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    custom_requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Purchase Requisition',
        readonly=True,
        copy=True
    )

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.origin:
            purchase = self.env["purchase.order"].search([("name", "=", res.origin),
                                                          ("company_id", "=", res.company_id.id)])
            if purchase:
                res.update({
                    "custom_requisition_id": purchase.custom_requisition_id.id,
                    "project_id": purchase.project_id.id,
                    "job_id": purchase.job_id.id,
                    "cost_sheet_id": purchase.cost_sheet_id.id,
                })
        return res

    project_id = fields.Many2one("project.project", string="Project",
                                 store=True, required=True)

    job_id = fields.Many2one('project.task', 'Job order', readonly=True)
    cost_sheet_id = fields.Many2one("job.costing.sheet", "Cost Sheet",default=lambda self: self.custom_requisition_id.cost_sheet_id.id)


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    custom_requisition_line_id = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisitions Line',
        copy=True
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
