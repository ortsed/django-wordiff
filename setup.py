#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()
        # Upgrade().run(dist=True)
        # test.run(self, *args, **kwargs)

setup(
    name="django-wordiff",
    version="1",
    author="Llewellyn Hinkes",
    author_email="ortsed@gmail.com",
    url="http://github.com/ortsed/django-wordiff",
    description = "N-gram parsing and comparison app",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
#        "",
    ],
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)