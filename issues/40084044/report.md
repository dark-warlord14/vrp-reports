# Security:  Read access violation on same-origin, cross-process frames

| Field | Value |
|-------|-------|
| **Issue ID** | [40084044](https://issues.chromium.org/issues/40084044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **CVE IDs** | CVE-2016-1661 |
| **Reporter** | wa...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-04-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

Opening a cross origin window X in a separate renderer, then redirecting it to the opener origin can lead to read access violation when the opener manipulates  

the X.location object.

When i know more about how it may be exploitable, i will share it here.

**VERSION**  

Chrome Version: 49.0.2623.110 m  

Operating System: Windows, 7, service pack 1

**REPRODUCTION CASE**

1- Open <http://127.0.1.1/crashs.html>  

2- Click on one of the crash buttons

Type of crash: Tab  

Crash State: Changeable, one example:

(4a88.4980): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\49.0.2623.110\chrome\_child.dll -  

eax=04376180 ebx=442c9f90 ecx=04376180 edx=59d1ff50 esi=04376180 edi=60528b0b  

eip=604b3dce esp=0035ec68 ebp=0035ec6c iopl=0 nv up ei pl nz na po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

chrome\_child!ovly\_debug\_event+0x43813:  

604b3dce 8b02 mov eax,dword ptr [edx] ds:002b:59d1ff50=????????

## Attachments

- [crashs.html](attachments/crashs.html) (text/plain, 1.8 KB)
- [redirection.html](attachments/redirection.html) (text/plain, 203 B)

## Timeline

### ke...@chromium.org (2016-04-08)

Thanks for the report. I can't seem to reproduce this locally, are you able to provide some sample crash IDs (from chrome://crashes)?

### wa...@gmail.com (2016-04-08)

My crash report is disabled. I will enable it if it is necessary.
You should open http://127.0.1.1/crashs.html not http://localhost/crashs.html.


### sh...@chromium.org (2016-04-09)

Thank you for providing more feedback. Adding requester "kenrb@chromium.org" for another review and adding "Needs-Review" label for tracking.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2016-04-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-04-11)

Interesting bug. On trunk I am seeing bad casts (RemoteFrame -> LocalFrame and RemoteDOMWindow -> LocalDOMWindow) triggered from receiving a message from the opener. I am not sure the crashes on stable are the same, because of recent changes to how swapped out works.

The sequence seems to be:
- window.open() creates a new window
- the new window's opener is set to null
- the opener navigates the new window to a different site instance, causing it to move to a different renderer process, but a redirect moves it back to the original process
- the opener interacts with the location property of the window
- the renderer crashes

### sh...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### wa...@gmail.com (2016-04-12)

The manipulations of the Location object of the opened window X that crash the renderer (like reading X.location or setting X.location.hostname ) all share this code: 

toLocalFrame(m_frame)->document()->url()

And those who don't cause a crash (like setting X.location or executing X.location.Replace) don't have it.


The Address of the read violation is attacker influenced (controlled?) and could be an address of a valid and allocated memory.

Strategy steps for an exploit might be:

1-Heap spray with ArrayBuffers
2-Use X.location.hostname="..."(or port, pathname...) to overwrite the length field of one ArrayBuffer and getting read/write primitive
3-Overwrite a vtable pointer or a jit code of a function

### dc...@chromium.org (2016-04-12)

I'll take an initial look.

### dc...@chromium.org (2016-04-12)

I'm pretty sure this is similar to the other bug we were just talking about: it's possible for a RemoteFrame to pass the security checks. Blink makes the simplifying assumption that passing the security checks implies a LocalFrame, but there are cases where that will be false.

[Monorail components: Internals>Sandbox>SiteIsolation]

### dc...@chromium.org (2016-04-12)

Nick is working on a test and I'm working on a small Blink-side patch that can be cherry-picked to M50.

### cr...@chromium.org (2016-04-12)

