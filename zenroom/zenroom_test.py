import json

import pytest

from zenroom import zenroom
from zenroom.zenroom import ZenroomException

LOAD_FATIGUE = 200


def test_basic():
    script = "print('Hello world')"
    output, errors = zenroom.zenroom_exec(script)

    assert "Hello world" == output


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
    assert "{}" == result


def test_create_petition_with_rng():
    script = """Scenario 'coconut': "Citizen creates a new petition, using his own key, the credential and the credential issuer's public"
Given that I am known as 'identifier'
and I have my keypair
and I have a signed credential
and I use the verification key by 'issuer_identifier'
When I aggregate all the verification keys
and I generate a credential proof
and I create a new petition 'petition'
Then print all data
    """
    keys = '{"identifier":{"schema":"cred_keypair","zenroom":"0.9","encoding":"hex","public":"04356878b230d0bffc7e913736dbc2cdcfecfc21f02195177c1d501513a1c10fafc534668a306db5a7dcd57df8242226d61920f766bc0dca690598bdcd7aae09490d7681f9ec6197d84c8ed9e5484a8ad21717d7a224697fd3649279089970c71d","private":"aeea220f7c4d3d39b58acc20c84553f6b2864fde01ff1373018e5197074302b3","curve":"bls383"},"credential":{"h":"04424954e09f573023b34e5c764ee3ea07b0942cadc9f738ba057afed1a52eef78edd3172d58c4cdfcfbd393686a0b11fe25662dd4e632752e26814236699cde98b4c04139fe73a63414cb1775c72654e2024559a1b46ea164f41a2e53f9bdb90f","zenroom":"0.9","curve":"bls383","schema":"aggsigma","encoding":"hex","s":"042c52807efc2506e16ec1f0db6002d5cf6d55b16e9645be9ba3a557a7bde9f2302272014f63591bc05a3bae35a7462a4b3ef2ef956e34210cdde9be9286ad9571d2c18c8ebd175924c42270e425391e4f279c5d498ae9f97f06d40f4bf6cd21a1"}}'
    data = '{"issuer_identifier":{"verify":{"beta":"0d619263c6048d0ab94f825f0f9f30d5f441df3d78e6c34e64eb3d6a2d3b764d51f7722dc18456b986a8291a525985e747841ebd9788b1c505ca5584d752a3b9e5d294666745cf14b0df49fd81dd35ffe16f752fcd8dc9a4f69579528cdebf932272a28dc8c9c7d70af121e8061b8dc0867f0540e2b05306344c987d65c63d63179bf5d64ea7c6211a4e65bebc5b4eae4e649e46eb70094c5ae8fb271dfccce5d56ef7385ebb46c7e538a07fa8e4afbdeba03c71cc882a72a9042f8db2374a6b","alpha":"12835db70ccae8be2b58e6b73068368871189b19e2602dbfbf05bcbe7702d9b92916b3ecbaff93c6c560f48bc13cdc80469275f1adac04b5e568cda5a6c56651a2f8976dd947e9c72910432b495e6a605b99f97c5f3b955979e1668cac3f4ca13739b6e7a1866f7da679e8764d6f2ff54450f74b2033d1f2ae8cd1f32379df9242c255a773c0d44f23a5b666fcd20b0938e99c7b8f9d61bfa7982dcdd054d691266d3271fac6ea7491a8af4597dee7c1d409040a8014e1ad3c32370852ca4dc7"}}}'
    results = []
    for _ in range(LOAD_FATIGUE):
        result, error = zenroom.zencode_exec_rng(script=script,
                                                 data=data,
                                                 keys=keys,
                                                 random_seed=bytearray("random_se3d", "utf=8"))
        sorted_result = json.dumps(json.loads(result), sort_keys=True)
        results.append(sorted_result)
    assert len(set(results)) == 1


