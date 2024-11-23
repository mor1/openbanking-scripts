_default:
    @just --list

endpoints := "name-endpoints.json"

# re-initialise venv
reinitialise:
    rm -rf .venv .ruff_cache
    uv sync

# scrape endpoints
endpoints:
    uv run -- endpoints.py >| {{endpoints}}

# list target URLs
urls:
  cat {{endpoints}} \
  | jq '(.name | gsub("[^A-Za-z0-9._-]";"";"g")) + " " + (.urls[])' \
  | tr -d '"' \
  | while read bank url; do curl -Ls -w "$bank %{url_effective}\n" -o /dev/null "$url" ; done
