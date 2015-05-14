# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from cliente_app.cliente_model import Cliente



class ClienteSaveForm(ModelForm):
    """
    Form used to save and update Cliente
    """
    _model_class = Cliente
    _include = [Cliente.nome, 
                Cliente.formacao, 
                Cliente.experiencias, 
                Cliente.telefone, 
                Cliente.endereco, 
                Cliente.arquivo, 
                Cliente.email]


class ClienteForm(ModelForm):
    """
    Form used to expose Cliente's properties for list or json
    """
    _model_class = Cliente


class GetClienteCommand(NodeSearch):
    _model_class = Cliente


class DeleteClienteCommand(DeleteNode):
    _model_class = Cliente


class SaveClienteCommand(SaveCommand):
    _model_form_class = ClienteSaveForm


class UpdateClienteCommand(UpdateNode):
    _model_form_class = ClienteSaveForm


class ListClienteCommand(ModelSearchCommand):
    def __init__(self):
        super(ListClienteCommand, self).__init__(Cliente.query_by_creation())