def test_random():
    script = """rng = RNG.new()
    buf = rng:octet(16)
    print(buf)
    """
    results = []
    for _ in range(LOAD_FATIGUE):
        result, error = zenroom.zenroom_exec_rng(script=script, random_seed=bytearray("random_seed", "utf=8"))
        results.append(result)
    assert len(set(results)) == 1

def test_load_test():
    contract = """Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
    Given that I am known as 'identifier'
    When I create my new keypair
    Then print all data
        """

    for _ in range(LOAD_FATIGUE):
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

    for _ in range(LOAD_FATIGUE):
        print(f"#{_} CONTRACT")
        result, _ = zenroom.zenroom_exec(contract)
        assert 'private' in result

def test_data():
    script = "print(DATA)"
    data = "3"

    result, error = zenroom.zenroom_exec(script=script, data=data, verbosity=3)
    assert "3" == result


def test_tally():
    contract = """Scenario 'coconut': "Count"
Given that I receive a petition
and I receive a tally
When I count the petition results
Then print all data    
"""
    data = """{"verifier":{"alpha":"26ed76c322d2d5a7ae054ae7cb8ff48965f72af8659af231413a5ef2bd8f63fa99fec211ced1f868776fda9b8e3e50080dfb0b196de451e509858a737edceacf7bcb4ff5d295559672b0ea7192d98cec617208536f2ade9c670e93343b78dc41458813f0b36415018f7fde018ea9abeb111f812187e78664481ee86f1788b3b4f99144636400e68f71547db1d5b014125045dc425f844696bd1c79526644c92514fd7745a6d00c90a0690b980dc88369cf596918416e9b4895a0ce6396b1f732","zenroom":"0.9","beta":"0dbc2ef91831b09d1d755994d267d55136edd66e52202e2a14d76045fa24af3e2e62121d35941cc1f595b64b2ffd33e91bcdc576a53c8b5537de81e560eae9e22152b821f791a862321be60f1e74137abfcb35c6f2a6007ac598ee811589372b4b903abb70832049d77d4f758bee22708782f1d0320474726bb07626bf98984db77e13986a929466a6970073998e968d11f5bc157cb20d1f36ad2e636f585006fe150173dfbeb42fceda7ea1638724de907b5715bfe611436b50b1a05be80a14","curve":"bls383","schema":"issue_verify","encoding":"hex"},"petition":{"owner":"0425d40a99d767d34ce85baab8d4763701b13d91b4fafc43976a88cc2a38948a4e66690b3f7d899cae879714280d35ce431020d63e8c0b2ec30a97f905fe01df395178fb986d9b764318dff30d0cbe725c183efbff75a6d5efd9c3cc844086299e","zenroom":"0.9","curve":"bls383","list":{"040e9c19ba56a0cc48fd9b92a24c5c9946e57069bf8b219bd35abe5f8acdb74081aaad945a6c5f6223559971b4136a562035d64b636b20265646580ba78bdd6312065f9c97342a75f413aadc309e3f8cf0be5d34eba43e18278848a69ad26774e2":true},"encoding":"hex","scores":{"zenroom":"0.9","pos":{"left":"04265e9161af6cabce36ba1cdf2e4d5330db7cf493617090a8dff6f309fae4f4f154db620d05d84488e6f51a6c6252bee23c60e165285b7ae68b9d3392f71dfea64ef36870b3329816403a14c5201473efe771d02e1e0857a90476464b41b6f986","right":"0416da678fe475bca4bd68a56955c78068349c44949133999c90baa119463f51aeb2ddbca2afa8e3679c07ffffe35ee8ad00a1d105657d8ae72ef0bf3896cbac17e659ee1eeb456aaf32fb029651252bbd7a8f8c0b627b39c91486a5ace70195b4"},"curve":"bls383","neg":{"left":"04265e9161af6cabce36ba1cdf2e4d5330db7cf493617090a8dff6f309fae4f4f154db620d05d84488e6f51a6c6252bee2190475303c4ff3cf14d07a3128cc93de51b9ddbc40330cfb6bf7a33c494cb104931a6efb6c5c2d82d5c0d71943f3b725","right":"0414a5bed322d6bc186f4f6bb4f7ab7f60913f1047d237e1dd84991d7714619dc81ce497e47ca56abb42dc4a3229a42d562a46f41f85cc043a8429e9d9d4a182f3ae062928baaca8a8e783d4c90db52e307e0343e46c42dc1e61a5df5abc43724c"},"schema":"petition_scores","encoding":"hex"},"schema":"petition","uid":"petition"}}"""
    keys = """{"tally":{"dec":{"neg":"0414a5bed322d6bc186f4f6bb4f7ab7f60913f1047d237e1dd84991d7714619dc81ce497e47ca56abb42dc4a3229a42d562b1e6275dedf6a7b1c43c3ea4b490f90f2a71d0438b8fc68c4ade3385babf6c3fc88fb451e21a90d78913e09c9673e5f","pos":"0414a5bed322d6bc186f4f6bb4f7ab7f60913f1047d237e1dd84991d7714619dc81ce497e47ca56abb42dc4a3229a42d562a46f41f85cc043a8429e9d9d4a182f3ae062928baaca8a8e783d4c90db52e307e0343e46c42dc1e61a5df5abc43724c"},"c":"64045531ba689dda727152d68aec0d3736e106be06143a6c61d5f6a887eada2e","schema":"petition_tally","zenroom":"0.9","encoding":"hex","curve":"bls383","rx":"2e1e1ef4a2e82fd7b6d4855437f1f797fd71d79be017f084b3e789c5e9604783","uid":"petition"},"petition":{"zenroom":"0.9","uid":"petition","schema":"petition","encoding":"hex","scores":{"neg":{"left":"04265e9161af6cabce36ba1cdf2e4d5330db7cf493617090a8dff6f309fae4f4f154db620d05d84488e6f51a6c6252bee2190475303c4ff3cf14d07a3128cc93de51b9ddbc40330cfb6bf7a33c494cb104931a6efb6c5c2d82d5c0d71943f3b725","right":"0414a5bed322d6bc186f4f6bb4f7ab7f60913f1047d237e1dd84991d7714619dc81ce497e47ca56abb42dc4a3229a42d562a46f41f85cc043a8429e9d9d4a182f3ae062928baaca8a8e783d4c90db52e307e0343e46c42dc1e61a5df5abc43724c"},"zenroom":"0.9","schema":"petition_scores","encoding":"hex","curve":"bls383","pos":{"left":"04265e9161af6cabce36ba1cdf2e4d5330db7cf493617090a8dff6f309fae4f4f154db620d05d84488e6f51a6c6252bee23c60e165285b7ae68b9d3392f71dfea64ef36870b3329816403a14c5201473efe771d02e1e0857a90476464b41b6f986","right":"0416da678fe475bca4bd68a56955c78068349c44949133999c90baa119463f51aeb2ddbca2afa8e3679c07ffffe35ee8ad00a1d105657d8ae72ef0bf3896cbac17e659ee1eeb456aaf32fb029651252bbd7a8f8c0b627b39c91486a5ace70195b4"}},"curve":"bls383","owner":"0425d40a99d767d34ce85baab8d4763701b13d91b4fafc43976a88cc2a38948a4e66690b3f7d899cae879714280d35ce431020d63e8c0b2ec30a97f905fe01df395178fb986d9b764318dff30d0cbe725c183efbff75a6d5efd9c3cc844086299e"}}"""

    result, _ = zenroom.zencode_exec(script=contract, data=data, keys=keys, verbosity=3)
    json_result = json.loads(result)

    assert "result" in json_result
    assert 1 == json_result["result"]
    assert "uid" in json_result
    assert "petition" == json_result["uid"]