Yes, we think it's likely the same problem as https://crbug.com/chromium/602821, where we end up with same-origin frames in different processes.

### dc...@chromium.org (2016-04-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-04-13)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-04-13)

Copied from https://crbug.com/chromium/602821:

This shows up in the wild as blink::SecurityOrigin::canAccessCheckSuborigins, such as crash ID fe0f29c400000000.

For context, here's why this case is possible (copied from the discussion on https://codereview.chromium.org/1887553002/):

Since Chrome launched, we've made browser-initiated cross-site navigations go cross-process, but renderer-initiated cross-site navigations usually don't.  This was to preserve compatibility in cases that a cross-site iframe opens a popup (e.g., OAuth), etc.  It's explained in the following doc and paper:
https://www.chromium.org/developers/design-documents/process-models
http://www.charlesreis.com/research/publications/eurosys-2009.pdf

As a result, you could have two windows on site A, go cross-process in the second one to site B (by typing in the omnibox), and then click a link in both to site C.  They'll be same-site but different processes.  Yes, this breaks a possible script relationship, but it's unlikely to matter in practice relative to the OAuth case.  (We decided it was a good tradeoff because the user initiated the navigation to B, basically leaving the previous context behind.  You can almost view that as creating a new unit of related browsing contexts / BrowsingInstance.  Maybe we can formalize that concept.)

This wasn't a problem to Blink before RemoteFrames, because the origin of the cross-process window looked like swappedout://.  With RemoteFrames, we replicate the origin and it looks like it should pass the check.

Full --site-per-process mode would eliminate this possibility, but most realistic modes (even those with OOPIFs) still have it.  It's worth noting that TDI actually depends on this ability a bit more to avoid process inversions (where main frames would frequently end up in the subframe process).

### bu...@chromium.org (2016-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e

commit f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e
Author: dcheng <dcheng@chromium.org>
Date: Wed Apr 13 21:08:20 2016

Make sure binding security checks don't pass if the frame is remote.

Blink assumes that remote frames will always fail the security origin
check. Unfortunately, reality is not that simple. There are several
instances where this assumption fails to hold. For example:

  1. Navigate to a.com.
  2. a.com opens a new window.
  3. Navigate the new window to b.com via the omnibox.
  4. Click a link to c.com in both windows.

Because browser-initiated navigations go cross-process but
renderer-initiated navigations do not [1], the two c.com windows will
end up in different renderer processes.

Both windows have the same origin but see each other as RemoteFrames.
This means that SecurityOrigin's canAccess check will pass… but this
ends up violating many assumptions in Blink that passing the security
check implies a local frame.

[1] https://www.chromium.org/developers/design-documents/process-models#Caveats

BUG=601629
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1887553002

