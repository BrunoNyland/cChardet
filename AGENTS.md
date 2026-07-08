# AGENTS.md

Compact guidance for OpenCode sessions working in this repo.

## Project

cChardet is a Python binding to the C++ [uchardet](https://github.com/PyYoshi/uchardet) charset detector, built via Cython. The package lives in `src/cchardet/`; the uchardet C++ sources are a git submodule at `src/ext/uchardet/` (vendored, not on PyPI).

## First-time setup

- `git submodule update --init --recursive` -- **required**. The build compiles C++ from `src/ext/uchardet/`, and the test suite globs `src/ext/uchardet/test/*/*.txt` for fixtures. Without the submodule, both build and tests fail.
- `pip install -r requirements-dev.txt` -- cython, pytest, ruff, setuptools, chardet (used by `bench.py`).

## Build / test commands

The extension must be cythonized to C++ before it can be compiled. The flow is: **cythonize -> build_ext -> test**.

- `make cython` -- `cython --cplus src/cchardet/_cchardet.pyx` -> generates `src/cchardet/_cchardet.cpp`.
- `python setup.py build_ext -i -f` -- compiles the Cython-generated C++ plus the uchardet sources listed in `setup.py` into `_cchardet*.so` in place.
- `make test` -- runs `clean -> cython -> build_ext -> pytest tests`. Note: `make clean` deletes `src/cchardet/*.cpp`, so after any `make clean` you must re-cythonize before building.
- `pytest tests` -- run the suite after building.
- `pytest tests/test_1.py::TestCChardet::test_ascii` -- single test.
- `make bench` -- `clean -> cython -> build_ext -> python tests/bench.py` (compares throughput vs `chardet`).

## Lint / format

- `ruff check` / `ruff format`. Config in `pyproject.toml`: line length 100, target py39, double quotes, selects `E,F,I,N`.
- `src/ext` (the submodule) is excluded from ruff -- do not lint or reformat it.

There is no typecheck step configured.

## Architecture notes

- `src/cchardet/_cchardet.pyx` is the Cython source; it `cdef extern`s uchardet's C API and exposes `detect_with_confidence()` and the `UniversalDetector` cdef class.
- `src/cchardet/__init__.py` wraps those into the public `detect(msg)` function and a Python `UniversalDetector` proxy class. **Encoding-name quirk:** `MAC-CENTRALEUROPE` is remapped to `maccentraleurope` here; tests rely on this.
- `src/cchardet/cli/cchardetect.py` is the `cchardetect` console script (also `python -m cchardet`). It streams files in chunks through `UniversalDetector`.
- `setup.py` explicitly enumerates every uchardet `.cpp` source (LangModels + core). When updating the uchardet submodule, check whether new language-model files need to be added there.

## Test gotchas

- Test fixtures come from the **submodule** (`src/ext/uchardet/test/<lang>/<encoding>.txt`), not `tests/samples/`. `tests/samples/` only holds a few hand-picked files (e.g. the SJIS Wikipedia sample used by `test_detector` and `bench.py`).
- `tests/test_1.py` has `SKIP_LIST_DETECT` / `SKIP_LIST_DEC` for encodings known to misdetect (gb18030, ja/utf-16le/be, es/iso-8859-15, da/iso-8859-1, he/iso-8859-8, plus a few Python-undecodable ones). These skips are intentional -- don't remove them without investigating the underlying detection.
- Expected encoding is derived from each fixture's filename (e.g. `ja/shift_jis.txt` -> `shift_jis`) and compared case-insensitively.

## CI / release

- `.github/workflows/test.yml`: matrix over Python 3.13-3.14 on ubuntu/windows/macos. Flow: checkout with `submodules: recursive` -> install dev reqs -> `make cython` -> `pip install .` -> `ruff check` -> `pytest -vs tests`.
- `.github/workflows/release.yaml`: on every push to master, auto-bumps the alpha version (`tools/bump_version.py`), commits + tags `v<X.Y.ZaN>` (with `[skip ci]` to avoid loop), builds wheels via cibuildwheel v4.1.0 across ubuntu/windows/macos, and publishes a GitHub Release with all wheel artifacts. Also triggers on manual dispatch.
- **Wheel builds do not run tests** -- the cibuildwheel `test-command` is intentionally disabled (see comment in `pyproject.toml`) because some detection cases fail inside the cibuildwheel environment. Don't re-enable without fixing those cases.
- cibuildwheel v4.1.0 builds CPython 3.14 (and free-threaded `cp314t`) by default; uchardet free-threading safety is not audited.
- Supported Python: `>=3.13`-`3.14` (3.14 included in CI; `allow-prereleases` retained for future 3.15-dev).
- C++ standard: the extension compiles with `-std=c++14` (set in `setup.py` `extra_compile_args`). Don't downgrade to c++11 -- cChardet requires c++14 features.
- Version source: `src/cchardet/__init__.py` defines both `version` (tuple) and `__version__` (string). `pyproject.toml` reads `cchardet.__version__` dynamically. `tools/bump_version.py` increments the alpha segment and updates both.
