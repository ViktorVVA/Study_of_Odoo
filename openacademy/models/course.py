# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'
#     _description = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Courses'
    _priority = "1"
    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', string='Responsible', ondelete='set null', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name!=description)',
         "The title of the course should not be the description"),
        ('name_unique',
         'UNIQUE(name)',
         "The title course must be unique")
    ]


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Sessions'
    name = fields.Char(required=True)
    # start_date = fields.Date()
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    # instructor_id = fields.Many2one('res.partner', string='Instructor')
    instructor_id = fields.Many2one('res.partner', string='Instructor',
                                    domain=['|', ('category_id', '=', "Teacher/Level 1"),
                                            '|', ('instructor', '=', True),
                                            '|',  ('category_id', '=', "Teacher/Level 2"),
                                            ('category_id', '=', "Prospects")])

    course_id = fields.Many2one('openacademy.course', string='Course', ondelete='cascade', recuired=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendies")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(string="End date", store=True,
                           compute='get_end_date', inverse='set_end_date')
    attendees_count = fields.Integer(
        string="Attendees Count", compute='_get_attendees_count', store=True)
    color = fields.Integer()

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats


    @api.onchange('seats', 'attendee_ids')
    def veryfi_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': 'The number of avilable seats may not be negative'
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': 'Increase seats or remove excess attendees'
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def check_instructor_is_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)


    @api.depends('start_date', 'duration')
    def get_end_date(self):
        for r in self:
            if not(r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date+duration

    def set_end_date(self):
        for r in self:
            if not(r.start_date and r.end_date):
                continue
            r.duration = (r.end_date-r.start_date).days + 1