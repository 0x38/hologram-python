# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
# LICENSE: Distributed under the terms of the MIT License
#
# test_HologramCloud.py - This file implements unit tests for the HologramCloud class.

import sys
import pytest
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
from Hologram.Authentication import *
from Hologram.HologramCloud import HologramCloud
from Hologram.Network import Network

from tests.MockModem import MockModem

credentials = {'devicekey':'12345678'}

def mock_scan(network):
    return ['MockModem']

@pytest.fixture
def no_modem(monkeypatch):
    monkeypatch.setattr(Network, '_scan_for_modems', mock_scan)
    monkeypatch.setattr(Network, '_modemHandlers', {'MockModem': MockModem})

def test_create(no_modem):
    hologram = HologramCloud(credentials, enable_inbound = False)

    assert hologram.send_host == 'cloudsocket.hologram.io'
    assert hologram.send_port == 9999
    assert hologram.receive_host == '0.0.0.0'
    assert hologram.receive_port == 4010

def test_invalid_sms_length(no_modem):

    hologram = HologramCloud(credentials, authentication_type='csrpsk', enable_inbound = False)

    temp = '111111111234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    with pytest.raises(Exception, match = 'SMS cannot be more than 160 characters long'):
        hologram.sendSMS('+1234567890', temp)

def test_get_result_string(no_modem):

    hologram = HologramCloud(credentials, enable_inbound = False)

    assert hologram.getResultString(-1) == 'Unknown error'
    assert hologram.getResultString(0) == 'Message sent successfully'
    assert hologram.getResultString(1) == 'Connection was closed so we couldn\'t read the whole message'
    assert hologram.getResultString(2) == 'Failed to parse the message'
    assert hologram.getResultString(3) == 'Auth section of the message was invalid'
    assert hologram.getResultString(4) == 'Payload type was invalid'
    assert hologram.getResultString(5) == 'Protocol type was invalid'
    assert hologram.getResultString(6) == 'Internal error in Hologram Cloud'
    assert hologram.getResultString(7) == 'Metadata was formatted incorrectly'
    assert hologram.getResultString(8) == 'Topic was formatted incorrectly'