from setuptools import setup, find_packages
from codecs import open
from os import path


__version__ = "0.1.24"

here = path.abspath(path.dirname(__file__))

long_description_for_pypi = """
# Spydy

spydy is a light-weight high-level web-crawling framework for fast-devlopment and high performance, which is inspired by unix pipeline.

---

[Code](https://github.com/superjcd/spydy)

[Document](https://superjcd.github.io/spydy/)

---

## Install

```
pip install spydy
```



## How to use

There are two ways of running spydy:

- one way is to prepare a configuration file, and run spydy from cmd:

```
spydy myconfig.cfg
```

`myconfig.cfg` may looks like below:

```
[Globals]
run_mode = async_forever
nworkers = 4

[PipeLine]
url = DummyUrls
request = AsyncHttpRequest
parser = DmozParser
log = MessageLog
store = CsvStore

[url]
url = https://dmoz-odp.org
repeat = 10

[store]
file_name = result.csv
```



- or run it from a python file(e.g. ` spider.py`):

```
from spydy.engine import Engine
from spydy.utils import check_configs
from spydy import urls, request, parsers, logs, store

myconfig = {
    "Globals":{
        "run_mode": "async_forever",
        "nworkers": "4"
    },
    "PipeLine":[urls.DummyUrls(url="https://dmoz-odp.org", repeat=10),
                request.AsyncHttpRequest(), parsers.DmozParser(), logs.MessageLog(), store.CsvStore(file_name=FILE_NAME)]
    }

check_configs(myconfig)
spider = Engine.from_dict(myconfig)
spider.run()
```

then run it :

```
$ python spider.py
```
"""

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

setup(
    name="spydy",
    version=__version__,
    description="light-weight high-level web-crawling framework",
    long_description=long_description_for_pypi,
    long_description_content_type="text/markdown",
    url="https://github.com/superjcd/spydy",
    download_url="https://github.com/superjcd/spydy/tarball/" + __version__,
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    keywords="",
    entry_points={
        "console_scripts": [
            "spydy=spydy.main:fire",
        ],
    },
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    author="Jiang Chaodi",
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email="929760274@qq.com",
)
