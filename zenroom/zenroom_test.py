import json

import pytest

from zenroom import zenroom
from zenroom.zenroom import Error


def test_basic():
    script = "print('Hello world')"
    output, errors = zenroom.execute(script)

    assert output.decode() == "Hello world"


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
    output, _ = zenroom.execute(script, verbosity=3)
    result = json.loads(output.decode())
    assert 'public' in result
    assert 'private' in result


def test_zencode():
    contract = """Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
Given that I am known as 'identifier'
When I create my new keypair
Then print all data
    """

    result, _ = zenroom.zencode(contract)
    assert result
    assert b'public' in result
    assert b'private' in result


def test_broken_script():
    with pytest.raises(Error) as e:
        script = "print('"
        result, errors = zenroom.execute(script)

    assert e


def test_broken_zencode():
    contract = """Scenario 'coconut': "broken"
    Given that I am known as '
    When I create my new keypair
    Then print all data
    """
    with pytest.raises(Error) as e:
        result, _ = zenroom.zencode(contract, verbosity=3)

    assert e


def test_load_test():
    contract = """Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
    Given that I am known as 'identifier'
    When I create my new keypair
    Then print all data
        """

    for _ in range(90):
        print(f"#{_} CONTRACT")
        result, _ = zenroom.zencode(contract)
        assert b'private' in result


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

    for _ in range(90):
        print(f"#{_} CONTRACT")
        result, _ = zenroom.execute(contract)
        assert b'private' in result
