# Security: Continued AddEventListener GC problems

| Field | Value |
|-------|-------|
| **Issue ID** | [40057344](https://issues.chromium.org/issues/40057344) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2021-09-21 |
| **Bounty** | $5,000.00 |

## Description

https://bugs.chromium.org/p/chromium/issues/detail?id=1248435#c63 suggests that https://crbug.com/chromium/1248435 is not fully fixed. Copied from that comment:

=========

I'm very sorry to reopen the case, the fuzzer based on the asan-win32-release_x64-922637.zip version still has the same crash for a while.
=================================================================
==10784==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7ffab8cf32a0 at pc 0x7ffaa97b9f6e bp 0x0078b49fb8a0 sp 0x0078b49fb8e8
READ of size 8 at 0x7ffab8cf32a0 thread T0
==10784==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffaa97b9f6d in blink::EventListenerMap::Add C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144
    #1 0x7ffaa63bec65 in blink::EventTarget::AddEventListenerInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_target.cc:481
    #2 0x7ffaace8c273 in blink::MediaCustomControlsFullscreenDetector::Attach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\media_custom_controls_fullscreen_detector.cc:86
    #3 0x7ffaa938fd67 in blink::HTMLVideoElement::InsertedInto C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\html_video_element.cc:128
    #4 0x7ffaa676b531 in blink::ContainerNode::NotifyNodeInsertedInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:994
    #5 0x7ffaa6765d42 in blink::ContainerNode::InsertNodeVector<blink::ContainerNode::AdoptAndAppendChild> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:333
    #6 0x7ffaa6761323 in blink::ContainerNode::AppendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:913
    #7 0x7ffaa6500ee2 in blink::Node::appendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:757
    #8 0x7ffaaa14c90a in blink::`anonymous namespace'::v8_node::AppendChildOperationCallbackForMainWorld C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:476
    #9 0x7ffa9d557817 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152
    #10 0x7ffa9d554b94 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #11 0x7ffa9d551f7f in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #12 0x7ffa9d5512cc in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #13 0x7ecf000c113b  (<unknown module>)

0x7ffab8cf32a0 is located 32 bytes to the left of global variable '<string literal>' defined in '../..\third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.h:52:12' (0x7ffab8cf32c0) of size 32
  '<string literal>' is ascii string 'ElementIntersectionObserverData'
0x7ffab8cf32a0 is located 8 bytes to the right of global variable '??_7ElementIntersectionObserverData@blink@@6B@' defined in '../../third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.cc' (0x7ffab8cf3280) of size 24
SUMMARY: AddressSanitizer: global-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144 in blink::EventListenerMap::Add
Shadow bytes around the buggy address:
  0x11d831b9e600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e610: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e630: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e640: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11d831b9e650: 00 00 00 f9[f9]f9 f9 f9 00 00 00 00 f9 f9 f9 f9
  0x11d831b9e660: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e670: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e690: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e6a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==10784==ABORTING


====

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [fuzz-00004.html](attachments/fuzz-00004.html) (text/plain, 212.6 KB)
- deleted (application/octet-stream, 0 B)
- [min.html](attachments/min.html) (text/plain, 32.3 KB)

## Timeline

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-22)

install node 
install puppeteer-core
python -m http.server 80
node ch.test3.js D:\chrome_asan\asan-win32-release_x64-922637\chrome.exe http://localhost/fuzz-00012.html

I tested i9 9900kf 32gb, 3950x 64gb 2 environments and reproduced quickly



### [Deleted User] (2021-09-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2021-09-23)

I cannot immediately repro the attached test case

### m....@gmail.com (2021-09-23)

I provide a replay video, this time it took 2 minutes to reproduce.
Put the fuzz-00004.html file in the POC directory can speed up the reproduction

### aj...@google.com (2021-09-23)

Adding some folks related to the stacktrace in case you have any ideas.

### ja...@chromium.org (2021-09-23)

What's a "global-buffer-overflow"? Does that mean that the renderer process just ran out of ram or something?

### m....@gmail.com (2021-09-24)

re https://crbug.com/chromium/1251673#c8
No, it mean something like this.
```
// file: example1-main.c
// global-buffer-overflow error

// AddressSanitizer reports a buffer overflow at the first line
// in function main() in all cases, REGARDLESS of the order in 
// which the object files: a.obj, b.obj, and c.obj are linked.
  
double x[5];
 
int main() { 
    int rc = (int) x[5];  // Boom!
    return rc; 
}
```

