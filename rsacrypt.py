#!/usr/bin/env python3.11

###############################################################################
#
# Libz
#
##

try:
	from Crypto.PublicKey import RSA
	from Crypto.Cipher import PKCS1_OAEP
except:
	print("Failed to import Crypto. Tr: pip3 install pycryptodome")
	exit()
from base64 import encodebytes,decodebytes
from sys import argv, exit
from zlib import compress,decompress



###############################################################################
#
# Globalz
#
##

DEFAULT_RSA_KEY_SIZE = 4096
DEFAULT_KEY_PUB      = "key.pub"
DEFAULT_KEY_PEM      = "key.pem"



###############################################################################
#
# Funcz
#
##

def usage(errcode=0):
	APP = __file__.split("/")[-1]
	print("\n# Usage:")

	print("\033[1;35m%s\033[0m [-e|-d|-g] [-f file] [-o outfile] [-pubkey key.pub] [-privkey key.pem] [-v]" % APP)


	print("\n# Exemples:")

	print("\n## Encryption:")
	print("\033[1;35m%s\033[0m \033[0;34m# Default operation is encryption. Requires %s and %s to exists, be valid keys.\033[0m" % (APP,DEFAULT_KEY_PUB,DEFAULT_KEY_PEM))
	print("\033[1;35m%s\033[0m -e \033[0;34m# Default input is STDIN, default output is STDOUT and default keys are %s and %s\033[0m" % (APP,DEFAULT_KEY_PUB,DEFAULT_KEY_PEM))
	print("\033[1;35m%s\033[0m -e -f secret.encrypted \033[0;34m# Show output to STDOUT\033[0m" % APP)
	print("\033[1;35m%s\033[0m -e -privkey private.pem -f secret.encrypted -o secret.txt" % APP)

	print("\n## Decryption:")
	print("\033[1;35m%s\033[0m -d \033[0;34m# Defaults same as encryption\033[0m" % APP)
	print("\033[1;35m%s\033[0m -d -f secret.encrypted \033[0;34m# Show output to STDOUT\033[0m" % APP)
	print("\033[1;35m%s\033[0m -d -privkey private.pem -f secret.encrypted -o secret.txt" % APP)

	print("\n## Key generation:")
	print("\033[1;35m%s\033[0m -g \033[0;34m# Default keys are %s and %s\033[0m" % (APP,DEFAULT_KEY_PUB,DEFAULT_KEY_PEM))
	print("\033[1;35m%s\033[0m -g -s 2048" % APP)
	print("\033[1;35m%s\033[0m -g -s 8192 -pubkey my-key.pub -privkey private.pem" % APP)

	exit(errcode)



###############################################################################
#
# Funcz:RSA
#
##

def rsa_getsize(keyfile):
	try:
		return(RSA.importKey( open(keyfile,"rb").read() ).size_in_bits())
	except Exception as error:
		print(error)
		exit(1)

def rsa_keygen(key_size,keyfile_private="key.pem",keyfile_public="key.pub"):
	key = RSA.generate(key_size)
	k = key.exportKey('PEM')
	p = key.publickey().exportKey('PEM')
	open(keyfile_private,'w').write(k.decode())
	open(keyfile_public,'w').write(p.decode())
	return(keyfile_private,keyfile_public)

def rsa_encrypt(src,keyfile="key.pub"):
	key_sze = int(rsa_getsize(keyfile)/16)
	rsa = PKCS1_OAEP.new( RSA.importKey( open(keyfile,"rb").read() ) )
	arr = [ src[x:x+key_sze] for x in range(0,len(src),key_sze) ]
	arr = [ rsa.encrypt(x) for x in arr ]
	enc = b"".join(arr)
	enc = encodebytes(enc)
	return(enc)

def rsa_decrypt(src,keyfile="key.pem",key_sze=DEFAULT_RSA_KEY_SIZE):
	key_sze = int(rsa_getsize(keyfile)/8)
	src = decodebytes(src)
	rsa = PKCS1_OAEP.new( RSA.importKey( open(keyfile,"rb").read() ) )
	arr = [ src[x:x+key_sze] for x in range(0,len(src),key_sze) ]
	arr = [ rsa.decrypt(x) for x in arr ]
	dec = b"".join(arr)
	return(dec)

def rsa_file_encrypt(infile,outfile,keyfile="key.pub"):
	open(outfile,"wb").write(
		rsa_encrypt(
			open(infile,"rb").read(),
			keyfile
		)
	)

def rsa_file_decrypt(infile,outfile,keyfile="key.pem"):
	open(outfile,"wb").write(
		rsa_decrypt(
			open(infile,"rb").read(),
			keyfile
		)
	)



###############################################################################
#
# Argz
#
##

verbose  = 0
key_size = DEFAULT_RSA_KEY_SIZE
infile   = "/dev/stdin"
outfile  = "/dev/stdout"
pubkey   = DEFAULT_KEY_PUB # "key.pub"
privkey  = DEFAULT_KEY_PEM # "key.pem"
op       = "encode"

i=0
for i in range(1,len(argv)):

	a = argv[i]

	if a == "-f":
		i += 1
		infile = argv[i]

	if a == "-o":
		i += 1
		outfile = argv[i]

	if a == "-s":
		i += 1
		key_size = argv[i]

	if a == "-pubkey":
		i += 1
		pubkey = argv[i]

	if a == "-privkey":
		i += 1
		privkey = argv[i]

	if a == "-v":
		verbose = 1

	if a == "-h":
		usage(0)

	if a == "-g" or a == "--gen":
		op = "keygen"

	if a == "-d" or a == "--decode":
		op = "decode"

	if a == "-e" or a == "--encode":
		op = "encode"

	o = a



###############################################################################
#
# Main
#
##

if verbose == 1:
	print(f"\n\033[1;34mSummary\033[0m")
	print(f"\033[1;34m-------\033[0m")
	print(f"infile   : \033[1;35m{infile}\033[0m")
	print(f"outfile  : \033[1;35m{outfile}\033[0m")
	print(f"pubkey   : \033[1;35m{pubkey}\033[0m")
	print(f"privkey  : \033[1;35m{privkey}\033[0m")
	print(f"key_size : \033[1;35m{key_size}\033[0m")
	print(f"op ..... : \033[1;35m{op}\033[0m")
	print(f"\n\033[1;34mOutput\033[0m")
	print(f"\033[1;34m-------\033[0m")


if op == "keygen":

	key_size = int(key_size)
	rsa_keygen(key_size,privkey,pubkey)
	print(f"Private key: {privkey}\nPublic key : {pubkey}")

elif op == "encode":

	rsa_file_encrypt(infile,outfile,pubkey)

elif op == "decode":

	rsa_file_decrypt(infile,outfile,privkey)

