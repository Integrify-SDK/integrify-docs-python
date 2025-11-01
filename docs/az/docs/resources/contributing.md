# Development - Contributing

İlk öncə (və ən rahat), proyekti ulduzlayaraq yardımçı ola bilərsiniz.

## Tərcümə { #translation }

Bəzi inteqrasiya dokumentasiyaları bir dildədir (ya ancaq Azərbaycanca, ya da ancaq ingiliscə). Həmin səhifələri tərcümə etməyə kömək etməklə yardım ola bilərsiniz. Mövcud dil qovluğunu (`docs/az` və ya `docs/en`) kopyalayıb, bütün markdown fayllarını tərcümə edərək editləmək bəs edir.

## Issue

Githubda yeni issue açaraq, yeni feature təklif edə, və ya mövcud bugları qeyd edə bilərsiniz.
Bug qeyd etdikdə, istifadə etdiyiniz əməliyyat sistemi və kitabxananın versiyasını qeyd etməyiniz tövsiyyə olunur.

## Development

İlk öncə nəzərə çatdırmaq lazımdır ki, Integrify əvvəlcə bir repoluq proyekt olsa da, sonradan dəyişdirilərək, hər inteqrasiya üçün bir repository-ə ayırdılmışdır. Beləliklə, bir inteqrasiyadakı dəyişikliklər başqalarına təsir etmir. Bununla bərabər, [python namespace package](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/) məntiqindən istifadə edilib.

Əgər mövcud inteqrasiyanın üzərində işləmək istəyirsinizsə, fork edib, üzərində işləyin. Bitirdikdən sonra isə, PR açın.

Əgər yeni inteqrasiya işləmək istəyirsinizsə, [integrify-docs](https://github.com/Integrify-SDK/integrify-docs-python/issues/new) reposunda issue açın. Sizin üçün repo yaradılacaq, və əvvəl qeyd edildiyi kimi, fork edib işə başlaya bilərsiniz.

Növbəti mərhələləri izləyərək öz kodunuzu əlavə edə bilərsiniz. Contribution sadə və sürətli olsun deyə test və linting-i lokal mühitinizdə icra etməyiniz məsləhət görülür. Integrify-ın başqa kitabxanalardan çox az asılılığı olduğundan quraşdırılma çox sadədir.

!!! tip

    **tl;dr:** Kodu format etmək üçün `make format`, test və lint etmək üçün `make test`/`make lint` və dokumentasiya generasiya etmək üçün `make docs` kommandını icra edin.

### Rekvizitlər { #requisites }

* Python 3.9 və 3.13 arası istənilən versiya
* git
* make
* [uv](https://github.com/astral-sh/uv)
* [pre-commit](https://pre-commit.com/)

### İnstallasiya və quraşdırılma  { #installation }

```bash
# Proyekti klonlayın və həmin qovluğa keçin
git clone git@github.com:<your username>/integrify-integration_name-python.git
cd integrify-integration_name-python

# uv yükləyin (https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
curl -LsSf https://astral.sh/uv/install.sh | sh
# For windows `powershell -c "irm https://astral.sh/uv/install.ps1 | more"`

# Mühiti quraşdırın
uv sync
make setup
```

### Yeni branch-a keçin və öz dəyişiklikləriniz əlavə edin  { #new-branch }

```bash
# Yeni branch-a keçid edin
git checkout -b my-new-feature-branch
# Öz dəyişikliklərini əlavə edin...
```

???+ warning

    Branch adını uyğun seçin:

    * Bug düzəldirsizsə, `bug/branch-name`
    * Yeni APIlər əlavə edirsizsə, `api/integration-name`
    * Kiçik fix-dirsə: `fix/branch-name`
    * Dokumentasiya üzərində işləyirsinizsə: `docs/branch-name`

### Test və Linting { #test-and-linting }

Kod dəyişiklikləriniz etdikdən sonra lokalda testləri və lintingi işə salın:

```bash
make format
# Integrify Rust-da yazılmış ruff Python linterini istifadə edir
# https://github.com/astral-sh/ruff

make all
# Bu kommand öz içində bir neçə başqa kommandı icra edir (`format`, `lint`, `type-check və `test`)
```

### Yeni dokumentasiyanı generasiya edin { #generate-docs }

Əgər dokumentasiyada (və ya funksiyalarda, klass definitionlarında və ya docstring-lərdə) dəyişiklik etmisinizsə, yeni dokumentasiya generasiya edin.
Dokumentasiya üçün `mkdocs-material` alətindən istifadə edirik.

```bash
# Dokumentasiya generasiya edin
make docs
# Əgər dokumentasiyaya təsir edəcək kod dəyişikliyi etmisinizsə,
# əmin olun ki, yeni dokumentasiya uğurlar generasiya olunur.

# make docs-serve kommandını icra etsəz, localhost:8000 addresində yeni dokumentasiyanı da görə bilərsiniz.
```

Nəzərə alın ki, dokumentasiya başqa repo tərəfindən icra olunur və həmin repo `docs/partial.yml` faylını oxuyub, öz `mkdocs.yml` faylına əlavə edir.

### Dəyişiklikləriniz commit və push edin  { #commit-push-and-pr }

Dəyişikliklərinizi bitirdək sonra, commit və öz branch-ınıza push edib, bizə pull request yaradın.

Pull request-iniz review üçün hazırdırsa, "Zəhmət olmazsa, review edin" comment-ini yazın, ən yaxın zamanda nəzər yetirəcəyik.

## Kod arxitekturası (!) { #code-architecture }

Bu hissə uzun və detallı yazılmalı olduğundan, məqalə [burada](./code-architecture.md) yerləşdirilib.

## Dokumentasiya { #documentation }

Dokumentasiya markdown-da yazılır və [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) aləti ilə generasiya olunur. API dokumentasiyası isə docstring-lərdən [mkdocstrings](https://mkdocstrings.github.io/) ilə generasiya olunur.

Ümumiyyətlə, dokumentasiya əlçatan üslubda yazılmalıdır. Oxunması və başa düşülməsi asan olmalı, qısa və konkret olmalıdır.

### Kodun dokumentləşdirilməsi { #incode-documentation-style }

Öz dəyişikliklərinizi əlavə edərkən, bütün kodun dokumentləşdirildiyindən əmin olun. Qeyd olunanlar format olunmuş docstring-lərlə yaxşıca dokumentləşdirilməlidir:

* Modullar
* Klass definition-ları
* Funksiya definition-ları
* Module səviyyəsində dəyişənlər

Integrify [PEP 257](https://www.python.org/dev/peps/pep-0257/) standartları ilə format olunmuş [Google-style docstring-lərdən](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) istifadə edir. (Əlavə məlumat üçün [Example Google Style Python Docstrings-ə](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) baxın.)

Docstring-lərdə misal (example) göstərə bilərsiniz. Bu misal tam işlənə bilən kod olmalıdır.