### aj...@google.com (2021-09-27)

I've also tried with this extra file with no luck. I suggest you work on minimizing the testcase.

### m....@gmail.com (2021-09-28)

re https://crbug.com/chromium/1251673#c10
I tried it before, even if I delete a code that I’m sure it won’t execute, it will affect the reproduce of the problem. I’ll give a try again.

### m....@gmail.com (2021-10-01)

install node 
install puppeteer-core
python -m http.server 80

node ch.test.js D:\chrome_asan\asan-win32-release_x64-925640\chrome.exe http://localhost/min1.html

Tested on APU4750g 64gb win10,x64

### om...@chromium.org (2021-10-01)

m.cooolie@, can you patch in the CL from https://chromium-review.googlesource.com/c/v8/v8/+/3199872 and tell us whether the issue still reproduces? Thanks.

### ad...@google.com (2021-10-01)

As I understand it, a duplicate bug has been reported which is more readily reproducible, so this may be resolved as a duplicate once we're sure the root causes match. m.cooolie@, the VRP panel will consider both reports together.

### m....@gmail.com (2021-10-02)

re https://crbug.com/chromium/1251673#c13
Can you give me pre-compiled link from here gs://chromium-browser-asan/win32-release_x64/

https://crbug.com/chromium/1251673#c14 Agree,if root cause is the same.

### om...@chromium.org (2021-10-02)

gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-927512.zip should have it already.

### m....@gmail.com (2021-10-02)

re https://crbug.com/chromium/1251673#c16
Still reproduce on asan-win32-release_x64-927512.zip very stable.
I made a smaller reproducible sample work with https://crbug.com/chromium/1251673#c12


### ml...@chromium.org (2021-10-04)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-04)

Whoops, that should have not been merged then.

### xi...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@google.com (2021-10-15)

any updates on this one?

### ml...@chromium.org (2021-10-15)

Hard to say as it never really reproduced for us.

We landed another fix in https://crbug.com/chromium/1259587 that could be related here.

m.cooolie@: Any chacne you can try anything that rolled passed 931448?

### m....@gmail.com (2021-10-15)

Seem not reproduce on asan-win32-release_x64-931402, i will let fuzzer run a while.

### m....@gmail.com (2021-10-16)

get a reproduce on asan-win32-release_x64-931402, is asan-win32-release_x64-931402 landed the fix?

### ml...@chromium.org (2021-10-16)

I don't think so. The fix is in anything >931448.

### m....@gmail.com (2021-10-17)

re #27 seem fix on asan-win32-release_x64-932277, fuzzer don't get reproduce any more.

### ml...@chromium.org (2021-10-18)

Thanks, both issues show similar symptoms (C++ GC marking + ephemerons) which is why I can see how this is fixed as well.

adetaylor: See the other bug for details.

### ad...@google.com (2021-10-18)

Thanks.

VRP panel should see https://bugs.chromium.org/p/chromium/issues/detail?id=1259587#c22 for a summary of the rewardability situation.

### ad...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M95. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-18)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-18)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-18)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2021-10-18)

The merge review is actually happening in https://bugs.chromium.org/p/chromium/issues/detail?id=1259587. Anything I am missing?

### ad...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Hi - just for awareness and full disclosure, despite this issue being reported in the follow-up of https://crbug.com/chromium/1248435 and on 21 September, prior to https://crbug.com/chromium/1259587 on 8 October, we have decided to go against our normal rules and precedent in this specific case and extend VRP rewards for both reports. The other reporter's initial report (https://crbug.com/chromium/1252878) was instrumental in allowing for the issue to be reproducible by our teams and root cause to be identified, which is why we have decided in the interest in utmost fairness that both reports could be eligible for a reward in this case.

The VRP Panel has decided to award you $5000 for this report! Thank you for the follow up report from your fuzzing/automation tools and we appreciate you letting us know this issue could still be reproduced in such a timely manner. 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

Based on my https://crbug.com/chromium/1251673#c41 and that VRP consideration and processing has been long since been completed, I feel like is very safe to merge this report into the previously reported https://crbug.com/chromium/1259587

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1251673?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1259587]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057344)*
