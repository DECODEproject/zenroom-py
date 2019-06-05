import json

import pytest

from zenroom import zenroom
from zenroom.zenroom import ZenroomException


def test_basic():
    script = "print('Hello world')"
    output, errors = zenroom.zenroom_exec(script)

    assert "Hello world\n" == output


def test_keygen():
    script = """
    -- generate a simple keyring
    keyring = ECDH.new()
    keyring:keygen()
    
    -- export the keypair to json
    export = JSON.encode(
       {
          public  = keyring: public():base64(),
          private = keyring:private():base64()
       }
    )
    print(export)
    """
    output, _ = zenroom.zenroom_exec(script, verbosity=3)
    result = json.loads(output)
    assert 'public' in result
    assert 'private' in result


def test_zencode():
    contract = """Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
Given that I am known as 'identifier'
When I create my new keypair
Then print all data
    """

    result, _ = zenroom.zencode_exec(contract)
    assert result
    assert 'public' in result
    assert 'private' in result


def test_broken_script():
    with pytest.raises(ZenroomException) as e:
        script = "print('"
        result, errors = zenroom.zenroom_exec(script)

        assert e
        assert "line 1" in e


def test_broken_zencode():
    contract = """Scenario 'coconut': "broken"
    Given that I am known as '
    When I create my new keypair
    Then print all data
    """
    result, error = zenroom.zencode_exec(contract, verbosity=3)
    assert error
    assert "{}\n" == result


def test_random():
    script = """rng = RNG.new()
    buf = rng:octet(16)
    print(buf)
    """
    result, _ = zenroom.zenroom_exec_rng(script=script, random_seed=bytearray(1024))
    print(result)
    assert result


def test_load_test():
    contract = """Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
    Given that I am known as 'identifier'
    When I create my new keypair
    Then print all data
        """

    for _ in range(200):
        print(f"#{_} CONTRACT")
        result, _ = zenroom.zencode_exec(contract)
        assert 'private' in result


def test_load_script():
    contract = """-- 0 for silent logging
ZEN:begin(0)

ZEN:parse([[
Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
Given that I am known as 'identifier'
When I create my new keypair
Then print all data
]])

ZEN:run()
    """

    for _ in range(200):
        print(f"#{_} CONTRACT")
        result, _ = zenroom.zenroom_exec(contract)
        assert 'private' in result

