import json

import webapp2

from .create_worksheet import create_worksheet


class SheetMakerWeb(webapp2.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        title = body.get('title', 'Worksheet')
        lines = body.get('lines')
        sources = body.get('sources', [])
        remove_commas = body.get('removeCommas', True)
        pos = self.get_pos(body)
        if lines is None:
            return self.abort(400)

        sheet, keys = create_worksheet(title, lines, sources, remove_commas, pos)
        self.response.write(sheet.getvalue())
        self.response.write(', key: ')
        self.response.write(keys.getvalue())

    @staticmethod
    def get_pos(body):
        data = [
            ('Subject', body.get('nounColor')),
            ('Verb', body.get('verbColor')),
            ('DO', body.get('directObjectColor')),
            ('IO', body.get('indirectObjectColor')),
            ('PN', body.get('predicateNominativeColor')),
            ('PA', body.get('predicateAdjectiveColor')),
            ('Preposition', body.get('prepositionColor')),
            ('Appositive', body.get('appositiveColor')),
            ('Participle', body.get('participleColor')),
            ('Infinitive', body.get('infinitiveColor')),
        ]
        result = {}
        for index, (name, color) in enumerate(data):
            if color is not None:
                result[name] = {
                    'name': name,
                    'id': index,
                    'rgb': color
                }
        return result
