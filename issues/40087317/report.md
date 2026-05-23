# Security: DoCanonicalizeMailtoURL() fails to canonicalize characters leading to command injection

| Field | Value |
|-------|-------|
| **Issue ID** | [40087317](https://issues.chromium.org/issues/40087317) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | jo...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2017-04-12 |
| **Bounty** | $1,000.00 |

## Description

I saw interesting report this so i did via security@google.com, Eduardo told me that is a different program and pass me that.

A video was attached, feel free to contact me for further information.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2017-04-12)

The video begins with the text:

"When Google Chrome call to mailto protocol on Unix it call via xdg-email which is a bash script, Google Chrome don't sanitize the * and when Bash interpret it expand it as directory.

This issue was tested in other browser as Firefox and the * is not expanded showing the char *.

The next proof of concept shows how expand in bash when Google Chrome call it and how in other browsers dont works.

This can allow on some conditions to exfiltrate de directory of the user.

### el...@chromium.org (2017-04-12)

I wasn't able to reproduce this on my Linux machine with 57.0.2987.0. The fake email address contains a literal * instead of the expanded list of folder names.

The last checkin to our //src/third_party/xdg-utils/scripts/xdg-email was six years ago (https://chromium.googlesource.com/chromium/deps/xdg-utils.git/+/55dfec5814ddb0f4f3f1cd67b673fc1325667a5a) but I don't think that's relevant in this issue (and it's not clear to me that it's even our fork of this script that's the one that runs.)

Instead //src/chrome/browser/platform_util_linux.cc is where we invoke the XDGEmail(const std::string& email) function, which calls RunCommand("xdg-email", base::FilePath(), email); That doesn't appear to perform any sort of escaping on the arguments.

[Monorail components: Internals>PlatformIntegration]

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### jo...@gmail.com (2017-04-13)

Thats the checksum of maa file xdg-email
user@host:~$ md5sum /usr/bin/xdg-email.save 
59c01c2eb1ecc27a6d593356c1afbce5  /usr/bin/xdg-email.save

Thats my xdg-utils version
user@host:~$ dpkg -s xdg-utils | grep Version
Version: 1.1.1-1ubuntu2

Thats my Chrome version
Google Chrome 57.0.2987.133 (64-bit)

The problem here is that Chrome dont apply URL Encode as Firefox and other browsers do so when the strings 'x * x' appear it expand the metachar, in Firefox for example appears like this 'x%20*%20x' and obviously this is not expand because need spaces


### jo...@gmail.com (2017-04-13)

Obviusly xdg-utils dont apply any type of protection on this side, but its obvious that Chrome dont URL Encode that and thats because this happen

### el...@chromium.org (2017-04-13)

The URL should be encoded at the point that it reaches here:

void OpenExternal(Profile* profile, const GURL& url) {
  if (url.SchemeIs("mailto"))
    XDGEmail(url.spec());

Canonicalization of mailto URIs is performed by the DoCanonicalizeMailtoURL function.

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### el...@chromium.org (2017-04-13)

Would you mind pasting your original repro code into this bug? It keeps getting lost and retyping it from the video is tiresome. :)

### jo...@gmail.com (2017-04-13)

var iframe = document.createElement('iframe');
var a = 'XXXXXXXXXXXXXXXXXXXXx * ../* ../../* x?subject=x * ../* ../../* x';
iframe.src = 'mailto: f00@f00,' + a;
document.body.appendChild(iframe);


### el...@chromium.org (2017-04-13)

This is indeed a bug in DoCanonicalizeMailtoURL().

Given "mailto:a@b.com?subject=1 2 3", the URL passed externally is canonicalized to "mailto:a@b.com?subject=1%202%203"

However, given "mailto:a@b.com, b@c * x?subject=1 2 3", the URL passed externally is canonicalized to "mailto:a@b.com, b@c * x?subject=1%202%203", leaving the spaces unencoded.

That's because DoCanonicalizeMailtoURL uses a more lax encoding strategy for the "path" portion of the URL than for the query portion.

Changing  
   if (uch < 0x20 || uch >= 0x80)

to 
   if (uch <= 0x20 || uch >= 0x80)

... is the simplest fix for this issue, but it assumes that there are no other problematic characters.

[Monorail components: -Internals>PlatformIntegration Blink>Network]

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### jo...@gmail.com (2017-04-13)

[Comment Deleted]

### el...@chromium.org (2017-04-13)

