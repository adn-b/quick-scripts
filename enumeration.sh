#!/bin/bash

# Script for school pen testing class.

# CHANGE e.g "10.0.0"
iprange="first_3_octets_of_your_ip"

task() {
    ttl="64"
    packetsize="64"
    timeout="2"

    > nmap_output.txt

    echo "DNS Information:"
    cat /etc/resolv.conf

    echo "ICMP RESULT [IPV4] - ARP RESULT [MAC ADDRESS] - OPEN PORTS"
    for host in {0..254}; do
        # CHANGE e.g. 10.0.0.$host"
        ip="$iprange.$host"
        icmp=`sudo ping -W 2 -c 1 -t $ttl -s $packetsize $ip`
        if [[ "${icmp}" == *"icmp_seq"* ]]; then
            ipv4=$ip
        else
            ipv4="Offline"
        fi
        arp=`sudo arping -w 2 -c 1 -r $ip`
        if [[ "${arp}" == *"Timeout"* ]]; then
            mac="Offline"
        else
            mac=$arp
        fi

        ports=()
        for port in {20,22,25,80,443}; do
            declare -a ports
            port_result=$(nmap --host-timeout 5s -p $port "${ip}")
            echo "$port_result" >> nmap_output.txt

            if [[ "${port_result}" == *"open"* ]]; then
                ports+=($port)
            fi
        done
        echo "$ipv4 - $mac - ${ports[*]}"
    done
}

task