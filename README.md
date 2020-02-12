## Docker compose snippet
Add to `docker-compose.override.yml` (build  locally as it is a temporary service)
```
doc-migration:
  build: https://github.com/kanselarij-vlaanderen/document-model-migration.git
```

## Configuration
The query batch size can be configured through the `BATCH_SIZE` env var, but the default of `75` should work fine.

## Running instructions
1. Bring the stack into a maintenance state
```
drc down
```
2. Start the DB
```
drc up triplestore
```
3. Start the migration
```
drc up doc-migration
```