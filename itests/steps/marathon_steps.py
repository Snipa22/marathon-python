import sys
import time

import marathon
from behave import given, when, then
import mock

from itest_utils import get_marathon_connection_string
sys.path.append('../')


@given('a working marathon instance')
def working_marathon(context):
    """Adds a working marathon client as context.client for the purposes of
    interacting with it in the test."""
    if not hasattr(context, 'client'):
        marathon_connection_string = "http://%s" % \
            get_marathon_connection_string()
        context.client = marathon.MarathonClient(marathon_connection_string)


@then(u'we get the marathon instance\'s info')
def get_marathon_info(context):
    assert context.client.get_info()


@when(u'we create a trivial new app')
def create_trivial_new_app(context):
    context.client.create_app('test-trivial-app', marathon.MarathonApp(cmd='sleep 100', mem=16, cpus=1))


@when(u'we create a complex new app')
def create_complex_new_app_with_unicode(context):
    app_config = {
        'container': {
            'type': 'DOCKER',
            'docker': {
                'portMappings': [{'protocol': 'tcp', 'containerPort': 8888, 'hostPort': 0}],
                'image': u'localhost/fake_docker_url',
                'network': 'BRIDGE',
            },
            'volumes': [{'hostPath': u'/etc/stuff', 'containerPath': u'/etc/stuff', 'mode': 'RO'}],
        },
        'instances': 1,
        'mem': 30,
        'args': [],
        'backoff_factor': 2,
        'cpus': 0.25,
        'uris': ['file:///root/.dockercfg'],
        'backoff_seconds': 1,
        'constraints': None,
        'cmd': u'/bin/true',
        'health_checks': [
            {
                'protocol': 'HTTP',
                'path': '/health',
                'gracePeriodSeconds': 3,
                'intervalSeconds': 10,
                'portIndex': 0,
                'timeoutSeconds': 10,
                'maxConsecutiveFailures': 3
            },
        ],
    }
    context.client.create_app('test-complex-app', marathon.MarathonApp(**app_config))


@then(u'we should see the {which} app running via the marathon api')
def see_complext_app_running(context, which):
    print(context.client.list_apps())
    assert context.client.get_app('test-%s-app' % which)
