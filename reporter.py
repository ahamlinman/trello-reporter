#!/usr/bin/env python3


class Reporter:
    def __init__(self):
        self.sections = []

    def add_section(self, title, items):
        item_list = '\n'.join([f'• {i}' for i in items])
        self.sections.append(f'{title}\n\n{item_list}')

    def format(self, heading):
        sections = '\n\n'.join(self.sections)
        return f'{heading}\n\n{sections}'
