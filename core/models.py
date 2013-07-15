from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _

class Auditable (models.Model):
    """
    Abstract class
    Contains the basic information for auditing an object
    """
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created on'))
    modified_on = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False, verbose_name=_('Modified on'))
    created_by = models.ForeignKey(User, related_name='creations', editable=False, verbose_name=_('Created by'))
    modified_by = models.ForeignKey(User, related_name='modifications', editable=False, verbose_name=_('Modified by'))

    class Meta:
        abstract = True


class Puzzle (models.Model):
    name = models.CharField(max_length=120, verbose_name=_('Name'), unique=True)
    hostname = models.CharField(max_length=250, verbose_name=_('Hostname'))
    use_blacklist = models.BooleanField(default=True, help_text=_('Indicates if the list will be a blacklist or a whitelist'))


class IP (models.Model):
    puzzle = models.ForeignKey(Puzzle, related_name='ip_list', editable=False)
    ip = models.GenericIPAddressField(protocol='both', verbose_name=_('IP Address'))

    class Meta:
        order_with_respect_to = 'puzzle'


class DNS (models.Model):
    ip = models.GenericIPAddressField(protocol='both', verbose_name=_('IP Address'))
    description = models.CharField(max_length=150, verbose_name=_('Description'))
    puzzle = models.ForeignKey(Puzzle, editable=False, related_name=_('dns_list'))

    class Meta:
        order_with_respect_to = 'puzzle'


class Route (models.Model):
    puzzle = models.ForeignKey(Puzzle, editable=False)
    ip = models.GenericIPAddressField(protocol='both', verbose_name=_('IP Address'))
    netmask = models.GenericIPAddressField(protocol='both', default='255.255.255.0', verbose_name=_('Netmask'))
    gateway = models.GenericIPAddressField(protocol='both', verbose_name=_('Gateway'))
    device = models.ForeignKey(Interface, verbose_name=_('Network Interface'))
    default = models.BooleanField(verbose_name=_('Is default gateway'))

    class Meta:
        order_with_respect_to = 'puzzle'


class Interface (models.Model):
    puzzle = models.ForeignKey(Puzzle, editable=False)
    device_name = models.CharField(max_length=8, editable=False, verbose_name=_('Device Name'))
    ip = models.GenericIPAddressField(protocol='both', verbose_name=_('IP Address'))
    netmask = models.GenericIPAddressField(protocol='both', verbose_name=_('Netmask'))
    is_wlan = models.BooleanField(verbose_name=_('Is WLAN'), help_text=_('Is the interface connected to the internet'))
    mac_address = models.CharField(editable=False, verbose_name=_('Hardware Address'))

    class Meta:
        order_with_respect_to = 'puzzle'


class Network (models.Model):
    """
    Class that represents a Net / Subnet
    """
    interface = models.ForeignKey(Interface, verbose_name=_('Network Interface'))
    name = models.CharField(max_length=120, verbose_name=_('Name'), help_text=_('Name that describes the net/subnet'))
    ip = models.GenericIPAddressField(protocol='both', verbose_name=_('IP Address'))
    netmask = models.GenericIPAddressField(protocol='both', verbose_name=_('Netmask'))
    vlsm = models.PositiveIntegerField(verbose_name=_('VLSM'), help_text=_('Variable Length Subnet Mask'))

    class Meta:
        order_with_respect_to = 'puzzle'


class Node (models.Model):
    fqdn = models.CharField(max_length=250, db_index=True, unique=True, verbose_name=_('FQDN'))
    network = models.ForeignKey(Network, verbose_name=_('Network'), help_text=_('Network the node belogns'))
    ip = models.GenericIPAddressField(protocol='both', blank=True, null=True, verbose_name=_('IP Address'), help_text=_('Leave blank if you want to use the fqdn'))

    class Meta:
        order_with_respect_to = 'puzzle'


class Module (models.Model):
    puzzle = models.ForeignKey(Puzzle, editable=False)
    name = models.CharField(max_length=120, unique=True, verbose_name=_('Name'))
    is_enabled = models.BoleanField(default=False, verbose_name=_('Is enabled'))
    dependencies = models.ManyToManyField('self', verbose_name=_('Dependencies'))
    installed_path = models.FilePathField(verbose_name=_('Installed Path'))

    class Meta:
        order_with_respect_to = 'puzzle'
        ordering = ['is_enabled', 'name']


class LogStatus (object):
    SUCCESS = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    CHOICES = (
        (SUCCESS, _('Success')),
        (INFO, _('Information')),
        (WARNING, _('Warning')),
        (ERROR, _('Error')),
    )

class Protocol(object):
    ANY = 0
    TCP = 1
    UDP = 2
    ICMP = 3
    IP = 4

    CHOICES = (
        (ANY, 'any'),
        (TCP, 'tcp'),
        (UDP, 'udp'),
        (ICMP, 'icmp'),
        (IP, 'ip'),
    )


class Service (models.Model):
    port = model.PositiveIntegerField(verbose_name=_('Port'))
    protocol = model.SmallPositiveIntegetField(choices=Protocol.CHOICES, verbose_name=_('Protocol'))
    name = model.CharField(max_length=20, verbose_name=_('Name'))

    class Meta:
        unique_together = [('port', 'protocol')]
        ordering = ['port', 'protocol']


class Log (models.Model):
    datetime_registered = models.DateTimeField(auto_now_add=True, editable=False, db_index=True, verbose_name=_('Datetime'))
    status = models.PositiveSmallIntergerField(choices=LogStatus.CHOICES, editable=False, db_index=True, verbose_name=_('Status'))
    description = models.TextField(editable=False, verbose_name=_('Description'))
    url = models.URLField(editable=False, verbose_name=_('URL'))
    user = models.ForeignKey(User, null=True, blank=True, editable=False, verbose_name=_('User'), related_name='events')

    class Meta:
        ordering = ['-datetime']
