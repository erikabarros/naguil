# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from cliente_app import cliente_facade
from routes import clientes
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index(cliente_id):
    cliente = cliente_facade.get_cliente_cmd(cliente_id)()
    cliente_form = cliente_facade.cliente_form()
    context = {'save_path': router.to_path(save, cliente_id), 'cliente': cliente_form.fill_with_model(cliente)}
    return TemplateResponse(context, 'clientes/cliente_form.html')

@login_not_required
def save(cliente_id, **cliente_properties):
    cmd = cliente_facade.update_cliente_cmd(cliente_id, **cliente_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'cliente': cliente_properties}

        return TemplateResponse(context, 'clientes/cliente_form.html')
    return RedirectResponse(router.to_path(clientes))

