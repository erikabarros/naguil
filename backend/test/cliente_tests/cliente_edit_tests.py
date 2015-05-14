# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from cliente_app.cliente_model import Cliente
from routes.clientes.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        cliente = mommy.save_one(Cliente)
        template_response = index(cliente.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        cliente = mommy.save_one(Cliente)
        old_properties = cliente.to_dict()
        redirect_response = save(cliente.key.id(), nome='nome_string', formacao='formacao_string', experiencias='experiencias_string', telefone='telefone_string', endereco='endereco_string', arquivo='arquivo_string', email='email_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_cliente = cliente.key.get()
        self.assertEquals('nome_string', edited_cliente.nome)
        self.assertEquals('formacao_string', edited_cliente.formacao)
        self.assertEquals('experiencias_string', edited_cliente.experiencias)
        self.assertEquals('telefone_string', edited_cliente.telefone)
        self.assertEquals('endereco_string', edited_cliente.endereco)
        self.assertEquals('arquivo_string', edited_cliente.arquivo)
        self.assertEquals('email_string', edited_cliente.email)
        self.assertNotEqual(old_properties, edited_cliente.to_dict())

    def test_error(self):
        cliente = mommy.save_one(Cliente)
        old_properties = cliente.to_dict()
        template_response = save(cliente.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['nome', 'formacao', 'experiencias', 'telefone', 'endereco', 'arquivo', 'email']), set(errors.keys()))
        self.assertEqual(old_properties, cliente.key.get().to_dict())
        self.assert_can_render(template_response)
