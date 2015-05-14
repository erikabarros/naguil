# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from formacao_app.formacao_model import Formacao
from routes.formacaos import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Formacao)
        mommy.save_one(Formacao)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        formacao_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'nome']), set(formacao_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Formacao.query().get())
        json_response = rest.new(None, nome='nome_string')
        db_formacao = Formacao.query().get()
        self.assertIsNotNone(db_formacao)
        self.assertEquals('nome_string', db_formacao.nome)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        formacao = mommy.save_one(Formacao)
        old_properties = formacao.to_dict()
        json_response = rest.edit(None, formacao.key.id(), nome='nome_string')
        db_formacao = formacao.key.get()
        self.assertEquals('nome_string', db_formacao.nome)
        self.assertNotEqual(old_properties, db_formacao.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        formacao = mommy.save_one(Formacao)
        old_properties = formacao.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, formacao.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome']), set(errors.keys()))
        self.assertEqual(old_properties, formacao.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        formacao = mommy.save_one(Formacao)
        rest.delete(None, formacao.key.id())
        self.assertIsNone(formacao.key.get())

    def test_non_formacao_deletion(self):
        non_formacao = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_formacao.key.id())
        self.assertIsNotNone(non_formacao.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

