# Heap-use-after-free in blink::MutationObserverRegistration::unregister

| Field | Value |
|-------|-------|
| **Issue ID** | [40081291](https://issues.chromium.org/issues/40081291) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-01-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

chrome-heap-use-after-free-blinkMutationObserverRegistrationunregister that crashes on

==20307==ERROR: AddressSanitizer: heap-use-after-free on address 0x60600015c928 at pc 0x0001125c6b36 bp 0x7fff53c359c0 sp 0x7fff53c359b8

**VERSION**  

Chrome Version: 42.0.2276.0 dev  

Operating System: Mac OS X

**REPRODUCTION CASE**  

Open Attached minimized test case POC.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: asanlog.txt

## Attachments

- [POC.html](attachments/POC.html) (text/html, 1.5 KB)
- [asanlog.txt](attachments/asanlog.txt) (text/plain, 18.3 KB)
- [min.html](attachments/min.html) (text/html, 381 B)

## Timeline

### sa...@gmail.com (2015-01-29)

the --js-flags=--expose-gc switch should be used sorry for not including it in original report 

### cl...@chromium.org (2015-01-29)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5750223883206656

### cl...@chromium.org (2015-01-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5750223883206656

Uploader: rickyz@chromium.org
Job Type: Mac_asan_chrome

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c00019fdc8
Crash State:
  blink::MutationObserverRegistration::unregister
  blink::MutationObserver::disconnect
  blink::MutationObserverV8Internal::disconnectMethodCallback
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=313665:313666

Minimized Testcase (0.90 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94k9y-oYe1S4m4cNMvRBvr8wHWpMk6dlX9hueQNvyq1z-RRJpFTV3y8uZYyZTaP5n3OBR0UlPl2MwedQjQj3zI35g33sTUJBqI2p9l_G7bIUSm_D74aB2qS9Af0-XKcXN9VHUgGBuQmPKfdtx7HUtlcKnlJYA
<script>
try{ HTML0=document.createElement("ABBR")} catch(e){}
try{ HTML1=document.createElement("TITLE")} catch(e){}
try{ HTML2=document.createElement("THEAD")} catch(e){}
try{ HTML0.appendChild(HTML2)} catch(e){}
try{ HTML3=document.createElement("PROGRESS")} catch(e){}
try{ HTML1.appendChild(HTML3)} catch(e){}
try{ HTML4=document.createElement("INS")} catch(e){}
try{ HTML1.appendChild(HTML4)} catch(e){}
try{ var observer0= new MutationObserver(function() {})} catch(e){}
try{ observer0.observe(HTML4,{childList:1, })} catch(e){}
try{ observer0.observe(HTML1,{childList:1, subtree:1, })} catch(e){}
try{ HTML3=HTML3.nextSibling} catch(e){}
try{ HTML4=HTML2.parentNode} catch(e){}
try{ HTML3.outerHTML=HTML4.innerHTML} catch(e){}
try{ delete createdElements['HTML4']} catch(e){}
try{ HTML3=HTML4.previousSibling} catch(e){}
try{ gc()} catch(e){}
try{ observer0.disconnect()} catch(e){}
window.location.reload()
</script>





### cl...@chromium.org (2015-01-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-29)

Author: zhaoze.zhou@partner.samsung.com
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/b0f21fa42c4367b07d7faaa8f269f31d5333c7fa
Time: Wed Jan 14 05:33:44 2015
The CL last changed line 160 of file MutationObserver.cpp, which is stack frame 1.

### in...@chromium.org (2015-01-29)

Weird, it says zhaoze.zhou@partner.samsung.com email is wrong. +Cc reviewers for that cl.

### ri...@chromium.org (2015-01-29)

Nice find. I hand-minimized it down to the attached file.

It looks like you have:

holder -> target

And you observe holder (with subtree) and target. This creates two MutationObserverRegistration that are owned by the each node.

When target is removed from holder, observedSubtreeNodeWillDetach is called, which converts the node to a transient registration node, and the nulling/gc makes holder's MutationObserverRegistration the owner of target.

When the observer is disconnected, it makes a copy of its registration list and starts iterating through it (https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/MutationObserver.cpp&l=158). First, it unregisters the registration on parent, which deletes target along with its registration. Then it hits target, which  has now been deleted.

Would it be valid to add a similar check to https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/Node.cpp&l=367 for non-transient observers?

Also, how correct is making a copy of the registration set and iterating through that? Would a while (!m_registrations.isEmpty()) loop be a correct fix for this?

Adding adamk@ who has looked at a similar bug in the past.

### cl...@chromium.org (2015-01-29)

[Empty comment from Monorail migration]

### sa...@gmail.com (2015-01-30)

Thank you for the explanation it's really awesome of you I appreciate it

### dc...@chromium.org (2015-01-30)

https://chromium.googlesource.com/chromium/blink.git/+/8816db0d28f1dceff04721619e17bbae89b53f9c is a better culprit. https://chromium.googlesource.com/chromium/blink.git/+/b0f21fa42c4367b07d7faaa8f269f31d5333c7fa just uses a C++11 foreach loop, which should have no effect on the correctness of this code.

### in...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2015-02-02)

The first solution that comes to mind is to make MutationRegistrations RefCounted and make the transientRegistry hold RefPtrs; it seems like that should make this test case stop crashing, and since transient registrations are cleared at the end of each microtask, it seems unlikely to lead to memory leaks. I'm not working on Blink full time these days (nor is rafaelw), but I'd be happy to review such a change.

As a side note, this seems related to other MutationObserver GC bugs, like https://crbug.com/chromium/329103. target's JS wrapper shouldn't be collected by the GC, since there's a MutationRecord with a reference to it in observer's m_records. But I don't think that fixing 329103 would necessarily make the existing code safe.

### in...@chromium.org (2015-02-12)

Rafael, since you caused the regression, can you please take a look or suggest an owner. Ricky is on the security team, so wont be fixing this.

### [Deleted User] (2015-02-12)

@inferno, it's unclear to me how I caused this regression (other than helping to create this feature originally), but as Adam points out, I don't work on blink anymore either.

If I'm really the only person available to do this, I will.

That said, objects like MutationObserver which have subtle GC behavior have long been problems for blink and it's been quite a long time since I've understood how any of it works. Me fixing it would require investing time in re-leaning the current system and it seems like that would be a better investment for someone who continues to work on blink.

@pdr or @adamk, can you think of a good candidate who still works on blink?

### ad...@chromium.org (2015-02-12)

+haraken, who runs a team with "DOM" in its name...

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-27)

rafaelw@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-13)

