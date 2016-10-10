# -*- coding: utf-8 -*-
import pytest
from comport.data.models import IncidentsUpdated
from comport.department.models import Department

@pytest.mark.usefixtures('db')
class TestIncidentsUpdated:
    def test_delete_records(self):
        ''' Delete incidents_updated records using the delete_records method.
        '''
        # create a couple of departments
        department_bpd = Department.create(name="B Police Department", short_name="BPD")
        department_impd = Department.create(name="IM Police Department", short_name="IMPD")

        # create some 'incidents updated' records
        uof_type = "uof"
        ois_type = "ois"
        ids_and_types = [
            ("123abc", uof_type, department_bpd.id), ("234bcd", uof_type, department_bpd.id),
            ("345cde", ois_type, department_bpd.id), ("456def", uof_type, department_impd.id),
            ("567efg", uof_type, department_impd.id), ("678fgh", ois_type, department_impd.id)
        ]
        for opaque_id, use_type, department_id in ids_and_types:
            IncidentsUpdated.create(department_id=department_id, opaque_id=opaque_id, incident_type=use_type)

        # verify that the records were saved as expected
        assert len(IncidentsUpdated.query.all()) == len(ids_and_types)
        assert len(IncidentsUpdated.query.filter_by(department_id=department_bpd.id).all()) == 3
        assert len(IncidentsUpdated.query.filter_by(department_id=department_impd.id).all()) == 3
        assert len(IncidentsUpdated.query.filter_by(incident_type=uof_type).all()) == 4
        assert len(IncidentsUpdated.query.filter_by(incident_type=ois_type).all()) == 2

        # delete the impd records
        num_deleted = IncidentsUpdated.delete_records(department_id=department_impd.id)
        assert num_deleted == len(ids_and_types) / 2

        # verify the results
        assert len(IncidentsUpdated.query.all()) == len(ids_and_types) - num_deleted
        assert len(IncidentsUpdated.query.filter_by(department_id=department_bpd.id).all()) == 3
        assert len(IncidentsUpdated.query.filter_by(department_id=department_impd.id).all()) == 0
        assert len(IncidentsUpdated.query.filter_by(incident_type=uof_type).all()) == 2
        assert len(IncidentsUpdated.query.filter_by(incident_type=ois_type).all()) == 1

        # delete the bpd uof records
        num_deleted = IncidentsUpdated.delete_records(department_id=department_bpd.id, incident_type=uof_type)
        assert num_deleted == 2

        # verify the results
        assert len(IncidentsUpdated.query.all()) == 1
        assert len(IncidentsUpdated.query.filter_by(department_id=department_bpd.id).all()) == 1
        assert len(IncidentsUpdated.query.filter_by(incident_type=uof_type).all()) == 0
        assert len(IncidentsUpdated.query.filter_by(incident_type=ois_type).all()) == 1
