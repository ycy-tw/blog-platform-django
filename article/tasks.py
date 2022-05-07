from __future__ import absolute_import, unicode_literals
import logging
import os
from celery import shared_task
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from .models import Post


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'knowslist-0eb53f458d7d.json'


def run_views_report():
    """Runs a simple report on a Google Analytics 4 property."""

    #  Google Analytics 4 property ID before running the sample.
    property_id = "310383954"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    # pagePathPlusQueryString : relative url
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePathPlusQueryString")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="2022-04-10", end_date="today")],
    )
    response = client.run_report(request)

    result = {}
    for row in response.rows:
        url = row.dimension_values[0].value
        page_views = row.metric_values[0].value

        if url.startswith('/a/'):

            slug = url[3:]
            result[slug] = int(page_views)

    return result


@shared_task
def update_post_views():

    post_views = run_views_report()
    for slug, views in post_views.items():
        if Post.objects.filter(slug=slug).exists():
            post = Post.objects.filter(slug=slug)[0]
            post.post_views = views
            post.save()

    now = datetime.now()
    logging.info(f'Current:{now}, Result:{post_views}')
