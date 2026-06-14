# Out-of-bounds write in ipcz while deserializing message

| Field | Value |
|-------|-------|
| **Issue ID** | [368208152](https://issues.chromium.org/issues/368208152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** |  130.0.6710.2 |
| **Reporter** | bl...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2024-09-19 |
| **Bounty** | $35,000.00 |

## Description

# Steps to reproduce the problem

1. Apply `renderer.diff` as a compromised renderer in the latest dev branch (commit fe006cb71900560b8fefb24b70b5ef49c583f36d).
2. Build chrome with asan, and run chrome directly.

```
gn gen out/ReleaseAsan --args="is_debug=false symbol_level=2 is_asan=true enable_nacl=false is_component_build=true"
autoninja -C out/ReleaseAsan chrome
./out/ReleaseAsan/chrome

```

3. Out-of-bounds writing occurs in broker process, see `asan.log`

# Problem Description

In ipcz, [Router::Deserialize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ipcz/src/ipcz/router.cc;drc=451093bbaf7fe812bf67d27d760f3bb64c92830b;bpv=1;bpt=1;l=699?gsn=Deserialize&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dthird_party%2Fipcz%2Fsrc%2Fipcz%2Frouter.cc%23nswF0_XVTePmcRT9dgZG35q9sXQktBDmbmZqjjKYDAY) is responsible for handling `HandleType::kPortal` messages. It uses [BufferPool::GetFragment](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ipcz/src/ipcz/buffer_pool.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;bpv=1;bpt=1;l=21?gsn=GetFragment&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dthird_party%2Fipcz%2Fsrc%2Fipcz%2Fbuffer_pool.cc%23iaMXHzWZm91A6E57I2NSLbgqK1LvjFUyYZ_nk-PjJ7I) to create a fragment from the description of the messages.

```
Breakpoint 0 hit
mojo_core_embedder_internal!ipcz::Fragment::MappedFromDescriptor+0x1d:
00007fff`9465ddad 4d399080000000  cmp     qword ptr [r8+80h],r10 ds:00000254`3bd70d18=0000000000020000
0:013> dt descriptor
Local var @ rdx Type ipcz::FragmentDescriptor*
   +0x000 buffer_id_       : ipcz::StrongAlias<ipcz::BufferIdTag,unsigned long long>
   +0x008 offset_          : 0x17d00
   +0x00c size_            : 0x100

```

`offset_` and `size_` are transmitted from client processes, such as renderer, via mojo pipe. In the renderer.diff, `offset_` and `size_` correspond to `idata[6]` and `idata[7]` respectively.

The callstack when creating a fragment:

```
0:016> k
 # Child-SP          RetAddr               Call Site
00 000000ac`e4ffc2e8 00007ffe`e9b49dc4     mojo_core_embedder_internal!ipcz::Fragment::MappedFromDescriptor [F:\Chromium\src\third_party\ipcz\src\ipcz\fragment.cc @ 18] 
01 000000ac`e4ffc2f0 00007ffe`e9bc470e     mojo_core_embedder_internal!ipcz::BufferPool::GetFragment+0x1a4 [F:\Chromium\src\third_party\ipcz\src\ipcz\buffer_pool.cc @ 33] 
02 000000ac`e4ffc3b0 00007ffe`e9be9e76     mojo_core_embedder_internal!ipcz::NodeLinkMemory::GetFragment+0x2e [F:\Chromium\src\third_party\ipcz\src\ipcz\node_link_memory.cc @ 290] 
03 000000ac`e4ffc400 00007ffe`e9b9f12a     mojo_core_embedder_internal!ipcz::Router::Deserialize+0x4d6 [F:\Chromium\src\third_party\ipcz\src\ipcz\router.cc @ 748] 
04 000000ac`e4ffca70 00007ffe`e9bd2fe5     mojo_core_embedder_internal!ipcz::NodeLink::OnAcceptParcel+0x2aa [F:\Chromium\src\third_party\ipcz\src\ipcz\node_link.cc @ 559] 
05 000000ac`e4ffcca0 00007ffe`e9bd1e5e     mojo_core_embedder_internal!ipcz::msg::NodeMessageListener::DispatchMessage+0x1c5 [F:\Chromium\src\third_party\ipcz\src\ipcz\node_messages_generator.h @ 357] 
06 000000ac`e4ffccf0 00007ffe`e9bd2625     mojo_core_embedder_internal!ipcz::msg::NodeMessageListener::OnMessage+0x1e [F:\Chromium\src\third_party\ipcz\src\ipcz\node_messages_generator.h @ 10] 

```

BufferPool::GetFragment performs a check to make sure `(offset_ + size_) < mapping.size_`, but it does not verify if `size_` is greater than a minimum value.

And then out-of-bound writing occurs when ipcz tries to lock that fragment:

```
00 (Inline Function) --------`--------     mojo_core_embedder_internal!std::__Cr::__cxx_atomic_compare_exchange_weak [F:\Chromium\src\third_party\libc++\src\include\__atomic\cxx_atomic_impl.h @ 400] 
01 (Inline Function) --------`--------     mojo_core_embedder_internal!std::__Cr::__atomic_base<unsigned int,0>::compare_exchange_weak [F:\Chromium\src\third_party\libc++\src\include\__atomic\atomic_base.h @ 93] 
02 00000081`8c5fe458 00007fff`354e5b06     mojo_core_embedder_internal!ipcz::RouterLinkState::SetSideStable+0x16 [F:\Chromium\src\third_party\ipcz\src\ipcz\router_link_state.cc @ 50] 
03 00000081`8c5fe460 00007fff`354e9387     mojo_core_embedder_internal!ipcz::Router::Flush+0x806 [F:\Chromium\src\third_party\ipcz\src\ipcz\router.cc @ 1487] 
04 00000081`8c5fe800 00007fff`354d2283     mojo_core_embedder_internal!ipcz::Router::Deserialize+0x7d7 [F:\Chromium\src\third_party\ipcz\src\ipcz\router.cc @ 802] 

```

The vulnerability is present in ipcz, a core inter-process communication module used by Chrome. We assess it as being of high severity and exploitable.

# Summary

Out-of-bounds write in ipcz while deserializing message

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

Xiantong Hou and Pisanbao of Wuheng Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [renderer.diff](attachments/renderer.diff) (text/x-diff, 971 B)
- [asan.log](attachments/asan.log) (text/plain, 28.0 KB)

## Timeline

### ma...@google.com (2024-09-19)

ajgo@, could you take a look at this one?

### pe...@google.com (2024-09-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### aj...@chromium.org (2024-09-20)

(I'm OOO sick - CC'ing some other folks until I can take a look)

### ro...@chromium.org (2024-09-21)

Thanks - will send out a fix ASAP

### bl...@gmail.com (2024-09-23)

And the suggested patch is:

```
diff --git a/third_party/ipcz/src/ipcz/fragment.cc b/third_party/ipcz/src/ipcz/fragment.cc
index 2ef4ed8dcfa0a..ff7e431a64eee 100644
--- a/third_party/ipcz/src/ipcz/fragment.cc
+++ b/third_party/ipcz/src/ipcz/fragment.cc
@@ -16,7 +16,7 @@ namespace ipcz {
 // static
 Fragment Fragment::MappedFromDescriptor(const FragmentDescriptor& descriptor,
                                         DriverMemoryMapping& mapping) {
-  if (descriptor.is_null()) {
+  if (descriptor.is_null() || descriptor.size() < 8) {
     return {};
   }
 

```

### ro...@google.com (2024-09-23)

The patch already out for review is here: <https://chromium-review.googlesource.com/c/chromium/src/+/5876623>

### ap...@google.com (2024-09-23)

Project: chromium/src
Branch: main

commit c333ed99544992f66e6e03621fa938d75ad01f70
Author: Ken Rockot <rockot@google.com>
Date:   Mon Sep 23 19:26:24 2024

    ipcz: Validate link state fragment before adoption
    
    Fixed: 368208152
    Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623
    Commit-Queue: Ken Rockot <rockot@google.com>
    Reviewed-by: Daniel Cheng <dcheng@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1358968}

