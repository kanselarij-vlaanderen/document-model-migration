FROM mikidi/mu-python-template:python3-port
LABEL maintainer="info@redpencil.io"

ENV MU_APPLICATION_GRAPH "http://mu.semte.ch/graphs/public"
ENV MU_SPARQL_ENDPOINT "http://triplestore:8890/sparql"
ENV MU_SPARQL_UPDATEPOINT "http://triplestore:8890/sparql"