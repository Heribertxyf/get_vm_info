#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" project wsgi file """

from __future__ import absolute_import, unicode_literals

from get_vm_info import get_vm_info_app


if __name__ == '__main__':
    get_vm_info_app.debug = True
    get_vm_info_app.run()
