#coding=utf-8
__author__ = 'wt'
import openerp.http
from openerp.http import request
from base import odootask_qweb_render
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
    @openerp.http.route("/index.html", type='http', auth="none", methods=["GET"])
    def index_page(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.index", context=context)

    @openerp.http.route("/search.html", type='http', auth="none", methods=["GET"])
    def search_page(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.search", context=context)

    @openerp.http.route("/detail.html", type='http', auth="none", methods=["GET"])
    def detail_page(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.detail", context=context)

    @openerp.http.route("/upload.html", type='http', auth="none", methods=["GET"])
    def upload_page(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.upload", context=context)

    @openerp.http.route("/donator.html", type='http', auth="none", methods=["GET"])
    def donator_page(self, **kwargs):
        context = dict()
        return odootask_qweb_render.render("odootask.donator", context=context)

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
            category_id = task[0]["category_id"][0]
            category_obj = env['odootask.task_category'].sudo().search_read([("id", "=",category_id )])[0]
            if category_obj["unit"] :
                unit = category_obj["unit"]
            else:
                unit = [False,""]
            good = task[0]
            good["unit"] = unit
            good["create_date"] = str(datetime.datetime.strptime(good["create_date"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                    hours=8)).split(".")[0]
            tracks = env['odootask.track'].sudo().search_read([("id", "in", task[0]["track"])],order="%s desc"%"create_date")
            res["data"]["good"] = task[0]
            res["data"]["tracks"] = tracks
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/communitys', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def communitys(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            communitys = env['odootask.community'].sudo().search_read()
            res["data"]["communitys"] = communitys
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/good_types', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def good_types(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            good_types = env['odootask.task_category'].sudo().search_read()
            res["data"]["good_types"] = good_types
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/donator_number', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def donator_number(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            mobile = kw.get("mobile","")
            if mobile == "":
                raise Exception("请输入手机号")

            donators = env['res.partner'].sudo().search_read([("phone","=",mobile)])
            if len(donators):
                donator = donators[0]
            else:
                donator = {}
            res["data"]["donator"] = donator
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/units', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def units(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            units = env['odootask.unit'].sudo().search_read()
            res["data"]["units"] = units
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/upload', type='http', auth="none", methods=["POST"])
    @serialize_exception
    def upload(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            community_name = kw.get("community_name")
            phone = kw.get("phone","")
            phone_code = kw.get("phone_code","")
            cardid = kw.get("cardid","")
            donator_name = kw.get("donator_name")
            good_type = kw.get("good_type")
            amount = kw.get("amount")
            remark = kw.get("remark","")
            image_path = kw.get("image_path","")
            image_url = kw.get("image_url","")
            state = "confirmed"
            #存储捐赠人信息
            donators = env['res.partner'].sudo().search_read(["&",("partner_type", "=", "donator"), ("phone","=",phone)])
            if len(donators) > 0 :
                donator = donators[0]
                donaor_number =  donator.get("number","")
                donator_id = donator["id"]

                donator_obj = {}
                donator_obj["id"] = donator_id
                donator_obj["display_name"] = donator_name
                donator_obj["name"] = donator_name
                donator_obj["cardid"] = cardid
                env["res.partner"].sudo().write(donator_obj)
            else:
                donator = dict(
                    display_name = donator_name,
                    name = donator_name,
                    partner_type = "donator",
                    phone = phone,
                    cardid = cardid,
                    goods = [],
                )
                try:
                    env["res.partner"].sudo().create(donator)
                except:
                    pass
                donators = env['res.partner'].sudo().search_read(["&",("partner_type","=","donator")
                ,("phone","=",phone)])
                donator_obj = donators[0]
                donator_obj["number"] = "DR"  + str(donator_obj["id"]).zfill(6)
                donaor_number = donator_obj["number"]
                donator_id = donator_obj["id"]
                env["res.partner"].sudo().write({"id":donator_id,"number":donaor_number})

            community_obj = env['odootask.community'].sudo().search_read([("name","=",community_name)])
            community_numer = community_obj[0]["number"]
            good_type_obj = env['odootask.task_category'].sudo().search_read([("name","=",good_type)])
            good_type_id = good_type_obj[0]["id"]

            good = dict(
                donator_id = donator_id,
                category_id = good_type_id,
                amount = amount,
                remark = remark,
                image_path = image_path,
                image_url = image_url,
                state = state,
            )
            good_obj = env["odootask.task"].sudo().create(good)
            good_obj = env["odootask.task"].sudo().search_read([("id","=",good_obj.id)])[0]
            good_obj_update = {}
            good_obj_update["id"] = good_obj["id"]
            good_obj_update["number"] = "W" + "-" + community_numer  + "-"+ str(good_obj["id"]).zfill(6)
            env["odootask.task"].sudo().write(good_obj_update)

            created_goods = env['odootask.task'].sudo().search_read([("id","=",good_obj["id"])])
            res["data"]["good"] = created_goods[0]
            res["data"]["donator_number"] = donaor_number
            # try:
            #     utils.send_106sms(phone,donaor_number)
            # except Exception,e:
            #     print e

        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/goods', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def goods(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            donator_number = kw.get("donator_number")
            donators = env['res.partner'].sudo().search_read([("partner_type","=","donator"),("number", "=", donator_number)])
            if len(donators) == 0:
                goods = []
            else:
                donator = donators[0]
                goods = env["odootask.task"].sudo().search_read([("donator_id","=",donator["id"])])
                goods.sort(key=lambda obj:obj["create_date"])
                goods.reverse()
                for good in goods:
                    good["create_date"] = str(datetime.datetime.strptime(good["create_date"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)).split(".")[0]
            res["data"]["goods"] = goods
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/nearby_donate', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def nearby_donate(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            goods = env['odootask.task'].sudo().search_read()
            goods.sort(key=lambda obj:obj["create_date"])
            goods.reverse()
            goods = goods[0:5]
            for good in goods :
                create_date = good["create_date"]
                create_date = str(datetime.datetime.strptime(create_date, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)).split(".")[0]
                date = create_date.split(" ")[0]
                time = create_date.split(" ")[1]
                curr_date = str(datetime.datetime.now()).split(" ")[0]
                if date == curr_date :
                    show_date = "今天"
                else:
                    show_date = date.split("-")[1] + "-"+ date.split("-")[2]
                show_time = time.split(":")[0] +":"+ time.split(":")[1]
                good["create_date"] = create_date
                good["show_date"] = show_date
                good["show_time"] = show_time

            res["data"]["goods"] = goods
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/image', type='http', auth="none", methods=["GET"])
    def image(self, **kw):
        res = None
        env = request.env
        good_number = kw.get("good_number", "")
        task = env['odootask.task'].sudo().search_read([("number", "=", good_number)])
        if len(task) == 0:
            return res
        tracks = env['odootask.track'].sudo().search_read([("id", "in", task[0]["track"])],
                                                          order="%s desc" % "create_date")
        category_id = task[0]["category_id"][0]
        category_obj = env['odootask.task_category'].sudo().search([("id", "=", category_id)])
        image_data = category_obj.image
        import base64
        image_data = base64.b64decode(image_data)
        headers = [('Content-Type', 'image/png')]
        import hashlib
        hashed_session = hashlib.md5(request.session_id).hexdigest()
        retag = hashed_session
        headers.append(('ETag', retag))
        headers.append(('Content-Length', len(image_data)))
        try:
            ncache = int(kw.get('cache'))
            headers.append(('Cache-Control', 'no-cache' if ncache == 0 else 'max-age=%s' % (ncache)))
        except:
            pass
        return request.make_response(image_data,headers)

    @http.route('/donators', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def donators(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            donators = env['res.partner'].sudo().search_read([("partner_type","=","donator")])
            res["data"]["donators"] = donators
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/donator', type='http', auth="none", methods=["GET"])
    @serialize_exception
    def donator(self, **kw):
        res = utils.init_response_data()
        try:
            env = request.env
            phone = kw.get("mobile","")
            donators = env['res.partner'].sudo().search_read(["&",("partner_type","=","donator"),("phone","=",phone)])
            if len(donators):
                donator = donators[0]
            else:
                donator = {}
            res["data"]["donator"] = {}
            res["data"]["donator"]["donator_name"] = donator.get("name","")
            res["data"]["donator"]["cardid"] = donator.get("cardid","")
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

