# Heap-use-after-free in blink::PendingScript::stopWatchingForLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40080712](https://issues.chromium.org/issues/40080712) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2014-10-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The latest asan build crashes when loading the following testcase.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-301067  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o32=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
document.documentElement.appendChild(o32);
o43=o32.contentDocument.implementation.createDocument('http://www.w3.org/1999/02/22-rdf-syntax-ns#','window');
o82=o43.createElementNS('http://www.w3.org/2000/svg','tref');
o123=document.createElementNS('http://www.w3.org/2000/svg','use');
o219=document.createRange();
o219.selectNodeContents(o82);
o219.surroundContents(o123);
o225=document.createElement('script');
document.documentElement.appendChild(o225);
o241=o123.ownerDocument;
o225.onerror=cb\_onerror\_493\_1;
o225.src='javascript:x();';
}
function cb\_onerror\_493\_1() {
o241.removeChild(o241.documentElement);
o241.appendChild(document.documentElement);
location.reload(true);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: attached in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 21.0 KB)

## Timeline

### cl...@chromium.org (2014-10-25)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6454861624246272

### in...@chromium.org (2014-10-25)

Thanks cloudfuzzer for yet another awesome bug!

### cl...@chromium.org (2014-10-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6454861624246272

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f000049680
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  

Minimized Testcase (0.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Ufbxi68f1xQnFD733PcjJfGepQn_0YNzyvn-l2ZsmLY6jH8QDh0rzhRr11QzVOg76vRjtvUwIwuD8ucLb972nlLggeAuBbKyFo3xyjop5_HyJszcTA25q9LBsgRLnX2nzx_IpQpzzim-a8h70U8zjoF79VA



### in...@chromium.org (2014-10-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6454861624246272

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f000049680
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  

Minimized Testcase (0.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv961G1V0xzCZTTknv9XmnGaysRdQBYjMMz1H9MnWEf_ldH0U_qX3th00f3I0nTZYAVc5FTJfSEdWo_14Xalnauo_q884A4_AIEjjEEFJ0cMJ7DYc6JHZwxuLpgrabUVJiP_54eGNB7KYyzBq05aVNy8gPTwFqA



### cl...@chromium.org (2014-10-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-25)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ma...@chromium.org (2014-10-27)

This is legit, and I think the cause is that when I refactored, I assumed that ScriptRunner holds no dangling pointers to ScriptLoaders in the end, and we can just detach the existing ScriptLoaders in ~ScriptRunner.

But seems like by design, ScriptRunner *can* hold dangling pointers: When a HTMLScriptElement is deleted, it deletes the ScriptLoader too, and makes no effort to remove it from the ScriptRunner. So after that point, ScriptRunner should just not access the invalid ScriptLoader pointer.

The fix is easy but horrible.

### ma...@chromium.org (2014-10-27)

Hmm, no, I don't fully understand this yet. It's related to my refactoring for sure.

Note to self: The part I don't yet get: how come we manage to delete the HTMLScriptElement, when a ScriptLoader holds a PendingScript which holds a RefPtr to the HTMLScriptElement?

### ma...@chromium.org (2014-10-27)

More information (mainly for me):

The problem is that this ASSERT in ScriptRunner::notifyScriptLoadError is not true:

ASSERT(m_pendingAsyncScripts.contains(scriptLoader));

and after my CL it's fatal.

The ScriptLoader is moved to a different ScriptRunner (ScriptRunner::movePendingAsyncScript), but still the old ScriptRunner gets this notification.

### ha...@chromium.org (2014-10-27)

+Sibjorn (who implemented movePendingAsyncScript)


### ma...@chromium.org (2014-10-27)

CL which implements movePendingAsyncScript: https://codereview.chromium.org/496443008/

I'm still not sure why the old ScriptRunner gets the notification; that part makes no sense.

### ma...@chromium.org (2014-10-27)

Lol! dispatchErrorEvent() inside ScriptLoader::notifyFinished moves the script. This is obvious looking at the repro case in OP.

So first we get the ScriptRunner, then dispatchErrorEvent(), then we fail to notice that the ScriptRunner has changed.

Very subtle. Very interesting!

### ma...@chromium.org (2014-10-27)

CL here: https://codereview.chromium.org/648393004


### bu...@chromium.org (2014-10-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=184455

------------------------------------------------------------------
r184455 | marja@chromium.org | 2014-10-27T15:15:26.503072Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptLoader.cpp?r1=184455&r2=184454&pathrev=184455

Fix: ScriptLoader didn't handle script elements moving gracefully.

ScriptLoader::notifyFinished didn't take into account that dispatchErrorEvent()
can move the HTMLScriptElement to a new Document. In that case, it used to
notify the ScriptRunner of the old Document, not the ScriptRunner of the new
Document.

AFAICS, this problem has been present "forever" (moving scripts is implemented
by https://codereview.chromium.org/496443008/). There was an ASSERT in
ScriptRunner::notifyScriptLoadError which just silently failed (plus maybe
holding the PendingScript alive leaked?). My refactoring (
https://codereview.chromium.org/669603002 ) made this error case more fatal
(since we now do cleanup in ~ScriptRunner) and exposed this bug.

A test will follow in a separate CL. See bug for a reproduction case.

BUG=427108

Review URL: https://codereview.chromium.org/648393004
-----------------------------------------------------------------

### in...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-10-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=184508

------------------------------------------------------------------
r184508 | marja@chromium.org | 2014-10-28T10:38:11.208043Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-by-onerror-crash-expected.txt?r1=184508&r2=184507&pathrev=184508
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-by-onerror-crash.html?r1=184508&r2=184507&pathrev=184508
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptLoader.cpp?r1=184508&r2=184507&pathrev=184508

Follow-up to script element moving fix (r184455).

This CL adds a test and also fixes the fix.

BUG=427108

Review URL: https://codereview.chromium.org/680263002
-----------------------------------------------------------------

### cl...@chromium.org (2014-10-29)

ClusterFuzz has detected this issue as fixed in range 301101:301780.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6454861624246272

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f000049680
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300226:300272
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=301101:301780

Minimized Testcase (0.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv961G1V0xzCZTTknv9XmnGaysRdQBYjMMz1H9MnWEf_ldH0U_qX3th00f3I0nTZYAVc5FTJfSEdWo_14Xalnauo_q884A4_AIEjjEEFJ0cMJ7DYc6JHZwxuLpgrabUVJiP_54eGNB7KYyzBq05aVNy8gPTwFqA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-01-22)

Another $2000 here. 

### cl...@chromium.org (2015-02-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/427108?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080712)*
