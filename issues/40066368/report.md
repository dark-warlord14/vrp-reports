# UAF in media_router::IssuesObserver::~IssuesObserver()

| Field | Value |
|-------|-------|
| **Issue ID** | [40066368](https://issues.chromium.org/issues/40066368) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Cast |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2023-06-25 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

repro steps:

1. python3 -m http.server 8000 --dir=|PATH|
2. chrome\_asan\_shared/chrome --no-sandbox --incognito --user-data-dir=/tmp/a1 <http://localhost:8000/crash.html>
3. click the button and immediately repro the UAF.

**Problem Description:**  

==1352561==ERROR: AddressSanitizer: heap-use-after-free on address 0x5190008e44d8 at pc 0x56321811ac9f bp 0x7ffe5be31330 sp 0x7ffe5be31328  

READ of size 1 at 0x5190008e44d8 thread T0 (chrome)  

#0 0x56321811ac9e in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) *asan\_rtl*:17  

#1 0x56321811a7f9 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) *asan\_rtl*:5  

#2 0x563213b60cc6 in SafelyUnwrapPtrForDereference<media\_router::IssueManager> ./../../base/allocator/partition\_allocator/pointers/raw\_ptr\_hookable\_impl.h:75:7  

#3 0x563213b60cc6 in GetForDereference ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:1038:12  

#4 0x563213b60cc6 in operator-> ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:806:12  

#5 0x563213b60cc6 in media\_router::IssuesObserver::~IssuesObserver() ./../../components/media\_router/browser/issues\_observer.cc:19:5  

#6 0x56322d40cc58 in ~UiIssuesObserver ./../../chrome/browser/ui/media\_router/media\_router\_ui.cc:354:52  

#7 0x56322d40cc58 in media\_router::MediaRouterUI::UiIssuesObserver::~UiIssuesObserver() ./../../chrome/browser/ui/media\_router/media\_router\_ui.cc:354:52  

#8 0x56322d4029c1 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#9 0x56322d4029c1 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#10 0x56322d4029c1 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#11 0x56322d4029c1 in media\_router::MediaRouterUI::~MediaRouterUI() ./../../chrome/browser/ui/media\_router/media\_router\_ui.cc:100:1  

#12 0x56322d4037ed in media\_router::MediaRouterUI::~MediaRouterUI() ./../../chrome/browser/ui/media\_router/media\_router\_ui.cc:93:33  

#13 0x56322d3a2bad in CastDeviceListHost::~CastDeviceListHost() ./../../chrome/browser/ui/global\_media\_controls/cast\_device\_list\_host.cc:100:43  

#14 0x56322d3872d9 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#15 0x56322d3872d9 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#16 0x56322d3872d9 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#17 0x56322d3872d9 in ~SelfOwnedReceiver ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:100:32  

#18 0x56322d3872d9 in mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::Close() ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:80:18  

#19 0x56322d386961 in mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::OnDisconnect(unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:109:5  

#20 0x56322d3870be in Invoke<void (mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::\*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost> \*, unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &> ./../../base/functional/bind\_internal.h:746:12  

#21 0x56322d3870be in MakeItSo<void (mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::\*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &> ./../../base/functional/bind\_internal.h:925:12  

#22 0x56322d3870be in RunImpl<void (mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::\*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#23 0x56322d3870be in base::internal::Invoker<base::internal::BindState<void (mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>::\*)(unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&), base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver<global\_media\_controls::mojom::DeviceListHost>, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, s

**Additional Comments:**

\*\*Chrome version: \*\* 116.0.5845.4 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 298 B)
- [asan.log](attachments/asan.log) (text/plain, 33.1 KB)
- [test-2023-06-26_12.16.53.mp4](attachments/test-2023-06-26_12.16.53.mp4) (video/mp4, 935.1 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 337 B)

## Timeline

### [Deleted User] (2023-06-25)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-26)

Thanks for reporting this!

I can't reproduce ;-(
See video. Would you have additional instruction to be able to reproduce?

Reading the code, it seems reasonable to think the bug exists.

# Owner:

I would have liked to send it to @imcheng, but he is not more working on Chrome. So, I will look into: chrome/browser/media/router/OWNERS:

+takumif@ Could you please start investigating this, or re-route it toward the right owner?

# Security_Severity-Critical

This is memory corruption in the browser process. It only requires a user gesture, so I don't consider this to be a "specific" user interaction. This is protected by MiraclePtr starting from M115, so it should be considered "High". If we can reproduce on M114, this might be "Critical" instead.
I will use "Critical" for now tentatively.
Please adjust after finding the root cause.

# Security_Impact-Stable
# FoundIn=114

I can't reproduce. So I am using the current extended-stable version.
Please adjust after finding the root cause.

# Platform:

Tentatively: All except ios. I guess they all share the same implementation.

[Monorail components: Internals>Cast]

### [Deleted User] (2023-06-26)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-06-26)


I may have found why you couldn't reproduce the issue in the video. The error message "Scripts may close only the windows that were opened by them" suggests that you may have opened the browser first and then clicked on "crash.html," which prevented the browser close action from being executed.

You can try the following directly:
chrome_asan_shared/chrome       --no-sandbox   --incognito --user-data-dir=/tmp/a1 http://localhost:8000/crash.html

### em...@gmail.com (2023-06-26)

Alternatively, you can try adding the "-disable-gesture-requirement-for-presentation" flag and test it with the attached "crash2.html" file. Run it 2 or 3 times, and the issue should be reproducible.
./chrome --disable-gesture-requirement-for-presentation   --no-sandbox   --incognito --user-data-dir=/tmp/a1 http://localhost:8605/crash2/crash2.html

tested version:
Chromium 117.0.5855.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1162327.zip)


