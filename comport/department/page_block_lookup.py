# -*- coding: utf-8 -*-

class PageBlockLookup:

    def get_uof_blocks(short_name):
        if short_name == "IMPD":
            return {
                'introduction': 'uof-introduction',
                'first-block': 'uof-force-type',
                'blocks': [
                    'uof-by-inc-district',
                    'officer-demographics',
                    'uof-race'
                ]
            }

        if short_name == "BPD":
            return {
                'introduction': 'uof-introduction',
                'first-block': 'uof-force-type',
                'blocks': [
                    'uof-by-inc-district',
                    'officer-demographics',
                    'uof-race'
                ]
            }
