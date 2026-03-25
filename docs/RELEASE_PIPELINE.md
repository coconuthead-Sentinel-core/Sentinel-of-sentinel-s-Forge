# Release Pipeline

The GitHub Actions release workflow now performs a real container release instead of a placeholder checkout:

1. Runs the Python test suite
2. Runs security coverage gates (dependency audit, static security analysis, secret scan, container filesystem scan)
3. Builds the production Docker image from `Dockerfile`
4. Pushes the image to a container registry
5. Publishes a `release-manifest.txt` artifact, and attaches it to GitHub releases

## Security Coverage Gates

The release and CI workflows now enforce these gates before release publish:

1. `pip-audit` dependency vulnerability scan
2. `bandit -r backend -ll` static security scan
3. `gitleaks` secret scanning
4. `trivy` HIGH/CRITICAL filesystem scan

If any gate fails, the release pipeline is blocked.

## Default Registry

By default the workflow publishes to:

`ghcr.io/coconuthead-sentinel-core/sentinel-of-sentinel-s-forge`

That default comes from the repository remote and the workflow fallback to `ghcr.io/${github.repository}`.

## GitHub Actions Configuration

### Required repository settings

- Actions workflow permissions must allow `GITHUB_TOKEN` to write packages
- The repository must have GitHub Container Registry enabled

### Optional repository variables

- `CONTAINER_REGISTRY`: alternate registry hostname such as `index.docker.io` or `<name>.azurecr.io`
- `CONTAINER_IMAGE`: alternate namespace/image path such as `team/sentinel-forge`

### Required secrets for non-GHCR registries

- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`

### Runtime deployment secrets

These are not consumed by the build job, but the deploy target must provide them before the published image will run correctly:

- `API_KEY`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_ID_STARTER`
- `STRIPE_PRICE_ID_PRO`
- `STRIPE_PRICE_ID_ENTERPRISE`
- `AOAI_ENDPOINT`
- `AOAI_KEY`
- `COSMOS_ENDPOINT`
- `COSMOS_KEY`

## Manual Runs

The workflow also supports `workflow_dispatch`. Supply `release_tag` if you want a custom image tag for a manual publish; otherwise the workflow uses a short Git SHA.
