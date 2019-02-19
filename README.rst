.. contents:: Table of Contents


Introduction
============

Some useful Tools for CMFPlone

The tools provided by this package are not meant to be perfect or anything like it. Every time I am too lazy to do
something manually and it could be automated, a new function for this package will be created. ATM I will no be
versioning this package, but maybe I will one day... probably (that's why I didn't remove the ``docs/HISTORY.txt``).

If you find any bugs or want to have your idea for a tool added, make an Issue or even better a Pull Request.


Usage
-----

The views in this package are all according to this schema:  ``useful-tools/TOOLBOX_NAME/FUNCTION``

- **useful-tools**: prefix for all views
- **TOOLBOX_NAME**: name for the "group", eg. for ``ftw.simplelayout`` tools it's ``sl``, for ``ftw.trash`` it's ``trash``
- **FUNCTION**: name of the function, eg. ``synchronize`` as in ``useful-tools/sl/synchronize``.

If you don't know what a view does, just go look in the code. There is always a small docstring for each function
(mainly because Plone wants it that way, otherwise the functions defined by ``allowed_interface`` are `ignored <https://github.com/zopefoundation/Zope/blob/827018bd3ee1f1587fef2baccc45b3cd99e17a17/src/Products/Five/browser/metaconfigure.py#L152>`_)


Views
+++++

::

    useful-tools/
        sl/ (ftw.simplelayou)
            synchronize/ => Run synchronize page configuration on all sl sub pages starting with the current path
            show_objects/ => Show all sl objects filtered by current path
                ?blocks=1/0 => Show sl blocks or not
                ?pages=1/0 => Show sl pages or not

        trash/ (ftw.trash)
            clear_trash/ => Clean the trash
            cleanup/ => Clean the trash and then run collective.solr cleanup

        misc/ (miscellaneous)
            page_counter/ => Count objects of a site with multi language support
                ?old=1 => Search for main types typically used on older plone sites using old simplelayout.baes
                ?pathfilter=1 => Limit search to current path
                ?clear=1 => Clear the default type list
                ?types=foo,-bar => Add / Remove (prepend -) types from being searched, parsed from left to right stronger than ?clear
            page_counter_json/ => The same as `page_counter` but as JSON

        misc-anon/ (miscellaneous anonymous)
            pdb/ => Start pdb at for current context


- For boolean get parameters like ``?pathfilter`` these values can be used (case insensitive):
  ::

      yes / enable / activate / on / true / 1
      no / disable / deactivate / off / false / 0

- List parameters like ``?types`` are usually separated by a comma


Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        nachtalb.useful_tools


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/Nachtalb/nachtalb.useful_tools
- Issues: https://github.com/Nachtalb/nachtalb.useful_tools/issues

Package / Code template used for this project:

- bobtemplates.4teamwork: https://github.com/4teamwork/bobtemplates.4teamwork

Copyright
=========

This package is copyrighted by `Nachtalb <https://github.com/Nachtalb/>`_.

``nachtalb.useful_tools`` is licensed under GNU General Public License, version 2.
