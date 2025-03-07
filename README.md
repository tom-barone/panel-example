## Development

```bash
poetry run panel serve panel_example/main.py --basic-auth credentials.json --cookie-secret $(openssl rand -base64 32 | tr -- '+/' '-_') --dev
```

## Dokku

Relevant files:

- `.buildpacks`
- `.python-version`
- `Procfile`

```bash
# Create the app
ssh -t tbone@au-adelaide.tombarone.net dokku apps:create panel.tombarone.net

# Add the dokku git remote, so we can git push to the server and deploy
git remote add dokku dokku@au-adelaide.tombarone.net:panel.tombarone.net

# Set the deployed website domain
dokku domains:set panel.tombarone.net

# Set any environment variables
dokku config:set PANEL_COOKIE_SECRET=$(openssl rand -base64 32 | tr -- '+/' '-_')

# Setup LetsEncrypt certs
# - Make sure to have your domain DNS settings point to the server before running this
dokku letsencrypt:enable

# Scale up any processes (web, worker, etc)
dokku ps:scale web=1

# Push the code to the server and deploy
git push dokku main
```

## GCP Cloud Run

Relevant files:

- `Dockerfile`

```bash
gcloud auth login
# Create requirements.txt file from poetry
poetry export -f requirements.txt --output requirements.txt
gcloud run deploy --source .
```
