# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2020 Association Prologin <association@prologin.org>

import jinja2
from pathlib import Path

from .filters import load_library


class Generator:
    def __init__(self, template_namespace: str, game, out_dir: Path, **kwargs):
        self.game = game
        self.out_dir = out_dir
        template_folder = str(
            Path(__file__).parent / 'templates' / template_namespace)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=template_folder),
            lstrip_blocks=True,
            trim_blocks=True,
            keep_trailing_newline=True,
            **kwargs
        )
        self.env.globals['stechec2_generated'] = (
            "This file was generated by stechec2-generator. DO NOT EDIT.")
        self.register_filters()

    def template(self, name, out_name=None, **params):
        if out_name is None:
            out_name = name
        tpl = self.env.get_template(name + '.jinja2')
        out = tpl.stream(game=self.game, **params)
        out_path = self.out_dir / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out.dump(out_path.open('w'))

    def register_filters(self):
        filter_library = load_library()
        for filter_name, filter in filter_library.items():
            self.env.filters[filter_name] = filter
