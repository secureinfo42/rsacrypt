#!/bin/sh

gen_sample()
{
	file="$1"
	count=$2
	bs=$3
	printf "\r [\033[1;33m✺\033[0m] File %-4s" "$file"
	dd if=/dev/urandom of=$file count=$count bs=$bs >/dev/null 2>&1
	sz="$(stat -c "%s" "$file")"
	printf "\r [\033[1;32m✔︎\033[0m] File %-4s (%s bytes)\n" "$file" "$sz"
}

gen_keys()
{
	SIZERSA=$1

	rm -f *.enc *.dec
	mkdir -p keys

	echo
	printf "[+] Generating RSA $SIZERSA keys..."
	SIZERSA=8192
	python3.7 rsa_encrypt_file.py gen $SIZERSA keys/private.key keys/public.pem
	printf "\b\b\b, done.\n"

}

clear

echo > report.txt
echo "=== Full RSA encryption test, buffer size : 128 bytes ===" >> report.txt
echo >> report.txt

echo
echo "[+] Generating sample from '/dev/urandom' files..."
echo

gen_sample 1k   1   1024
gen_sample 10k  10  1024
gen_sample 100k 100 1024
gen_sample 1M   1   $((1024*1024))
gen_sample 10M  10  $((1024*1024))

printf -- "\n%-11s | %-15s | %-20s | %-20s | %s" "RSA keysize" "Size (bytes)" "Encryption time (ms)" "Decryption time (ms)" "Checked (md5(decrypted) = md5(original)" >> report.txt
printf -- "\n%-11s | %-15s | %-20s | %-20s | %s" "-----------" "------------" "--------------------" "--------------------" "-------" >> report.txt
printf -- "\n%-11s | %-15s | %-20s | %-20s | %s" "RSA keysize" "Size (bytes)" "Encryption time (ms)" "Decryption time (ms)" "Checked (md5(decrypted) = md5(original)"
printf -- "\n%-11s | %-15s | %-20s | %-20s | %s" "-----------" "------------" "--------------------" "--------------------" "-------"

for s in 2048 4096 8192 ; do

	python3 rsacrypt.py -g -s $s

	for f in 1k 10k 100k 1M 10M ; do

		rm -f $f.enc $f.dec
		sz=$(stat -c "%s" "$f")

		printf "\n%-11s | " "$s bits"
		printf "File : %-8s | " "$f"
		printf "Encryption..."

		te1=$(date +"%s%N")
		python3 rsacrypt.py -e -f $f -o $f.enc
		te2=$(date +"%s%N")
		te=$(echo "($te2-$te1)/1000000"|bc)
		printf "\b\b\b : %-7s" "$te"

		printf " | Decryption..."
		td1=$(date +"%s%N")
		python3 rsacrypt.py -d  -f $f.enc -o $f.dec
		td2=$(date +"%s%N")
		td=$(echo "($td2-$td1)/1000000"|bc)
		printf "\b\b\b : %-7s" "$td"

		c=$(md5sum $f $f.dec|cut -d' ' -f1|uniq|wc -l|grep -sq 1 && echo OK || echo KO)
		printf " | Checking : $c"

		printf -- "\n%-11s | %-15s | %-20s | %-20s | %s" "$s" "$sz" "$te" "$td" "$c" >> report.txt

	done

done

echo >> report.txt

rm -f *.enc *.dec


