# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from cliente_app import cliente_facade


def index():
    cmd = cliente_facade.list_clientes_cmd()
    cliente_list = cmd()
    cliente_form = cliente_facade.cliente_form()
    cliente_dcts = [cliente_form.fill_with_model(m) for m in cliente_list]
    return JsonResponse(cliente_dcts)


def new(_resp, **cliente_properties):
    cmd = cliente_facade.save_cliente_cmd(**cliente_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **cliente_properties):
    cmd = cliente_facade.update_cliente_cmd(id, **cliente_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = cliente_facade.delete_cliente_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        cliente = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    cliente_form = cliente_facade.cliente_form()
    return JsonResponse(cliente_form.fill_with_model(cliente))

