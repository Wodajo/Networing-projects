# NMAT
In this project I take old, boring, well known nmap ideas and create my own, brand new exciting version.

Brace yourself for the scanning, that is coming.

## How it works
1. First is ICMP echo request scan (prepares active host IP list). It can be skipped.
2. For next scans you can use active hosts list from ICMP, or enter your own range of addresses
3. Ports are always entered manually

## To do:
- threading
- cleaning code (old comments, unused code)
- make IP&ports selection even more usable
- TCP SYN-ACK port scan is, well, quite raw. Prettify it.
- Make new TCP port scans

After making some basic scanning tools - create a new tool for precise and sneaky scanning:D