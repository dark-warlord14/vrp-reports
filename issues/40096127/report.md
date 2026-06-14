# Security: Accessing set::end in GamepadService

| Field | Value |
|-------|-------|
| **Issue ID** | [40096127](https://issues.chromium.org/issues/40096127) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GamepadAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mm...@semmle.com |
| **Assignee** | ma...@google.com |
| **Created** | 2019-08-28 |
| **Bounty** | $15,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

I'm filing this tentatively as I don't fully understand what's going on here. Please feel free to mark it as invalid if it turns out to be safe.

In GamepadService::ConsumerBecameInactive, the consumers\_ set is searched for to find the ConsumerInfo corresponding to the input GamepadConsumer:

```
void GamepadService::ConsumerBecameInactive(device::GamepadConsumer\* consumer) {  
  DCHECK(provider_);  
  DCHECK(num_active_consumers_ > 0);  
  auto consumer_it = consumers_.find(consumer);   
  DCHECK(consumer_it != consumers_.end());    
  const ConsumerInfo& info = \*consumer_it;  //<-- consumer_it may well be consumers_.end()  
  DCHECK(info.is_active);  

  info.is_active = false;  //<-- write to info, which may have come from consumers_.end()  

```

By calling GamepadMonitor::GamepadStopPolling without first calling GamepadMonitor::GamepadStartPolling (via mojo interface), consumers\_ will not contain the input GamepadConsumer (GamepadMonitor), this would result in consumers\_.end() being de-referenced and written to. By changing the DCHECK to a CHECK, I can verify that this is the case, however, I am unable to obtain an asan crash. (See the Reproduction case section)

**VERSION**  

Chrome Version: built from master commit faf9f3f, release build  

Operating System: Tested on Ubuntu 18.04.2 LTS with no effect, but results may be platform dependent (see REPRODUCTION CASE).

**REPRODUCTION CASE**  

First run the attached copy\_mojo\_js\_bindings.py to copy the generated mojo javascript files across.

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen

After that, create a directory hierarchy device/gamepad/public/mojom and copy the attached gamepad.mojom.js file into it. (This is specific to the commit faf9f3f, may need to change the file to test a different commit, for some reason the above file is not generated when I build)

Then run

$ python -m SimpleHTTPServer&

Change the following DCHECK into a CHECK:

<https://cs.chromium.org/chromium/src/device/gamepad/gamepad_service.cc?gsn=consumers_&g=0&rcl=e83e287f638ab87320d12e9218b2763f9eb6132e&l=119>

and run the following to simulate a compromised renderer.

$out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abc '<http://localhost:8000/gamepad_monitor3.html>'

This should cause an assertion failure showing that consumers\_.end() is being de-referenced. However, I'm unable to obtain an asan crash, so I don't know if there's other subtle protection that's in place.

To test whether this is an asan problem, I tried the following unit test case (I included it in flat\_set\_unittest.cc):

TEST(FlatSet, EmptySetInClass) {  

struct ConsumerInfo {  

ConsumerInfo(int consumer)  

: consumer(consumer), did\_observe\_user\_gesture(false) {}

```
bool operator<(const ConsumerInfo& other) const {  
  return consumer < other.consumer;  
}  

int consumer;  
mutable bool is_active;  
mutable bool did_observe_user_gesture;  

```

};

class B {  

public:  

std::set<ConsumerInfo> s;  

int x;  

void setActive(int consumer) {  

auto it = s.find(consumer);  

const ConsumerInfo& info = \*it;  

info.is\_active = false;  

}  

};  

B\* b = new B;  

b->setActive(1);  

delete b;  

}

Running it in an asan build will crash with heap over flow, so it looks like accessing set::end can result in access violation and asan is capable of detecting it.

However, I don't understand why it does not detect the case in GamepadService and I cannot be certain about whether this is actually safe or not. I am curious about why this is the case, so any insight into this will be greatly appreciated. This is tested on ubuntu linux 18.04.2 LTS but the behaviour may well be platform dependent.

Thank you very much for your help and please let me know if there is anything that I can help. Thanks!

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Man Yue Mo of Semmle Security Research Team

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [gamepad_monitor3.html](attachments/gamepad_monitor3.html) (text/plain, 416 B)
- [gamepad.mojom.js](attachments/gamepad.mojom.js) (text/plain, 67.6 KB)

## Timeline

### ct...@chromium.org (2019-08-28)

+gamepad/devices folks to help confirm whether this is a security issue. Thanks!

Conservatively setting security labels. If this is triggerable from a compromised renderer, it looks like this would (1) de-reference past the end of the iterator, (2) write into it (although as far as I can tell, this would be constrained to just the `info.is_active = false`).

[Monorail components: Blink>GamepadAPI]

### sh...@chromium.org (2019-08-29)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2019-08-31)

I think the analysis above is correct and a compromised renderer could cause us to write to set::end().

GamepadService should not trust the renderer to call GamepadStartPolling, GamepadStopPolling in a consistent way. I noticed there's some questionable behavior around |num_active_consumers_| as well. It is always incremented in GamepadStartPolling (even if the consumer was already active) and always decremented in GamepadStopPolling (even if the consumer wasn't found). This could cause unexpected calls to provider_->Pause and provider_->Resume. If GamepadStopPolling is called before any consumer becomes active, provider_ can be dereferenced before it's initialized.

