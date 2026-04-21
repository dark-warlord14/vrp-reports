# Google Linux package signing keys include 1024-bit DSA key

| Field | Value |
|-------|-------|
| **Issue ID** | [40055191](https://issues.chromium.org/issues/40055191) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Installer |
| **Platforms** | Linux |
| **Reporter** | pa...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-03-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Chrome Linux (Debian) Package Repository Ships Weak DSA 1024 bit key

**VERSION**

Chrome Version: any  

Operating System: any Debian / APT based

**REPRODUCTION CASE**

As per 14 March 2021, Google wants you to run the following command.

<http://web.archive.org/web/20210314103851/https://www.google.com/linuxrepositories/>

Instructions include:

wget -q -O - <https://dl.google.com/linux/linux_signing_key.pub> | sudo apt-key add -

1. Download <https://dl.google.com/linux/linux_signing_key.pub>
2. View OpenPGP key information.

gpg --keyid-format long --import --import-options show-only --with-fingerprint linux\_signing\_key.pub

3. Will show.

```
pub   dsa1024/A040830F7FAC5991 2007-03-08 [SC]  
      Key fingerprint = 4CCA 1EAF 950C EE4A B839  76DC A040 830F 7FAC 5991  
uid                            Google, Inc. Linux Package Signing Key <linux-packages-keymaster@google.com>  
sub   elg2048/4F30B6B4C07CB649 2007-03-08 [E]  
  
gpg: key 7721F63BD38B4796: 2 signatures not checked due to missing keys  
pub   rsa4096/7721F63BD38B4796 2016-04-12 [SC]  
      Key fingerprint = EB4C 1BFD 4F04 2F6D DDCC  EC91 7721 F63B D38B 4796  
uid                            Google Inc. (Linux Packages Signing Authority) <linux-packages-keymaster@google.com>  
sub   rsa4096/78BD65473CB3BD13 2019-07-22 [S] [expires: 2022-07-21]  

```

The first key shows dsa1024 which means a DSA key with only 1024 bits.

IMPACT

This effectively results in installing a weak cryptography key (DSA key with only 1024 bits) as a Debian package manager APT key.

What this does is using the wget command line downloader to download an APT signing key and then using Debian's apt-key utility to install the signing key to the system's APT keyring /etc/apt/trusted.gpg.

On Debian based platforms (using the APT package manager), every signing key installed on the system in /etc/apt/trusted.gpg (or drop-in folder /etc/apt/trusted.gpg.d) can sign any package Repository listed in /etc/apt/sources.list (or /etc/apt/sources.list.d drop-in folder).

Therefore when following Google Chrome instructions, installing linux\_signing\_key.pub, even the user's packages.debian.org APT repository (or any repository) could be signed by a man-in-the-middle attack (MITM). The user's package manager APT on Debian or Debian based distributions couldn't notice that since it would fully trust the weak DSA 1024 bit key for any repository. Any malicious installed package on Debian based platforms has full root access during installation, could overwrite any file, install malware, a backdoor.

This bug is worsened by the fact that the Chromium Debian Package Repository uses unauthenticated HTTP instead of authenticated HTTPS (TLS), for which I created a separate bug report. <https://bugs.chromium.org/p/chromium/issues/detail?id=1188054>

In January 2011 the National Institute of Standards and Technology (NIST) stated

<https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-131a.pdf>

> Disallowed after 2013

Google seems to agree with this assessment since their signing key file linux\_signing\_key.pub already contains a newer key rsa4096 (RSA with 4096 bits). There is however no need whatsoever to still include the weak dsa1024 in the signing key file linux\_signing\_key.pub.

**CREDIT INFORMATION**

Reporter credit: Patrick Schleizer, Whonix developer

## Timeline

### [Deleted User] (2021-03-15)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-03-15)

mmoss: Another one, PTAL?

[Monorail components: Internals>Installer]

### me...@chromium.org (2021-03-16)

It seems like we previously treated similar bugs as non-security issues (https://crbug.com/chromium/596074, https://crbug.com/chromium/594414). Given that precedent, I'll mark this as low severity.

### [Deleted User] (2021-03-16)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-03-16)

This issue was migrated from crbug.com/chromium/1188057?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### el...@chromium.org (2025-01-08)

Security shepherd: updating the subject line to reflect the actual problem; I'll take this one on for now.

### el...@chromium.org (2025-01-22)

I've passed this onto the team that maintains the Linux package signing repos, and they are working on internal bug [b/391616588](https://issues.chromium.org/issues/391616588). I'll keep you updated :)

### el...@chromium.org (2025-05-08)

Update on this: the internal team that manages these keys have not taken action yet.

### el...@chromium.org (2025-05-15)

The team that manages those keys has removed them from the published key set:

```
$ curl -o keys.pub https://dl.google.com/linux/linux_signing_key.pub ; gpg --keyid-format long --import --import-options show-only --with-fingerprint keys.pub
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 17382  100 17382    0     0   188k      0 --:--:-- --:--:-- --:--:--  190k
pub   rsa4096/7721F63BD38B4796 2016-04-12 [SC]
      Key fingerprint = EB4C 1BFD 4F04 2F6D DDCC  EC91 7721 F63B D38B 4796
uid                            Google Inc. (Linux Packages Signing Authority) <linux-packages-keymaster@google.com>
sub   rsa4096/E88979FB9B30ACF2 2023-02-15 [S] [expires: 2026-02-14]
sub   rsa4096/32EE5355A6BC6E42 2024-01-30 [S] [expires: 2027-01-29]
sub   rsa4096/FD533C07C264648F 2025-01-07 [S] [expires: 2028-01-07]

```

### ch...@google.com (2025-05-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Thank you reward for allowing us to make a security relevant change to better protect out Chrome supply chain.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-22)

Thank you for reporting this issue to us!

### ch...@google.com (2025-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you reward for allowing us to make a security relevant change to better protect out Chrome supply chain.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055191)*
