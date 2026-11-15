# Contributing to Trikeel

Thanks for helping. Trikeel stays useful by staying small.

## Principles

- **Keep the template lean.** Every line in `SUPERVISOR.md` and `STUDY.md` costs tokens in every session. Add a line only if it changes behaviour.
- **No fabricated numbers.** Claims about token or time savings need a method and data. See [`docs/measure-it.md`](docs/measure-it.md).
- **No secrets, ever.** Examples use placeholders only.

## Good contributions

- Worked examples of a full triad for a different kind of project
- Improvements to the gates or stop rules, with the failure they prevent
- Checker improvements (new secret shapes, clearer messages)
- Measured results from your own runs (open an issue with your log)

## Workflow

1. Fork and branch.
2. Run the checker on anything you touch:
   ```bash
   python3 scripts/trikeel_check.py template --strict
   python3 scripts/trikeel_check.py examples/invoice-reminder --strict
   ```
3. Open a PR describing the problem the change solves.

By contributing you agree that your work is released under the [MIT License](LICENSE).
