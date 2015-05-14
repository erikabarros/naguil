# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from cliente_app.cliente_model import Cliente
from routes.clientes import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Cliente)
        mommy.save_one(Cliente)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        cliente_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'nome', 'formacao', 'experiencias', 'telefone', 'endereco', 'arquivo', 'email']), set(cliente_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Cliente.query().get())
        json_response = rest.new(None, nome='nome_string', formacao='formacao_string', experiencias='experiencias_string', telefone='telefone_string', endereco='endereco_string', arquivo='arquivo_string', email='email_string')
        db_cliente = Cliente.query().get()
        self.assertIsNotNone(db_cliente)
        self.assertEquals('nome_string', db_cliente.nome)
        self.assertEquals('formacao_string', db_cliente.formacao)
        self.assertEquals('experiencias_string', db_cliente.experiencias)
        self.assertEquals('telefone_string', db_cliente.telefone)
        self.assertEquals('endereco_string', db_cliente.endereco)
        self.assertEquals('arquivo_string', db_cliente.arquivo)
        self.assertEquals('email_string', db_cliente.email)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome', 'formacao', 'experiencias', 'telefone', 'endereco', 'arquivo', 'email']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        cliente = mommy.save_one(Cliente)
        old_properties = cliente.to_dict()
        json_response = rest.edit(None, cliente.key.id(), nome='nome_string', formacao='formacao_string', experiencias='experiencias_string', telefone='telefone_string', endereco='endereco_string', arquivo='arquivo_string', email='email_string')
        db_cliente = cliente.key.get()
        self.assertEquals('nome_string', db_cliente.nome)
        self.assertEquals('formacao_string', db_cliente.formacao)
        self.assertEquals('experiencias_string', db_cliente.experiencias)
        self.assertEquals('telefone_string', db_cliente.telefone)
        self.assertEquals('endereco_string', db_cliente.endereco)
        self.assertEquals('arquivo_string', db_cliente.arquivo)
        self.assertEquals('email_string', db_cliente.email)
        self.assertNotEqual(old_properties, db_cliente.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        cliente = mommy.save_one(Cliente)
        old_properties = cliente.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, cliente.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome', 'formacao', 'experiencias', 'telefone', 'endereco', 'arquivo', 'email']), set(errors.keys()))
        self.assertEqual(old_properties, cliente.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        cliente = mommy.save_one(Cliente)
        rest.delete(None, cliente.key.id())
        self.assertIsNone(cliente.key.get())

    def test_non_cliente_deletion(self):
        non_cliente = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_cliente.key.id())
        self.assertIsNotNone(non_cliente.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