### ar...@chromium.org (2023-06-26)

Thanks! I tried again and I can reproduce.

### [Deleted User] (2023-06-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-26)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2023-06-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-26)

This appears that it would require a compromised renderer and browser shutdown to trigger, thus sev-high rather than critical. If this is incorrect, please feel free to readjust accordingly. 

### am...@chromium.org (2023-06-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ffc0dfef649ad5b1149f89bb24c70d43405442ba

commit ffc0dfef649ad5b1149f89bb24c70d43405442ba
Author: Takumi Fujimoto <takumif@chromium.org>
Date: Mon Jul 10 22:25:26 2023

Destroy CastDeviceListHost during KeyedServices shutdown

This makes MediaNotificationService destroy all the CastDeviceListHosts
that it's instantiated in its KeyedService shutdown. This is necessary
because CastDeviceListHost depends on MediaRouter, another KeyedService.

Bug: 1457757
Change-Id: I453279da77b141ad9cd89310fc8128cc7d2919f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672319
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1168361}

[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/media_notification_service.cc
[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/cast_device_list_host_unittest.cc
[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/media_notification_service_unittest.cc
[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/cast_device_list_host.h
[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/cast_device_list_host.cc
[modify] https://crrev.com/ffc0dfef649ad5b1149f89bb24c70d43405442ba/chrome/browser/ui/global_media_controls/media_notification_service.h


### ta...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-11)

Requesting merge to stable M114 because latest trunk commit (1168361) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1168361) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1168361) appears to be after dev branch point (1160321).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge review required: M115 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge review required: M114 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2023-07-12)

Answering https://crbug.com/chromium/1457757#c16

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4672319

2. Has this fix been tested on Canary?
Yes, verified on 117.0.5883.0 macOS Canary

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
I think the risk of a stability regression is low, but nonzero.

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No

I'll cherrypick into M116, but I'm not sure whether it's worth cherrypicking into M115 if we want to be on the safe side regarding stability risks.

### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/357cdfaffdc2f7ad5114fe069276df806d7ae75d

commit 357cdfaffdc2f7ad5114fe069276df806d7ae75d
Author: Takumi Fujimoto <takumif@chromium.org>
Date: Wed Jul 12 03:47:43 2023

Destroy CastDeviceListHost during KeyedServices shutdown

This makes MediaNotificationService destroy all the CastDeviceListHosts
that it's instantiated in its KeyedService shutdown. This is necessary
because CastDeviceListHost depends on MediaRouter, another KeyedService.

(cherry picked from commit ffc0dfef649ad5b1149f89bb24c70d43405442ba)

Bug: 1457757
Change-Id: I453279da77b141ad9cd89310fc8128cc7d2919f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672319
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1168361}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4680520
Auto-Submit: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#431}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/media_notification_service.cc
[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/cast_device_list_host_unittest.cc
[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/media_notification_service_unittest.cc
[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/cast_device_list_host.h
[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/cast_device_list_host.cc
[modify] https://crrev.com/357cdfaffdc2f7ad5114fe069276df806d7ae75d/chrome/browser/ui/global_media_controls/media_notification_service.h


### [Deleted User] (2023-07-12)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-17)

M115 and M114 merges approved; please merge this fix to M115/branch 5790 and M114/branch 5735 at your earliest convenience. Thank you!

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20

commit e3ee4dd0cc843bde32fd48d00525d9cfe0797b20
Author: Takumi Fujimoto <takumif@chromium.org>
Date: Tue Jul 18 18:18:08 2023

Destroy CastDeviceListHost during KeyedServices shutdown

This makes MediaNotificationService destroy all the CastDeviceListHosts
that it's instantiated in its KeyedService shutdown. This is necessary
because CastDeviceListHost depends on MediaRouter, another KeyedService.

(cherry picked from commit ffc0dfef649ad5b1149f89bb24c70d43405442ba)

Bug: 1457757
Change-Id: I453279da77b141ad9cd89310fc8128cc7d2919f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672319
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1168361}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4692661
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Auto-Submit: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1486}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/media_notification_service.cc
[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/cast_device_list_host_unittest.cc
[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/media_notification_service_unittest.cc
[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/cast_device_list_host.h
[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/cast_device_list_host.cc
[modify] https://crrev.com/e3ee4dd0cc843bde32fd48d00525d9cfe0797b20/chrome/browser/ui/global_media_controls/media_notification_service.h


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/abb3ebd3d2ef3614fd888160d81505702b932f2c

commit abb3ebd3d2ef3614fd888160d81505702b932f2c
Author: Takumi Fujimoto <takumif@chromium.org>
Date: Tue Jul 18 18:20:16 2023

Destroy CastDeviceListHost during KeyedServices shutdown

This makes MediaNotificationService destroy all the CastDeviceListHosts
that it's instantiated in its KeyedService shutdown. This is necessary
because CastDeviceListHost depends on MediaRouter, another KeyedService.

(cherry picked from commit ffc0dfef649ad5b1149f89bb24c70d43405442ba)

Bug: 1457757
Change-Id: I453279da77b141ad9cd89310fc8128cc7d2919f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672319
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1168361}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4692442
Auto-Submit: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#1763}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/media_notification_service.cc
[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/cast_device_list_host_unittest.cc
[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/media_notification_service_unittest.cc
[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/cast_device_list_host.h
[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/cast_device_list_host.cc
[modify] https://crrev.com/abb3ebd3d2ef3614fd888160d81505702b932f2c/chrome/browser/ui/global_media_controls/media_notification_service.h


### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $5,000 for this report mildly mitigated security bug, mitigated by shutdown. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-27)

Already merged to M114.

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1457757?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066368)*
