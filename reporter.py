#!/usr/bin/env python3


class Reporter:
    def __init__(self):
        self.sections = []

    def add_section(self, title, items):
        lines = ['• {}'.format(i) for i in items]
        self.sections.append(
            '{name}\n\n{lines}'.format(name=title, lines='\n'.join(lines))
        )

    def format(self, heading):
        return '{heading}\n\n{sections}'.format(
            heading=heading,
            sections='\n\n'.join(self.sections)
        )
