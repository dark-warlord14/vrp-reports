# Security: blink::WeekInputType uaf vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40083041](https://issues.chromium.org/issues/40083041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **CVE IDs** | CVE-2015-6777 |
| **Reporter** | lv...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2015-10-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A blink::WeekInputType object is freed in a event handler,but be used again after the handler. A simple analysis and poc file is in the attachment.

**VERSION**  

Chrome Version: 46.0.2490.71 stable  

Operating System: win7 with full pack

CRASH  

(fb0.1ee0): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

eax=4f416850 ebx=00000000 ecx=4f48c8d0 edx=62e05cb4 esi=40690000 edi=4f48c8d0  

eip=61005f6a esp=0028df00 ebp=0028df78 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010206  

chrome\_child!blink::Element::userAgentShadowRoot+0x10:  

61005f6a 8bb688000000 mov esi,dword ptr [esi+88h] ds:0023:40690088=????????  

0:000> dd edi  

4f48c8d0 e0ca484f 30404030 30404000 3042c3f4  

4f48c8e0 00000000 00000000 00000000 00000000  

4f48c8f0 00000000 00000000 00000000 00000001  

4f48c900 00000004 30404030 30404000 30438078  

4f48c910 00000000 00000000 00000000 00000000  

4f48c920 00000000 00000000 00000000 00000001  

4f48c930 00000005 30404030 30404000 304bc000  

4f48c940 00000000 00000000 00000000 00000000  

0:000> kvn L20

# ChildEBP RetAddr Args to Child

00 (Inline) -------- -------- -------- -------- chrome\_child!blink::Element::userAgentShadowRoot+0x10 (Inline Function @ 61005f6a) (CONV: thiscall)  

01 (Inline) -------- -------- -------- -------- chrome\_child!blink::BaseMultipleFieldsDateAndTimeInputType::clearButtonElement+0x13 (Inline Function @ 61005f6a) (CONV: thiscall)  

02 0028df78 61005d08 62e05e40 3047c000 0028e288 chrome\_child!blink::BaseMultipleFieldsDateAndTimeInputType::updateClearButtonVisibility+0x20 (FPO: [Non-Fpo]) (CONV: thiscall)  

03 0028e1c0 60bf5849 62e05e40 3047c000 0028e288 chrome\_child!blink::BaseMultipleFieldsDateAndTimeInputType::updateView+0x48f (FPO: [Non-Fpo]) (CONV: thiscall)  

04 0028e1e0 60a3f134 62e05e40 0028e288 0028e288 chrome\_child!blink::HTMLInputElement::parseAttribute+0x413 (FPO: [Non-Fpo]) (CONV: thiscall)  

05 0028e210 60a821fd 62e05e40 0028e288 00000000 chrome\_child!blink::Element::attributeChanged+0x60 (FPO: [Non-Fpo]) (CONV: thiscall)  

06 0028e230 60a81cce 62e05e40 0028e288 0028e2ec chrome\_child!blink::Element::didAddAttribute+0x48 (FPO: [Non-Fpo]) (CONV: thiscall)  

07 (Inline) -------- -------- -------- -------- chrome\_child!blink::Element::appendAttributeInternal+0x44 (Inline Function @ 60a81cce) (CONV: thiscall)  

08 (Inline) -------- -------- -------- -------- chrome\_child!blink::Element::setAttributeInternal+0x6d (Inline Function @ 60a81cce) (CONV: thiscall)  

09 0028e268 612d87af 62e05e40 0028e288 00000000 chrome\_child!blink::Element::setAttribute+0xf3 (FPO: [Non-Fpo]) (CONV: thiscall)  

0a 0028e28c 612d8826 0028e3a4 0866a3f8 0028e2d0 chrome\_child!blink::HTMLInputElementV8Internal::minAttributeSetter+0x60 (FPO: [Non-Fpo]) (CONV: cdecl)  

0b 0028e29c 609e3628 0028e2b4 0028e39c 0028e39c chrome\_child!blink::HTMLInputElementV8Internal::minAttributeSetterCallback+0x3e (FPO: [Non-Fpo]) (CONV: cdecl)  

