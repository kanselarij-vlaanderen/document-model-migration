import escape_helpers
import os.path

def construct_select_docs_query(batch_size, batch_number):
    offset = batch_number * batch_size
    with open('/usr/src/app/ext/app/queries/1-select-docs.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# LIMIT_PLACEHOLDER', str(batch_size))
        template = template.replace('# OFFSET_PLACEHOLDER', str(offset))
        return template

def construct_list_doc_versions_query(document_uris):
    document_uris = '\n      '.join(map(escape_helpers.sparql_escape_uri, document_uris))
    with open('/usr/src/app/ext/app/queries/2-list-doc-versions.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# DOC_URIS_PLACEHOLDER', document_uris)
        return template

def construct_insert_triples(triples):
    query = """
    PREFIX pav: <http://purl.org/pav/>
    PREFIX dct: <http://purl.org/dc/terms/>
    
    INSERT DATA {
      GRAPH <http://mu.semte.ch/graphs/organizations/kanselarij> {
    """
    for s, p, o in triples:
        query += "    {} {} {} .\n".format(s, p, o)
    query += """
      }
    }
    """
    return query

def construct_migrate_docs(document_uris):
    document_uris = '\n      '.join(map(escape_helpers.sparql_escape_uri, document_uris))
    with open('/usr/src/app/ext/app/queries/4-migrate-docs.sparql', 'r') as file:
        template = file.read()
        template = template.replace('# DOC_URIS_PLACEHOLDER', document_uris)
        return template

