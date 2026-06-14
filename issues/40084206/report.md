# Security: Heap-use-after-free in autofill components

| Field | Value |
|-------|-------|
| **Issue ID** | [40084206](https://issues.chromium.org/issues/40084206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | va...@chromium.org |
| **Created** | 2016-04-29 |
| **Bounty** | $1,000.00 |

## Description

Chrome version: 50.0.2661.75

There are multiple UAF vulnerabilities in the autofill components, caused by the fact that autofill is implemented by calling WebFormControlElement::setValue with sendEvents=true. As a result, whenever a form field is auto-filled, the input event listeners of the web page are triggered, which can invalidate the frame, destruct the RenderFrameObserver and result in a UAF.

The attached PoC offers simple instructions to reproduce the UAF: Generate autofill data, and choose a suggested autofill item.

 
Vulnerable locations:
- https://chromium.googlesource.com/chromium/src/+/5bc61f8f605564730b06f14e243681e930c7cb88/components/autofill/content/renderer/form_autofill_util.cc#894

- https://chromium.googlesource.com/chromium/src/+/888a550ad227b3546baa480c386640e206f36319/components/autofill/content/renderer/form_cache.cc#215
- https://chromium.googlesource.com/chromium/src/+/888a550ad227b3546baa480c386640e206f36319/components/autofill/content/renderer/form_cache.cc#224
- https://chromium.googlesource.com/chromium/src/+/888a550ad227b3546baa480c386640e206f36319/components/autofill/content/renderer/form_cache.cc#232

- https://chromium.googlesource.com/chromium/src/+/48c8ef0f7d7dccfbf818c289c771ca2ddaece9aa/components/autofill/content/renderer/password_autofill_agent.cc#502
- https://chromium.googlesource.com/chromium/src/+/48c8ef0f7d7dccfbf818c289c771ca2ddaece9aa/components/autofill/content/renderer/password_autofill_agent.cc#608
- https://chromium.googlesource.com/chromium/src/+/48c8ef0f7d7dccfbf818c289c771ca2ddaece9aa/components/autofill/content/renderer/password_autofill_agent.cc#681 (=PoC)
- https://chromium.googlesource.com/chromium/src/+/48c8ef0f7d7dccfbf818c289c771ca2ddaece9aa/components/autofill/content/renderer/password_autofill_agent.cc#807
- https://chromium.googlesource.com/chromium/src/+/48c8ef0f7d7dccfbf818c289c771ca2ddaece9aa/components/autofill/content/renderer/password_autofill_agent.cc#812

- https://chromium.googlesource.com/chromium/src/+/578305d33ed2580610f3cdbb8ca529dfc3faf195/components/autofill/content/renderer/password_generation_agent.cc#96
- https://chromium.googlesource.com/chromium/src/+/578305d33ed2580610f3cdbb8ca529dfc3faf195/components/autofill/content/renderer/password_generation_agent.cc#277

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan-autofill-auto-50.0.2661.75.log](attachments/asan-autofill-auto-50.0.2661.75.log) (text/plain, 19.8 KB)
- [uaf-autofill-auto.html](attachments/uaf-autofill-auto.html) (text/plain, 1.3 KB)
- [uaf-autofill-clear-email.html](attachments/uaf-autofill-clear-email.html) (text/plain, 1.1 KB)
- [asan-autofill-clear-email-50.0.2661.94.log](attachments/asan-autofill-clear-email-50.0.2661.94.log) (text/plain, 20.0 KB)
- [npe-autofill-set-email.html](attachments/npe-autofill-set-email.html) (text/plain, 876 B)
- [asan-autofill-set-email-50.0.2661.94.log](attachments/asan-autofill-set-email-50.0.2661.94.log) (text/plain, 6.6 KB)

## Timeline

### rs...@chromium.org (2016-05-02)

Seems like a general variant of https://crbug.com/chromium/608100.

### rs...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### is...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-05-02)

