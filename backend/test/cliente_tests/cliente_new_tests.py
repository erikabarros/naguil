# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from cliente_app.cliente_model import Cliente
from routes.clientes.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Cliente.query().get())
        redirect_response = save(nome='nome_string', formacao='formacao_string', experiencias='experiencias_string', telefone='telefone_string', endereco='endereco_string', arquivo='arquivo_string', email='email_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_cliente = Cliente.query().get()
        self.assertIsNotNone(saved_cliente)
        self.assertEquals('nome_string', saved_cliente.nome)
        self.assertEquals('formacao_string', saved_cliente.formacao)
        self.assertEquals('experiencias_string', saved_cliente.experiencias)
        self.assertEquals('telefone_string', saved_cliente.telefone)
        self.assertEquals('endereco_string', saved_cliente.endereco)
        self.assertEquals('arquivo_string', saved_cliente.arquivo)
        self.assertEquals('email_string', saved_cliente.email)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['nome', 'formacao', 'experiencias', 'telefone', 'endereco', 'arquivo', 'email']), set(errors.keys()))
        self.assert_can_render(template_response)
