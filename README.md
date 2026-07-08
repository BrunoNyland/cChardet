# cChardet

[![PyPI version](https://badge.fury.io/py/cchardet.svg)](https://badge.fury.io/py/cchardet)
[![Tests](https://github.com/BrunoNyland/cChardet/actions/workflows/test.yml/badge.svg)](https://github.com/BrunoNyland/cChardet/actions/workflows/test.yml)
[![Release](https://github.com/BrunoNyland/cChardet/actions/workflows/release.yaml/badge.svg)](https://github.com/BrunoNyland/cChardet/actions/workflows/release.yaml)
[![Python](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MPL%2FGPL%2FLGPL-orange.svg)](COPYING)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-green.svg)](https://github.com/BrunoNyland/cChardet/releases)

High-speed universal character encoding detector -- a Python binding to [uchardet](https://github.com/PyYoshi/uchardet), built with [Cython](https://cython.org/).

A C++-powered drop-in alternative to [chardet](https://github.com/chardet/chardet), offering **~2000x** faster detection.

> **Note:** This is a maintained fork of [PyYoshi/cChardet](https://github.com/PyYoshi/cChardet), updated for Python 3.13-3.14 with C++14 and automated releases.

## Install

From PyPI:

```bash
pip install cchardet
```

From the latest GitHub release -- download the `.whl` matching your Python version and platform from [Releases](https://github.com/BrunoNyland/cChardet/releases/latest), then:

```bash
pip install cchardet-*.whl
```

Or with the GitHub CLI:

```bash
gh release download --repo BrunoNyland/cChardet --pattern "*cp313*manylinux*x86_64*.whl"
pip install cchardet-*.whl
```

Pre-built wheels are available for Python 3.13-3.14 (including free-threaded 3.14t) on Linux, macOS, and Windows.

## Usage

```python
import cchardet as chardet

with open("example.txt", "rb") as f:
    result = chardet.detect(f.read())
    print(result)
    # {'encoding': 'SHIFT_JIS', 'confidence': 0.99}
```

Streaming detection via `UniversalDetector`:

```python
from cchardet import UniversalDetector

detector = UniversalDetector()
with open("example.txt", "rb") as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
detector.close()
print(detector.result)
```

Command-line tool:

```bash
cchardetect example.txt
# example.txt: SHIFT_JIS with confidence 0.99
```

## Benchmark

| Detector            | Calls/s |
|---------------------|---------|
| chardet v5.2.0      | ~1      |
| cchardet v2.2.0a6   | ~2200   |

Run your own:

```bash
pip install -r requirements-dev.txt
make test
make bench
```

## How it works

- **[uchardet](https://github.com/PyYoshi/uchardet)** -- C++ charset detector (Mozilla-derived), the encoding engine.
- **cChardet** -- Cython binding that exposes `detect()` and `UniversalDetector` to Python.
- **[chardet](https://github.com/chardet/chardet)** -- pure-Python detector used as the benchmark baseline; cChardet is API-compatible as a drop-in replacement.

## Supported encodings

UTF-8, UTF-16BE/LE, UTF-32BE/LE, ISO-8859-1 through -16, WINDOWS-1250 through -1257, BIG5, EUC-JP/ KR/ TW, GB18030, HZ-GB-2312, ISO-2022-JP/ KR/ CN, SHIFT_JIS, KOI8-R, and more -- covering 30+ languages.

## License

See [COPYING](COPYING). MPL 1.1 / GPL / LGPL (dual-licensed via uchardet).

## Links

- [Releases](https://github.com/BrunoNyland/cChardet/releases)
- [Issues](https://github.com/BrunoNyland/cChardet/issues)
- [Original repo (PyYoshi/cChardet)](https://github.com/PyYoshi/cChardet)
- [uchardet (C++ engine)](https://github.com/PyYoshi/uchardet)
- [chardet (pure-Python)](https://github.com/chardet/chardet)
