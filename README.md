# rsacrypt

Encrypt files with RSA

## Synopsis

```sh
# Usage:
rsacrypt [-e|-d|-g] [-f file] [-o outfile] [-pubkey key.pub] [-privkey key.pem] [-v]

# Exemples:

## Encryption:
rsacrypt # Default operation is encryption. Requires key.pub and key.pem to exists, be valid keys.
rsacrypt -e # Default input is STDIN, default output is STDOUT and default keys are key.pub and key.pem
rsacrypt -e -f secret.encrypted # Show output to STDOUT
rsacrypt -e -privkey private.pem -f secret.encrypted -o secret.txt

## Decryption:
rsacrypt -d # Defaults same as encryption
rsacrypt -d -f secret.encrypted # Show output to STDOUT
rsacrypt -d -privkey private.pem -f secret.encrypted -o secret.txt

## Key generation:
rsacrypt -g # Default keys are key.pub and key.pem
rsacrypt -g -s 2048
rsacrypt -g -s 8192 -pubkey my-key.pub -privkey private.pem
```

## Performances

Done with checks.sh

```
 [✔︎] File 1k   (1024 bytes)
 [✔︎] File 10k  (10240 bytes)
 [✔︎] File 100k (102400 bytes)
 [✔︎] File 1M   (1048576 bytes)
 [✔︎] File 10M  (10485760 bytes)

RSA keysize | Size (bytes)    | Encryption time (ms) | Decryption time (ms) | Checked (md5(decrypted) = md5(original)
----------- | ------------    | -------------------- | -------------------- | -------
2048 bits   | File : 1k       | Encryption : 136     | Decryption : 198     | Checking : OK
2048 bits   | File : 10k      | Encryption : 160     | Decryption : 323     | Checking : OK
2048 bits   | File : 100k     | Encryption : 423     | Decryption : 1562    | Checking : OK
2048 bits   | File : 1M       | Encryption : 3103    | Decryption : 14309   | Checking : OK
2048 bits   | File : 10M      | Encryption : 30035   | Decryption : 138420  | Checking : OK
4096 bits   | File : 1k       | Encryption : 84      | Decryption : 192     | Checking : OK
4096 bits   | File : 10k      | Encryption : 110     | Decryption : 354     | Checking : OK
4096 bits   | File : 100k     | Encryption : 275     | Decryption : 1994    | Checking : OK
4096 bits   | File : 1M       | Encryption : 2078    | Decryption : 18965   | Checking : OK
4096 bits   | File : 10M      | Encryption : 19908   | Decryption : 189150  | Checking : OK
8192 bits   | File : 1k       | Encryption : 88      | Decryption : 443     | Checking : OK
8192 bits   | File : 10k      | Encryption : 107     | Decryption : 953     | Checking : OK
8192 bits   | File : 100k     | Encryption : 318     | Decryption : 5991    | Checking : OK
8192 bits   | File : 1M       | Encryption : 2475    | Decryption : 58776   | Checking : OK
8192 bits   | File : 10M      | Encryption : 23840   | Decryption : 583420  | Checking : OK
```
