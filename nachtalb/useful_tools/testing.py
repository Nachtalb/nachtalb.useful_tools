from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class Useful_toolsLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'nachtalb.useful_tools')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nachtalb.useful_tools:default')


USEFUL_TOOLS_FIXTURE = Useful_toolsLayer()
USEFUL_TOOLS_FUNCTIONAL = FunctionalTesting(
    bases=(USEFUL_TOOLS_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="nachtalb.useful_tools:functional")
