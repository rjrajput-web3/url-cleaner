# url-cleaner

Strip tracking parameters from URLs, from the terminal. Paste a link full
of `utm_source`, `fbclid`, or `gclid` junk and get back the clean link —
everything else (path, useful parameters, fragment) stays untouched.

Stdlib only. Nothing leaves your machine.

## What it removes

Any `utm_*` parameter, plus: `fbclid`, `gclid`, `gbraid`, `wbraid`,
`msclkid`, `mc_cid`, `mc_eid`, `igshid`, `twclid`, `srsltid`, `vero_id`,
`_ga`, `_gl`, `dclid`, `yclid`, `scid`.

## Usage

```sh
python3 url_cleaner.py "https://example.com/post?utm_source=newsletter&utm_medium=email&ref=home&fbclid=abc123"
# https://example.com/post?ref=home

python3 url_cleaner.py "https://example.com/page?gclid=xyz&gbraid=pqr"
# https://example.com/page
```

No arguments? It reads one URL per line from stdin:

```sh
echo "https://example.com/a?utm_campaign=x&keep=1" | python3 url_cleaner.py --show-removed
# https://example.com/a?keep=1
```

## Options

- `--keep utm_source,fbclid` — keep listed parameters even if they look
  like trackers. Example:

  ```sh
  python3 url_cleaner.py --keep utm_source "https://example.com/post?utm_source=newsletter&utm_medium=email"
  # https://example.com/post?utm_source=newsletter
  ```

- `--show-removed` — print the removed parameter names to stderr.

## Exit codes

- `0` — all URLs cleaned.
- `1` — at least one input was not a valid http(s) URL (the rest still
  cleaned; the bad line is reported on stderr).
- `2` — no URLs given.

## Example output

```sh
python3 url_cleaner.py "https://example.com/clean?ref=home#section"
# https://example.com/clean?ref=home#section
```

Untracked links pass through unchanged, fragment included.
