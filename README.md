# Static Site Generator

This is a [Boot.dev guided project](https://www.boot.dev/courses/build-static-site-generator-python).
It converts Markdown files in `content/` into HTML pages in `docs/` using `template.html` and copies assets from `static/`.

## How it works
- `src/main.py` reads an optional base path from CLI args.
- Static files are copied from `static/` to `docs/`.
- Markdown files are recursively converted and written to matching paths in `docs/`.

## Running it
Build pages with the deployment base path:
```bash
./build.sh
```

Run directly (default base path `/`):
```bash
python3 src/main.py
```

Serve locally:
```bash
./main.sh
```

## Project layout
- `src/` parser and generator code
- `content/` Markdown source content
- `template.html` HTML template
- `static/` static assets (CSS/images)
- `docs/` generated output
- `public/` locally served generated output
