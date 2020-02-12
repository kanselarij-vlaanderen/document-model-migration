import escape_helpers

def construct_select_docs_query(batch_size, graph):
    with open('/usr/src/app/ext/app/queries/1-select-docs.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# GRAPH_PLACEHOLDER', escape_helpers.sparql_escape_uri(graph))
        template = template.replace('# LIMIT_PLACEHOLDER', str(batch_size))
        return template

def construct_list_doc_versions_query(document_uris, graph):
    document_uris = '\n      '.join(map(escape_helpers.sparql_escape_uri, document_uris))
    with open('/usr/src/app/ext/app/queries/2-list-doc-versions.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# GRAPH_PLACEHOLDER', escape_helpers.sparql_escape_uri(graph))
        template = template.replace('# DOC_URIS_PLACEHOLDER', document_uris)
        return template

def construct_insert_triples(triples, graph):
    query = """
    PREFIX pav: <http://purl.org/pav/>
    PREFIX dct: <http://purl.org/dc/terms/>
    
    INSERT DATA {
      GRAPH # GRAPH_PLACEHOLDER {
    """
    query = query.replace('# GRAPH_PLACEHOLDER', escape_helpers.sparql_escape_uri(graph))
    for s, p, o in triples:
        query += "    {} {} {} .\n".format(s, p, o)
    query += """
      }
    }
    """
    return query

def construct_migrate_docs(document_uris, graph):
    document_uris = '\n      '.join(map(escape_helpers.sparql_escape_uri, document_uris))
    with open('/usr/src/app/ext/app/queries/4-migrate-docs.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# GRAPH_PLACEHOLDER', escape_helpers.sparql_escape_uri(graph))
        template = template.replace('# DOC_URIS_PLACEHOLDER', document_uris)
        return template

