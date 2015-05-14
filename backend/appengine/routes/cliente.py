# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cliente_app.cliente_model import Formacao
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from routes.clientes.new import save
from tekton import router


@login_not_required
@no_csrf
def index():
    contexto = {'salvar_path': router.to_path(save)}
    contexto['formacoes'] = Formacao.query().fetch()
    return TemplateResponse(contexto)

@login_not_required
@no_csrf
def form():
    contexto = {'salvar_path': router.to_path(save)}
    return TemplateResponse(contexto)




