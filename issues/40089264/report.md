# CVE-2017-5123: Chrome Sandbox escape through linux kernel vulnerability introduced in 4.13 in waitid

| Field | Value |
|-------|-------|
| **Issue ID** | [40089264](https://issues.chromium.org/issues/40089264) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2017-5123 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gr...@chromium.org |
| **Created** | 2017-10-09 |
| **Bounty** | $15,000.00 |

## Description

A linux kernel vulnerability introduced in 4.13 can be used to escape the chrome sandbox. 4.13 is a stable release and is included in Ubuntu 17.10 which is set to be released on October 19th. 

Vulnerability Details:
In the linux kernel, inside the waitid syscall, unsafe_put_user is used to copy the results to usermode. However, access_ok is not checked on the pointer, allowing a kernel address to be given, and overwrite arbitrary kernel memory.
https://github.com/torvalds/linux/blob/master/kernel/exit.c#L1614

Exploit:
It is quite easy to exploit the bug without SMAP. Simply write over the upper bytes of a structure pointer, such as the cgroup structures to point it at userland and control function pointers. Then rop to gain privileges and escape the sandbox.

I've included 2 different exploits. One is reliable and does not bypass SMAP. One is very unreliable, but includes a working SMAP bypass.
As it is a sandbox bypass and not a full RCE exploit they need to start with code execution inside the sandbox.
To test these proof of concepts, I modified the v8 code to compile in my sandbox escape and trigger it with javascript from the renderer.

These exploits are tested and working on ubuntu-17.10-beta2.
This is the right version:
md5sum ubuntu-17.10-beta2-desktop-amd64.iso is e47df00b078b5f9daed0871f0e90d33f
http://releases.ubuntu.com/17.10/ubuntu-17.10-beta2-desktop-amd64.iso

I've also included 2 standalone pocs which exploit the bug with and without SMAP by emulating the chrome sandbox.

The files include notes describing the exploit at the top.

Files included:
exploit_no_smap.c - reliable exploit from chrome assuming no smap
exploit_smap_bypass.c - unreliable exploit from chrome, bypassing smap
standalone_poc_no_smap.c - reliable standalone poc, which emulates the chrome sandbox and does not bypass smap
standalone_poc_smap_bypass.c - unreliable standalone poc, which emulates the chrome sandbox and bypasses smap
chrome_seccomp_filter - seccomp filter installed in standalone proof of concepts


## Attachments

- [exploit_no_smap.c](attachments/exploit_no_smap.c) (text/plain, 10.3 KB)
- [exploit_smap_bypass.c](attachments/exploit_smap_bypass.c) (text/plain, 25.4 KB)
- [standalone_poc_no_smap.c](attachments/standalone_poc_no_smap.c) (text/plain, 12.8 KB)
- [standalone_poc_smap_bypass.c](attachments/standalone_poc_smap_bypass.c) (text/plain, 28.3 KB)
- [chrome_seccomp_filter](attachments/chrome_seccomp_filter) (text/plain, 3.6 KB)

## Timeline

### el...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### oc...@chromium.org (2017-10-09)

Thanks for the report. Has this been reported upstream?

groeck, could you please take a look to see if this affects ChromeOS?

### gr...@chromium.org (2017-10-09)

It doesn't immediately affect ChromeOS since we don't ship anything above chromeos-4.4 at this time. Our latest development version is chromeos-4.12 which is not affected either. It _will_ affect chromeos-4.14 unless fixed.

However, unless I am really missing something, the bug is absolutely valid, critical, and does affect v4.13 and later kernels. I set severity and impact fields accordingly.

Kees, are you aware of this problem ? Do you know if it is already being worked on, and if there is a CVE ?

[ I assigned the bug to myself, primarily for tracking. Strictly speaking this would be a WontFix, since it doesn't apply to existing ChromeOS versions, but it is too critical to ignore. ]


### ke...@chromium.org (2017-10-09)

This is the first I've seen the issue. Introduced upstream in commit 4c48abe91be03d191d0c20cc755877da2cb35622. Assigned as CVE-2017-5123.

### gr...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### oc...@chromium.org (2017-10-09)

Thanks for investigating.

Removing Security-Impact-None since users using Linux would be impacted too. 

Severity-High for sandbox escape, since Critical is reserved for full chain exploits.

I think ExternalDependency is the right status here since there's nothing actionable for us right now.

### ke...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### gr...@chromium.org (2017-10-10)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-10-10)

Thanks for the quick response. Has this been reported upstream or to someone who
 will fix it? Or is that something I need to do?

### gr...@chromium.org (2017-10-10)

Fix should be straightforward and a two-liner. I'll be happy to do it unless someone else wants to pick it up. Kees - is it ok to submit a patch upstream ? If so, anything to watch out for ?


### gr...@chromium.org (2017-10-10)

... and if I submit a patch, can/should I add the submitter of this bug as Reported-by: ?


### ch...@gmail.com (2017-10-10)

Of course I'd like to be acknowledged in the "reported by" field if possible :)

### ke...@chromium.org (2017-10-10)

I've reported this upstream (with credit to Chris), it should be publish on the 12th. (Technically a 4 line change, since it's needed in two places, but yes.) :)

### gr...@chromium.org (2017-10-10)

#13: I assume that means that someone else (Al Viro ?) will submit a patch ?


### ke...@chromium.org (2017-10-10)

I submitted the patch already, but tried to open discussion about just doing a revert. I think they're going to just go with the patch instead.

### gr...@chromium.org (2017-10-10)

Great, thanks!


### gr...@chromium.org (2017-10-17)

Fixed upstream with commit 96ca579a1ecc ("waitid(): Add missing access_ok() checks"). Fixed in v4.13.7 with commit sha 3da54587cf4c. Marking as WontFix (not applicable to any chromeos kernels, and fixed in all affected upstream kernels).


### ke...@chromium.org (2017-10-17)

Doesn't this qualify for the Vulnerability Rewards Program?

### oc...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-26)

Congratulations chrissalls5@! The VRP panel decided to award $15,000 for this bug!  A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2017-10-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-10-26)

Wow. Thank you very much!!

### sh...@chromium.org (2018-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-05-28)

[Comment Deleted]

### aw...@google.com (2019-05-28)

[Comment Deleted]

### is...@google.com (2019-05-28)

This issue was migrated from crbug.com/chromium/772848?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089264)*
