# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from cliente_app.cliente_model import Cliente
from routes.clientes.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Cliente)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        cliente = mommy.save_one(Cliente)
        redirect_response = delete(cliente.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(cliente.key.get())

    def test_non_cliente_deletion(self):
        non_cliente = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_cliente.key.id())
        self.assertIsNotNone(non_cliente.key.get())

