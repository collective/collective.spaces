.. contents::

Introduction
============

.. image:: docs/spaces-logo.png
   :align: right

`collective.spaces` is a simple way of creating mini-sites within the Plone
CMS.  This product deploys a light-weight custom Dexterity-based content type
(``Space``) within Plone and provides various additions that would be useful
in a self-managed, collaborative environment.  For instance:

* Ability for users to self-create Spaces
* Customisable logo per-Space
* Each Space appears as a subsite 

Why Spaces?
===========

* Simple Dexterity-based content type
* Attempts to use as little voodoo as possible
* Leverages existing Plone tech where possible (such as INavigationRoot and
  Dexterity behaviours)
* Because almost all of what ``collective.lineage`` offers isn't necessary
* Specific requirements for self-management
