

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError


class TailorLead(models.Model):
    _inherit = 'mrp.production'

    employeee_name = fields.Many2many('hr.employee', string="Employee")
    shortt_name = fields.Char(string="Prefix", readonly=True)
    line_no = fields.Char(string='Reference No')

    def action_confirm(self):
        mr_id = self.id
        res = super(TailorLead, self).action_confirm()
        for i in self.employeee_name:
            print('asddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',i.id)
            # for i in self.employeee_name.id:
            new_pr = self.env['planning.slot'].create({
                'employee_id': i.id,
                'user_id': self.user_id.id,
                'name': self.name,
                'role_id': 4,
                'start_datetime': self.date_planned_start,
                'end_datetime': self.date_deadline,
                'company_id': self.company_id.id,
                # 'id': mr_id,
            })
        return res

    @api.model
    def create(self, vals):
        res = super(TailorLead, self).create(vals)
        manufacture = self.env['sale.order'].search([('name', '=', res.origin)])
        if manufacture:
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', manufacture.order_location.code)
            res.write({'shortt_name': manufacture.order_location.code,
                               })
        # res.shortt_name = res.origin.order_location.code
            print('dddddddddddddddddddddddddddddddddddddddddddddddddd', manufacture.order_location.code)
            print('dddddddddddddddddddddddddddddddddddddddddddddddddd', res.origin)
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production')
            print("vals", vals['name'])
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhh',res.shortt_name)
            seq = vals['name'].replace('SOM', res.shortt_name)
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhh',seq)
            res.write({
                        'name': seq,
                    })
        return res
