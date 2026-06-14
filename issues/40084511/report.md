# Security: Parameter sanitization failure in DevTools leads to privileged script execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40084511](https://issues.chromium.org/issues/40084511) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Same vulnerability as <https://crbug.com/chromium/607939>. Fix for it is insufficient as it checks only if "remoteFrontendUrl" starts with "<https://chrome-devtools-frontend.appspot.com/>" but fails to sanitize any data that follows it. Since the remoteFrontendUrl is decoded in the remote frontend page before the iframe src's is written via document.write(), arbitrary html tags can be injected into the page.

Example Simple URL that shows alert if XSS-Auditor is disabled (via cmdline):  

chrome-devtools://devtools/remote/serve\_rev/@199588/devtools.html?remoteFrontendUrl=<https://chrome-devtools-frontend.appspot.com/%27%3E%3C/iframe%3E%3Ciframe%20src=%27javascript:alert(document.domain)>

I was able to achieve XSS-Auditor bypass for that page by splitting the JS snippet [executed via onerror event on an img tag] across two parameters.

Format for URL:  

chrome-devtools://devtools/remote/serve\_rev/@199588/devtools.html?[JSSNIP2]=0&remoteFrontendUrl=[https://chrome-devtools-frontend.appspot.com/%27%3E%3C/iframe%3E%3Cimg%20src=x%20onerror=%27javascript:[JSSNIP1]](https://chrome-devtools-frontend.appspot.com/%27%3E%3C/iframe%3E%3Cimg%20src=x%20onerror=%27javascript:%5BJSSNIP1%5D)

(Working PoC URL is attached).

**VERSION**  

Chrome Version: 51.0.2704.84 m + stable  

Operating System: All

**REPRODUCTION CASE**  

Copy-paste the full URL from the attached Devtools-Crafted-URI2.txt into Chrome omnibox.  

For demo purposes, it displays the content of C:\ drive

SUGGESTED FIX  

In addition to existing check, It should check for quote character required for injection in the remoteFrontendUrl param data. Attached modified function [sanitizeRemoteFrontendUrl()] as a suggested patch.

## Attachments

- [Devtools-Crafted-URI2.txt](attachments/Devtools-Crafted-URI2.txt) (text/plain, 1.7 KB)
- [SuggestedPatchFunction.txt](attachments/SuggestedPatchFunction.txt) (text/plain, 546 B)

## Timeline

### np...@chromium.org (2016-06-10)

I can't repro this: When I load this into omnibox (on Mac M51), the spinner just spins but with no other events.

[Monorail components: Platform>DevTools>Platform]

### gr...@gmail.com (2016-06-10)

Please try it with Windows system. The Repro case is for Windows OS; but the vulnerability should affected all OS.

### gr...@gmail.com (2016-06-10)

PoC Video (Unlisted): https://drive.google.com/file/d/0BzBNDrWkH6nFbHRsczItTTJPN2M/view?usp=sharing

### np...@chromium.org (2016-06-10)

I was able to repro on Win M51 -- it effectively outputs the dir listing of C:\. 

meacer-- Is it correct that extensions can navigate to chrome-devtool:// URLs? And if so, could they then read the contents of the page?

### me...@chromium.org (2016-06-10)

> meacer-- Is it correct that extensions can navigate to chrome-devtool:// URLs? And if so, could they then read the contents of the page?

They can navigate to chrome-devtool:// URLs but shouldn't be able to read page contents.

I think this bug is medium severity given that it needs an extension install (mitigating factor), similar to https://crbug.com/chromium/607939.

### np...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

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


### sh...@chromium.org (2016-06-23)

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

### go...@chromium.org (2016-07-22)

+awhalley@ whether to take this merge in for M53 Dev release on Tuesday (07/26).

### dg...@chromium.org (2016-07-22)

The fix has landed as r400768, which is way before M53 was branched (r403382).

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

[Comment Deleted]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

Thanks - $1,000 for this one.

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

This issue was migrated from crbug.com/chromium/618333?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084511)*
