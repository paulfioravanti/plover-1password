# Plover 1Password

[![Build Status][Build Status image]][Build Status url] [![PyPI - Version][PyPI version image]][PyPI url] [![PyPI - Downloads][PyPI downloads image]][PyPI url] [![linting: pylint][linting image]][linting url]

This [Plover][] [extension][] [plugin][] contains a [meta][] that allows you to
retrieve secrets defined in your [1Password][] vaults.

## Install

### Pre-Plover Plugin Registry inclusion (Current)

```console
git clone git@github.com:paulfioravanti/plover-1password.git
cd plover-1password
plover --script plover_plugins install --editable .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

Then:

1. When it finishes installing, restart Plover
2. Complete the [Setup][] steps
3. Open the Plover Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
4. Open the Plugins tab
5. Check the box next to `plover_1password` to activate the plugin

### Post-Plover Plugin Registry inclusion (Future)

1. In the Plover application, open the Plugins Manager (either click the Plugins
   Manager icon, or from the `Tools` menu, select `Plugins Manager`).
2. From the list of plugins, find `plover-1password`
3. Click "Install/Update"
4. When it finishes installing, restart Plover
5. Complete the [Setup][] steps
6. After re-opening Plover, open the Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
7. Open the Plugins tab
8. Check the box next to `plover_1password` to activate the plugin

## Setup

Setting up 1Password to allow this plugin to make connections is a bit of an
involved process, but you will only have to do it once.

### Create a new Vault

Since 1Password does not allow third-party applications to access your Private
or Personal vaults, you will need to put secrets you intend to access from
Plover into a separate vault. Therefore, either [create a new vault][]
specifically for Plover to access, or use another existing non-Private/Personal
vault you have.

Individual secrets cannot be shared across vaults, so if you have information in
your Personal vault you want Plover to access, you will need to [move or copy
items][] from your Personal vault to the vault that Plover will access.

### Create a Service Account Token

Follow the steps to [create a Service Account][], which will enable Plover to
talk to 1Password.

This plugin only needs to retrieve secrets from 1Password, so when you get to
the "Grant vault access" section of the Service Account creation process, after
choosing the vault that Plover will access, set its access permissions to
"Read Items" only.

Once the Service Account Token has been generated (and you save it to one of
your vaults), you will need to copy the token into a local [environment
variable][] called `$OP_SERVICE_ACCOUNT_TOKEN`, as per the requirements of the
[1Password Python SDK][], which this plugin uses to connect with 1Password:

**macOS or Linux**

```bash
export OP_SERVICE_ACCOUNT_TOKEN=<your-service-account-token>
```

**Windows**

```powershell
$Env:OP_SERVICE_ACCOUNT_TOKEN = "<your-service-account-token>"
```

### Manually install 1Password Python SDK

The [1Password Python SDK][] is not currently available on [PyPI][], which means
you will need to install it manually directly via URL with the following
Python [pip][] command in order for the plugin to work properly:

```console
pip install git+ssh://git@github.com/1Password/onepassword-sdk-python.git@v0.1.1
```

Unfortunately, PyPi does not allow [direct URL dependencies][] in projects, so
in order to get this plugin on to PyPI, the SDK could not be listed as an
`install_requires` library (eg
`onepassword @ git+ssh://git@github.com/1Password/onepassword-sdk-python.git@v0.1.1`,
meaning a manual installation process instead of the plugin automatically doing
it for you.

### Install 1Password CLI and turn on desktop app integration

Follow all the steps to [Get started with 1Password CLI][] to install the
[1Password Command-line tool][], and turn on its [1Password app integration][].

Once you have completed this step, a new [Copy Secret Reference][] option will
become available to you in the `v` dropdown menu, next to the Copy button, at
the end of each field in your document item. It is these [secret references][],
which can be thought of as references or pointers to where a secret is saved,
rather than the value of the secret itself, that will be used directly in steno
outline translations. They have the following format:

```txt
op://<vault-name>/<item-name>/[section-name/]<field-name>
```

