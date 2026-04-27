# sysnet-auth

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/SYSNET-CZ/auth-lib)
![PyPI - Version](https://img.shields.io/pypi/v/sysnet-auth)
![Python Version](https://img.shields.io/pypi/pyversions/sysnet-auth)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?style=flat&logo=fastapi)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Tests](https://img.shields.io/badge/tests-passed-brightgreen.svg)

Sdilena autentizacni knihovna pro FastAPI mikrosluzby s Keycloak (OIDC/JWT).

## Installation

```bash
pip install sysnet-auth
```

## Features

- JWT validation using Keycloak public keys
- Async JWKS caching with stale-if-error support
- Automated authentication dependency for FastAPI
- Permission-based access control (scopes/roles)
