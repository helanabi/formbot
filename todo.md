- Handle post submission scenarios: show success message, redirect
- Add dry-run mode: `formbot leads.csv url --dry-run`,
Which: prints actions, does not click submit
- Add strict mode: skip on row length mismatch, error on unexpected values
and missing controls
- Add retry on failure
- Field mapping config, example: `formbot --config mapping.yaml`
- Add fs error handling
- Add user-selectable wait strategy: --wait networkidle|url-change|
selector:#success|fixed:2
- Handle multiple action matches