M       third_party/ipcz/src/ipcz/node_link.cc
M       third_party/ipcz/src/ipcz/node_link_memory.h
M       third_party/ipcz/src/ipcz/node_link_memory_test.cc
M       third_party/ipcz/src/ipcz/router.cc

https://chromium-review.googlesource.com/5876623


### pe...@google.com (2024-09-24)

Security Merge Request Consideration: Requesting merge to extended stable (M128) because latest trunk commit (1358968) appears to be after extended stable branch point (1331488).
Security Merge Request Consideration: Requesting merge to stable (M129) because latest trunk commit (1358968) appears to be after stable branch point (1343869).
Security Merge Request Consideration: Requesting merge to beta (M130) because latest trunk commit (1358968) appears to be after beta branch point (1356013).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ro...@google.com (2024-09-24)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/5876623>
2. Yes
3. No
4. No
5. No

### pe...@google.com (2024-09-24)

Merge review required: M130 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-09-24)

Merge review required: M129 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-09-24)

Merge review required: M128 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### ro...@google.com (2024-09-24)

1. High-severity security fix
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5876623>
3. Yes
4. Not a feature
5. N/A
6. No

### am...@chromium.org (2024-09-26)

<https://crrev.com/c/5876623> approved for merges; please merge to M130 beta / branch 6723, M129 Stable / branch 6668, M128 Extended / branch 6613 by 10am Pacific time tomorrow, Friday 27 September to ensure this fix is in the next respective updates -- thanks1

