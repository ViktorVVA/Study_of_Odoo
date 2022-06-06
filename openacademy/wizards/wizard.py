from odoo import models,fields,api

class Wizard(models.TransientModel):
    _name = 'openacademy.wizards.wizard'
    _description = "Wizard: Qiuck Regisration of Attendees to Sessions"

    # def _default_session(self):
    #     return self.env['openacademy.session'].browse(self._context.get('active_id'))
    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    # session_id = fields.Many2one('openacademy.session',
    #                            string="Session", required=True, default=_default_session)

    session_ids = fields.Many2many('openacademy.session',
                                 string="Session", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    # def subscribe(self):
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     return{}
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
            return{}