# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    milestone_id = fields.Many2one('project.milestone', string="Milestone")
    # product_id = fields.Many2one(
    #     comodel_name="product.product",
    #     related="milestone_id.name.product_id",
    #     string="Product",
    #     readonly=True,
    # )
    # project_id = fields.Many2one(comodel_name="project.project", string="Project",)
    # name_id = fields.Selection(onchange_mum_id, string="Milestone Name",)
    # name_id = fields.Selection(
    #     selection=lambda self: self.env['project.milestone'].get_selection_field('name'))
    # percentage = fields.Float(string="Percentage",)
    # project_milestone_ids = fields.One2many('project.milestone','project_id', string="Project Milestone")

    # @api.onchange('milestone_id')
    # def action_check_qty(self):
    #     sum = 0
    #     for i in self.project_milestone_ids:
    #         sum += i.percentage
    #         print('summmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', sum)
    #         if sum > 100:
    #             print('heloooooooooooooooooooooooooooooooooonoooooooooooooooooo')
    #             raise UserError(("Milestone Limit Reached"))

    # @api.onchange('project_id')
    def onchange_mum_id(self):
        print('helllloooooooooooooooooooooooooooooooooooo', self.project_id.id)
        project_name = self.env['project.milestone'].search([('project_id', '=', self.project_id.id)])
        if project_name:
            print('helllloooooooooooooooooooooooooooooooooooo')
            # for i in project_name.project_milestone_ids:
            # for i in self.project_id.project_milestone_ids:
            for i in project_name:
                self.name_id = i.name
                print('yyyyyyyyyyyyyyyyyyyysssssssssssssssss', i.name)
        else:
            print('noooooooooooooooooooooooooooooooo')
            self.name_id = False

            # self.name_id = self.project_id.name

    # @api.onchange('percentage')
    # def check_milestone_percent(self):
    #     print('helooooooooooooooooooooooooooooooooooooooooooo')
    #     self.env.cr.execute("""
    #                                                   SELECT project_id, sum(percentage) as percentage
    #                                                   FROM project_milestone
    #                                                   WHERE project_id = self.milestone_id.project_id.id
    #                                                   group by project_id""")
    #     count_list = self.env.cr.dictfetchall()
    #     total = 0
    #     for i in count_list:
    #         print('inameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', i['percentage'])
    #         check = i['percentage']
    #         print('checkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk', check)
    #         print('checkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk', self.milestone_id.percentage)
    #         add = self.milestone_id.percentage + check
    #         total = add
    #         print('aaaaaaaaaaaaaaaaaadddddddddddddddddddddddddddddddddddddddddd', add)
    #         print('totallllllllllllllllllllllllllllllllllllllll', total)
    #         if add > 101:
    #             print('heloooooooooooooooooooooooooooooooooonoooooooooooooooooo')
    #             raise UserError(("Milestone Limit Reached"))

    @api.onchange('milestone_id')
    def onchange_medium_id(self):
        domain = [('id','in',[])]
        if self._context.get('active_model') == 'sale.order' and self._context.get('active_id', False):
            sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
            project_id = sale_order.project_id
            sale_order.cost_test = self.milestone_id.percentage
            print('heyyyyyyyyyyyyyyyyyyyyjudeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',self.milestone_id.percentage)
            print('heyyyyyyyyyyyyyyyyyyyyjudeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',self.milestone_id.percentage)
            # mr_id = self.id
            # line = self.env['sale.order'].search([('name', '=', sale_order.name)])
            # # if line:
            # print('heyyyyyyyyyyyyyyyyyyyyjudeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',sale_order.name)
            # # print('heyyyyyyyyyyyyyyyyyyyyjudeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',line.invoice_origin)
            # new_pr = line.create({
            #     'cost_test': self.milestone_id.percentage,
            #     # 'alloc_ids': mr_id,
            #     # 'move_id': mr_id,
            # })
            if project_id and project_id.project_milestone_ids:
                project_milestone_ids = project_id.project_milestone_ids.ids
                if sale_order.milestone_ids:
                    sale_milestone_ids = sale_order.milestone_ids.ids
                    milestone_lst = list(set(project_milestone_ids) - set(sale_milestone_ids))
                    domain = [('id','in',milestone_lst)]
                else:
                    domain = [('id','in',project_milestone_ids)]
        return {'domain':{'milestone_id':domain}}

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        account_order = self.env['account.move'].browse(self._context.get('active_id'))
        # print('account orderrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',account_order.invoice_line_ids.name_sale)
        if sale_orders and sale_orders.project_id:
            project_milestone_ids = sale_orders.project_id.project_milestone_ids.ids
            sale_milestone_ids = sale_orders.milestone_ids.ids
            if len(project_milestone_ids) != len(sale_milestone_ids) and not self.milestone_id:
                raise UserError(_('Please Select Milestone First !'))
            if self.milestone_id:
                sale_milestone_ids.append(self.milestone_id.id)
                sale_orders.write({'latest_milestone_id': self.milestone_id.id,'milestone_ids':[(6,False,sale_milestone_ids)]})
            mr_id = self.id
            # print("detailssssssssssssssssssssssssssssssssssssss\n", self.milestone_id.percentage)
            # line = account_order.create({
            #     'project_id': sale_orders.project_id.id,
            #     # 'move_id': mr_id,
            #     # project.analytic_account_id.id
            #     # 'account_id': self.env['account.account'].search(
                #     [('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)], limit=1).id,

            # })
        res = super(SaleAdvancePaymentInv,self).create_invoices()
        return res
