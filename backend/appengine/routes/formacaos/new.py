# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from formacao_app import formacao_facade
from routes import formacaos
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'formacaos/formacao_form.html')

@login_not_required
def save(**formacao_properties):
    cmd = formacao_facade.save_formacao_cmd(**formacao_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'formacao': formacao_properties}

        return TemplateResponse(context, 'formacaos/formacao_form.html')
    return RedirectResponse(router.to_path(formacaos))

