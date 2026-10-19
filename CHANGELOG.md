# Changelog

All notable changes to Perlite are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-19

### Added

- First public release.
- `/perlite:init`: creates the vault structure, the `PERLITE.md` rules file and the
  core pages; never overwrites existing files.
- `/perlite:ingest`: turns inbox files, pasted text or approved URLs into linked,
  source-cited notes and archives the originals in `.raw/`.
- `/perlite:query`: read-only answers grounded in the vault, citing notes.
- `/perlite:save`: saves selected conversation content as a note.
- `/perlite:lint`: read-only health check with an optional standard-library Python
  checker.
- Vault discovery through a path in the request, the `PERLITE_VAULT` environment
  variable, or the nearest folder containing `PERLITE.md`.