> [!NOTE]
> Secret references adhere to the following set of [syntax rules][]:
> 
> - alphanumeric characters (`a-z`, `A-Z`, `0-9`)
> - `-`, `_`, `.` and the whitespace character
>
> Therefore, make sure your vault, item, section, and field names adhere to
> these rules and do not contain any other types of characters.

## How To Use

In your steno outline translations, use the [secret references][] provided by
1Password to specify the secret you wish to retrieve.

For example, the following outline would retrieve the "Mobile" secret defined in
a "Plover" vault, within a "Personal" item, under a "Phone" section:

```json
"TPOEPB/TPOEPB": "{:1PASSWORD:op://Plover/Personal/Phone/Mobile}"
```

> [!NOTE]
> Service account tokens are subject to [rate limits][] by 1Password, but they
> should be more than enough for normal usage of this plugin.

## Development

Clone from GitHub with [git][]:

```console
git clone git@github.com:paulfioravanti/plover-1password.git
cd plover-1password
```

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### Testing

- [Pytest][] with [pytest-asyncio][] are used for testing in this plugin.
- [Coverage.py][] and [pytest-cov][] are used for test coverage, and to run
  coverage within Pytest
- [Pylint][] is used for code quality
- [Mypy][] is used for static type checking

Currently, the only parts able to be tested are ones that do not rely directly
on Plover.

Run tests, coverage, and linting with the following commands:

```console
pytest --cov --cov-report=term-missing
pylint plover_1password
mypy plover_1password
```

To get a HTML test coverage report:

```console
coverage run --module pytest
coverage html
open htmlcov/index.html
```

### Deploying Changes

After making any code changes, deploy the plugin into Plover with the following
command:

```console
plover --script plover_plugins install --editable .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

When necessary, the plugin can be uninstalled via the command line with the
following command:

```console
plover --script plover_plugins uninstall plover-1password
```

[1Password]: https://1password.com/
[1Password app integration]: https://developer.1password.com/docs/cli/app-integration/
[1Password Command-line tool]: https://1password.com/downloads/command-line/
[1Password Python SDK]: https://github.com/1Password/onepassword-sdk-python
[Build Status image]: https://github.com/paulfioravanti/plover-1password/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-1password/actions/workflows/ci.yml
[Copy Secret Reference]: https://developer.1password.com/docs/cli/secret-reference-syntax/#with-the-1password-desktop-app
[Coverage.py]: https://github.com/nedbat/coveragepy
[create a new vault]: https://support.1password.com/create-share-vaults/#create-a-vault
[create a Service Account]: https://developer.1password.com/docs/service-accounts/get-started/#create-a-service-account
[direct URL dependencies]: https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#direct-url-dependencies
[environment variable]: https://en.wikipedia.org/wiki/Environment_variable
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[Get started with 1Password CLI]: https://developer.1password.com/docs/cli/get-started/
[Git]: https://git-scm.com/
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
[meta]: https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
[move or copy items]: https://support.1password.com/move-copy-items/
[Mypy]: https://github.com/python/mypy
[pip]: https://pip.pypa.io/en/stable/
[PyPI]: https://pypi.org/
[PyPI downloads image]:https://img.shields.io/pypi/dm/plover-1password
[PyPI version image]: https://img.shields.io/pypi/v/plover-1password
[PyPI url]: https://pypi.org/project/plover-1password/
[Plover]: https://www.openstenoproject.org/
[Plover Plugins Registry]: https://github.com/openstenoproject/plover_plugins_registry
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[Pytest]: https://pytest.org/
[pytest-asyncio]: https://github.com/pytest-dev/pytest-asyncio
[pytest-cov]: https://github.com/pytest-dev/pytest-cov/
[rate limits]: https://developer.1password.com/docs/service-accounts/rate-limits/#hourly-limits
[secret reference]: https://developer.1password.com/docs/cli/secret-reference-syntax/
[secret references]: https://developer.1password.com/docs/cli/secret-reference-syntax/
[Setup]: ./#Setup
[syntax rules]: https://developer.1password.com/docs/cli/secret-reference-syntax/#syntax-rules
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
