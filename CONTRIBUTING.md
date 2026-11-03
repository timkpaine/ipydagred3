# Contributing

If you want to contribute to this repository here are some helpful guidelines.

## Reporting bugs, feature requests, etc.

To report bugs, request new features or similar, please open an issue on the Github
repository.

A good bug report includes:

- Expected behavior
- Actual behavior
- Steps to reproduce (preferably as minimal as possible)
- Possibly any output from the browser console (typically available via Ctrl + Shift + J or via F12).

## Minor changes, typos etc.

Minor changes can be contributed by navigating to the relevant files on the Github repository,
and clicking the "edit file" icon. By following the instructions on the page you should be able to
create a pull-request proposing your changes. A repository maintainer will then review your changes,
and either merge them, propose some modifications to your changes, or reject them (with a reason for
the rejection).

## Setting up a development environment

If you want to help resolve an issue by making some changes that are larger than that covered by the above paragraph, it is recommended that you:

- Fork the repository on Github

- Clone your fork to your computer

- Run the following commands inside the cloned repository:

  - `pip install -e '.[develop]'` - This will install the Python package in development
    mode.

- Validate the install by running the tests:

  - `make test` - Run the Python tests.
  - `make lint` - Run Python and documentation checks.
  - `make build` and `make checks` - Build and validate Python distributions.

Once you have such a development setup, you should:

- Make the changes you consider necessary
- Run the tests to ensure that your changes does not break anything
- If you add new code, preferably write one or more tests for checking that your code works as expected.
- Commit your changes and publish the branch to your github repo.
- Open a pull-request (PR) back to the main repo on Github.

## Updating project scaffolding

The `.copier-answers.yaml` file records the Python template variant, project answers, and template
revision. From a clean checkout, update the scaffold with:

```bash
uv tool run copier update --answers-file=.copier-answers.yaml --defaults --vcs-ref=HEAD
```

Review the generated diff and run `make lint`, `make test`, `make build`, and `make checks`.
Project-specific dependencies, version configuration, and widget code are retained as customizations.

Recurring update pull requests use the
[Python Templates Copier Update GitHub App](https://github.com/apps/python-templates-copier-update).
The App needs access to this repository; no repository-local Copier workflow is required.