@resek (https://crbug.com/chromium/608101#c1)
Sorry for the confusion, I attached the test cases and stack traces to the wrong report.

This bug differs from https://crbug.com/chromium/608100 in that their root causes are different: This one could be fixed by making sure that WebFormControlElement::setValue does not synchronously trigger events in the web page, the other bug has to be resolved in a different way.

I've deleted the test case and log file from the initial report, see https://crbug.com/chromium/608100 if you want to see it anyway.

### va...@chromium.org (2016-05-03)

To fix the related https://crbug.com/chromium/608100 I am postponing the deletion of the agent in https://codereview.chromium.org/1943873002/. It seems to me that this postponing will also fix this issue. Therefore I'll mark this one as a duplicate of https://crbug.com/chromium/608100. Please speak up if you disagree.

### ro...@robwu.nl (2016-05-03)

Re-opening because the patch for the other bug did not fix this bug. You only addressed two of the 4 files.


FormCache::ClearFormWithElement [1] is still vulnerable to UAF. I didn't build master with your patch, because the ASAN trace clearly shows that the UAF occurs before control is returned to the classes that you fixed.
See asan-autofill-clear-email-50.0.2661.94.log and uaf-autofill-clear-email.html for a UAF.
See asan-autofill-set-email-50.0.2661.94.log and npe-autofill-set-email.html for a nullptr dereference.

PasswordGenerationAgent also inherits from a RenderFrameObserver, so it is also vulnerable (I didn't bother with a test case yet, feel free to ask).


[1] https://chromium.googlesource.com/chromium/src/+/5bc61f8f605564730b06f14e243681e930c7cb88/components/autofill/content/renderer/form_autofill_util.cc#894

### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/50bf9075cac0e5d69f5adfc0763968d5afa1734b

commit 50bf9075cac0e5d69f5adfc0763968d5afa1734b
Author: vabr <vabr@chromium.org>
Date: Wed May 04 09:13:51 2016

Revert of Postpone deletion of (Password)AutofillAgent (patchset #1 id:1 of https://codereview.chromium.org/1943873002/ )

Reason for revert:
This fix is not complete, I need to also handle disabling the LegacyAutofillAgent.

Because the final fix is going to be merged, I prefer to have the complete solution in one CL. Therefore I am reverting this partial fix, and will reintroduce it in a new CL. Sorry for the noise.

BUG=609010, 609007, 608100, 608101

Original issue's description:
> Postpone deletion of (Password)AutofillAgent
>
> Currently, the two agent classes delete themselves immediately on destruction
> of the RenderFrame they are observing. This CL postpones the deletion to a
> separately posted task, to avoid the situation when the agent is deleted while
> still having methods in progress lower on the stack.
>
> BUG=608100
>
> Committed: https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506
> Cr-Commit-Position: refs/heads/master@{#391236}

TBR=mathp@chromium.org,dvadym@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=608100

Review-Url: https://codereview.chromium.org/1951813002
Cr-Commit-Position: refs/heads/master@{#391465}

[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/password_autofill_agent.h


### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9de81f45c73a8f9f215fc234a6adfe087b0eab74

commit 9de81f45c73a8f9f215fc234a6adfe087b0eab74
Author: vabr <vabr@chromium.org>
Date: Wed May 04 10:48:04 2016

Remove WeakPtrFactory from PasswordAutofillAgent

Unlike in AutofillAgent, the factory is no longer used in PAA.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101,433486

Review-Url: https://codereview.chromium.org/1945723003
Cr-Commit-Position: refs/heads/master@{#391475}

[modify] https://crrev.com/9de81f45c73a8f9f215fc234a6adfe087b0eab74/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/9de81f45c73a8f9f215fc234a6adfe087b0eab74/components/autofill/content/renderer/password_autofill_agent.h


### ro...@robwu.nl (2016-05-04)

Vaclav, the last version (patchset 4 of https://codereview.chromium.org/1946143002/) does not fix the UAF from #6, at
https://chromium.googlesource.com/chromium/src/+/888a550ad227b3546baa480c386640e206f36319/components/autofill/content/renderer/form_cache.cc#219

It seems that |element| points to invalid memory (assuming that the left hand side of == is evaluated first):

Thread 27 "Chrome_InProcRe" hit Breakpoint 3, ClearFormWithElement () at ../../components/autofill/content/renderer/form_cache.cc:190
.......
215           input_element->setValue(base::string16(), true);
(gdb) 
219           if (element == *input_element) {
(gdb) s
operator== () at ../../third_party/WebKit/public/web/WebNode.h:163
163         return a.equals(b);
(gdb) s
equals () at ../../third_party/WebKit/Source/web/WebNode.cpp:123
123         return m_private.get() == n.m_private.get();
(gdb) s
get () at ../../third_party/WebKit/Source/web/WebNode.cpp:123
123         return m_private.get() == n.m_private.get();
(gdb) s
get () at ../../third_party/WebKit/public/web/../platform/WebPrivatePtr.h:162
162         T* get() const { return m_handle ? m_handle->get() : 0; }
(gdb) s
=================================================================
==5436==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160004a6978 at pc 0x55555c8fb193 bp 0x7fffbcb909e0 sp 0x7fffbcb909d8



And you should also add a check after this line, or the next line is going to have a nullptr deference at best, or a UAF at worst:
https://chromium.googlesource.com/chromium/src/+/5bc61f8f605564730b06f14e243681e930c7cb88/components/autofill/content/renderer/form_autofill_util.cc#903

### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d62bc3e6e2c3be6bbb01fa325e3389f089974017

commit d62bc3e6e2c3be6bbb01fa325e3389f089974017
Author: vabr <vabr@chromium.org>
Date: Wed May 04 15:58:52 2016

Destroy (Password)AutofillAgent safely

AutofillAgent and related code often edits field values. Those edits may trigger JavaScript capable of deleting the associated frame. Currently, AutofillAgent and related classes are RenderFrameObservers and delete themselves on the frame deletion. This results in use-after-free if the deletion happens up in the stack and there is still the method which changed the field value down on the stack.

Therefore this CL postpones deletion by sending a DeleteSoon task on the frame destruction. The CL also changes a couple of places relying on render frame being alive if the observer is alive to handle a null frame gratefully.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101

Review-Url: https://codereview.chromium.org/1946143002
Cr-Commit-Position: refs/heads/master@{#391524}

[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_autofill_agent.h
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_generation_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_generation_agent.h


### bu...@chromium.org (2016-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7e112c1563632f57cfa1c4fa964987f823da17fa

commit 7e112c1563632f57cfa1c4fa964987f823da17fa
Author: Vaclav Brozek <vabr@chromium.org>
Date: Mon May 09 07:18:24 2016

Destroy (Password)AutofillAgent safely

AutofillAgent and related code often edits field values. Those edits may trigger JavaScript capable of deleting the associated frame. Currently, AutofillAgent and related classes are RenderFrameObservers and delete themselves on the frame deletion. This results in use-after-free if the deletion happens up in the stack and there is still the method which changed the field value down on the stack.

Therefore this CL postpones deletion by sending a DeleteSoon task on the frame destruction. The CL also changes a couple of places relying on render frame being alive if the observer is alive to handle a null frame gratefully.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101

Review-Url: https://codereview.chromium.org/1946143002
Cr-Commit-Position: refs/heads/master@{#391524}
(cherry picked from commit d62bc3e6e2c3be6bbb01fa325e3389f089974017)

Review URL: https://codereview.chromium.org/1960023002 .

Cr-Commit-Position: refs/branch-heads/2704@{#441}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_autofill_agent.h
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_generation_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_generation_agent.h


### cl...@chromium.org (2016-05-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-05-09)

Re-opening since there are still unpatched vulnerabilities, see https://crbug.com/chromium/608101#c6 and 9.

### va...@chromium.org (2016-05-09)

(I will be looking into this more, am just swamped at the moment.)

### ro...@robwu.nl (2016-05-09)

I just tested with ASAN on HEAD (52.0.2730.0) and the test case from https://crbug.com/chromium/608101#c6 does not crash any more.

In the test case in https://crbug.com/chromium/608101#c6 I overlooked that |element| in FormCache::ClearFormWithElement is owned by AutofillAgent. Your fix of deferrring the AutofillAgent destruction means that |element| is no longer a dangling pointer. so the issue as a whole has been fixed.

### va...@chromium.org (2016-05-10)

Thanks for the update!

I still think you are correct with the last sentence in #9 -- it is apparently possible to listen to selection changes, so the existence of the frame on line 905 should be checked. https://chromium.googlesource.com/chromium/src/+/5bc61f8f605564730b06f14e243681e930c7cb88/components/autofill/content/renderer/form_autofill_util.cc#905

I'll try to find time to put up a fix and ideally a test (I'm still owing to supply the tests for the already landed patch as well). It is still a bit fragile, though, anybody can introduce this kind of vulnerability in the future, I wonder what to do to prevent such interleaving of JavaScript and C++ code execution.

### ro...@robwu.nl (2016-05-10)

#16
At first I thought that setSelectionRange would trigger JS, but when I took a closer look it appears that WebFormControlElement::setSelectionRange does not dispatch events (and even if it did, then not synchronously), so there should not be any issue at that line.

You did a pretty good job at fixing it.


About preventing this kind of vulnerability: Blink has a (non-public) ScriptForbiddenScope object, which prevents script from running while the ScriptForbiddenScope is active. This could be used to eagerly detect such issues.

A general way to avoid side effects due to unexpected events is to not dispatch them synchronously, but schedule them for later (like setSelectionRange does).

### sh...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-05-10)

Thanks for the helpful answer (and for the great reports, by the way!).

Asynchronous dispatching looks indeed like a good option. But setSelectionRange actually seems to dispatch no events at all? I guess I'll need to understand more of how Blink works here before being able to fix this properly.

### ti...@google.com (2016-05-24)

Marking this as "started" as it appears as though there is more work to be done here.

### cl...@chromium.org (2016-05-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### va...@chromium.org (2016-05-25)

#20 -- No, sorry for my confusing phrasing. There is no more work to be done to fix this issue. The note in #19 is about preventing similar stuff in the future.

### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

Updating severity due to required interaction.

### ti...@google.com (2016-06-06)

$1,000 here as noted in the release notes. Panel provided a reduced amount due to the amount of interaction required.

I'll put this in the system this week for payment.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-31)

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

This issue was migrated from crbug.com/chromium/608101?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/608100]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084206)*
