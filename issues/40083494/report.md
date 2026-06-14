# ASSERTION FAILED: index < arraySize

| Field | Value |
|-------|-------|
| **Issue ID** | [40083494](https://issues.chromium.org/issues/40083494) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2016-01-06 |
| **Bounty** | $3,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium: 49.0.2615.0 (Developer Build) (64-bit)
          linux-release-asan-symbolized-linux-release-367812

Repro-file as an attachment.

ASAN-trace:

ASSERTION FAILED: index < arraySize
../../third_party/WebKit/Source/wtf/BitArray.h(44) : void WTF::BitArray<396>::set(unsigned int) [arraySize = 396]
1   0x5573f1e866ed
2   0x5573f4de9528
3   0x5573f5b5854a
4   0x5573f4f1db9a
5   0x5573f46c081d
6   0x5573f46c05d2
7   0x5573f46eb300
8   0x5573f46bde72
9   0x5573f46bdcbe
10  0x5573f46bd964
11  0x5573f46bd729
12  0x5573f6a2dc9e
13  0x5573f6a2d187
14  0x5573f2fc85f2
15  0x5573f23ed556
16  0x5573f2433934
17  0x5573f23f2320
18  0x7fbf5830c4bb
ASAN:DEADLYSIGNAL
=================================================================
==25975==ERROR: AddressSanitizer: SEGV on unknown address 0x00009f7537dd (pc 0x5573f4de9528 bp 0x7ffc279ab1f0 sp 0x7ffc279ab1e0 T0)
    #0 0x5573f4de9527 in WTF::BitArray<396u>::set(unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/BitArray.h:44 (discriminator 3)
    #1 0x5573f5b58549 in blink::StylePropertySerializer::StylePropertySetForSerializer::StylePropertySetForSerializer(blink::StylePropertySet const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/css/StylePropertySerializer.cpp:63 (discriminator 1)
    #2 0x5573f4f1db99 in blink::StylePropertySet::asText() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/css/StylePropertySet.cpp:395
    #3 0x5573f46c081c in blink::Element::synchronizeStyleAttributeInternal() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:3378 (discriminator 1)
    #4 0x5573f46c05d1 in blink::Element::synchronizeAllAttributes() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:404
    #5 0x5573f46eb2ff in cloneAttributesFromElement /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:3313
    #6 0x5573f46bde71 in blink::Element::cloneDataFromElement(blink::Element const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:3356
.
.
.

## Attachments

- [chrome-SEGV-WTFBitArray396uset10-min.html](attachments/chrome-SEGV-WTFBitArray396uset10-min.html) (text/html, 373 B)

## Timeline

### in...@chromium.org (2016-01-06)

Should we change these security asserts to release asserts, just like vector.h. Thoughts ?

### cl...@chromium.org (2016-01-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6485955483009024

### cl...@chromium.org (2016-01-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6485955483009024

Uploader: nparker@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: index < arraySize
  blink::StylePropertySerializer::StylePropertySetForSerializer::StylePropertySetF
  blink::StylePropertySet::asText
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=365683:366004

Minimized Testcase (0.17 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96y6LsyocBNonc1_9zLBoOqNf7hkHOJv7a16F6xKYiVpbHviOegAT6aoYNd5N3WRqG1btQvXFoePZI1cDNfhpn4F-q3zP7--7V-QdofW9qrftV7crmK5yrphRpNZLEitjJi-EK2cdUA0HYAcoZrXO8f2w8-dw
>
<script> 
var test0=document.body.appendChild(document.createElement("hgroup"))
test0.style['all']='initial';
test0.style.setProperty('--a','a');
test0.cloneNode();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-01-07)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-01-07)

Do you mean RELEASE_ASSERT_WITH_SECURITY_IMPLICATION or just RELEASE_ASSERT? I'm for the first one, because such cases probably lead to out-of-bounds read/write, so it would be useful to catch them with ASAN while fuzzing.

### in...@chromium.org (2016-01-07)

Well we have used RELEASE_ASSERT in past since that will lead to hard crashes. Atleast in vectors i remember we can hit those from several places, so hard to fix them all. For these ones, we can start with RELEASE_ASSERT_WITH_SECURITY_IMPLICATION  and based on results, move to RELEASE_ASSERT if noise is too much in fuzzing.

Example - https://code.google.com/p/chromium/codesearch#search/&q=file:wtf%20(ASSERT%7CASSERT_WITH_SECURITY_IMPLICATION)%5B(%5D.*index&sq=package:chromium&type=cs

We need to check if these are used in hot places since we can't regress performance. So, check out callers before converting.

Results 1 - 8 of 8 (0.094 seconds)
 
