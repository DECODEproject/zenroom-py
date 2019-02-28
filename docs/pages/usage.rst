.. _usage:

Usage
=====

The core Zenroom virtual machine exposes two primary functions by which
cryptographic operations may be invoked:

* ``zenroom_exec`` which takes as input a script, as well as optional keys and
  data fields, and when invoked the output of the script is written to stdout.

* ``zencode_exec`` which takes as input a ZENCODE, as well as optional keys and
  data fields, and when invoked the output of the ZENCODE is written to stdout.

* ``zenroom_exec_tobuf`` which takes the same basic parameters, but the output
  is written to a buffer provided by the caller.

* ``zencode_exec_tobuf`` like the later but executes a ZENCODE in place of a 
  script

For use in a library, these two latests function are the one that this library
attempts to expose, simplified slightly to expose a more idiomatically
Pythonic API surface.

Executing a simple zencode
-------------------------

The library only exposes a single function called ``execute``, which passes
its input parameters into the Zenroom VM, so to execute a simple script that
does not require any data or keys, the library can be used simply as follows:

.. code-block:: python

   from zenroom import zenroom

   contract = b'''
   Scenario 'coconut': Generate credential issuer keypair
     Given that I am known as 'ci_unique_id'
     When I create my new issuer keypair
     Then print all data
   '''

   output, errors = zenroom.zencode(contract)

   print(output)

This is a trite example obviously, but we wanted to demonstrate the simplest
possible Zencode script execution, that a caller can capture.

.. important:: Note that the contract value that is passed into the zencode 
   function must be a byte string. This is also true for any data or keys that
   are passed into Zenroom.

Executing a simple script
-------------------------

The library only exposes a single function called ``execute``, which passes
its input parameters into the Zenroom VM, so to execute a simple script that
does not require any data or keys, the library can be used simply as follows:

.. code-block:: python

   from zenroom import zenroom

   script = b'print("Hello world!")'

   output, errors = zenroom.execute(script)

   print(output)

This is a trite example obviously, but we wanted to demonstrate the simplest
possible Zencode script execution, that a caller can capture.

.. important:: Note that the script value that is passed into the execute
   function must be a byte string. This is also true for any data or keys that
   are passed into Zenroom.

Executing a script with keys and data
-------------------------------------

The example below is more involved, and shows how we can execute a script
with keys and data that must be fed into Zenroom to enable the script.

.. code-block:: python

   from zenroom import zenroom

   script = b"""
   -- define data schema
   msg = SCHEMA.Record {
      msg = SCHEMA.String
   }

   -- read and validate the data
   data = read_json(DATA, msg)

   -- read keys without validating
   keys = read_json(KEYS)

   -- now import recipient public key
   recipient_key = ECDH.new()
   recipient_key:public(base64(keys.recipient_public))

   -- now import our own private key (we are the data subject)
   own = ECDH.new()
   own:private(base64(keys.own_private))


   -- encrypt the fields
   out = {}
   out = LAMBDA.map(data,function(k,v)
     header = MSG.pack({key=k, pubkey=own:public()})
     enc = ECDH.encrypt(own,recipient_key,str(v), header)
     oct = MSG.pack( map(enc,base64) )
     return str(oct):base64()
   end)

   -- print out result
   print(JSON.encode(out))
   """

   keys = b"""
   {
     "own_private": "DYgWghvJuClxvHVCQSAfDpWQmeMQ4zh1/mGoNjM8UX0=",
     "own_public": "BAXRFKfMNSMge11U/cP+mCW2al166qIAY/cETmToEGmqe+4JnMdhmJ1FURvtUU+gA4QiEP+C7QFy/eoH+FDSRbw=",
     "recipient_public": "BCj962CsLq0Ey9Ibe6DEFSak4KqnQ5FhbNMv7MaMr6OzZZsnncUVOTrFK4Ym9WItAEMbpkGIOIjgfPESblAKlbw="
   }
   """

   data = b'{"msg":"top secret"}'

   result, errors = zenroom.execute(script, keys=keys, data=data)

   # Here we'd actually do something with the output
   print(result)


Note that the script parameter is the single required parameter, so here I
pass it it first as a positional argument; ``keys`` and ``data`` in contrast
are optional, so we choose to pass them as keyword arguments meaning we can
label them when calling the function, so reducing the risk of getting the
parameters in the wrong order.
