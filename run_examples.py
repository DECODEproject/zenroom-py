from zenroom import zenroom

print("EXAMPLE: HELLO WORLD\n")

script = b"print('Hello world')"
output, errors = zenroom.execute(script, verbosity=1)

print("OUTPUT>>>")
print(output.decode())
print("<<<END OUTPUT")
print("ERRORS>>>")

for error in errors:
    print(error)

print("<<<END ERRORS")


print("\n\nEXAMPLE: SIMPLE ZENCODE")

script = b"""ZEN:begin(0)
ZEN:parse([[
Scenario 'coconut': "To run over the mobile wallet the first time and store the output as keypair.keys"
         Given that I am known as 'foofofofodos'
         When I create my new credential request keypair
         Then print all data
]])

ZEN:run()"""
output, errors = zenroom.execute(script, verbosity=1)

print("OUTPUT>>>")
print(output.decode())
print("<<<END OUTPUT")
print("ERRORS>>>")

for error in errors:
    print(error)

print("<<<END ERRORS")


