# -*- coding: utf-8 -*-
#   2016 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openerp import fields, models, api


class TodoTask(models.Model):
    _name = 'todo.task'

    name = fields.Char(string='Description', required=True, size=64)
    is_done = fields.Boolean(string='Done?')
    active = fields.Boolean(string='Active?', default=True)
    date_deadline = fields.Date('Deadline')
    tage_id = fields.Many2one('todo.task.stage', 'Stage')
    user_id = fields.Many2one('res.users', 'Responsible')

    @api.one
    def do_toggle_done(self):
        self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        done_recs = self.search([('is_done', '=', True)])
        done_recs.write({'active': False})
        return True
    
    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count(
            [('user_id', '=', self.user_id.id)])

    user_todo_count = fields.Integer(
        'User To-Do Count',
        compute='compute_user_todo_count'
    )