### ap...@google.com (2024-09-26)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Ken Rockot <[rockot@google.com](mailto:rockot@google.com)>  

Link:      <https://chromium-review.googlesource.com/5894146>

[M130] ipcz: Validate link state fragment before adoption

---


Expand for full commit details
```
[M130] ipcz: Validate link state fragment before adoption

(cherry picked from commit c333ed99544992f66e6e03621fa938d75ad01f70)

Fixed: 368208152
Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1358968}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5894146
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6723@{#543}
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `third_party/ipcz/src/ipcz/node_link.cc`
- M `third_party/ipcz/src/ipcz/node_link_memory.h`
- M `third_party/ipcz/src/ipcz/node_link_memory_test.cc`
- M `third_party/ipcz/src/ipcz/router.cc`

---

Hash: 8a4b77f891fabc5d227c98837a0b0c4935f447cc  

Date:  Thu Sep 26 21:18:21 2024


---

### pe...@google.com (2024-09-26)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-09-26)

Project: chromium/src  

Branch: refs/branch-heads/6668  

Author: Ken Rockot <[rockot@google.com](mailto:rockot@google.com)>  

Link:      <https://chromium-review.googlesource.com/5894185>

[M129] ipcz: Validate link state fragment before adoption

---


Expand for full commit details
```
[M129] ipcz: Validate link state fragment before adoption

(cherry picked from commit c333ed99544992f66e6e03621fa938d75ad01f70)

