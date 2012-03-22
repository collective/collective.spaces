.. contents::

Introduction
============

.. image:: docs/spaces-logo.png
   :align: right

`collective.spaces` is a simple way of creating mini-sites within the Plone
CMS, with each mini-site based on a fully-customisable template.  
This product deploys a light-weight Dexterity-based content type
(called a ``Space``) within Plone and provides various additions that would
be useful in a self-managed, collaborative environment.  For instance:

* Ability for users to self-create Spaces
* Each Space appears as a subsite
* Customisable logo per-Space
* Ability for site administration to custom Space template

What this offers
================

* Simple Dexterity-based content type
* Web-based forms built using ``plone.app.z3cform`` and friends
* Leverages existing Plone tech (such as authentication, INavigationRoot and
  Dexterity behaviours)
* Attempts to use as little voodoo as possible to achieve just the features
  on offer.
* Other options like ``collective.lineage`` provide unnecessary features 
  and introduce undesireable depenedencies

Use Case (aka when-to-use-this)
===============================

#. Desire to allow various groups of users to collaborate but without
   administrative overhead/intervention
#. Users should be able to create new sub-sites at the Plone root, without
   the need for administrative intervention
#. Each workspace should be able to be self-managed
#. Each workspace can be allowed limited customisation
#. Workspaces should be all contained within a single Plone site

Installation
============

``collective.spaces`` is compatible with recent version of Plone and is 
tested with Plone 4.2 and Dexterity 1.2.1.  Add this egg to your Plone
instance in your buildout like so -- it's highly recommended that
you utilise a Known Good Set (KGS) for pinning versions of the form
libraries and Dexterity::

    [buildout]
    extends =
        ...
        http://good-py.appspot.com/release/dexterity/1.2.1?plone=4.2b2

    ...
    
    [instance]
    ...
    eggs =
        collective.spaces

ZCML registration is not necessary as this egg includes a 
``z3c.autoinclude`` entry point.

Suggestions
===========

* *Authentication*: enable user self-registration on Plone or enable
  another authentication mechanism to reduce administrative input needed
  (or both). Intertwining mechanisms like local authentication, LDAP, or 
  Shibboleth, can easily mean that users can self-manage collaboration with 
  local and external users.

* *Navigation*: if users are expected to be creating many Spaces, then the
  Plone portal tabs will quickly consume lots of space. To combat this, simply
  either turn off the ``Automatically generate tabs`` option in the ``Navigation
  settings`` control panel, or else de-select the ``Space`` content type from 
  the ``Displayed content types`` option. If using this latter strategy, then
  consider how users will actually access their Space - hiding from navigation
  entirely likely means users need directly access their URL.

* *Email notification*: A common situation may be where a site administrator
  wants to keep track of the Spaces being created. A Plone Content Rule is
  provided with this add-on to satisfy this use case.  Using this Rule is 
  completely optional -- it is installed but not enabled by default.

Collaboration
=============

Source code is available within the ``collective Github`` at 
`https://github.com/collective/collective.spaces`_ for submission of issues, 
fixes, and improvements.

To Do
=====

* Check scaling options for custom logo viewlet
* Handle issues with displaying ID field 
* More testing infrastructure for functionality

  * Check user 'Edit' permissions for the Space

* Complete email notification content rule