Inside Windows' OpenExternalOnFileThread() function, we attempt to prevent passing additional command line arguments to the mail client program by wrapping the invoked URL with " (0x22) characters. However, this is ineffective in this scenario because that function assumes that all quotes in the URL have already been escaped. DoCanonicalizeMailtoURL's limitation makes this an unsafe assumption, and an attacker can introduce his own " character and pass additional arguments to the mail program. 

   "mailto:a@b.com, " -setmailserver=whatever.com"

We've seen previous attacks of this nature, e.g. http://seclists.org/fulldisclosure/2004/Mar/410


This probably deserves at least Severity Medium and possibly Severity High, because mailto is a direct path out of the renderer sandbox, and we don't have any way to know what sort of badness a mail client may do when passed arbitrary arguments.

### np...@chromium.org (2017-04-13)

elawrence -- Since you've got a proposed fix, would you like to land it?

I'd call it medium since it's not clear that it can cause code execution, unless arbitrary bash commands can be injected. It can leak existence of directories, yes? 

### el...@chromium.org (2017-04-13)

Re #16: I don't know enough about how bash works to understand whether a command injection is possible on that platform. 

On Windows, the vector shown in #15 means that you can pass additional arguments to the target mail application. In the past Microsoft has rated such problems as RCE/Critical. I do not know whether any popular mail applications allow RCE or equivalent high-severity vulnerabilities today, but because we don't have any good way to tell, we should probably assume that they do.

### sh...@chromium.org (2017-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-14)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2017-04-14)

No, this isn't a regression.

https://codereview.chromium.org/2817213002

### bu...@chromium.org (2017-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/484ff36cdcb8dcf5efa999a471d1d509c0a8a5f2

commit 484ff36cdcb8dcf5efa999a471d1d509c0a8a5f2
Author: elawrence <elawrence@chromium.org>
Date: Mon Apr 17 22:39:49 2017

Improve canonicalization of mailto url path components

The canonicalization of the path component of mailto urls is too lax, leading to
information disclosure and possible command injection attacks against mail
clients. To fix this, we will percent-encode more characters in the path
component of mailto urls, matching other browsers.

BUG=711020
TEST=url_unittests

