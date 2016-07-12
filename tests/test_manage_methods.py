# -*- coding: utf-8 -*-
import pytest
import mock
from comport.department.models import Department
from manage import add_new_blocks
from comport.content.models import ChartBlock
from comport.content.defaults import ChartBlockDefaults

@pytest.mark.usefixtures('db')
class TestManageMethods:

    def test_add_chart_blocks(self):
        ''' Can add default chart blocks to multiple departments.
        '''
        department1 = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)
        department2 = Department.create(name="Random Police Department", short_name="RPD", load_defaults=False)

        mock_chart_blocks = [
            ChartBlock(title="Open Data Introduction", slug="introduction", dataset="introduction"),
            ChartBlock(title="Complaints By Year", slug="complaints-by-year", dataset="complaints"),
            ChartBlock(title="Complaints By Month", slug="complaints-by-month", dataset="complaints"),
            ChartBlock(title="Complaints By Allegation", slug="complaints-by-allegation", dataset="complaints"),
            ChartBlock(title="Complaints By Allegation Type", slug="complaints-by-allegation-type", dataset="complaints")
        ]

        with mock.patch.object(ChartBlockDefaults, 'defaults', mock_chart_blocks):
            add_new_blocks()

        assert len(department2.chart_blocks) == len(mock_chart_blocks)
        assert len(department1.chart_blocks) == len(mock_chart_blocks)
