# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from cliente_app.cliente_commands import ListClienteCommand, SaveClienteCommand, UpdateClienteCommand, ClienteForm,\
    GetClienteCommand, DeleteClienteCommand
from gaepermission.decorator import login_not_required


@login_not_required
def save_cliente_cmd(**cliente_properties):
    """
    Command to save Cliente entity
    :param cliente_properties: a dict of properties to save on model
    :return: a Command that save Cliente, validating and localizing properties received as strings
    """
    return SaveClienteCommand(**cliente_properties)

@login_not_required
def update_cliente_cmd(cliente_id, **cliente_properties):
    """
    Command to update Cliente entity with id equals 'cliente_id'
    :param cliente_properties: a dict of properties to update model
    :return: a Command that update Cliente, validating and localizing properties received as strings
    """
    return UpdateClienteCommand(cliente_id, **cliente_properties)

@login_not_required
def list_clientes_cmd():
    """
    Command to list Cliente entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListClienteCommand()

@login_not_required
def cliente_form(**kwargs):
    """
    Function to get Cliente's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ClienteForm(**kwargs)

@login_not_required
def get_cliente_cmd(cliente_id):
    """
    Find cliente by her id
    :param cliente_id: the cliente id
    :return: Command
    """
    return GetClienteCommand(cliente_id)


@login_not_required
def delete_cliente_cmd(cliente_id):
    """
    Construct a command to delete a Cliente
    :param cliente_id: cliente's id
    :return: Command
    """
    return DeleteClienteCommand(cliente_id)