Review-Url: https://codereview.chromium.org/2817213002
Cr-Commit-Position: refs/heads/master@{#465046}

[modify] https://crrev.com/484ff36cdcb8dcf5efa999a471d1d509c0a8a5f2/url/url_canon_mailtourl.cc
[modify] https://crrev.com/484ff36cdcb8dcf5efa999a471d1d509c0a8a5f2/url/url_canon_unittest.cc


### bu...@chromium.org (2017-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/468109cc91a8c236f4e74bd9e2dd094db5464d57

commit 468109cc91a8c236f4e74bd9e2dd094db5464d57
Author: alexmos <alexmos@chromium.org>
Date: Mon Apr 17 23:47:38 2017

Revert of Improve canonicalization of mailto url path components (patchset #2 id:20001 of https://codereview.chromium.org/2817213002/ )

Reason for revert:
appears to be breaking fast/url/mailto.html on at least the Mac bots:
https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Mac10.10/builds/32726
https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Mac10.12/builds/1614
https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Mac10.9/builds/45169

diffs:
-PASS canonicalize('mailto:addr1, addr2') is 'mailto:addr1, addr2'
+FAIL canonicalize('mailto:addr1, addr2') should be mailto:addr1, addr2. Was mailto:addr1,%20addr2.

Original issue's description:
> Improve canonicalization of mailto url path components
>
> The canonicalization of the path component of mailto urls is too lax, leading to
> information disclosure and possible command injection attacks against mail
> clients. To fix this, we will percent-encode more characters in the path
> component of mailto urls, matching other browsers.
>
> BUG=711020
> TEST=url_unittests
>
> Review-Url: https://codereview.chromium.org/2817213002
> Cr-Commit-Position: refs/heads/master@{#465046}
> Committed: https://chromium.googlesource.com/chromium/src/+/484ff36cdcb8dcf5efa999a471d1d509c0a8a5f2

TBR=brettw@chromium.org,elawrence@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=711020

Review-Url: https://codereview.chromium.org/2823883005
Cr-Commit-Position: refs/heads/master@{#465063}

[modify] https://crrev.com/468109cc91a8c236f4e74bd9e2dd094db5464d57/url/url_canon_mailtourl.cc
[modify] https://crrev.com/468109cc91a8c236f4e74bd9e2dd094db5464d57/url/url_canon_unittest.cc


### bu...@chromium.org (2017-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d75485096f20f4ba7365106c46200b18c0fcc848

commit d75485096f20f4ba7365106c46200b18c0fcc848
Author: elawrence <elawrence@chromium.org>
Date: Tue Apr 18 20:44:20 2017

Reland of 'Improve canonicalization of mailto url path components'

The canonicalization of the path component of mailto urls is too lax,
leading to information disclosure and possible command injection attacks
against mail clients. To fix this, we percent-encode more characters in
the path component of mailto urls, matching other Firefox/IE/Edge.

The original land of this patch (via 2817213002) omitted an update to
layout tests.

BUG=711020
TEST=url_unittests,run-webkit-tests fast/url

Review-Url: https://codereview.chromium.org/2820373002
Cr-Commit-Position: refs/heads/master@{#465357}

[modify] https://crrev.com/d75485096f20f4ba7365106c46200b18c0fcc848/third_party/WebKit/LayoutTests/fast/url/mailto-expected.txt
[modify] https://crrev.com/d75485096f20f4ba7365106c46200b18c0fcc848/third_party/WebKit/LayoutTests/fast/url/script-tests/mailto.js
[modify] https://crrev.com/d75485096f20f4ba7365106c46200b18c0fcc848/url/url_canon_mailtourl.cc
[modify] https://crrev.com/d75485096f20f4ba7365106c46200b18c0fcc848/url/url_canon_unittest.cc


### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-04-20)

+awhalley@ for security merge review

### aw...@chromium.org (2017-04-20)

abdulsyed@ - good for 59

### sh...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-04-21)

approving merge for m59 based on #28. 

### bu...@chromium.org (2017-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2

commit 18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2
Author: Eric Lawrence <elawrence@chromium.org>
Date: Fri Apr 21 20:00:58 2017

M59 Merge of 'Improve canonicalization of mailto url path components'

The canonicalization of the path component of mailto urls is too lax,
leading to information disclosure and possible command injection attacks
against mail clients. To fix this, we percent-encode more characters in
the path component of mailto urls, matching other Firefox/IE/Edge.

The original land of this patch (via 2817213002) omitted an update to
layout tests.

BUG=711020
TEST=url_unittests,run-webkit-tests fast/url

Review-Url: https://codereview.chromium.org/2820373002
Cr-Commit-Position: refs/heads/master@{#465357}
(cherry picked from commit d75485096f20f4ba7365106c46200b18c0fcc848)

Review-Url: https://codereview.chromium.org/2833983005 .
Cr-Commit-Position: refs/branch-heads/3071@{#128}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2/third_party/WebKit/LayoutTests/fast/url/mailto-expected.txt
[modify] https://crrev.com/18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2/third_party/WebKit/LayoutTests/fast/url/script-tests/mailto.js
[modify] https://crrev.com/18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2/url/url_canon_mailtourl.cc
[modify] https://crrev.com/18bf33f85e323bf4bf93f3db3c42e542dd9cb9f2/url/url_canon_unittest.cc


### jo...@gmail.com (2017-04-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

Congratulations! The VRP panel decided to award $1,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### jo...@gmail.com (2017-05-05)

Is a CVE going to be assigned to this issue?

### aw...@google.com (2017-05-05)

Hi Jose. This bug is currently marked as Security_Impact-Beta suggesting it doesn't impact a shipping Stable version of Chrome, which would mean it wouldn't get a CVE.  Though very interested to know if that's incorrect!

### el...@chromium.org (2017-05-05)

awhalley@ - This definitely impacts stable, going back at least 20 releases or more. The assignment of Security_Impact-Head in c#16 was in error, and the sheriffbot picked that up and ran with it.

### aw...@google.com (2017-05-05)

Thanks elawrence@!  In that case this will get assigned a CVE when M59 is released as Stable.

### jo...@gmail.com (2017-05-05)

[Comment Deleted]

### jo...@gmail.com (2017-05-05)

@elawrence this error could have had an impact on the bounty resolution? Because i was awarded with 1k usd bounty what i dont see enough, for example last year i reported a xss in mozilla socorro and i was awarded with 2,5k. I dont understand nothing.

### aw...@google.com (2017-05-05)

No, it would not have affected the bounty award. One thing that might have is report quality. Please see g.co/ChromeBugRewards, but we wouldn't consider this report to be High Quality which limits reward amount. Also, you seem to keep deleting the video?

### jo...@gmail.com (2017-05-05)

[Comment Deleted]

### jo...@gmail.com (2017-05-05)

@awhalley the video was undeleted, let me know if this is going to be public to delete it, because in it appears personal info that i dont want to make public.

### aw...@google.com (2017-05-05)

Thanks jose, I've deleted it again just so we don't expose it accidentally; we should have the information we need at this point.

I'd also be interested in hearing about your experiences with the Chrome and the other Google VRPs, and if you have any suggestions on how to make reporting easier and better. Drop me a line at awhalley@chromium.org

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/711020?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087317)*
