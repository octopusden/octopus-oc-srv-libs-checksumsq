from setuptools import setup, find_packages
import os, sys

if sys.version_info.major == 3:
    from unittest import TestLoader, TestSuite;

from datetime import datetime;

def dynamic_version( str_version ):
    """
    Returns full version of a package
    :param str_version: string, package version to append
    :return: str_version with appended build_id
    """

    str_vfile = 'version.txt';

    if not os.path.exists( str_vfile ):
        fl_out = open( str_vfile, 'w' );
        fl_out.write( datetime.strftime( datetime.now(), "%Y%m%d%H%M%S") );
        fl_out.close();

    fl_in = open( str_vfile );
    str_bid = fl_in.read().strip();
    fl_in.close();
    
    return '.'.join( [ str_version, str_bid ] );

included_packages=find_packages()


MAJOR=10
MINOR=2
RELEASE=0


setup(name='oc_checksumsq',
      version=dynamic_version( '.'.join( map( lambda x: str(x), [MAJOR, MINOR, RELEASE] ) ) ),
      description="Client for CDT checksums queue",
      long_description="",
      long_description_content_type="text/plain",
      install_requires=[
        "oc_cdt_queue2 >= 4.0.1",
        "requests",
      ],

      packages=included_packages,
      package_data={},

      scripts = [
                 "chkreg.py"
      ],

      #test_suite="setup.my_test_suite",
)
