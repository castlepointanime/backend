# AA-DR Backend

This project is WIP

See [AA-DR Portal README](https://github.com/castlepointanime/portal/blob/main/README.md) for setup instructions

## Developer Notes

### Folder Structure

`/controllers` API route definitions. This is where routes will be validated

`/database` Wrappers for MongoDB and Cognito DB calls.

`/managers` Perform the actual tasks done by Controllers. Managers assume that all route data has already been validated.

`/services` Wrappers for core features, like Docusign API, Google Docs API, Quickbooks, etc.

`/config` Global server environment and configuration settings

`/utilities` Miscellaneous small python modules

### Flasgger

[Flasgger](https://github.com/flasgger/flasgger) is a python module that allows for separate openapi files in multiple places. Flasgger can also can read these files and validate flask requests with the spec. This is added to make validation easier and to constantly keep the api documentation up to date.

To see the apidocs, view `http://localhost:3001/apidocs`

### Mypy/Flake8

[Mypy](https://github.com/python/mypy) is a static type checker for python. This is added to minimize bugs with dynamic typing and to improve readability.

[Flake8](https://flake8.pycqa.org/en/latest/) is a linter for python. It follows the PEP style guide for python.

To run both mypy and flake8, you can run these commands by entering into the container. This can be done like so:

```
docker exec -it $(docker ps -aqf "name=aa-dr-backend") /bin/sh
make check
```

MR's will not be accepted unless mypy and flake8 pass