rafaelw@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pd...@chromium.org (2015-03-13)

rafaelw no longer works on blink.

@haraken, would you be willing to triage this?

### ad...@chromium.org (2015-03-13)

For those late to this bug, the combination of comments 7 and 12 should pretty well explain the work to be done here.

### ad...@chromium.org (2015-03-13)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-03-25)

I don't have a bandwidth to look into this issue. Let me assign this to Adam at the moment.


### ad...@chromium.org (2015-03-25)

As I don't work on Blink anymore, this shouldn't sit in my queue. Marking as available to reflect the real state of the world. Though as rafaelw said above, if there's really no one on Blink who has time for this one of us may get to it eventually.

### pd...@chromium.org (2015-03-26)

Assigning to @inferno to triage/investigate because this is high severity.

### in...@chromium.org (2015-03-26)

Kouhei@, can you please take a look.

### ko...@chromium.org (2015-03-27)

I'll try to work on this for 2hrs, but I'm currently flooded with other urgent tasks/bugs so feel free to take this one.

### ko...@chromium.org (2015-03-27)

Never mind. Managed to write a fix with in 2hrs: https://codereview.chromium.org/1039523003/


### ko...@chromium.org (2015-03-31)

Waiting for clusterfuzz to pick up fix

### in...@chromium.org (2015-03-31)

This was a one-time crasher on CF (hit a few times), so it can't verify.

### cl...@chromium.org (2015-03-31)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192655

------------------------------------------------------------------
r192655 | kouhei@chromium.org | 2015-03-27T07:16:44.890912Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/MutationObserver.cpp?r1=192655&r2=192654&pathrev=192655

MutationObserver: add a check that iterating registration still exists in original set

The MutationObserver registration may be unregistered from the original set
while iterating on the cloned set.
Add a check so that it would only call unregister() on active registrations.

BUG=453279
TEST=manually tested from fuzzer repro case :(

Review URL: https://codereview.chromium.org/1039523003
-----------------------------------------------------------------

### ti...@google.com (2015-04-08)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-08)

Merge-Requested to M42 - branch 2311 

(noting that this request is after the stable candidate qualification, so may not go out with first M42 unless there's a respin)

### ti...@google.com (2015-04-08)

[Empty comment from Monorail migration]

### la...@google.com (2015-04-08)

[Automated comment] Less than 2 weeks to go before stable on M42, manual review required.

### am...@chromium.org (2015-04-08)

merge approved for m42 branch 2311

### bu...@chromium.org (2015-04-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=193431

------------------------------------------------------------------
r193431 | haraken@chromium.org | 2015-04-09T08:53:19.949390Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2311/Source/core/dom/MutationObserver.cpp?r1=193431&r2=193430&pathrev=193431

Merge 192655 "MutationObserver: add a check that iterating regis..."

> MutationObserver: add a check that iterating registration still exists in original set
> 
> The MutationObserver registration may be unregistered from the original set
> while iterating on the cloned set.
> Add a check so that it would only call unregister() on active registrations.
> 
> BUG=453279
> TEST=manually tested from fuzzer repro case :(
> 
> Review URL: https://codereview.chromium.org/1039523003

TBR=kouhei@chromium.org

Review URL: https://codereview.chromium.org/1072773002
-----------------------------------------------------------------

### ti...@google.com (2015-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-10)

Congrats - $3000 for this report. We'll start payment shortly.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-07)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

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

This issue was migrated from crbug.com/chromium/453279?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081291)*
