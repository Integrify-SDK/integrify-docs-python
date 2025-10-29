# Integrify

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify is library for easing API integrations</em>
</p>
<p  style='display:flex;flex-wrap:wrap;gap:5px;width:70%;justify-content:flex-start;margin: 0 auto;'>
<a href="https://github.com/mmzeynalli/integrify/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/mmzeynalli/integrify/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/mmzeynalli/integrify/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/mmzeynalli/integrify/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
<a href="https://pepy.tech/project/integrify" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/mmzeynalli/integrify" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/mmzeynalli/integrify.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)

**Kod**: [https://github.com/orgs/Integrify-SDK/repositories](https://github.com/orgs/Integrify-SDK/repositories)

---

## Main features { #main-features }

- Library supports both sync and async request/response exchange.
- All class, function and variables are documented.
- Type hinting for code editors are active, as all class, function and variables are typed.
- The flow logic of most of the requests are explained.

---

## Installation { #installation }

<div class="termy">

```console
$ # pip install integrify-integration
$ pip install integrify-clopos
---> 100%
```

</div>

## Usage { #usage }

For example, to use Clopos requests:

### Sync

```python
from integrify.clopos import CloposRequest

resp = CloposRequest.get_users(headers={'x-token': 'token'})
print(resp.ok, resp.body)

```

### Async

```python
from integrify.clopos import CloposAsyncRequest

# Async main loop artıq başlamışdır
resp = await CloposAsyncRequest.get_users(headers={'x-token': 'token'})
print(resp.ok, resp.body)

```

### Request response { #request-response }

Response type to any request is `ApiResponse` class:

```python
class ApiResponse:
    ok: bool
    """If status code is less than 400"""

    status_code: int
    """Response status code"""

    headers: dict
    """Response headers"""

    body: Varies
    """Response body"""
```

## List of supported API integrations { #supported-integrations }

???+ warning
    Even though all requests are written based on official documentations, Integrify in unofficial library.

| Service         |                                                 Main requests                                                 |                                                 All requests                                                  | Documentation                                                                                                 | Tested in prod environment                                                                                    | Main developer                                    |
| --------------- | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| EPoint          |                                                       ✅                                                       | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Full](https://integrify.mmzeynalli.dev/integrations/epoint/about/)                                           | ✅                                                                                                             | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| KapitalBank     |                                                       ✅                                                       |                                                       ✅                                                       | [Full](https://integrify.mmzeynalli.dev/integrations/kapital/about/)                                          | ✅                                                                                                             | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| LSIM            |                                                       ✅                                                       |                                                       ✅                                                       | [Full](https://integrify.mmzeynalli.dev/integrations/lsim/about/)                                             | ✅                                                                                                             | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| Posta Guvercini |                                                       ✅                                                       |                                                       ✅                                                       | [Full](https://integrify.mmzeynalli.dev/integrations/posta-guvercini/about/)                                  | ✅                                                                                                             | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| Azericard       |                                                       ✅                                                       | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Full](https://integrify.mmzeynalli.dev/integrations/azericard/about)                                         | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| Clopos          |                                                       ✅                                                       |                                                       ✅                                                       | [Full](https://integrify.mmzeynalli.dev/integrations/clopos/about)                                            | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| Payriff         | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Vahid Həsənzadə](https://github.com/vahidzhe)    |
