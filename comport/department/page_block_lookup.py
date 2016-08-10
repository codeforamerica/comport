# -*- coding: utf-8 -*-

class PageBlockLookup:

    def get_uof_blocks(short_name):
        return {
            'introduction': 'uof-introduction',
            'first-block': 'uof-force-type',
            'blocks': [
                'uof-by-assignment',
                'officer-demographics',
                'uof-race'
            ]
        }

    def get_ois_blocks(short_name):
        return {
            'introduction': 'ois-introduction',
            'first-block': 'ois-by-assignment',
            'blocks': [
                'ois-weapon-type',
                'officer-demographics',
                'ois-race',
            ]
        }

    def get_complaints_blocks(short_name):

        if short_name == 'BPD':
            return {
                'introduction': 'complaints-introduction',
                'first-block': 'complaints-by-month',
                'blocks': [
                    'complaints-by-allegation',
                    'complaints-by-allegation-type',
                    'complaints-by-disposition',
                    'complaints-by-assignment',
                    'officer-demographics',
                    'complaints-by-demographic',
                    'complaints-by-officer',
                ]
            }

        # We use IMPD as a default here
        return {
            'introduction': 'complaints-introduction',
            'first-block': 'complaints-by-month',
            'blocks': [
                'complaints-by-allegation',
                'complaints-by-allegation-type',
                'complaints-by-finding',
                'complaints-by-precinct',
                'officer-demographics',
                'complaints-by-demographic',
                'complaints-by-officer'
            ]
        }

    def get_complaint_schema_blocks(short_name):
        return {
            'introduction': 'complaints-schema-introduction',
            'footer': 'complaints-schema-footer',
            'disclaimer': 'complaints-schema-disclaimer',
            'blocks': 'complaints-schema-field-'
        }

    def get_uof_schema_blocks(short_name):
        return {
            'introduction': 'uof-schema-introduction',
            'footer': 'uof-schema-footer',
            'disclaimer': 'uof-schema-disclaimer',
            'blocks': 'uof-schema-field-'
        }

    def get_ois_schema_blocks(short_name):
        return {
            'introduction': 'ois-schema-introduction',
            'footer': 'ois-schema-footer',
            'disclaimer': 'ois-schema-disclaimer',
            'blocks': 'ois-schema-field-'
        }

    def get_assaults_blocks(short_name):
        return {
            'introduction': 'assaults-introduction',
            'first-block': 'assaults-by-service-type',
            'blocks': [
                'assaults-by-force-type',
                'assaults-by-officer'
            ]
        }

    def get_assaults_schema_blocks(short_name):
        return {
            'introduction': 'assaults-schema-introduction',
            'footer': 'assaults-schema-footer',
            'disclaimer': 'assaults-schema-disclaimer',
            'blocks': 'assaults-schema-field-'
        }
