# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from cliente_app import cliente_facade
from routes.clientes import new, edit
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index():
    cmd = cliente_facade.list_clientes_cmd()
    clientes = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    cliente_form = cliente_facade.cliente_form()

    def localize_cliente(cliente):
        cliente_dct = cliente_form.fill_with_model(cliente)
        cliente_dct['edit_path'] = router.to_path(edit_path, cliente_dct['id'])
        cliente_dct['delete_path'] = router.to_path(delete_path, cliente_dct['id'])
        return cliente_dct

    localized_clientes = [localize_cliente(cliente) for cliente in clientes]
    context = {'clientes': localized_clientes,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'clientes/cliente_home.html')


@login_not_required
def delete(cliente_id):
    cliente_facade.delete_cliente_cmd(cliente_id)()
    return RedirectResponse(router.to_path(index))

