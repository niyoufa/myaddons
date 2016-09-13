__author__ = 'wt'
import openerp.http
from openerp.http import request
from base import odootask_qweb_render
import math
import simplejson as json
import pdb

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

from dhuiaddons.dhuitask.rong import Rong

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

class TaskController(openerp.http.Controller):
    @openerp.http.route("/tasks", type='http', auth="none", methods=["GET"])
    def index(self, **kwargs):
        para_keyword = kwargs.get("k", "")
        para_category_id = kwargs.get("c", "")
        para_order = kwargs.get("o", "create_date")
        para_page = kwargs.get("p", "0")
        para_qty_per_page = kwargs.get("n", "10")

        domain = list()
        if para_keyword:
            domain.append(("name", "ilike", para_keyword))
        if para_category_id:
            domain.append(("category_id", "=", int(para_category_id)))

        env = request.env

        page_count = int(math.ceil(env['odootask.task'].sudo().search_count(domain) / float(para_qty_per_page)))

        page = int(para_page)
        qty_per_page = int(para_qty_per_page)
        tasks = env['odootask.task'].sudo().search(domain, order="%s desc" % para_order, offset=page * qty_per_page,
                                                   limit=qty_per_page)

        categories = env["odootask.task_category"].sudo().search([])
        count_for_category = [
            ((cat.name, cat.id),
             env['odootask.task'].sudo().search_count([("name", "ilike", para_keyword), ("category_id", "=", cat.id)]))
            for cat in categories]

        if para_keyword:
            count_for_category = filter(lambda cfc: cfc[1] > 0, count_for_category)
        count_for_category = dict(count_for_category)

        context = dict()
        context["tasks"] = tasks
        context["count_for_category"] = count_for_category

        context["category_id"] = para_category_id
        context["keyword"] = para_keyword
        context["page"] = para_page
        context["main_nav_task_active"] = True
        context["login_redirect"] = "/tasks"
        context["page_count"] = page_count

        return odootask_qweb_render.render("odootask.tasks", context=context)

    @openerp.http.route("/api/tasks", type='http', auth="public", methods=["GET"])
    def api_tasks(self,**kwargs):
        env = request.env
        tasks = env['odootask.task'].sudo().search([])
        j = json.dumps(tasks)
        return "%d" % len(tasks)

    @openerp.http.route("/task/<int:task_id>", type='http', auth="public", methods=["GET"])
    def task(self, task_id=None, **kwargs):
        try:
            if not task_id:
                # TODO return 404
                pass
            env = request.env
            task = env['odootask.task'].sudo().search([("id", "=", task_id)])
            context = dict()
            context["task"] = task
            context["login_redirect"] = "/task/%d" % task_id
            context["ret_url"] = kwargs.get("ret_url")
            context["user_id"] = env.user.id
            return odootask_qweb_render.render("odootask.task", context=context)
        except Exception as e:
            pass

    @openerp.http.route("/task", type='http', auth="user", methods=["GET", "POST"])
    def new_task(self, **kwargs):
        if request.httprequest.method == 'GET':
            try:
                task_categories = request.env["odootask.task_category"].search([]);
                context = dict()
                context["task_categories"] = task_categories
                return odootask_qweb_render.render("odootask.task_new", context=context)
            except Exception as ex:
                pass
                # TODO Error handler
        elif request.httprequest.method == 'POST':
            name = kwargs.get("name", "")
            description = kwargs.get("description", "")
            category_id = kwargs.get("category_id", "")
            values = dict()
            values["name"] = name
            values["description"] = description
            if category_id:
                values["category_id"] = int(category_id)
            request.env["odootask.task"].create(values)
            return "create ok"
        else:
            return "only GET POST is available!"

    @openerp.http.route("/task/apply/<int:task_id>", type='http', auth="user", methods=["GET", "POST"])
    def apply_task(self, task_id=None):
        try:
            if not task_id:
                # TODO return 404
                pass
            env = request.env
            task = env['odootask.task'].sudo().search([("id", "=", task_id)])
            task.apply(env.user.id)
            return "apply ok"
        except Exception as e:
            pass

    @openerp.http.route("/task/<int:task_id>/comment", type='http', auth="user", methods=["POST"])  # "GET",
    def comment(self, task_id=None, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                if not task_id:
                    # TODO return 404
                    pass
                content = kwargs.get("content", "")
                env = request.env
                task = env['odootask.task'].sudo().search([("id", "=", task_id)])
                if task:
                    env["odootask.task_comment"].create({"task_id": task.id, "content": content})
                    return "post comment ok"
            except Exception as e:
                pass

class GoodsController(openerp.http.Controller):
    @openerp.http.route("/search", type='http', auth="none", methods=["GET"])
    def index(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.index", context=context)

    @http.route('/good', type='http',auth="none", methods=["GET"])
    @serialize_exception
    def good(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            good_number = kw.get("good_number","10001")
            task = env['odootask.task'].sudo().search_read([("number", "=", good_number)])
            if len(task) == 0:
                return res
            tracks = env['odootask.track'].sudo().search_read([("id","in",task[0]["track"])])
            res["data"]["good"] = task[0]
            res["data"]["tracks"] = tracks
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/good', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def good(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            good_number = kw.get("good_number", "10001")
            task = env['odootask.task'].sudo().search_read([("number", "=", good_number)])
            if len(task) == 0:
                return res
            tracks = env['odootask.track'].sudo().search_read([("id", "in", task[0]["track"])],order="%s desc"%"create_date")
            res["data"]["good"] = task[0]
            res["data"]["tracks"] = tracks
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res
