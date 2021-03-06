from setuptools import setup, find_packages

version = '1.0.0.dev0'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing',
    'plone.app.testing',
    'plone.testing',
]

extras_require = {
    'tests': tests_require,
}


setup(
    name='nachtalb.useful_tools',
    version=version,
    description='nachtalb.useful_tools',
    long_description=open('README.rst').read(),

    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='nachtalb useful_tools',
    author='Nachtalb',
    author_email='mailto:info@nachtalb.ch',
    url='https://github.com/Nachtalb/nachtalb.useful_tools',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['nachtalb'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Plone',
        'plone.api',
        'plone.app.redirector',
        'plone.app.debugtoolbar',
        'setuptools',
        'ftw.upgrade',
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
