from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _

class Auditable (models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_by = models.ForeignKey(User, related_name='creations')
    modified_by = models.ForeignKey(User, related_name='modifications')

    class Meta:
        abstract = True

class Puzzle (models.Model):
    name = models.CharField(max_length=120)
    hostname = models.CharField(max_length=250)
    use_blacklist = models.BooleanField(default=True, help_text=_('Indicates if the list will be a blacklist or a whitelist'))

class IP (models.Model):
    puzzle = models.ForeignKey(Puzzle, related_name='ip_list')
    ip = models.GenericIPAddressField(protocol='both')

class DNS (models.Model):
    ip = models.GenericIPAddressField(protocol='both')
    description = models.TextField()
    puzzle = models.ForeignKey(Puzzle, editable=False)

class Route (models.Model):
    puzzle = models.ForeignKey(Puzzle, editable=False)
    ip = models.GenericIPAddressField(protocol='both')
    netmask = models.GenericIPAddressField(protocol='both', default='255.255.255.0')
    gateway = models.GenericIPAddressField(protocol='both')
    device = models.ForeignKey(Interface)
    default = models.GenericIPAddressField(protocol='both')

class Interface (models.Model):
    puzzle = models.ForeignKey(Puzzle, editable=False)
    device_name = models.CharField(max_length=10, editable=False)
    ip = models.GenericIPAddressField(protocol='both')
    netmask = models.GenericIPAddressField(protocol='both')
    is_wlan = models.BooleanField()
    mac_address = models.CharField(editable=False)

class Network (models.Model):
    interface = models.ForeignKey(Interface)
    name = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(protocol='both')
    netmask = models.GenericIPAddressField(protocol='both')
    shortmask = models.PositiveIntegerField()

class Node (models.Model):
    hostname = models.CharField(max_length=250, db_index=True, unique=True)
    network = models.ForeignKey(Network)
    ip = models.GenericIPAddressField(protocol='both')

class Module (models.Model):
    puzzle = models.ForeignKey(Puzzle)
    name = models.CharField(max_length=120, unique=True)
    is_enabled = models.BoleanField(default=False)
    dependencies = models.ManyToManyField('self')

    class Meta:
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
    port = model.PositiveIntegerField()
    protocol = model.SmallPositiveIntegetField(choices=Protocol.CHOICES)
    name = model.CharField(max_length=20)

    class Meta:
        unique_together = [('port', 'protocol')]
        ordering = ['port', 'protocol']

class Log (models.Model):
    datetime_registered = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    status = models.PositiveSmallIntergerField(choices=LogStatus.CHOICES, editable=False, db_index=True)
    description = models.TextField(editable=False)
    url = models.URLField(editable=False)
    user = models.ForeignKey(User, null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-datetime']
