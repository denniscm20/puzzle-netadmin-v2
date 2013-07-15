from django.db import models
from core.models import Auditable, Interface, Node, Protocol
from django.utils.translation import ugettext as _
import subprocess

class Squid (Auditable):
    http_ports = models.ManyToManyField(Interface, throught='HttpPort')

class HttpPort (models.Model):
    squid = models.ForeignKey(Squid)
    interface = models.ForeignKey(Interface)
    port = models.PositiveIntegerField()
    description = models.TextField()

class AccessType (object):
    HTTP_ACCESS = 0
    NO_CACHE = 1

    CHOICES = (
        (HTTP_ACCESS, 'http_access'),
        (NO_CACHE, 'no_cache'),
    )

class ACLType (object):
    SRC
    DST
    SRCDOMAIN
    DSTDOMAIN
    URL_REGEX

    CHOICES

class Action (models.Model):
    pass

class Rule (models.Model):
    squid = models.ForeignKey(Squid)
    access_type
    action
    
class ACL (models.Model):
    rule = models.ForeignKey(Rule)
    name
    acl_type

class ACLValue (models.Model):
    acl = models.ForeignKey(ACL)
    name

class PredefinedRule (models.Model):
    name
    description
    rule = models.ForeignKey(Rule)
