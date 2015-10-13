from .models import ChartBlock

class ChartBlockDefaults:
    defaults=[
        ChartBlock(
            title ="Complaints By Year",
            caption ="",
            slug ="complaints-by-year",
            dataset ="complaints",
            content ="Here is the content for Complaints By Year",
            date_updated = None,
            date_edited = None
        ),
        ChartBlock(
            title ="Complaints By Allegation",
            caption ="",
            slug ="complaints-by-allegation",
            dataset ="complaints",
            content ="Here is the content for Complaints By Allegation",
            date_updated = None,
            date_edited = None
        ),
        ChartBlock(
            title ="Complaints By Allegation Type",
            caption ="",
            slug ="complaints-by-allegation-type",
            dataset ="complaints",
            content ="Here is the content for Complaints By Allegation Type",
            date_updated = None,
            date_edited = None
        ),
        ChartBlock(
            title ="Complaints By Disposition",
            caption ="",
            slug ="complaints-by-disposition",
            dataset ="complaints",
            content ="Here is the content for Complaints By Disposition",
            date_updated = None,
            date_edited = None
        )
    ]
