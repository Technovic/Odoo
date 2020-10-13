# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    task_id = fields.Char(string='Task Allocated', readonly=True)


class PlanSlot(models.Model):
    _inherit = "planning.slot"

    @api.model
    def create(self, vals):
        record = super(PlanSlot, self).create(vals)
        # print('sssssssssssssssssssssssssssssssssssssssss', vals.get('employee_id'))
        employee_count = self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))])
        if employee_count:
            employee_count.task_id = "Allocated"
        return record

    def write(self, vals):
        record = super(PlanSlot, self).write(vals)
        # print('sssssssssssssssssssssssssssssssssssssssss', vals.get('employee_id'))
        employee_count = self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))])
        if employee_count:
            employee_count.task_id = "Allocated"
        return record

    def unlink(self):
        for rec in self:
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', rec.employee_id.id)
            employee_count = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            if employee_count:
                employee_count.task_id = False
        return super(PlanSlot, self).unlink()

    # def unlink(self):
    #     record = super(PlanSlot, self).unlink()
    #     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', self.employee_id.id)
    #     # employee_count = self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))])
    #     # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', employee_count)
    #     # if employee_count:
    #     #     employee_count.task_id = False
    #     return record



class FreeEmp(models.Model):
    _name = 'unalloc.employee'
    _description = 'Unallocated Employee'

    date = fields.Date(string="Till Date :", default=fields.Datetime.now, readonly=True)
    line_info = fields.One2many(
        comodel_name='unalloc.employee.line',
        inverse_name="line_ids",
        string="Unallocated Employee Details",
    )

    @api.onchange('date')
    def get_unallocated_employees(self):
        mr_id = self.id
        active_count = self.env['hr.employee'].search([('task_id', '=', False)])
        for i in self:
            if active_count:
                for a in active_count:
                    print(a.name)
                    line = self.env['unalloc.employee.line'].create({
                                'employee_name': a.name,
                                'line_ids': mr_id,
                            })


class UnallocTree(models.Model):
    _name = 'unalloc.employee.line'
    _description = 'Unallocated Employee Line'

    line_ids = fields.Many2one(
        comodel_name='unalloc.employee',
        string="Unallocated Employee Details",
        readonly=True
    )
    employee_name = fields.Char(string='Employee Name', readonly=True)