0c 0028e2d0 609e33cb 0028e348 612d87e8 0028e474 chrome\_child!v8::internal::FunctionCallbackArguments::Call+0x7e (FPO: [Non-Fpo]) (CONV: thiscall)  

0d 0028e364 60a457bf 0028e394 0866a3f8 0028e848 chrome\_child!v8::internal::HandleApiCallHelper<0>+0x3c0 (FPO: [Non-Fpo]) (CONV: cdecl)  

0e 0028e42c 609a8b6b 087e22d4 0028e848 0028e4e0 chrome\_child!v8::internal::Builtins::InvokeApiFunction+0xff (FPO: [Non-Fpo]) (CONV: cdecl)

## Attachments

- [poc.zip](attachments/poc.zip) (application/zip, 12.6 KB)

## Timeline

### cl...@chromium.org (2015-10-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6480023970643968

### cl...@chromium.org (2015-10-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6480023970643968

Uploader: ochang@google.com
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0d644ffc
Crash State:
  blink::BaseMultipleFieldsDateAndTimeInputType::updateClearButtonVisibility
  blink::BaseMultipleFieldsDateAndTimeInputType::updateView
  blink::BaseMultipleFieldsDateAndTimeInputType::stepAttributeChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=354442:354460

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95qhB6B-Ijg1pbcEGTBEXHaIU_60lzW6m-0jJ2i462kLqywZVrU-MFaAnr2RDMbeheuJVjF4jVZmnyOx9taijdSLQg4ibYH4RrrnUpx31a8dAB7QS5LJo8udyb4yUN9XuH1aTo9KJMx5WMp46fWeK7N181l1g
<script>			
 element_4=document.createElement('input'); 
 element_4.type='week'; 
element_4.stepUp(); 
 element_4.addEventListener('DOMCharacterDataModified',eventHandle); 
element_4.min=true; 
			function eventHandle(){
element_4.setAttribute('type','text');
			}			
		</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

I'll take this one since I fixed a similar bug in the past. Assuming high severity for now.

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

Did some digging, couldn't get the repro to work on Linux, but I suspect it's possible.

Here's a better stack of how the event handler (which causes the week element to be freed) gets reached (from the element_4.min = true; line):
00dca794 137e8c26 chrome_child!blink::Node::dispatchScopedEvent [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\Node.cpp @ 1984]
00dca870 137e3fcd chrome_child!blink::CharacterData::didModifyData+0x576 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\CharacterData.cpp @ 199]
00dca8f0 137e3a53 chrome_child!blink::CharacterData::setDataAndUpdate+0x2ed [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\wtf\RefPtr.h @ 58]
00dca934 137b252a chrome_child!blink::CharacterData::setData+0x153 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\CharacterData.cpp @ 54]
00dcab30 13d96d5f chrome_child!blink::Text::replaceWholeText+0x11ca [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\Text.cpp @ 221]
00dcac10 13d9ba63 chrome_child!blink::DateTimeFieldElement::updateVisibleValue+0x1af [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\wtf\PassRefPtr.h @ 73]
00dcac28 13d91bae chrome_child!blink::DateTimeNumericFieldElement::setValueAsInteger+0x73 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\html\shadow\DateTimeNumericFieldElement.cpp @ 181]
00dcac3c 13d87f18 chrome_child!blink::DateTimeWeekFieldElement::setValueAsDate+0x2e [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\html\shadow\DateTimeFieldElements.cpp @ 553]
00dcac70 13d57260 chrome_child!blink::DateTimeEditElement::setValueAsDate+0xc8 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp @ 748]
00dcb010 13d56738 chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::updateView+0xb20 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\html\forms\BaseMultipleFieldsDateAndTimeInputType.cpp @ 538]
00dcb018 139525dc chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::minOrMaxAttributeChanged+0x8 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\html\forms\BaseMultipleFieldsDateAndTimeInputType.cpp @ 466]
00dcb130 13662eb4 chrome_child!blink::HTMLInputElement::parseAttribute+0x148c [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\wtf\RefPtr.h @ 71]
00dcb248 1367a193 chrome_child!blink::Element::attributeChanged+0xe4 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\wtf\RawPtr.h @ 118]
00dcb270 1367978f chrome_child!blink::Element::didAddAttribute+0x203 [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\Element.cpp @ 3139]
00dcb2ec 13652bce chrome_child!blink::Element::appendAttributeInternal+0x1ff [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\Element.cpp @ 2284]
00dcb3b0 1624e345 chrome_child!blink::Element::setAttribute+0x44e [C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\core\dom\Element.cpp @ 1147]