Cr-Commit-Position: refs/heads/master@{#387087}

[modify] https://crrev.com/f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e/content/browser/frame_host/render_frame_host_manager_browsertest.cc
[modify] https://crrev.com/f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e/third_party/WebKit/Source/bindings/core/v8/BindingSecurity.cpp
[modify] https://crrev.com/f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e/third_party/WebKit/Source/core/frame/DOMWindow.cpp


### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-14)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### dc...@chromium.org (2016-04-19)

Well, there's not a lot of signal from the crash reports, but I think this should fix it and I haven't heard any reports of this breaking things. And this is definitely less broken than before, so I'll go ahead and request the merge.

### ti...@google.com (2016-04-19)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-04-19)

Merge approved for M50 (branch 2661). Pls go ahead merge.

### go...@chromium.org (2016-04-19)

We're cutting M50 Stable RC today (very soon). Please merge this to M50 ASAP. Thank you.

### bu...@chromium.org (2016-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a0bbe39f45e7bd26a4b9328ce2660bc6094ef84

commit 7a0bbe39f45e7bd26a4b9328ce2660bc6094ef84
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Apr 19 18:45:46 2016

Make sure binding security checks don't pass if the frame is remote.

Blink assumes that remote frames will always fail the security origin
check. Unfortunately, reality is not that simple. There are several
instances where this assumption fails to hold. For example:

  1. Navigate to a.com.
  2. a.com opens a new window.
  3. Navigate the new window to b.com via the omnibox.
  4. Click a link to c.com in both windows.

Because browser-initiated navigations go cross-process but
renderer-initiated navigations do not [1], the two c.com windows will
end up in different renderer processes.

Both windows have the same origin but see each other as RemoteFrames.
This means that SecurityOrigin's canAccess check will pass… but this
ends up violating many assumptions in Blink that passing the security
check implies a local frame.

[1] https://www.chromium.org/developers/design-documents/process-models#Caveats

BUG=601629
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1887553002

Cr-Commit-Position: refs/heads/master@{#387087}
(cherry picked from commit f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e)

Review URL: https://codereview.chromium.org/1898303002 .

Cr-Commit-Position: refs/branch-heads/2661@{#609}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/7a0bbe39f45e7bd26a4b9328ce2660bc6094ef84/content/browser/frame_host/render_frame_host_manager_browsertest.cc
[modify] https://crrev.com/7a0bbe39f45e7bd26a4b9328ce2660bc6094ef84/third_party/WebKit/Source/bindings/core/v8/BindingSecurity.cpp
[modify] https://crrev.com/7a0bbe39f45e7bd26a4b9328ce2660bc6094ef84/third_party/WebKit/Source/core/frame/DOMWindow.cpp


### dc...@chromium.org (2016-04-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-20)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### go...@chromium.org (2016-04-20)

Please merge your change to M51 branch 2704 before 5:00 PM PST today so we can take it for today's M51 Beta candidate cut. Thank you.

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c0f5608d576451f601245255a85342490039eb7

commit 0c0f5608d576451f601245255a85342490039eb7
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Apr 20 20:09:02 2016

Make sure binding security checks don't pass if the frame is remote.

Blink assumes that remote frames will always fail the security origin
check. Unfortunately, reality is not that simple. There are several
instances where this assumption fails to hold. For example:

  1. Navigate to a.com.
  2. a.com opens a new window.
  3. Navigate the new window to b.com via the omnibox.
  4. Click a link to c.com in both windows.

Because browser-initiated navigations go cross-process but
renderer-initiated navigations do not [1], the two c.com windows will
end up in different renderer processes.

Both windows have the same origin but see each other as RemoteFrames.
This means that SecurityOrigin's canAccess check will pass… but this
ends up violating many assumptions in Blink that passing the security
check implies a local frame.

[1] https://www.chromium.org/developers/design-documents/process-models#Caveats

BUG=601629
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1887553002

Cr-Commit-Position: refs/heads/master@{#387087}
(cherry picked from commit f23b8e77a83a5aafabf64acf723cf2ac02c5cf0e)

Review URL: https://codereview.chromium.org/1907603002 .

Cr-Commit-Position: refs/branch-heads/2704@{#152}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/0c0f5608d576451f601245255a85342490039eb7/content/browser/frame_host/render_frame_host_manager_browsertest.cc
[modify] https://crrev.com/0c0f5608d576451f601245255a85342490039eb7/third_party/WebKit/Source/bindings/core/v8/BindingSecurity.cpp
[modify] https://crrev.com/0c0f5608d576451f601245255a85342490039eb7/third_party/WebKit/Source/core/frame/DOMWindow.cpp


### ti...@google.com (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

Congratulations - Our reward panel has awarded you $3,000 for this report.

Our finance team will be in touch within 7 days to collect payment details. If that doesn't happen, please contact me directly at timwillis@ or update this bug.

We've credited you in our release notes: http://googlechromereleases.blogspot.com/2016/04/stable-channel-update_28.html - if you'd like to use a different credit name, please let me know so I can update the notes.

The CVE-ID for this vulnerability is CVE-2016-1661

Thanks again for this report - looking forward to seeing more bugs from you in the future.


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/601629?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/602821]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084044)*
