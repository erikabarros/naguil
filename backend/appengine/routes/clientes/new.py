# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from formacao_app.formacao_model import Formacao
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from cliente_app import cliente_facade
from routes import clientes
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'clientes/cliente_form.html')

@login_not_required
def save(**cliente_properties):
    try:
        chave = cliente_properties.pop('formacao', 0)[0]
        formacao = Formacao.get_by_id(int(chave))
        cliente_properties['formacao'] = formacao
        cmd = cliente_facade.save_cliente_cmd(**cliente_properties)

        cmd()
    except Exception as e:
        context = {'errors': cmd.errors,
                   'cliente': cliente_properties}

        return TemplateResponse(context, 'clientes/cliente_form.html')
    return RedirectResponse(router.to_path(clientes))