The problem here is that BaseMultipleFieldsDateAndTimeInputType::updateView doesn't expect |this| to be freed by anything it does, so when control returns and updateClearButtonVisibility gets called, we get a UAF. This can be easily fixed in this instance with a RefPtr, but seeing as we've seen bugs like this before I want to see if there is a better more general fix here to prevent these input type bugs.

### oc...@chromium.org (2015-10-16)

+tkent for thoughts.

### cl...@chromium.org (2015-10-17)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### tk...@chromium.org (2015-10-18)

In this test case, DOMCharacterDataModified should not be visible because the trigger node is in a shadow tree.

Hayato, do we have any behavior change recently?


### oc...@chromium.org (2015-10-20)

I've been trying to repro this on Linux today, but can't figure out why it doesn't.

My theory is that in ContainerNode::notifyNodeInsertedInternal:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/ContainerNode.cpp&l=832&cl=GROK&gsn=build&rcl=1445369217

    for (Node& node : NodeTraversal::inclusiveDescendantsOf(root)) {
        // As an optimization we don't notify leaf nodes when when inserting
        // into detached subtrees.
        if (!inDocument() && !node.isContainerNode())
            continue;

If the a child node in the tree that got inserted is not in the document and not a container node (e.g. a Text node), the |IsInShadowTreeFlag| flag doesn't get set, so when we get to DateTimeFieldElement::updateVisibleValue -> Text::replaceWholeText -> ... -> CharacterData::didModifyData(), the isInShadowTree() check fails and the DOMCharacterDataModified event gets dispatched.

I'll attempt to verify this locally on a Windows build.

### oc...@chromium.org (2015-10-21)

Verified locally that this is indeed the issue. Will put up a patch for review.

Also, it appears that this code path *does* reproduce under Linux -- I can see the mutation event triggering for my official build Chrome on my workstation, and my Debug non-ASan build.

It seems that ASan builds don't hit this at all (no fields get added to the DateTimeEditElement element by the DateTimeEditBuilder). Will take a look into this too.




### oc...@chromium.org (2015-10-21)

Ok I figured out why this wasn't hitting on Linux -- my container overflow annotations which disabled inlineCapacity was the reason -- the DateTimeEditElement::m_fields Vector expects an inlineCapacity of 8, but gets a capacity of 0 instead.

### bu...@chromium.org (2015-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb4d5d9ab41449b79fcf6f84d8983be2b12bd490

commit eb4d5d9ab41449b79fcf6f84d8983be2b12bd490
Author: ochang <ochang@chromium.org>
Date: Wed Oct 21 05:33:04 2015

Fix an optimisation in ContainerNode::notifyNodeInsertedInternal

R=tkent@chromium.org
BUG=544020

Review URL: https://codereview.chromium.org/1420653003

Cr-Commit-Position: refs/heads/master@{#355240}

[add] http://crrev.com/eb4d5d9ab41449b79fcf6f84d8983be2b12bd490/third_party/WebKit/LayoutTests/fast/forms/week-multiple-fields/week-multiple-fields-no-shadow-event-expected.txt
[add] http://crrev.com/eb4d5d9ab41449b79fcf6f84d8983be2b12bd490/third_party/WebKit/LayoutTests/fast/forms/week-multiple-fields/week-multiple-fields-no-shadow-event.html
[modify] http://crrev.com/eb4d5d9ab41449b79fcf6f84d8983be2b12bd490/third_party/WebKit/Source/core/dom/ContainerNode.cpp
[modify] http://crrev.com/eb4d5d9ab41449b79fcf6f84d8983be2b12bd490/third_party/WebKit/Source/core/dom/Element.h


### oc...@chromium.org (2015-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-10-21)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-47; it appears the fix may have landed after branch point, meaning a merge might be required. Please confirm if a merge is required here - if so add Merge-Request-47 label, otherwise remove Merge-TBD label. Thanks.

### cl...@chromium.org (2015-10-21)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6480023970643968

Uploader: ochang@google.com
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0d644ffc
Crash State:
  blink::BaseMultipleFieldsDateAndTimeInputType::updateClearButtonVisibility
  blink::BaseMultipleFieldsDateAndTimeInputType::updateView
  blink::BaseMultipleFieldsDateAndTimeInputType::stepAttributeChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=354442:354460

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95qhB6B-Ijg1pbcEGTBEXHaIU_60lzW6m-0jJ2i462kLqywZVrU-MFaAnr2RDMbeheuJVjF4jVZmnyOx9taijdSLQg4ibYH4RrrnUpx31a8dAB7QS5LJo8udyb4yUN9XuH1aTo9KJMx5WMp46fWeK7N181l1g
<script>			
 element_4=document.createElement('input'); 
 element_4.type='week'; 
element_4.stepUp(); 
 element_4.addEventListener('DOMCharacterDataModified',eventHandle); 
element_4.min=true; 
			function eventHandle(){
element_4.setAttribute('type','text');
			}			
		</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### oc...@chromium.org (2015-10-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-30)

[Automated comment] Request affecting a post-stable build (M46), manual review required.

### ti...@google.com (2015-10-30)

Congrats your change is auto-approved for M47 (branch: 2526)

### ke...@google.com (2015-11-02)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-02)

M46 Stable and Stable refresh have both launched, the merge bar for M46 is very high as we only consider 0-day level of critical Security/ Stability/ Critical regressions.

### ti...@google.com (2015-11-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d35b5d9521359610255d0322bfeaa3f84e3abf7d

commit d35b5d9521359610255d0322bfeaa3f84e3abf7d
Author: Martin Barbella <mbarbella@chromium.org>
Date: Fri Nov 06 21:29:48 2015

Fix an optimisation in ContainerNode::notifyNodeInsertedInternal

TBR=ochang@chromium.org
BUG=544020

Review URL: https://codereview.chromium.org/1420653003

Cr-Commit-Position: refs/heads/master@{#355240}
(cherry picked from commit eb4d5d9ab41449b79fcf6f84d8983be2b12bd490)

Review URL: https://codereview.chromium.org/1429303004 .

Cr-Commit-Position: refs/branch-heads/2526@{#340}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[add] http://crrev.com/d35b5d9521359610255d0322bfeaa3f84e3abf7d/third_party/WebKit/LayoutTests/fast/forms/week-multiple-fields/week-multiple-fields-no-shadow-event-expected.txt
[add] http://crrev.com/d35b5d9521359610255d0322bfeaa3f84e3abf7d/third_party/WebKit/LayoutTests/fast/forms/week-multiple-fields/week-multiple-fields-no-shadow-event.html
[modify] http://crrev.com/d35b5d9521359610255d0322bfeaa3f84e3abf7d/third_party/WebKit/Source/core/dom/ContainerNode.cpp
[modify] http://crrev.com/d35b5d9521359610255d0322bfeaa3f84e3abf7d/third_party/WebKit/Source/core/dom/Element.h


### bu...@chromium.org (2015-11-07)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/d35b5d9521359610255d0322bfeaa3f84e3abf7d

commit d35b5d9521359610255d0322bfeaa3f84e3abf7d
Author: Martin Barbella <mbarbella@chromium.org>
Date: Fri Nov 06 21:29:48 2015


### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Congratulations - our panel decided to award you $3,000 for your report!

We'll credit you in our M47 release notes as "lvbluesky". If you would like to use a different name, please update this bug and we can update the release notes. We'll also provide you with a CVE in a few hours from now for your reference.

A member of our finance team shall be in contact within a week to collect payment details. If that doesn't happen, please either update this bug or email me directly at timwillis@.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### lv...@gmail.com (2015-12-01)

Please credit  me as 'Long Liu of Qihoo 360Vulcan Team', thank you!

### ti...@google.com (2015-12-01)

Shall do - CVE is CVE-2015-6777. Thanks!

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-27)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/544020?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083041)*
