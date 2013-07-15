from django.db import models
from core.models import Auditable, Interface, Node, Protocol
from django.utils.translation import ugettext as _
import subprocess

class Iptables (Auditable):
    name = models.CharField(max_length=120)
    is_enabled = models.BooleanField(default=True)

class Table (object):
    FILTER = 0
    NAT = 1

    CHOICES = (
        (FILTER, 'filter'),
        (NAT, 'nat')),
    )

class Policy (object):
    ALLOW = 0
    DROP = 1

    CHOICES = (
        (ALLOW, 'Allow'),
        (DROP, 'Drop'),
    )

class Action (object):
    ALLOW = 0
    DROP = 1
    REJECT = 2
    LOG = 3

    CHOICES = (
        (ALLOW, 'Allow'),
        (DROP, 'Drop'),
        (REJECT, 'Reject'),
        (LOG, 'Log'),
    )

class Status (object):
    INVALID = 0
    NEW = 1
    ESTABLISHED = 2
    RELATED = 3
    UNTRACKED = 4
    SNAT = 5
    DNAT = 6

    CHOICES = (
        (INVALID, 'INVALID'),
        (NEW, 'NEW'),
        (ESTABLISHED, 'ESTABLISHED'),
        (RELATED, 'RELATED'),
        (UNTRACKED, 'UNTRACKED'),
        (SNAT, 'SNAT'),
        (DNAT, 'DNAT'),
    )

class Chain (models.Model):
    iptables = model.ForeignKey(Iptables, null=True, blank=True)
    table = models.SmallPositiveIntegerField(choices=Table.CHOICES)
    default_policy = models.SmallPositiveIntegerField(choices=Policy.CHOICES)

    class Meta:
        order_with_respect_to = 'iptables'
        unique_together = [('iptables', 'table')]
    
class Rule (models.Model):
    chain = models.ForeignKey(Chain, related_name='rules')
    order = PositiveIntegerField(db_index=True)
    input_interface = models.ForeignKey(Interface, related_name='iptables_input_rules')
    output_interface = models.ForeignKey(Interface, related_name='iptables_output_rules')
    start_port = models.PositiveIntegerField(blank=True)
    destination_port = models.PositiveIntegerField(blank=True)
    source_ip = models.GenericIPAddressField(protocol='both', blank=True)
    source_mask = models.GenericIPAddressField(protocol='both', blank=True)
    destination_ip = models.GenericIPAddressField(protocol='both', blank=True)
    destination_mask = models.GenericIPAddressField(protocol='both', blank=True)
    mac_address = models.GenericIPAddressField(protocol='both', blank=True)
    protocol = models.SmallPositiveIntegerField(choices=Protocol.CHOICES)
    status = models.CommaSeparatedIntegerField(choices=Status.CHOICES)
    source_host = models.ForeignKey(Node, null=True, blank=True)
    destination_host = models.ForeignKey(Node, null=True, blank=True)
    action = models.SmallPositiveIntegerField(choices=Action.CHOICES)

    class Meta:
        ordering = ['order']
        order_with_respect_to = 'chain'
        unique_together = [('chain', 'order')]

class PredefinedRule (models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    rules = models.ManyToMany(Rule)


