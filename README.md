# EnvGuard

**Catch missing, mistyped, and empty environment variables before they break your app.**

---

## The problem

You've been there.

App crashes on deploy because someone forgot to add a new env var.  
`.env.example` is three months out of date.  
A typo in a key name goes unnoticed until production.  
A required value is blank because no one documented it.

EnvGuard catches all of this before it reaches your users.

---

## What it does

- **Missing variables** — finds keys in `.env.example` that are absent from `.env`
- **Undocumented variables** — flags keys in `.env` that aren't in `.env.example`
- **Empty values** — catches blank required variables
- **Typo detection** — spots `STRPE_SECRET_KEY` and asks if you meant `STRIPE_SECRET_KEY?`
- **CI-ready** — exits with code `1` on any issue, works in any pipeline

---

## Scope in v0.1

EnvGuard v0.1 focuses on the most common `.env` mistakes:

- missing variables
- undocumented variables
- empty values
- likely typos

Schema validation and codebase scanning are planned for later versions.

---

## Install

```bash
pip install envguard
```

---

## Usage

```bash
envguard check
```

Defaults to `.env` and `.env.example` in the current directory.

Custom paths:

```bash
envguard check --env .env.production --example .env.example
```

---

## Example output

```
Missing in .env (defined in .env.example but not in .env)
  - NODE_ENV
  - STRIPE_SECRET_KEY

Undocumented variables (in .env but missing from .env.example)
  - FEATURE_FLAG_NEW_UI
  - STRPE_SECRET_KEY

Empty values
  - REDIS_URL=

Possible typos
  - STRPE_SECRET_KEY  →  did you mean STRIPE_SECRET_KEY?

✗ 4 issue(s) found.
```

---

## Use in CI (GitHub Actions)

```yaml
- name: Validate environment
  run: |
    pip install envguard
    envguard check --env .env.ci --example .env.example
```

If any issues are found, the step fails and the deploy stops.

---

## Roadmap

**v0.2 — Schema validation**
- Type checks: `int`, `bool`, `url`, `email`, `enum`
- Config file (`envguard.yml`)

**v0.3 — Codebase scan**
- Detect env vars used in code but missing from `.env.example`
- Detect vars documented but never actually used

**Pro**
- GitHub Action with inline PR annotations
- Framework presets (Next.js, Django, Rails, Laravel)
- Auto-fix suggestions
- Ignore rules and config profiles

---

## License

MIT