### re...@chromium.org (2019-09-11)

Matt, do you have a fix for this?

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-14)

mattreynolds: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2019-09-16)

Fix in progress: https://crrev.com/c/1804379

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8ce86e4dd397fd208f581045206f1ce47e8528d

commit c8ce86e4dd397fd208f581045206f1ce47e8528d
Author: Matt Reynolds <mattreynolds@chromium.org>
Date: Wed Sep 18 18:52:34 2019

[gamepad] Enforce GamepadService consumers invariant

GamepadService maintains a set of GamepadConsumers that are
registered to receive gamepad events. In normal operation,
ConsumerBecameActive is called when the consumer is ready to
receive events and ConsumerBecameInactive is called when the
consumer wants to temporarily pause events without
unregistering. The |num_active_consumers_| member tracks how
many consumers are currently active and should always equal
the count of consumers in |consumers_| that have the is_active
flag set.

If a consumer calls these methods in an invalid order, this
invariant may be broken. For instance, calling
ConsumerBecameInactive will decrement |num_active_consumers_|
even if the consumer was already inactive. This CL enforces
the invariant by changing DCHECKs into CHECKs.

This also fixes a bug where consumers_.end() may be
dereferenced when ConsumerBecameInactive is called for a
consumer that was never added to |consumers_|.

BUG=998431

Change-Id: I86c53a481601cf05a66b3b0a8b011412660c805e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1804379
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Commit-Position: refs/heads/master@{#697706}

[modify] https://crrev.com/c8ce86e4dd397fd208f581045206f1ce47e8528d/device/gamepad/gamepad_monitor.cc
[modify] https://crrev.com/c8ce86e4dd397fd208f581045206f1ce47e8528d/device/gamepad/gamepad_service.cc
[modify] https://crrev.com/c8ce86e4dd397fd208f581045206f1ce47e8528d/device/gamepad/gamepad_service.h
[modify] https://crrev.com/c8ce86e4dd397fd208f581045206f1ce47e8528d/device/gamepad/gamepad_service_unittest.cc


### ma...@google.com (2019-09-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-19)

Requesting merge to stable M77 because latest trunk commit (697706) appears to be after stable branch point (681094).

Requesting merge to beta M77 because latest trunk commit (697706) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-19)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2019-09-19)

1. Yes, this is a high-severity security bug.

2. https://crrev.com/c/1804379

3. Yes, I verified this on ToT. Instead of dereferencing set::end, the repro steps now cause us to terminate the mojo connection:

