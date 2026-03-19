# Nmap Snippets

## Purpose

Fast and effective Nmap usage for enumeration during OSCP+.

Core rules:
- Speed first, depth second
- Always identify open ports quickly
- Follow up with targeted scans
- Avoid unnecessary noise

---

# 1. FAST PORT DISCOVERY (FIRST STEP)

## Full TCP scan (fastest reliable method)

```bash
nmap -p- --min-rate 1000 -T4 <target>
```

---

## Faster aggressive scan

```bash
nmap -p- --min-rate 5000 -T4 <target>
```

---

## Save output

```bash
nmap -p- --min-rate 1000 -T4 -oA initial <target>
```

---

# 2. TARGETED SERVICE SCAN

## Scan discovered ports

```bash
nmap -p <ports> -sC -sV <target>
```

---

## Aggressive service scan

```bash
nmap -p <ports> -sC -sV -T4 <target>
```

---

## Save output

```bash
nmap -p <ports> -sC -sV -oA services <target>
```

---

# 3. FULL COMPREHENSIVE SCAN

## Full TCP + scripts + version

```bash
nmap -p- -sC -sV -T4 <target>
```

---

## Aggressive (use carefully)

```bash
nmap -p- -A -T4 <target>
```

---

# 4. UDP SCANNING

## Top UDP ports

```bash
nmap -sU --top-ports 20 <target>
```

---

## Specific UDP ports

```bash
nmap -sU -p 53,67,68,69,123,161,162,500 <target>
```

---

## Combine TCP + UDP

```bash
nmap -sS -sU -p T:1-1000,U:53,161 <target>
```

---

# 5. STEALTH / FILTER EVASION

## SYN scan (requires root)

```bash
sudo nmap -sS <target>
```

---

## No ping (important for pivoting)

```bash
nmap -Pn <target>
```

---

## Fragment packets

```bash
nmap -f <target>
```

---

# 6. ENUMERATION SCRIPTS

## Default scripts

```bash
nmap -sC <target>
```

---

## Specific script

```bash
nmap --script smb-enum-shares -p 445 <target>
```

---

## Multiple scripts

```bash
nmap --script smb-enum-users,smb-enum-shares -p 445 <target>
```

---

## All scripts (noisy)

```bash
nmap --script all <target>
```

---

# 7. OUTPUT OPTIONS

## Normal + grepable + XML

```bash
-oA scanname
```

---

## Grep open ports

```bash
grep open scanname.nmap
```

---

## Extract ports quickly

```bash
grep open scanname.nmap | cut -d "/" -f1 | tr '\n' ',' | sed 's/,$//'
```

---

# 8. HOST DISCOVERY

## Ping scan

```bash
nmap -sn <subnet>
```

---

## No ping (firewalled)

```bash
nmap -Pn <target>
```

---

# 9. PIVOTING (PROXYCHAINS)

## TCP scan through proxy

```bash
proxychains nmap -sT -Pn <target>
```

---

## Service scan through proxy

```bash
proxychains nmap -sT -sV -Pn <target>
```

---

# 10. QUICK WORKFLOW (CRITICAL)

1. Fast full port scan

```bash
nmap -p- --min-rate 1000 -T4 <target>
```

---

2. Targeted service scan

```bash
nmap -p <ports> -sC -sV <target>
```

---

3. UDP quick check

```bash
nmap -sU --top-ports 20 <target>
```

---

4. Deeper scans as needed

---

# 11. COMMON FAILURE POINTS

- forgetting -Pn (pivoting)
- scanning too slow
- missing UDP services
- ignoring uncommon ports
- relying only on default scripts

---

# 12. PERFORMANCE TUNING

## Increase speed

```bash
--min-rate 5000
```

---

## Reduce retries

```bash
--max-retries 1
```

---

## Timing templates

```bash
-T4 (fast)
-T5 (very aggressive)
```

---

# 13. GOLDEN RULES

- Always start with full port scan (-p-)
- Always follow with -sC -sV
- Always check UDP basics
- Always save output (-oA)
- Always use -Pn when pivoting