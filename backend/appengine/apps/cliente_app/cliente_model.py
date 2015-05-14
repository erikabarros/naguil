# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from formacao_app.formacao_model import Formacao
from gaegraph.model import Node
from gaeforms.ndb import property

class Cliente(Node):
    nome = ndb.StringProperty(required=False)
    email = ndb.StringProperty(required=False)
    telefone = ndb.StringProperty(required=False)
    endereco = ndb.StringProperty(required=False)
    formacao = ndb.KeyProperty(Formacao, required=False)
    experiencias = ndb.StringProperty(required=False)
    arquivo = ndb.StringProperty(required=False)



