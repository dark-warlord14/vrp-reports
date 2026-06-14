# IndexedDB with autoincrement fails on object put and crashes chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40052454](https://issues.chromium.org/issues/40052454) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink, Blink>Storage>IndexedDB |
| **Reporter** | sg...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2011-12-30 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 17.0.963.12  

OS Version: 6.1 (Windows 7, Windows Server 2008 R2)  

URLs (if applicable) : <http://dl.dropbox.com/u/73798/TestAutoIncrement.html>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5: FAIL  

Firefox 4.x: FAIL  

IE 7/8/9: FAIL

**What steps will reproduce the problem?**

1. Create an IndexedDB database
2. Create an object store with a keyPath property and autoIncrement set to true.
3. Try to store an object in the object store that does not have the keyPath property.
4. Doing anything else (like trying to read the object back) crashes chrome.  
   
   See the link for a simple example of this working.

**What is the expected result?**  

The object should have a property added with the keyPath property name and have its value set to 0 or the next available number.

**What happens instead?**  

Chrome never saves the object and Chrome behaves oddly (only some features work). Performing other actions on the indexeddb crashes chrome.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

Tested on Chrome dev channel and Chrome canary.

UserAgentString: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11

## Timeline

### sg...@gmail.com (2011-12-30)

This same behavior is observed when using [objectStore].add() instead of [objectStore].put().

### dg...@chromium.org (2012-01-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-05)

I can't repro the issue in linux build (top of tree) or in Chrome 16. It's possible it was in 17 but has since been fixed. I'm loading the sample page and clicking the buttons 1/2/3 and verifying that the values are being written.

sgoertzen - you mentioned you tried a canary build. Can you try another one and see if you're still seeing the crash? (That would let us know if either it's been fixed since 17 dev or if we're just failing to repro for some reason)

### sg...@gmail.com (2012-01-06)

I tested on two other machines and they seem to be working fine.  It appears this is a problem with my machine.  I have uninstalled and re-installed Chrome twice, but I always get the issue again.

I will continue to work with, if I can find a reliable way to reproduce the issue on the other machines I will update this ticket, but for now I recommend closing this issue.

### sg...@gmail.com (2012-01-09)

Quick update: I reinstalled my operating system and put on the stable version of Chrome and the error has occurred again.  

I believe the the main site I am developing has uncovered the problem, and once it happens almost all interactions with the IndexedDB fail.  That is why the test page is failing for me, since I first received the error on my main site.

I am going to continue to try and pinpoint the issue and make another test site that reproduces it.  I am also downloading the Chromium source code and will attempt to drill into that a little bit to see what is going on.

### js...@chromium.org (2012-01-20)

No repro for me on Win7, Chrome 18.0.1013.0 canary

### js...@chromium.org (2012-01-24)

Finally - repros for me in 17.0.963.38 beta-m  (Win7) but not 18.0.1017.0 canary (Win7)

This looks like a duplicate of 110372 - dgrogan, can you confirm?

Not sure why it's not reproducing in 18; I don't think it's fixed, but we've changed the timing of operations so it may not be as obvious.

### sg...@gmail.com (2012-01-24)

I am glad to see someone else can finally reproduce this.

I can reproduce this defect on a couple different machines, but only after using the site for a while.  I have been trying very hard to figure out the exact steps needed to reproduce it, but it is especially challenging because I have to re-install Chrome every time it happens to clear the error.

I can't seem to view https://crbug.com/chromium/110372 so I can't comment on if this is a duplicate.  This link gives me a 403 error: http://code.google.com/p/chromium/issues/detail?id=110372

### in...@chromium.org (2012-01-26)

