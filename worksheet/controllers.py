#coding=utf-8
__author__ = 'wt'
import openerp.http
from openerp.http import request
import math
import simplejson as json
import pdb
import datetime
import json,pdb

from openerp import http
from openerp.http import request
from openerp.http import serialize_exception as _serialize_exception


import status
import utils
import functools
import werkzeug.utils
import werkzeug.wrappers
import simplejson
import logging

_logger = logging.getLogger(__name__)

def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        res = utils.init_response_data()
        try:
            res = f(*args, **kwargs)
            res["message"] = status.Status().getReason(res["code"])
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["message"] = status.Status().getReason(res["code"])
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            res["error_info"] = error
            return simplejson.dumps(res)
        return simplejson.dumps(res)
    return wrap

class WorkController(openerp.http.Controller):
    @http.route('/worksheet/works', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def works(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            domain = [("worksheet", "=", True)]
            projects = env['project.project'].sudo().search_read(domain)
            task_ids = []
            for project in projects:
                task_ids.extend(project.get("task_ids",[]))

            curr_time = str(datetime.datetime.now()).split(" ")[0] 
            start_time = curr_time + " " + "00:00:00.000"
            end_time = curr_time + " " + "23:59:59.999"
            domain = [("create_date",">",start_time),("create_date","<",end_time),("task_id","in",task_ids)]
            works = env['project.task.work'].sudo().search_read(domain)
            res["data"]["works"] = works
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/worksheet/tasks', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def tasks(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            tasks = env['project.task'].sudo().search_read()
            res["data"]["tasks"] = tasks
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/worksheet/projects', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def projects(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            domain = []
            projects = env['project.project'].sudo().search_read(domain)
            res["data"]["projects"] = projects
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res
