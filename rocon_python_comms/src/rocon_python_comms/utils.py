#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_tools/license/LICENSE
##############################################################################
# Description
##############################################################################

"""
.. module:: utils
   :platform: Unix
   :synopsis: Utilities for working with python communications in ros.


Convenience utilities for ros 1.0 python communications.
----

"""

##############################################################################
# Imports
##############################################################################

import rocon_console.console as console
import rospy
import std_msgs.msg as std_msgs
from . import namespace

##############################################################################
# Mass Ros Communication Factories
##############################################################################


def publish_resolved_names(publisher, ros_communication_handles):
    """
    Worker that provides a string representation of all the resolved names
    and publishes it so we can use it as an introspection topic in runtime.
    """
    s = console.bold + "\nResolved Names\n\n" + console.reset
    for handle in ros_communication_handles:
        s += console.yellow + "  " + handle.resolved_name + "\n" + console.reset
        publisher.publish(std_msgs.String("%s" % s))


class Services(object):
    def __init__(self, services, introspection_topic_name="services"):
        """
        Converts the incoming list of service name, service type, callback function triples into proper variables of this class.

        .. code-block:: python

           services = rocon_python_comms.utils.Services(
               [
                   ('~dude', std_srvs.Empty, service_callback),
                   ('/dude/bob', std_srvs.Empty, service_callback),
               ]
           )

        Note: '~/introspection/dude' will become just 'dude'

        :param services: incoming list of service specifications
        :type services: list of (str, str, function) tuples representing (service_name, service_type, callback) pairs.
        :param str introspection_topic_name: where to put the introspection topic that shows the resolved names at runtime
        """
        self.__dict__ = {namespace.basename(service_name): rospy.Service(service_name, service_type, callback) for (service_name, service_type, callback) in services}
        publisher = rospy.Publisher("~introspection/" + introspection_topic_name, std_msgs.String, latch=True, queue_size=1)
        publish_resolved_names(publisher, self.__dict__.values())
        self.introspection_publisher = publisher


class ServiceProxies(object):
    def __init__(self, service_proxies, introspection_topic_name="service_proxies"):
        """
        Converts the incoming list of service name, service type pairs into proper variables of this class.

        .. code-block:: python

           service_proxies = rocon_python_comms.utils.ServiceProxies(
               [
                   ('~dude', std_srvs.Empty),
                   ('/dude/bob', std_srvs.Empty),
               ]
           )

        Note: '~/introspection/dude' will become just 'dude'

        :param services: incoming list of service proxy specifications
        :type services: list of (str, str) tuples representing (service_name, service_type) pairs.
        """
        self.__dict__ = {namespace.basename(service_name): rospy.ServiceProxy(service_name, service_type) for (service_name, service_type) in service_proxies}
        publisher = rospy.Publisher("~introspection/" + introspection_topic_name, std_msgs.String, latch=True, queue_size=1)
        publish_resolved_names(publisher, self.__dict__.values())
        self.introspection_publisher = publisher


class Publishers(object):
    def __init__(self, publishers, introspection_topic_name="publishers"):
        """
        Converts the incoming list of publisher name, type, latched, queue_size specifications into proper variables of this class.

        .. code-block:: python

           publishers = rocon_python_comms.utils.Publishers(
               [
                   ('~foo', std_msgs.String, True, 5),
                   ('/foo/bar', std_msgs.String, False, 5),
               ]
           )

        Note: '~/introspection/dude' will become just 'dude'

        :param publishers: incoming list of service specifications
        :type publishers: list of (str, str, bool, int) tuples representing (topic_name, publisher_type, latched, queue_size) specifications.
        """
        self.__dict__ = {namespace.basename(topic_name): rospy.Publisher(topic_name, publisher_type, latch=latched, queue_size=queue_size) for (topic_name, publisher_type, latched, queue_size) in publishers}
        publisher = rospy.Publisher("~introspection/" + introspection_topic_name, std_msgs.String, latch=True, queue_size=1)
        publish_resolved_names(publisher, self.__dict__.values())
        self.introspection_publisher = publisher


class Subscribers(object):
    def __init__(self, subscribers, introspection_topic_name="subscribers"):
        """
        Converts the incoming list of publisher name, service type pairs into proper variables of this class.

        .. code-block:: python

           subscribers = rocon_python_comms.utils.Subscribers(
               [
                   ('~dudette', std_msgs.String, subscriber_callback),
                   ('/dudette/jane', std_msgs.String, subscriber_callback),
               ]
           )

        Note: '~/introspection/dude' will become just 'dude'

        :param subscribers: incoming list of service specifications
        :type subscribers: list of (str, str, bool, int) tuples representing (topic_name, subscriber_type, latched, queue_size) specifications.
        """
        self.__dict__ = {namespace.basename(topic_name): rospy.Subscriber(topic_name, subscriber_type, callback) for (topic_name, subscriber_type, callback) in subscribers}
        publisher = rospy.Publisher("~introspection/" + introspection_topic_name, std_msgs.String, latch=True, queue_size=1)
        publish_resolved_names(publisher, self.__dict__.values())
        self.introspection_publisher = publisher

##############################################################################
# Parameters
##############################################################################

# Use a class decorator to extend a user's Parameter class
# http://python-3-patterns-idioms-test.readthedocs.org/en/latest/PythonDecorators.html
# http://stackoverflow.com/questions/9443725/add-method-to-a-class-dynamically-with-decorator
