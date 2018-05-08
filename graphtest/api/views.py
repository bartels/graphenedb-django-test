from __future__ import unicode_literals

from neo4j import v1 as neo4j
import py2neo

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import api_view
from rest_framework.response import Response

REST_ENDPOINT = 'hobby-lnbaldgbnnmpgbkeeghihdal.dbs.graphenedb.com:24780/db/data/'
BOLT_ENDPOINT = 'bolt://hobby-lnbaldgbnnmpgbkeeghihdal.dbs.graphenedb.com:24786'

CQL = """
MATCH (actor:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(movie)<-[:DIRECTED]-(director)
RETURN actor,movie,director
LIMIT 10
"""


def get_graphenedb_credentials():
    try:
        user = settings.GRAPHENEDB_USER
    except AttributeError:
        raise ImproperlyConfigured('Add "GRAPHENEDB_USER" to settings.py')
    try:
        password = settings.GRAPHENEDB_PASS
    except AttributeError:
        raise ImproperlyConfigured('Add "GRAPHENEDB_PASS" to settings.py')

    return user, password


@api_view(['post'])
def neo4j_driver_view(request):
    """
    neo4j-driver (official driver)

    Pass through CQL query and return JSON response
    """
    user, password = get_graphenedb_credentials()

    cqlQuery = request.body
    if not cqlQuery:
        return Response({'detail': 'Empty query'}, status=400)

    driver = neo4j.GraphDatabase.driver('{0}'.format(BOLT_ENDPOINT), auth=neo4j.basic_auth(user, password))

    with driver.session() as session:
        try:
            results = session.run(cqlQuery)
            return Response(results.data())
        except Exception as e:
            return Response({'detail': unicode(e)}, status=400)


@api_view(['get', 'post'])
def py2neo_view(request):
    """
    py2neo (community driver)

    Pass through CQL query and return JSON response
    """
    user, password = get_graphenedb_credentials()

    cqlQuery = request.body
    if not cqlQuery:
        return Response({'detail': 'Empty query'}, status=400)

    py2neo.authenticate(REST_ENDPOINT, user, password)
    graph = py2neo.Graph(BOLT_ENDPOINT, user=user, password=password, bolt=True, secure=True, http_port=24789, https_port=24780)

    try:
        results = graph.data(cqlQuery)
        return Response(results)
    except Exception as e:
        return Response({'detail': unicode(e)}, status=400)
