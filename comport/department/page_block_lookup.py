# -*- coding: utf-8 -*-

# Stores chart blocks for the various pages
class PageBlockLookup:

    #
    # MAIN DATA PAGES CHART BLOCKS
    #

    def get_uof_blocks(short_name):
        ''' Use of Force main data page blocks
        '''
        if short_name == 'BPD':
            return {
                'introduction': 'uof-introduction',
                'first-block': 'uof-by-month',
                'blocks': [
                    'uof-force-type',
                    'uof-by-assignment',
                    'officer-demographics',
                    'uof-race'
                ]
            }

        if short_name == 'LMPD':
            return {
                'introduction': 'uof-introduction',
                'first-block': 'uof-by-month',
                'blocks': [
                    'uof-force-type',
                    'uof-by-division',
                    'officer-demographics',
                    'uof-race'
                ]
            }

        if short_name == 'SRPD':
            return {
                'introduction': 'uof-introduction',
                'first-block': 'uof-by-month',
                'blocks': [
                    'uof-incident-force-type',
                    'uof-by-team',
                    'officer-demographics'
                ]
            }

        # IMPD's blocks are the default
        return {
            'introduction': 'uof-introduction',
            'first-block': 'uof-force-type',
            'blocks': [
                'uof-by-inc-district',
                'officer-demographics',
                'uof-race'
            ]
        }

    def get_ois_blocks(short_name):
        ''' Officer-Involved Shooting main data page blocks
        '''
        if short_name == 'BPD':
            return {
                'introduction': 'ois-introduction',
                'first-block': 'ois-by-month',
                'blocks': [
                    'ois-by-assignment',
                    'officer-demographics',
                    'ois-race'
                ]
            }

        if short_name == 'SRPD':
            return {
                'introduction': 'ois-introduction',
                'first-block': 'ois-by-month',
                'blocks': [
                    'ois-by-type',
                    'ois-by-team',
                    'officer-demographics'
                ]
            }

        # IMPD's blocks are the default
        return {
            'introduction': 'ois-introduction',
            'first-block': 'ois-by-inc-district',
            'blocks': [
                'ois-weapon-type',
                'officer-demographics',
                'ois-race'
            ]
        }

    def get_complaints_blocks(short_name):
        ''' Citizen Complaints main data page blocks
        '''
        if short_name == 'BPD':
            return {
                'introduction': 'complaints-introduction',
                'first-block': 'complaints-by-month',
                'blocks': [
                    'complaints-by-allegation',
                    'complaints-by-disposition',
                    'complaints-by-assignment',
                    'officer-demographics',
                    'complaints-by-demographic',
                    'complaints-by-officer-with-cap',
                ]
            }

        if short_name == 'SRPD':
            return {
                'introduction': 'complaints-introduction',
                'first-block': 'complaints-by-month',
                'blocks': [
                    'complaints-by-allegation',
                    'complaints-by-disposition',
                    'complaints-by-team',
                    'officer-demographics'
                ]
            }

        if short_name == 'WPD':
            return {
                'introduction': 'complaints-introduction',
                'first-block': 'complaints-by-month',
                'blocks': [
                    'complaints-by-allegation',
                    'complaints-by-allegation-type',
                    'complaints-by-finding',
                    'complaints-by-precinct',
                    'officer-demographics',
                    'complaints-by-demographic'
                ]
            }


        # IMPD's blocks are the default
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

    def get_pursuits_blocks(short_name):
        ''' Pursuits main data page blocks
        '''
        return {
            'introduction': 'pursuits-introduction',
            'first-block': 'pursuits-by-month',
            'blocks': [
                'pursuits-by-reason',
                'pursuits-by-distance',
                'pursuits-by-team'
            ]
        }

    def get_assaults_blocks(short_name):
        ''' Assaults on Officers main data page blocks
        '''
        return {
            'introduction': 'assaults-introduction',
            'first-block': 'assaults-by-service-type',
            'blocks': [
                'assaults-by-force-type',
                'assaults-by-officer'
            ]
        }

    #
    # SCHEMA PAGES CHART BLOCKS
    #

    def get_complaint_schema_blocks(short_name):
        ''' Citizen Complaint schema page blocks
        '''
        return {
            'introduction': 'complaints-schema-introduction',
            'footer': 'complaints-schema-footer',
            'disclaimer': 'complaints-schema-disclaimer',
            'blocks': 'complaints-schema-field-'
        }

    def get_uof_schema_blocks(short_name):
        ''' Use of Force schema page blocks
        '''
        return {
            'introduction': 'uof-schema-introduction',
            'footer': 'uof-schema-footer',
            'disclaimer': 'uof-schema-disclaimer',
            'blocks': 'uof-schema-field-'
        }

    def get_ois_schema_blocks(short_name):
        ''' Officer-Involved Shooting schema page blocks
        '''
        return {
            'introduction': 'ois-schema-introduction',
            'footer': 'ois-schema-footer',
            'disclaimer': 'ois-schema-disclaimer',
            'blocks': 'ois-schema-field-'
        }

    def get_pursuits_schema_blocks(short_name):
        ''' Pursuits schema page blocks
        '''
        return {
            'introduction': 'pursuits-schema-introduction',
            'footer': 'pursuits-schema-footer',
            'disclaimer': 'pursuits-schema-disclaimer',
            'blocks': 'pursuits-schema-field-'
        }

    def get_assaults_schema_blocks(short_name):
        ''' Assaults on Officers schema page blocks
        '''
        return {
            'introduction': 'assaults-schema-introduction',
            'footer': 'assaults-schema-footer',
            'disclaimer': 'assaults-schema-disclaimer',
            'blocks': 'assaults-schema-field-'
        }
