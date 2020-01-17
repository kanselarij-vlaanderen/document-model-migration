import os
import itertools
import helpers
import escape_helpers
from helpers import log
from .construct_queries import construct_select_docs_query, construct_list_doc_versions_query, construct_insert_triples, construct_migrate_docs

LATIN_ADVERBIAL_NUMERALS = {
    1: '',
    2: 'BIS',
    3: 'TER',
    4: 'QUATER',
    5: 'QUINQUIES',
    6: 'SEXIES',
    7: 'SEPTIES',
    8: 'OCTIES',
    9: 'NOVIES'
 }

def run_batch(batch_size, batch_number):

    documents = list(map(lambda res: res['doc']['value'], list(helpers.query(construct_select_docs_query(batch_size, batch_number))['results']['bindings'])))

    res = helpers.query(construct_list_doc_versions_query(documents))['results']['bindings']
    print(res)

    res_by_doc = itertools.groupby(res, lambda res: res['doc']['value'])

    triples = []
    for doc_uri, results in res_by_doc:
        results = list(results)
        for i in range(len(results)):
            res = results[i]
            try:
                title = res['stuknummerVR']['value']
            except KeyError:
                title = res['title']['value']
            versioned_title = title + LATIN_ADVERBIAL_NUMERALS[int(res['num']['value'])]
            triples.append((
                escape_helpers.sparql_escape_uri(results[i]['ver']['value']),
                'dct:title',
                escape_helpers.sparql_escape_string(versioned_title),
            ))
            if i > 0:
                triples.append((
                    escape_helpers.sparql_escape_uri(results[i]['ver']['value']),
                    'pav:previousVersion',
                    escape_helpers.sparql_escape_uri(results[i-1]['ver']['value']),
                ))
    if triples:
        query = construct_insert_triples(triples)
        print('constructed query\n' + query)
        res = helpers.update(query)

    query = construct_migrate_docs(documents)
    print('constructed query\n' + query)
    res = helpers.update(query)
    
    return documents

BATCH_SIZE = 75
batch_number = 0
while True:
    docs = run_batch(BATCH_SIZE, batch_number)
    if len(docs) < BATCH_SIZE:
        break