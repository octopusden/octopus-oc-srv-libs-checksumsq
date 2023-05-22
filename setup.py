from setuptools import setup

included_packages = ['oc_checksumsq']
__version = "10.2.1"

spec = {
        "name": 'oc-checksumsq',
        "version": __version,
        "description": "Client for CDT checksums queue",
        "long_description": "",
        "long_description_content_type": "text/plain",
        "install_requires": [
            "oc-cdt-queue2 >= 4.0.3",
            "requests"],
        "packages": included_packages,
        "scripts":["chkreg.py"],
        #"python_requires": ">= 3.6"
}

setup(**spec)
