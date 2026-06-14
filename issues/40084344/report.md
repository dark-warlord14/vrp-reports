# Security: Universal XSS via reentrancy in FrameLoader::startLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40084344](https://issues.chromium.org/issues/40084344) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>Frame |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-05-19 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/core/loader/FrameLoader.cpp:

void FrameLoader::startLoad(...)  

{  

ASSERT(client()->hasWebView());  

if (m\_frame->document()->pageDismissalEventBeingDispatched() != Document::NoDismissal)  

return;  

(...)  

m\_frame->document()->cancelParsing();  

detachDocumentLoader(m\_provisionalDocumentLoader);

```
// beforeunload fired above, and detaching a DocumentLoader can fire  
// events, which can detach this frame.  
if (!m_frame->host())  
    return;  

m_provisionalDocumentLoader = client()->createDocumentLoader(m_frame, request, (...));  
(...)  
m_provisionalDocumentLoader->startLoadingMainResource();  
(...)  

```
## }

Detaching the provisional document loader can trigger load event handlers that may reenter FrameLoader::startLoad and attach a new provisional loader. After |detachDocumentLoader| returns, the pointer to the new loader is immediately overwritten. As a result, the abandoned loader will remain attached to the frame for the duration of its lifetime, which allows an attacker to escape from FrameLoader::prepareForCommit without the risk of canceling the load.

**VERSION**  

Chrome 51.0.2704.54 (Beta)  

Chrome 52.0.2739.0 (Dev)  

Chromium 52.0.2742.0 (Release build compiled today)

## Attachments

- [exploit.html](attachments/exploit.html) (text/plain, 1.2 KB)
- [exploit.html](attachments/exploit_53269538.html) (text/plain, 1.0 KB)

## Timeline

### ma...@gmail.com (2016-05-19)

Please note that this exploit doesn't work in the stable version, where this code looks a bit different (that's before https://crrev.com/243c3522db). I have yet to check if I can accommodate the stable channel.

### lg...@chromium.org (2016-05-19)

Whew, neat! I can verify on OSX on Chrome 51.0.2704.29.

japhet@, it seems you wrote a lot of the code in this function. Could you take a look at this security bug?

[Monorail components: Blink>HTML>Frame]

### sh...@chromium.org (2016-05-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-20)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-05-21)

This is exploitable in the stable channel as well, some adjustments were needed to take a different timing of load events into account. Tested versions:

Chrome 50.0.2661.102 (Stable)
Chrome 51.0.2704.54 (Beta)
Chrome 52.0.2739.0 (Dev)
Chromium 53.0.2745.0 (Release build compiled today)

### sh...@chromium.org (2016-05-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-05-23)

Is this bug applicable to specific OS or all os?

Also We're getting closer to M51 Stable launch. pls make sure to land the fix and get it merged ASAP. All changes MUST be merged into the release branch by 5pm on May 23, Monday to make into the desktop Stable final build cut.

+timwillis@ (Security TPM)

### mm...@chromium.org (2016-05-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-05-23)

Smells like OS-All to me.

### ti...@google.com (2016-05-23)

This shouldn't block the release of M-51 that triggers today, as any fix will need bake time. We can consider a fix here to ride along with a post-stable update.

### ja...@chromium.org (2016-05-23)

I've yet to reproduce this locally on trunk with either repro. The alert() appears to be reporting the correct location, and I've added a "CHECK(!m_provisionalDocuemntLoader);" after detachDocumentLoader() that hasn't failed. Am I missing something?

### ma...@gmail.com (2016-05-23)

I can't get the exploit to fail, no matter what I try. The original version was sort of rushed, but I can't imagine what could fail in the revised one. Maybe if http://www.apple.com was handled faster than data:text/xml,? Can you try a different URL that responds slower? In a real-life scenario, an attacker would probably use a dedicated web server guaranteed not to handle the HTTP request too fast. Also, can you try increasing both timeouts significantly? Does it work in stable/beta/dev? I'll recompile the trunk to verify nothing has changed recently and get back to you with a debug version and a set of assertions to pinpoint the exact problem.

> and I've added a "CHECK(!m_provisionalDocuemntLoader);" after detachDocumentLoader() that hasn't failed.

Sorry, this appears to be a mistake in the original bug description: "After |detachDocumentLoader| returns" should have read "After |loader->detachFromFrame()| in detachDocumentLoader returns". |m_provisionalDocumentLoader| is passed as a reference, and it's already cleared in detachDocumentLoader. The proper check would be to set aside |m_provisionalDocumentLoader| when FrameLoader::detachDocumentLoader is entered and verify that it hasn't changed before |loader = nullptr;|. Apologies for the confusion, this was a rushed report and it shows.

### ja...@chromium.org (2016-05-23)

Ah, of course. I probably should've been able to figure that out :)

### ja...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### cs...@chromium.org (2016-05-25)

Hm I can't repro either (getting abc.xyz with abc.xyz alert). This causes the renderer to crash in canary 52.0.2721.0 (old version) though (every couple of tries).

I tried replacing apple.com with some other urls but still no dice.

I haven't added any CHECKs in the renderer yet.

### ma...@gmail.com (2016-05-25)

@csharrison: This is the expected result, abc.xyz should be protected by the same-origin policy. Swapping abc.xyz and apple.com URLs should yield XSS in apple.com.

### cs...@chromium.org (2016-05-25)

Ah okay I misread the source. Looks like we might be able to do a similar trick like we do in prepareForCommit wrt provisional document loader.

### ja...@chromium.org (2016-05-25)

I've got a tentative solution up at https://codereview.chromium.org/2006033002/, but given that I made the same mistake as https://crbug.com/chromium/613266#c17 in my first read of the repro, I want to walk through the repro a bit more and make sure I'm not missing anything.

### mm...@google.com (2016-05-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1948aefa8901dca0ccb993753fca00b15d2a6e25

commit 1948aefa8901dca0ccb993753fca00b15d2a6e25
Author: japhet <japhet@chromium.org>
Date: Thu May 26 18:42:57 2016

Disable frame navigations during DocumentLoader detach in FrameLoader::startLoad

BUG=613266

Review-Url: https://codereview.chromium.org/2006033002
Cr-Commit-Position: refs/heads/master@{#396241}

[add] https://crrev.com/1948aefa8901dca0ccb993753fca00b15d2a6e25/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach-expected.txt
[add] https://crrev.com/1948aefa8901dca0ccb993753fca00b15d2a6e25/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach.html
[modify] https://crrev.com/1948aefa8901dca0ccb993753fca00b15d2a6e25/third_party/WebKit/Source/core/html/HTMLAnchorElement.cpp
[modify] https://crrev.com/1948aefa8901dca0ccb993753fca00b15d2a6e25/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### aa...@google.com (2016-05-27)

Marking fixed for now based on c#22. If any more work shows up as a result of c#20, please feel free to reopen bug or file a new security bug for that variant.

### sh...@chromium.org (2016-05-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ja...@chromium.org (2016-05-31)

I haven't found any new, relevant crashes in recent canaries, so requesting merge to beta and stable.

### ti...@google.com (2016-05-31)

[Automated comment] Request affecting a post-stable build (M51), manual review required.

### ti...@google.com (2016-05-31)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### go...@chromium.org (2016-05-31)

Approving merge to M51 branch 2704 based on https://crbug.com/chromium/613266#c26. Please merge ASAP before 4:00 PM PST if possible so we take it for this week Stable release. Thank you.

### bu...@chromium.org (2016-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb

commit 7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb
Author: Nate Chapin <japhet@chromium.org>
Date: Tue May 31 21:58:06 2016

Disable frame navigations during DocumentLoader detach in FrameLoader::startLoad

BUG=613266

Review-Url: https://codereview.chromium.org/2006033002
Cr-Commit-Position: refs/heads/master@{#396241}
(cherry picked from commit 1948aefa8901dca0ccb993753fca00b15d2a6e25)

Review URL: https://codereview.chromium.org/2026823003 .

Cr-Commit-Position: refs/branch-heads/2743@{#153}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach-expected.txt
[add] https://crrev.com/7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach.html
[modify] https://crrev.com/7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb/third_party/WebKit/Source/core/html/HTMLAnchorElement.cpp
[modify] https://crrev.com/7fce40fb3697085b7a823d9bf0e7f2ca23bed7eb/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### bu...@chromium.org (2016-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd

commit 0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd
Author: Nate Chapin <japhet@chromium.org>
Date: Tue May 31 22:08:25 2016

Disable frame navigations during DocumentLoader detach in FrameLoader::startLoad

BUG=613266

Review-Url: https://codereview.chromium.org/2006033002
Cr-Commit-Position: refs/heads/master@{#396241}
(cherry picked from commit 1948aefa8901dca0ccb993753fca00b15d2a6e25)

Review URL: https://codereview.chromium.org/2021373003 .

Cr-Commit-Position: refs/branch-heads/2704@{#687}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[add] https://crrev.com/0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach-expected.txt
[add] https://crrev.com/0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd/third_party/WebKit/LayoutTests/http/tests/navigation/start-load-during-provisional-loader-detach.html
[modify] https://crrev.com/0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd/third_party/WebKit/Source/core/html/HTMLAnchorElement.cpp
[modify] https://crrev.com/0a0e03cf8a52aab2ad2d1fe3bc0d3dcbe57911bd/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

As noted in the release notes - $7500 here. Congrats!

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-02)

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

This issue was migrated from crbug.com/chromium/613266?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084344)*