This is use after free in the browser. :( David is looking into it if it affect stable.

### dg...@chromium.org (2012-01-26)

I'm not sure if this affects stable.

There are two parts to the use-after-free.  There was a bug in our webkit code that caused the utility process to crash, but cleanly, and our utility process is sandboxed (newly).  This was fixed on trunk in http://trac.webkit.org/changeset/105891, but not merged anywhere (jsbell, could you confirm all these webkit-side details?)

The use-after-free is in the chromium code that doesn't properly handle the utility process crashing.  When the process crashes, UtilityProcessHost gets free'd but we still try to use it.  This offending chromium code has been around for a while, we've just never seen the utility process crash before.

The webkit avenue to crash the utility process is new to 17.  (Again, Josh, can you confirm?)  Without it, there are no known ways to crash the utility process, but if there were, it would expose our use-after-free error in chromium.

### in...@chromium.org (2012-01-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-26)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-26)

Confirmed that there was a webkit bug that allowed crashing the utility process, fixed in  http://trac.webkit.org/changeset/105891 on the WebKit side, but the fix also required Chromium changes; see http://crbug.com/110956 - all of that would be new in 17, fixed in 18 (with an unfortunately large set of changes required for the correct fix)

http://crbug.com/108012 appears to be another way to crash the utility process via IDB, which would expose this use-after-free


### bu...@chromium.org (2012-01-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=119340

------------------------------------------------------------------------
r119340 | dgrogan@chromium.org | Thu Jan 26 18:04:48 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/utility_process_host.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/in_process_webkit/indexed_db_key_utility_client.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/browser_child_process_host_impl.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/importer/external_process_importer_client.h?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/importer/external_process_importer_client.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/utility_process_host.h?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/indexed_db/idbbindingutilities_browsertest.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/webstore_install_helper.h?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/plugin_loader_posix.h?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/plugin_loader_posix.cc?r1=119340&r2=119339&pathrev=119340
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/webstore_install_helper.cc?r1=119340&r2=119339&pathrev=119340

A few clients of the utility process had a race condition that could lead to a browser crash if the utility process crashed.  IndexedDB was the worst offender.  WebstoreInstallHelper, the profile importer, and posix plugin loader were also affected.

As a side effect, NaClProcessHost and GpuProcessHost are now notified when their respective processes are killed and treat such an occurrence as a crash.

BUG=108871
TEST=


Review URL: http://codereview.chromium.org/9235052
------------------------------------------------------------------------

### dg...@chromium.org (2012-01-27)

I don't know if bugdroid will pick it up but this was merged to 963 in http://src.chromium.org/viewvc/chrome?view=rev&revision=119343.

### bu...@chromium.org (2012-01-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=119343

------------------------------------------------------------------------
r119343 | dgrogan@chromium.org | Thu Jan 26 18:15:29 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/in_process_webkit/indexed_db_key_utility_client.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/utility_process_host.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/importer/external_process_importer_client.h?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/importer/external_process_importer_client.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/utility_process_host.h?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/idbbindingutilities_browsertest.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/extensions/webstore_install_helper.h?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/browser_child_process_host.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/plugin_loader_posix.cc?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/plugin_loader_posix.h?r1=119343&r2=119342&pathrev=119343
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/extensions/webstore_install_helper.cc?r1=119343&r2=119342&pathrev=119343

Backport fix for http://crbug.com/108871 to m17's 963 branch.

Original CL description:

Fix race condition in utility process clients

A few clients of the utility process had a race condition that could lead to a
browser crash if the utility process crashed. IndexedDB was the worst offender.
WebstoreInstallHelper, the profile importer, and posix plugin loader were also
affected.

As a side effect, NaClProcessHost and GpuProcessHost are now notified when
their respective processes are killed and treat such an occurrence as a crash.

BUG=108871
TEST=
1) in Release mode, open http://trac.webkit.org/export/106000/trunk/LayoutTests/storage/indexeddb/cursor-reverse-bug.html
2) kill the utility process
3) reload
4) watch chrome not die
Review URL: https://chromiumcodereview.appspot.com/9297001
------------------------------------------------------------------------

### in...@chromium.org (2012-01-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-27)

Does this affect M16 or just M17?
If it's an M17 regression, I think we should respin a final M17 release to avoid shipping a Critical regression to stable.

### in...@chromium.org (2012-01-27)

The bug looks to have existed for a long time, check out c#10.

Also, the fix is going into m17 stable. Jason cut the branch yesterday with this fix in. We managed to sneak this one in :)

### an...@chromium.org (2012-01-27)

[Empty comment from Monorail migration]

### dg...@chromium.org (2012-01-27)

This bug is present in m16.

### sc...@gmail.com (2012-02-05)

@sgoertzen: thank you very much for this bug!
As you can see, it turned out to be a security bug. We have a reward program for security bugs.

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issue.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

In these situations we normally reward $500, but given the severity of the issue (critical, affecting whole browser process) we'd like to offer a $1000 Chromium Security Reward.

We'd also like to credit you in our Chrome 17 release notes if we may. Any particular name / affiliation you'd like used?

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sg...@gmail.com (2012-02-05)

Wow, that is very unexpected, thank you.  

Name would be: Shawn Goertzen
No affiliation.

Let me know what other contact details you need if anything.  I can be reached at my username @gmail.com as well.

Shawn

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sg...@gmail.com (2012-05-04)

Was wondering what I need to do to receive the security reward.  I have filled out the contractor form but don't know what other steps I need to take.

### sc...@gmail.com (2012-05-04)

Looking into this now. Sorry for the delay.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-05-18)

Payment finally in system :)

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2012-10-17)

[Empty comment from Monorail migration]

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/108871?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>Storage>IndexedDB]
[Monorail mergedwith: crbug.com/chromium/110372]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052454)*
