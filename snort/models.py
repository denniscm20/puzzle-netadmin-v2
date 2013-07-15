from django.db import models
from core.models import Auditable, Interface, Node, Protocol
from django.utils.translation import ugettext as _
import subprocess

class Snort (Auditable):
    preprocessors = models.ManyToMany(Preproceesor)
    predefined_rules

class Rule (models.Model):
    preprocessor = models.FoireignKey(Preprocessor, related_name='custom_preprocessor_rule')
    rule_type
    action
    protocol
    is_ip_excluded
    source_ip_address
    source_cidr
    are_source_ports_excluded
    source_port_lower
    source_posrt_higher
    destination_ip_address
    destination_cidr
    destination_port_lower
    destinarion_port_higher
    are_destination_ports_excluded
    rule_options
    activated_by = models.ForeignKey('self', null=True, blank=True)

class Preprocessor (models.Model):
    name
    description

class PreprocessorVariable (models.Model):
    preprocessor = models.ForeignKey(Preprocessor)
    variable_name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    variable_type = models.SmallPositiveIntegerField(choices=DataType.CHOICES)

class DataType (object):
    CHOICES = (
        (0, _('Numeric')),
        (1, _('String')),
        (3, _('Boolean')),
        (4, _('Flag')),
    )

class PreprocessorVariableValue (models.Model):
    snort = models.ForeignKey(Snort)
    preprocessor = models.ForeignKey(Preprocessor)
    preprocessorVariable = models.ForeignKey(PreprocessorVariable)
    variable_value = models.CharField(max_length=120)

class Event (models.Model):
    pass

class RuleOption (models.Model):
    rule
    option
    type = models.CharField()
    threshold = models.ForeignKey(Threshold)

class Threshold (models.Model):
    threshold = models.PositiveSmallIntegerField(choices=ThresholdType.CHOICES)
    track = models.PositiveSmallIntegerField(choices=TrackType.CHOICES)
    count = models.PositiveSmallIntegerField()
    seconds = models.PositiveSmallIntegerField()

class ThresholdType (object):
    CHOICHES = (
        (0, 'limit'),
        (1, 'threshold'),
        (2, 'both'),
    )

class TrackType (object):
    CHOICES = (
        (0, 'by_src'),
        (1, 'by_dst'),
    )

class RuleType (models.Model):
    """
    Custom Action
    """
    name = models.CharField(max_length=120)
    type = models.SmallPositiveIntegerField(choices=Actions.CHOICES)
    output_modules = models.ManyToManyField(Output, throught='OutputVariableValue')

class Option (objects):
    GENERAL = 0
    PAYLOAD = 1
    NON_PAYLOAD = 2
    POST_DETECTION = 3

    CHOICES = (
        (GENERAL,'general'),
        (PAYLOAD,'payload'),
        (NON_PAYLOAD,'non payload'),
        (POST_DETECTION,'post detection'),
    )

class GeneralOption (models.model):
    rule = models.ForeignKey(Rule)
    msg
    reference # system,id
    gid # > 1000000; SID
    sid # unique; REV
    rev 
    classtype # category; classification.config: name,description,priority
    priority # severity; overrides default priority from classification.config
    metadata
    
class PayloadOption (models.Model):
    rule
    negate_content
    content
    nocase = models.BooleanField()
    rawbytes
    depth
    offset
    distance
    within
    http_client_body 
    http_cookie
    http_raw_cookie 
    http_header
    http_raw_header
    http_method
    http_uri
    http_raw_uri 
    http_stat_code
    http_stat_msg
    http_encode 
    fast_pattern
    uricontent
    urilen
    isdataat
    pcre
    pkt_data 
    file_data 
    base64_decode 
    base64_data
    byte_test 
    byte_jump 
    byte_extract 
    ftpbounce
    asn1
    cvs
    dce_iface 	
    dce_opnum 
    dce_stub_data 
    sip_method 
    sip_stat_code 
    sip_header 
    sip_body 
    gtp_type 
    gtp_info 
    gtp_version     

class NonPayloadOption (models.Model):
    fragoffset
    ttl
    tos
    _id
    ipopts
    fragbits
    dsize
    flags
    flow
    flowbits
    seq
    ack
    window
    itype
    icode
    icmp_id
    icmp_seq
    rpc
    ip_proto
    sameip
    stream_reassemble
    stream_size

class PostDetection (models.Model):
    logto
    session
    resp
    react
    tag
    activates
    activated_by
    count
    replace
    detection_filter  

class Output (models.Model):
    name
    description

class OutputVariable (models.Model):
    output = models.ForeignKey(Output)
    name

class OutputVariableValue (models.Model):
    rule_type = models.ForeignKey(RuleType)
    output = models.ForeignKey(Output)
    variable = models.ForeignKey(OutputVariable)
    value = models.CharField(max_length=120)

class Actions (object):
    ALERT=0
    LOG=1
    PASS=2
    ACTIVATE=3
    DYNAMIC=4
    DROP=5
    REJECT=6
    SDROP=7

    CHOICES = (
        (ALERT, 'alert'),
    )