Fixed: 368208152
Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1358968}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5894185
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/branch-heads/6668@{#1467}
Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

```

---

Files:

- M `third_party/ipcz/src/ipcz/node_link.cc`
- M `third_party/ipcz/src/ipcz/node_link_memory.h`
- M `third_party/ipcz/src/ipcz/node_link_memory_test.cc`
- M `third_party/ipcz/src/ipcz/router.cc`

---

Hash: e4fafb9cc7d71aab77c6a3317d6996c74cd516a6  

Date:  Thu Sep 26 21:43:53 2024


---

### ap...@google.com (2024-09-30)

Project: chromium/src  

Branch: refs/branch-heads/6613  

Author: Ken Rockot <[rockot@google.com](mailto:rockot@google.com)>  

Link:      <https://chromium-review.googlesource.com/5893005>

[M128] ipcz: Validate link state fragment before adoption

---


Expand for full commit details
```
[M128] ipcz: Validate link state fragment before adoption

(cherry picked from commit c333ed99544992f66e6e03621fa938d75ad01f70)

Fixed: 368208152
Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1358968}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5893005
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/branch-heads/6613@{#2136}
Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

```

---

Files:

- M `third_party/ipcz/src/ipcz/node_link.cc`
- M `third_party/ipcz/src/ipcz/node_link_memory.h`
- M `third_party/ipcz/src/ipcz/node_link_memory_test.cc`
- M `third_party/ipcz/src/ipcz/router.cc`

---

Hash: 337d11374c9f11ed8fd9efc301638beb5813188f  

Date:  Mon Sep 30 06:33:13 2024


---

### pe...@google.com (2024-10-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-10-02)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5876623
2. Medium - there are a few conflicts in a file.
3. 128, 129, and 130
4. Yes

### sp...@google.com (2024-10-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $35000.00 for this report.

Rationale for this decision:
high quality report of demonstrated memory corruption in a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-03)

Congratulations Xiantong Hou and Pisanbao! Thank you for the excellent report of this impactful bug -- great work!

### bl...@gmail.com (2024-10-04)

Thank you very much!

I would like to know if this case could be reassessed for a higher reward if we provide an exploit later. We reported the vulnerability as soon as we discovered it, but we haven't had enough time to develop a complete exploit.

### am...@chromium.org (2024-10-04)

Hi -- yes [1], we actually prefer that reporters report the issue as soon as possible and follow up with the exploit to allow us to fix the bug and get a fix to users sooner. We're happy to reassess for a potential higher reward if a controlled write or RCE can be demonstrated through an exploit.

[1] <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/vrp-faq.md#can-i-submit-my-report_s_and-provide-a-working-exploit-later>

### ap...@google.com (2024-10-14)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/5901253>

[M126-LTS] ipcz: Validate link state fragment before adoption

---


Expand for full commit details
```
[M126-LTS] ipcz: Validate link state fragment before adoption

(cherry picked from commit c333ed99544992f66e6e03621fa938d75ad01f70)

Fixed: 368208152
Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1358968}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5901253
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Cr-Commit-Position: refs/branch-heads/6478@{#1983}
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/ipcz/src/ipcz/node_link.cc`
- M `third_party/ipcz/src/ipcz/node_link_memory.h`
- M `third_party/ipcz/src/ipcz/node_link_memory_test.cc`
- M `third_party/ipcz/src/ipcz/router.cc`

---

Hash: 330cf6ec1306a04c2414fd5dd9829edd551a5fbe  

Date:  Mon Oct 14 07:51:57 2024


---

### ap...@google.com (2024-11-11)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/6011311>

[CfM-R126] ipcz: Validate link state fragment before adoption

---


Expand for full commit details
```
[CfM-R126] ipcz: Validate link state fragment before adoption 
 
(cherry picked from commit c333ed99544992f66e6e03621fa938d75ad01f70) 
 
(cherry picked from commit 330cf6ec1306a04c2414fd5dd9829edd551a5fbe) 
 
Fixed: 368208152 
Change-Id: I0e2ece4b0857b225d229134b2e55abc3e08348ee 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876623 
Commit-Queue: Ken Rockot <rockot@google.com> 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1358968} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5901253 
Owners-Override: Artem Sumaneev <asumaneev@google.com> 
Reviewed-by: Artem Sumaneev <asumaneev@google.com> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1983} 
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6011311 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478_182@{#99} 
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/ipcz/src/ipcz/node_link.cc`
- M `third_party/ipcz/src/ipcz/node_link_memory.h`
- M `third_party/ipcz/src/ipcz/node_link_memory_test.cc`
- M `third_party/ipcz/src/ipcz/router.cc`

---

Hash: 05afa213ef2e330167c6bee3f58497fd2368d2e5  

Date:  Mon Nov 11 18:55:50 2024


---

### pe...@google.com (2024-12-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/368208152)*
