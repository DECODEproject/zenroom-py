# test cases

from zenroom import zenroom

def test_basic():
    script = b"print('Hello world')"
    output = zenroom.execute(script)

    assert output.decode("utf-8") == b"Hello world".decode("utf-8")

def test_encrypt_decrypt():
    encryptKeys = b"""
    {
        "device_id": "anonymous",
        "community_id": "smartcitizens",
        "community_pubkey": "BBLewg4VqLR38b38daE7Fj\/uhr543uGrEpyoPFgmFZK6EZ9g2XdK\/i65RrSJ6sJ96aXD3DJHY3Me2GJQO9\/ifjE="
    }
    """

    data = b"secret message"

    encryptScript = b"""
    curve = 'ed25519'
    keys_schema = SCHEMA.Record {
        device_id        = SCHEMA.String,
        community_id     = SCHEMA.String,
        community_pubkey = SCHEMA.String
    }

    payload_schema = SCHEMA.Record {
        device_id = SCHEMA.String,
        data      = SCHEMA.String
    }

    output_schema = SCHEMA.Record {
        device_pubkey = SCHEMA.String,
        community_id  = SCHEMA.String,
        payload       = SCHEMA.String
    }

    keys = read_json(KEYS, keys_schema)

    devkey = ECDH.keygen(curve)

    payload = {}
    payload['device_id'] = keys['device_id']
    payload['data']      = DATA
    validate(payload, payload_schema)

    header = {}
    header['device_pubkey'] = devkey:public():base64()
    header['community_id'] = keys['community_id']

    output = ECDH.encrypt(
        devkey,
        base64(keys.community_pubkey),
        MSG.pack(payload),
        MSG.pack(header)
    )

    output = map(output, O.to_base64)
    output.zenroom = VERSION
    output.encoding = 'base64'
    output.curve = curve

    print(JSON.encode(output))
    """

    decryptKeys = b"""
    {
        "community_seckey": "D19GsDTGjLBX23J281SNpXWUdu+oL6hdAJ0Zh6IrRHA="
    }
    """

    decryptScript = b"""
    keys_schema = SCHEMA.Record { community_seckey = SCHEMA.String }

    data_schema = SCHEMA.Record {
        text     = SCHEMA.string,
        iv       = SCHEMA.string,
        header   = SCHEMA.string,
        checksum = SCHEMA.string
    }

    payload_schema = SCHEMA.Record {
        device_id   = SCHEMA.String,
        data        = SCHEMA.String
    }

    data = read_json(DATA) -- TODO: data_schema validation
    keys = read_json(KEYS, keys_schema)
    head = OCTET.msgunpack( base64(data.header) )

    dashkey = ECDH.new()
    dashkey:private( base64(keys.community_seckey) )

    payload,ck = ECDH.decrypt(dashkey,
        base64( head.device_pubkey ),
        map(data, base64))

    validate(payload, payload_schema)

    print(JSON.encode(OCTET.msgunpack(payload.text)))
    """

    encryptedMessage = zenroom.execute(encryptScript, keys=encryptKeys, data=data)

    assert len(encryptedMessage) != 0

    decryptedMessage = zenroom.execute(decryptScript, keys=decryptKeys, data=encryptedMessage)

    assert decryptedMessage.encode("utf-8") == "secret message"
