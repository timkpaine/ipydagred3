#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Tim Paine
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'ipydagre-d3',
        'require': 'ipydagre-d3/extension'
    }]
