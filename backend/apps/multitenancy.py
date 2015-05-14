# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from google.appengine.api.namespace_manager.namespace_manager import set_namespace
from gaepermission.decorator import login_not_required
from tekton.gae.middleware import Middleware

_domain_dct = {}
_subdomain_dct = defaultdict(lambda: '')

@login_not_required
def set_domain(domain, namespace):
    _domain_dct[domain] = namespace

@login_not_required
def set_subdomain(subdomain, namespace):
    _subdomain_dct[subdomain] = namespace

@login_not_required
def get_namespace(host):
    domain = host.split(':')[0]
    ns = _domain_dct.get(domain)
    if ns:
        return ns
    subdomain = domain.split('.')[0]
    return _subdomain_dct[subdomain]


class MultitenacyMiddleware(Middleware):
    def set_up(self):
        ns = get_namespace(self.handler.request.host)
        if ns:
            set_namespace(ns)
