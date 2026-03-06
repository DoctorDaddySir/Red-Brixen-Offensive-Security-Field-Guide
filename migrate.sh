#!/usr/bin/env bash
set -euo pipefail

echo "Resetting content files to COMING SOON..."

find . -type f -name "*.md" \
! -name "README.md" \
! -name "00_START_HERE.md" \
! -name "*index.md" \
! -name "*toc.md" \
| while read file
do
    echo "# COMING SOON" > "$file"
    echo "Reset: $file"
done


echo
echo "Creating hacker mindset section..."

mkdir -p hacker-mindset

###################################
# Hacker Mindset README
###################################

cat > hacker-mindset/README.md << 'EOF'
# Hacker Mindset

Technical knowledge alone does not make a strong offensive security professional.

The real skill is **how you think about systems, problems, and constraints.**

This section focuses on developing the **mental models used by experienced attackers**.

Topics include:

- Enumeration mindset
- Hypothesis driven hacking
- Pattern recognition
- Breaking assumptions
- Lateral thinking
- Practicing creativity in security

EOF


###################################
# Table of Contents
###################################

cat > hacker-mindset/00_mindset_index.md << 'EOF'
# Hacker Mindset Index

Start here when practicing offensive thinking.

## Core Thinking Models

enumeration_mindset.md  
hypothesis_loop.md  
pattern_recognition.md  
assumption_breaking.md  

## Practice Drills

practice_reverse_engineering.md  
practice_service_analysis.md  
practice_exploit_ideas.md  

## OSCP Mindset

oscp_exam_mindset.md

EOF


###################################
# Enumeration Mindset
###################################

cat > hacker-mindset/enumeration_mindset.md << 'EOF'
# Enumeration Mindset

Enumeration is not running tools.

Enumeration is **building a mental model of the system.**

Questions to constantly ask:

- What services exist?
- What accounts exist?
- What trust relationships exist?
- What technologies are in use?
- What version differences exist?

Goal:

Turn the target into a **map of attack paths**.

Practice:

Pick a machine and list **every possible attack surface** before exploiting anything.

EOF


###################################
# Hypothesis Loop
###################################

cat > hacker-mindset/hypothesis_loop.md << 'EOF'
# Hypothesis Driven Hacking

Experienced hackers operate in loops:

1. Observe
2. Hypothesize
3. Test
4. Refine

Example:

Observation:
SMB share contains backup scripts.

Hypothesis:
Scripts may contain credentials.

Test:
Download scripts and inspect.

Refine:
Credentials found → attempt lateral movement.

Practice:

When solving boxes, write down **three hypotheses before testing anything.**

EOF


###################################
# Pattern Recognition
###################################

cat > hacker-mindset/pattern_recognition.md << 'EOF'
# Pattern Recognition

Most machines fall into patterns.

Examples:

- CMS exploit → webshell → credential reuse
- SMB share → password leak → WinRM
- SUID binary → GTFOBins
- Cron job → script hijack

Developing intuition means seeing these patterns quickly.

Practice:

After solving a box, identify the **pattern category** it belongs to.

EOF


###################################
# Assumption Breaking
###################################

cat > hacker-mindset/assumption_breaking.md << 'EOF'
# Breaking Assumptions

Security failures often occur because developers assume something is safe.

Examples:

- "Users won't see this directory"
- "No one will guess this endpoint"
- "The service won't run as root"

Attackers succeed by **challenging assumptions**.

Practice:

Whenever you see a design choice, ask:

"What assumption does this rely on?"

EOF


###################################
# Practice Reverse Engineering
###################################

cat > hacker-mindset/practice_reverse_engineering.md << 'EOF'
# Reverse Engineering Thinking Practice

Download random binaries from:

- HackTheBox
- CTF challenges

Questions to ask:

- What input does it accept?
- What libraries does it use?
- What assumptions does it make?

Goal:

Train the brain to analyze **unknown software quickly**.

EOF


###################################
# Service Analysis Practice
###################################

cat > hacker-mindset/practice_service_analysis.md << 'EOF'
# Service Analysis Practice

Choose a random network service.

Examples:

FTP
SMTP
SMB
LDAP

Ask:

- What authentication exists?
- What commands exist?
- What trust relationships exist?

Goal:

Understand how services behave.

EOF


###################################
# Exploit Idea Practice
###################################

cat > hacker-mindset/practice_exploit_ideas.md << 'EOF'
# Exploit Idea Practice

Pick a real vulnerability.

Example:

CVE entry.

Before reading the exploit:

Ask yourself:

- What inputs are attacker controlled?
- Where could memory corruption occur?
- Could authentication be bypassed?

Then compare with the real exploit.

EOF


###################################
# OSCP Mindset
###################################

cat > hacker-mindset/oscp_exam_mindset.md << 'EOF'
# OSCP Exam Mindset

Key principles:

1. Enumeration solves most machines
2. Stay methodical
3. Avoid rabbit holes
4. Reset and rethink when stuck

Recommended loop:

1. Scan
2. Enumerate
3. Attempt exploitation
4. Re-enumerate with new context

Most OSCP boxes follow **predictable attack chains**.

The challenge is recognizing them quickly.

EOF


echo
echo "Repository content reset complete."
echo "Hacker mindset section created."