View style
chromium src/third_party/WebKit/Source/wtf/Deque.h Show 4 matches
 WTF::DequeIteratorBase::increment
   506: {
   507:     ASSERT(m_index != m_deque->m_end);
   508:     ASSERT(m_deque->m_buffer.capacity());
 WTF::DequeIteratorBase::decrement
   517: {
   518:     ASSERT(m_index != m_deque->m_start);
   519:     ASSERT(m_deque->m_buffer.capacity());
 WTF::DequeIteratorBase::after
   528: {
   529:     ASSERT(m_index != m_deque->m_end);
   530:     return &m_deque->m_buffer.buffer()[m_index];
chromium src/third_party/WebKit/Source/wtf/BitArray.h
 WTF::BitArray::set
    43: {
    44:     ASSERT_WITH_SECURITY_IMPLICATION(index < arraySize);
    45:     m_data[index / 8] |= 1 << (index & 7);
 WTF::BitArray::clear
    49: {
    50:     ASSERT_WITH_SECURITY_IMPLICATION(index < arraySize);
    51:     m_data[index / 8] &= ~(1 << (index & 7));
 WTF::BitArray::get
    55: {
    56:     ASSERT_WITH_SECURITY_IMPLICATION(index < arraySize);
    57:     return !!(m_data[index / 8] & (1 << (index & 7)));
chromium src/third_party/WebKit/Source/wtf/dtoa/utils.h
 WTF::double_conversion::Vector
   167: T& operator[](int index) const {
   168:     ASSERT(0 <= index && index < length_);
   169:     return start_[index];


### in...@chromium.org (2016-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-10)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-01-11)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-12)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### am...@google.com (2016-01-12)

Looks like OS-Linux at a minimum, please add additional platforms if they are impacted as well.

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-26)

mmoroz@: Uh oh! This issue is still open and hasn't been updated in the last 18 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/061aa9a7b651d4e1adf2cbe6348d37d26cbf5d3c

commit 061aa9a7b651d4e1adf2cbe6348d37d26cbf5d3c
Author: mmoroz <mmoroz@chromium.org>
Date: Fri Feb 05 00:19:14 2016

Change assert to release assert for Deque to prevent out-of-bounds access.

R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org
BUG=574802

Review URL: https://codereview.chromium.org/1657933004

Cr-Commit-Position: refs/heads/master@{#373676}

[modify] http://crrev.com/061aa9a7b651d4e1adf2cbe6348d37d26cbf5d3c/third_party/WebKit/Source/wtf/Deque.h


### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8d32dd6e615b7b76c8e89d36f6ccf8786102180

commit c8d32dd6e615b7b76c8e89d36f6ccf8786102180
Author: mmoroz <mmoroz@chromium.org>
Date: Fri Feb 05 04:52:07 2016

Change assert to release assert for BitArray to prevent out-of-bounds access.

R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org
BUG=574802

Review URL: https://codereview.chromium.org/1672603002

Cr-Commit-Position: refs/heads/master@{#373745}

[modify] http://crrev.com/c8d32dd6e615b7b76c8e89d36f6ccf8786102180/third_party/WebKit/Source/wtf/BitArray.h


### cl...@chromium.org (2016-02-05)

ClusterFuzz has detected this issue as fixed in range 373744:373758.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6485955483009024

Uploader: nparker@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: index < arraySize
  blink::StylePropertySerializer::StylePropertySetForSerializer::StylePropertySetF
  blink::StylePropertySet::asText
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=365683:366004
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=373744:373758

Minimized Testcase (0.17 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96y6LsyocBNonc1_9zLBoOqNf7hkHOJv7a16F6xKYiVpbHviOegAT6aoYNd5N3WRqG1btQvXFoePZI1cDNfhpn4F-q3zP7--7V-QdofW9qrftV7crmK5yrphRpNZLEitjJi-EK2cdUA0HYAcoZrXO8f2w8-dw
>
<script> 
var test0=document.body.appendChild(document.createElement("hgroup"))
test0.style['all']='initial';
test0.style.setProperty('--a','a');
test0.cloneNode();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ad618c3357e189fb685ea88fe4b8b25ac34f2c75

commit ad618c3357e189fb685ea88fe4b8b25ac34f2c75
Author: mmoroz <mmoroz@chromium.org>
Date: Tue Feb 09 18:50:34 2016

Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access.

R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org
BUG=574802

Review URL: https://codereview.chromium.org/1677363002

Cr-Commit-Position: refs/heads/master@{#374424}

[modify] http://crrev.com/ad618c3357e189fb685ea88fe4b8b25ac34f2c75/third_party/WebKit/Source/wtf/dtoa/utils.h


### in...@chromium.org (2016-02-09)

I think all 3 CLs are in, closing.

### bu...@chromium.org (2016-02-09)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-49; it appears the fix may have landed after branch point, meaning a merge might be required. Please confirm if a merge is required here - if so add Merge-Request-49 label, otherwise remove Merge-TBD label. Thanks.

### mm...@chromium.org (2016-02-09)

Thanks for closing. Yes, CLs are in.

Link to performance dashboard:
1st: https://chromeperf.appspot.com/group_report?rev=373676
2nd: https://chromeperf.appspot.com/group_report?rev=373745
3rd (is not processed yet): https://chromeperf.appspot.com/group_report?rev=374424

### cl...@chromium.org (2016-02-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mm...@chromium.org (2016-02-09)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-02-09)

This needs some time running on trunk, so we won't merge it for now.

### go...@chromium.org (2016-02-09)

Ok, sounds good. Please request a merge when you think it is ready. Thank you.

### bu...@chromium.org (2016-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64cb1f5327522142c658100746f34f8a012a45fa

commit 64cb1f5327522142c658100746f34f8a012a45fa
Author: inferno <inferno@chromium.org>
Date: Sun Feb 14 18:20:57 2016

Revert of Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access. (patchset #2 id:20001 of https://codereview.chromium.org/1677363002/ )

Reason for revert:
Perf failures. Speculative revert to see if it fixes.

BUG=586581,574802

Original issue's description:
> Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access.
>
> R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org
> BUG=574802
>
> Committed: https://crrev.com/ad618c3357e189fb685ea88fe4b8b25ac34f2c75
> Cr-Commit-Position: refs/heads/master@{#374424}

TBR=mbarbella@chromium.org,ochang@chromium.org,tkent@chromium.org,mmoroz@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=574802

Review URL: https://codereview.chromium.org/1694093002

Cr-Commit-Position: refs/heads/master@{#375389}

[modify] http://crrev.com/64cb1f5327522142c658100746f34f8a012a45fa/third_party/WebKit/Source/wtf/dtoa/utils.h


### bu...@chromium.org (2016-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba5210f9c6de2dbff15775abb509553f87002f41

commit ba5210f9c6de2dbff15775abb509553f87002f41
Author: inferno <inferno@chromium.org>
Date: Thu Feb 18 00:12:17 2016

Reland of Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access. (patchset #1 id:1 of https://codereview.chromium.org/1694093002/ )

Reason for revert:
This revert was not the culprit CL. Reverting the revert.

Original issue's description:
> Revert of Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access. (patchset #2 id:20001 of https://codereview.chromium.org/1677363002/ )
>
> Reason for revert:
> Perf failures. Speculative revert to see if it fixes.
>
> BUG=586581,574802
>
> Original issue's description:
> > Change assert to release assert for WTF::double_conversion::Vector to prevent OOB memory access.
> >
> > R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org
> > BUG=574802
> >
> > Committed: https://crrev.com/ad618c3357e189fb685ea88fe4b8b25ac34f2c75
> > Cr-Commit-Position: refs/heads/master@{#374424}
>
> TBR=mbarbella@chromium.org,ochang@chromium.org,tkent@chromium.org,mmoroz@chromium.org
> # Not skipping CQ checks because original CL landed more than 1 days ago.
> BUG=574802
>
> Committed: https://crrev.com/64cb1f5327522142c658100746f34f8a012a45fa
> Cr-Commit-Position: refs/heads/master@{#375389}

TBR=mbarbella@chromium.org,ochang@chromium.org,tkent@chromium.org,mmoroz@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=586581,574802

Review URL: https://codereview.chromium.org/1708703003

Cr-Commit-Position: refs/heads/master@{#376043}

[modify] http://crrev.com/ba5210f9c6de2dbff15775abb509553f87002f41/third_party/WebKit/Source/wtf/dtoa/utils.h


### ti...@google.com (2016-02-29)

@inferno / @mmoroz: Do you want this in M-49? If so, the last beta is cut tomorrow at 5pm PST, so please ensure that you add "merge-request-49" ASAP if you want this in M-49.

### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-03-01)

I think this is ready to merge. Adding "Merge-Request-49". Thanks Tim.

### ti...@google.com (2016-03-01)

[Automated comment] Less than a week to go before stable on M49, we might already have a stable candidate build. Manual review required.

### ss...@google.com (2016-03-01)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-03-01)

Please merge this change to M49 branch 2623 before 5:00 PM PST today if it is a safe merge. We're cutting last M49 Beta build @ 5:00 PM PST today.

### bu...@chromium.org (2016-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b4814226bb75a37d4609a7faea742e8244ad3d01

commit b4814226bb75a37d4609a7faea742e8244ad3d01
Author: Oliver Chang <ochang@chromium.org>
Date: Tue Mar 01 20:34:42 2016

Change assert to release assert for BitArray to prevent out-of-bounds access.

R=inferno@chromium.org, mbarbella@chromium.org, ochang@chromium.org, tkent@chromium.org, mmoroz@chromium.org
BUG=574802

Review URL: https://codereview.chromium.org/1672603002

Cr-Commit-Position: refs/heads/master@{#373745}
(cherry picked from commit c8d32dd6e615b7b76c8e89d36f6ccf8786102180)

Review URL: https://codereview.chromium.org/1752073002 .

Cr-Commit-Position: refs/branch-heads/2623@{#554}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] https://crrev.com/b4814226bb75a37d4609a7faea742e8244ad3d01/third_party/WebKit/Source/wtf/BitArray.h


### bu...@chromium.org (2016-03-01)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/b4814226bb75a37d4609a7faea742e8244ad3d01

commit b4814226bb75a37d4609a7faea742e8244ad3d01
Author: Oliver Chang <ochang@chromium.org>
Date: Tue Mar 01 20:34:42 2016


### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

Congrats Atte - as mentioned in the release notes, $3000 for this report.



### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-18)

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

This issue was migrated from crbug.com/chromium/574802?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083494)*
