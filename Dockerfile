ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}

WORKDIR /local/cdt_checksumsq
COPY . /local/cdt_checksumsq

RUN chgrp -R 0 /local/cdt_checksumsq && \
    chmod -R g=u /local/cdt_checksumsq

RUN \ 
 (python3 -m pip install --upgrade pip setuptools wheel || /bin/true) && \
 (python2 -m pip install --upgrade pip\<=19.2.3 setuptools\<=44.1.1 wheel\<=0.33.6 || /bin/true) && \
 python -m pip install --upgrade coverage && \
 python -m pip install  . && \
 python -m coverage run ./setup.py test && \
 mkdir -p /build/reports && \
 python -m coverage xml --include=./cdt_checksumsq/checksums_interface.py -o /build/reports/cdt_checksumsq_python-$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')_coverage.xml && \
 python ./setup.py bdist_wheel