[43704:43704:0919/154424.493496:ERROR:validation_errors.cc(87)] Invalid message: VALIDATION_ERROR_MESSAGE_HEADER_UNKNOWN_METHOD
[43704:43713:0919/154424.493693:ERROR:render_process_host_impl.cc(4608)] Terminating render process for bad Mojo message: Received bad user message: Validation failed for GamepadMonitor RequestValidator [VALIDATION_ERROR_MESSAGE_HEADER_UNKNOWN_METHOD
[43704:43713:0919/154424.493805:ERROR:bad_message.cc(27)] Terminating renderer for bad IPC message, reason 123

4. This fixes a high-severity security bug.

5. Not a new feature.

6. No Finch flag.

### ma...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-09-20)

Thanks for fixing this. The patch looks good and should prevent the problem. However, from the error message that you get with the repro, the mojo connection is likely to be terminated because the generated files in the test server is not up-to-date with the ones in the commit that you tested. (It is giving a VALIDATION_ERROR_MESSAGE_HEADER_UNKNOWN_METHOD which means that the affected method (GamepadStopPolling) wasn't actually triggered. This type of error usually means that the method id in the IPC message from renderer to browser does not match any method id in the compiled version of Chrome.) Try to run

$ python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen

again on the test server and then open the page again. The mojo connection should terminate with something like:

Terminating render process for bad Mojo message: GamepadMonitor::GamepadStopPolling failed

Please let me if that works. Thanks.

### sh...@chromium.org (2019-09-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2019-09-21)

Thanks mmo@, I'm getting the correct error message now:

[15100:15118:0920/180107.851523:ERROR:render_process_host_impl.cc(4608)] Terminating render process for bad Mojo message: Received bad user message: GamepadMonitor::GamepadStopPolling faile
[15100:15118:0920/180107.851620:ERROR:bad_message.cc(27)] Terminating renderer for bad IPC message, reason 123

### ma...@google.com (2019-09-21)

BTW, you can generate .js bindings with the blink_tests target, they aren't generated for the chrome build target:

autoninja -C out/asan blink_tests

I confirmed that the generated gamepad.mojom.js had the correct method IDs but was still getting VALIDATION_ERROR_MESSAGE_HEADER_UNKNOWN_METHOD. Turns out Chrome had cached the old version and kept using the old IDs.

### mm...@semmle.com (2019-09-23)

Thanks for the tip! I did wonder why some .js bindings are not generated and I sometimes have to copy them from code search. Yea I often spent sometime trying to figure out why some IPC doesn't work and then realised I forgot to clear the cache too :)

### na...@google.com (2019-09-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $15,000 for this report!

### na...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### ma...@google.com (2019-09-26)

+lakpamarthy@

This is still waiting for merge approval, please see the responses #14

### mm...@semmle.com (2019-09-26)

natashapabrai@ Thanks! My employer has a policy of donating reward to charity. Do you mind donating the reward to WWF (wwf.org.uk) please? Thanks.

### la...@google.com (2019-09-27)

merge approved to M78 branch 3904

mattreynolds@ - please merge to M78 ASAP so we can test this in next week's Beta. We will take this into M77 branch 3865 right after

Setting next action date as 10/04/19


### sr...@google.com (2019-09-27)

Please help complete the merge to M78 branch 3904 before Monday Sept 30, end of day PST.

### go...@chromium.org (2019-09-30)

Please merge your change to M78 branch 3904 ASAP if change continue to look good in canary. Thank you.

### ma...@google.com (2019-09-30)

Merged to M78 branch 3904:

https://chromium-review.googlesource.com/c/chromium/src/+/1831415

### sr...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### la...@google.com (2019-10-04)

merge approved for M77 branch 3865. please merge today as we are planning an M77 respin for 10/07.

### la...@google.com (2019-10-04)

rejecting this merge as the fix introduced a new crash in M78 (crbug/1011132) and is not ready for M77


### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

mattreynolds@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### sh...@chromium.org (2019-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/998431?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096127)*
