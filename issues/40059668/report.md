# Security: heap-after-free on iOS 15.4 simulator + Chromium Dev Asan

| Field | Value |
|-------|-------|
| **Issue ID** | [40059668](https://issues.chromium.org/issues/40059668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Mobile>AppMenu |
| **Platforms** | iOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | bw...@google.com |
| **Created** | 2022-05-14 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This Heap Uaf occurs when build iOS chromium with asan. I'm not familiar with stack trace in iOS, I think it's worth to take a look.

I share screencast on Google drive.

**VERSION**  

Chrome Version: 104.0.5063.0  

Operating System: iOS 15.4 simulator

**REPRODUCTION CASE**  

(\*) Build Asan for IoS  

(\*) run with out/Debug-iphonesimulator/iossim -d 'iPad Pro (12.9-inch) (5th generation)' -s '15.4' \  

out/Debug-iphonesimulator/Chromium.app/  

(\*) Navigate to settings -> Downloads

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==30653==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000038310 at pc 0x000123f37b94 bp 0x000312fe7470 sp 0x000312fe6c38  

READ of size 4 at 0x604000038310 thread T0  

==30653==WARNING: Can't read from symbolizer at fd 49  

==30653==WARNING: Can't read from symbolizer at fd 50  

==30653==WARNING: Can't read from symbolizer at fd 51  

==30653==WARNING: Can't read from symbolizer at fd 52  

==30653==WARNING: Failed to use and restart external symbolizer!  

#0 0x123f37b93 in **asan\_after\_dynamic\_init ??:0:0  

#1 0x10315d86a in base::RecordAction(base::UserMetricsAction const&) ??:0:0  

#2 0x102d889d8 in invocation function for block in (anonymous namespace)::CreateOverflowMenuDestination(int, (anonymous namespace)::Destination, NSString\*, NSString\*, void () block\_pointer) ??:0:0  

#3 0x102520039 in $sIeyB\_Ieg\_TR ??:0:0  

#4 0x102dad79b in $sIeg\_ytIegr\_TR ??:0:0  

#5 0x102dad7f0 in $sIeg\_ytIegr\_TRTA ??:0:0  

#6 0x102dadc7b in $sytIegr\_Ieg\_TR ??:0:0  

#7 0x102d9f090 in $s042ios\_chrome\_browser\_ui\_popup\_menu\_overflow\_f1\_g1\_F6\_swift27OverflowMenuDestinationViewV4bodyQrvgyycfU* ??:0:0  

#8 0x11ee1ac54 in $s7SwiftUI18WrappedButtonStyle33\_AEEDD090E917AC57C12008D974DC6805LLV8makeBody13configurationQrAA09PrimitivedE13ConfigurationV\_tFyycAHcfu\_yycfu0\_TA ??:0:0  

#9 0x11f33d482 in $s7SwiftUI25PressableGestureCallbacksV8dispatch5phase5stateyycSgAA0D5PhaseOyxG\_SbztFyycfU* ??:0:0  

#10 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#11 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#12 0x11ec489d7 in $sIeg\_ytIegr\_TRTA.5406 ??:0:0  

#13 0x11ef33e3d in $sytIegr\_Ieg\_TR ??:0:0  

#14 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#15 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#16 0x11ec489e2 in $sIeg\_ytIegr\_TRTA.5414 ??:0:0  

#17 0x11ef0d749 in $s7SwiftUI6UpdateO3endyyFZ ??:0:0  

#18 0x11f008e1c in $s7SwiftUI19EventBindingManagerC4sendyySDyAA0C2IDVAA0C4Type\_pGF ??:0:0  

#19 0x11f526528 in $s7SwiftUI18EventBindingBridgeC4send\_6sourceySDyAA0C2IDVAA0C4Type\_pG\_AA0cD6Source\_ptFTf4nen\_nAA22UIKitGestureRecognizerC\_Tg5 ??:0:0  

#20 0x11f524a85 in $s7SwiftUI22UIKitGestureRecognizerC4send025\_062C14327F4C9197D92807A7H6DF7F3BLL7touches5event5phaseyShySo7UITouchCG\_So7UIEventCAA10EventPhaseOtF ??:0:0  

#21 0x11f525229 in $s7SwiftUI22UIKitGestureRecognizerC12touchesBegan\_4withyShySo7UITouchCG\_So7UIEventCtFToTm ??:0:0  

#22 0x11f524b0d in $s7SwiftUI22UIKitGestureRecognizerC12touchesEnded\_4withyShySo7UITouchCG\_So7UIEventCtFTo ??:0:0  

#23 0x140658ec8 in -[UIGestureRecognizer \_componentsEnded:withEvent:] ??:0:0  

#24 0x140c23556 in -[UITouchesEvent \_sendEventToGestureRecognizer:] ??:0:0  

#25 0x14064d37e in \_\_47-[UIGestureEnvironment \_updateForEvent:window:]\_block\_invoke ??:0:0  

#26 0x14064d008 in -[UIGestureEnvironment \_updateForEvent:window:] ??:0:0  

#27 0x140bd0097 in -[UIWindow sendEvent:] ??:0:0  

#28 0x140ba615f in -[UIApplication sendEvent:] ??:0:0  

#29 0x140c3ecfc in \_\_dispatchPreprocessedEventFromEventQueue ??:0:0  

#30 0x140c4149f in \_\_processEventQueue ??:0:0  

#31 0x140c37ccc in \_\_eventFetcherSourceCallback ??:0:0  

#32 0x118f4b832 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION** ??:0:0  

#33 0x118f4b72a in \_\_CFRunLoopDoSource0 ??:0:0  

#34 0x118f4abf7 in \_\_CFRunLoopDoSources0 ??:0:0  

#35 0x118f452f3 in \_\_CFRunLoopRun ??:0:0  

#36 0x118f44a8f in CFRunLoopRunSpecific ??:0:0  

#37 0x118210c8d in GSEventRunModal ??:0:0  

#38 0x140b8690d in -[UIApplication \_run] ??:0:0  

#39 0x140b8b568 in UIApplicationMain ??:0:0  

#40 0x100f48cc3 in main ??:0:0  

#41 0x11659af20 in \_platform\_memmove ??:0:0  

#42 0x20dff351d (<unknown module>)

0x604000038310 is located 0 bytes inside of 48-byte region [0x604000038310,0x604000038340)  

freed by thread T0 here:  

#0 0x123f65fe9 in **asan\_memmove ??:0:0  

#1 0x102d889a8 in invocation function for block in (anonymous namespace)::CreateOverflowMenuDestination(int, (anonymous namespace)::Destination, NSString\*, NSString\*, void () block\_pointer) ??:0:0  

#2 0x102520039 in $sIeyB\_Ieg\_TR ??:0:0  

#3 0x102dad79b in $sIeg\_ytIegr\_TR ??:0:0  

#4 0x102dad7f0 in $sIeg\_ytIegr\_TRTA ??:0:0  

#5 0x102dadc7b in $sytIegr\_Ieg\_TR ??:0:0  

#6 0x102d9f090 in $s042ios\_chrome\_browser\_ui\_popup\_menu\_overflow\_f1\_g1\_F6\_swift27OverflowMenuDestinationViewV4bodyQrvgyycfU* ??:0:0  

#7 0x11ee1ac54 in $s7SwiftUI18WrappedButtonStyle33\_AEEDD090E917AC57C12008D974DC6805LLV8makeBody13configurationQrAA09PrimitivedE13ConfigurationV\_tFyycAHcfu\_yycfu0\_TA ??:0:0  

#8 0x11f33d482 in $s7SwiftUI25PressableGestureCallbacksV8dispatch5phase5stateyycSgAA0D5PhaseOyxG\_SbztFyycfU* ??:0:0  

#9 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#10 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#11 0x11ec489d7 in $sIeg\_ytIegr\_TRTA.5406 ??:0:0  

#12 0x11ef33e3d in $sytIegr\_Ieg\_TR ??:0:0  

#13 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#14 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#15 0x11ec489e2 in $sIeg\_ytIegr\_TRTA.5414 ??:0:0  

#16 0x11ef0d749 in $s7SwiftUI6UpdateO3endyyFZ ??:0:0  

#17 0x11f008e1c in $s7SwiftUI19EventBindingManagerC4sendyySDyAA0C2IDVAA0C4Type\_pGF ??:0:0  

#18 0x11f526528 in $s7SwiftUI18EventBindingBridgeC4send\_6sourceySDyAA0C2IDVAA0C4Type\_pG\_AA0cD6Source\_ptFTf4nen\_nAA22UIKitGestureRecognizerC\_Tg5 ??:0:0  

#19 0x11f524a85 in $s7SwiftUI22UIKitGestureRecognizerC4send025\_062C14327F4C9197D92807A7H6DF7F3BLL7touches5event5phaseyShySo7UITouchCG\_So7UIEventCAA10EventPhaseOtF ??:0:0  

#20 0x11f525229 in $s7SwiftUI22UIKitGestureRecognizerC12touchesBegan\_4withyShySo7UITouchCG\_So7UIEventCtFToTm ??:0:0  

#21 0x11f524b0d in $s7SwiftUI22UIKitGestureRecognizerC12touchesEnded\_4withyShySo7UITouchCG\_So7UIEventCtFTo ??:0:0  

#22 0x140658ec8 in -[UIGestureRecognizer \_componentsEnded:withEvent:] ??:0:0  

#23 0x140c23556 in -[UITouchesEvent \_sendEventToGestureRecognizer:] ??:0:0  

#24 0x14064d37e in \_\_47-[UIGestureEnvironment \_updateForEvent:window:]\_block\_invoke ??:0:0  

#25 0x14064d008 in -[UIGestureEnvironment \_updateForEvent:window:] ??:0:0  

#26 0x140bd0097 in -[UIWindow sendEvent:] ??:0:0  

#27 0x140ba615f in -[UIApplication sendEvent:] ??:0:0  

#28 0x140c3ecfc in \_\_dispatchPreprocessedEventFromEventQueue ??:0:0  

#29 0x140c4149f in \_\_processEventQueue ??:0:0

previously allocated by thread T0 here:  

#0 0x123f65ea0 in \_\_asan\_memmove ??:0:0  

#1 0x103059e16 in operator new(unsigned long) ??:0:0  

#2 0x10305be59 in std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char>>::**init(char const\*, unsigned long) ??:0:0  

#3 0x102d88944 in invocation function for block in (anonymous namespace)::CreateOverflowMenuDestination(int, (anonymous namespace)::Destination, NSString\*, NSString\*, void () block\_pointer) ??:0:0  

#4 0x102520039 in $sIeyB\_Ieg\_TR ??:0:0  

#5 0x102dad79b in $sIeg\_ytIegr\_TR ??:0:0  

#6 0x102dad7f0 in $sIeg\_ytIegr\_TRTA ??:0:0  

#7 0x102dadc7b in $sytIegr\_Ieg\_TR ??:0:0  

#8 0x102d9f090 in $s042ios\_chrome\_browser\_ui\_popup\_menu\_overflow\_f1\_g1\_F6\_swift27OverflowMenuDestinationViewV4bodyQrvgyycfU* ??:0:0  

#9 0x11ee1ac54 in $s7SwiftUI18WrappedButtonStyle33\_AEEDD090E917AC57C12008D974DC6805LLV8makeBody13configurationQrAA09PrimitivedE13ConfigurationV\_tFyycAHcfu\_yycfu0\_TA ??:0:0  

#10 0x11f33d482 in $s7SwiftUI25PressableGestureCallbacksV8dispatch5phase5stateyycSgAA0D5PhaseOyxG\_SbztFyycfU* ??:0:0  

#11 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#12 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#13 0x11ec489d7 in $sIeg\_ytIegr\_TRTA.5406 ??:0:0  

#14 0x11ef33e3d in $sytIegr\_Ieg\_TR ??:0:0  

#15 0x11ef33e29 in $sIeg\_ytIegr\_TR ??:0:0  

#16 0x11ebfd955 in $sIeg\_ytIegr\_TRTA ??:0:0  

#17 0x11ec489e2 in $sIeg\_ytIegr\_TRTA.5414 ??:0:0  

#18 0x11ef0d749 in $s7SwiftUI6UpdateO3endyyFZ ??:0:0  

#19 0x11f008e1c in $s7SwiftUI19EventBindingManagerC4sendyySDyAA0C2IDVAA0C4Type\_pGF ??:0:0  

#20 0x11f526528 in $s7SwiftUI18EventBindingBridgeC4send\_6sourceySDyAA0C2IDVAA0C4Type\_pG\_AA0cD6Source\_ptFTf4nen\_nAA22UIKitGestureRecognizerC\_Tg5 ??:0:0  

#21 0x11f524a85 in $s7SwiftUI22UIKitGestureRecognizerC4send025\_062C14327F4C9197D92807A7H6DF7F3BLL7touches5event5phaseyShySo7UITouchCG\_So7UIEventCAA10EventPhaseOtF ??:0:0  

#22 0x11f525229 in $s7SwiftUI22UIKitGestureRecognizerC12touchesBegan\_4withyShySo7UITouchCG\_So7UIEventCtFToTm ??:0:0  

#23 0x11f524b0d in $s7SwiftUI22UIKitGestureRecognizerC12touchesEnded\_4withyShySo7UITouchCG\_So7UIEventCtFTo ??:0:0  

#24 0x140658ec8 in -[UIGestureRecognizer \_componentsEnded:withEvent:] ??:0:0  

#25 0x140c23556 in -[UITouchesEvent \_sendEventToGestureRecognizer:] ??:0:0  

#26 0x14064d37e in \_\_47-[UIGestureEnvironment \_updateForEvent:window:]\_block\_invoke ??:0:0  

#27 0x14064d008 in -[UIGestureEnvironment \_updateForEvent:window:] ??:0:0  

#28 0x140bd0097 in -[UIWindow sendEvent:] ??:0:0  

#29 0x140ba615f in -[UIApplication sendEvent:] ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/rhezashandikri/Library/Developer/CoreSimulator/Devices/EC42276C-C6D5-4AAD-B4CB-998794D9C7E0/data/Containers/Bundle/Application/B8B4C190-D5D4-4EE7-8FCA-A9EE72C59376/Chromium.app/libclang\_rt.asan\_iossim\_dynamic.dylib:x86\_64+0x17b93) (BuildId: 9aa25f6a3a8d3dee900b3dd74861a5c225000000100000000000090000040e00) in \_\_asan\_after\_dynamic\_init+0x963  

Shadow bytes around the buggy address:  

0x0c780000f010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c780000f020: fa fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0c780000f030: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f040: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f050: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

=>0x0c780000f060: fa fa[fd]fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f070: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f080: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f090: fa fa 00 00 00 00 00 fa fa fa fd fd fd fd fd fd  

0x0c780000f0a0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c780000f0b0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==30653==ABORTING

screencast: <https://drive.google.com/drive/folders/1LRGaLZFoDdLfn3aREsNOKHgps7LxtpDr?usp=sharing>

## Timeline

### [Deleted User] (2022-05-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-15)

Thank you for your report. I agree there looks like a UAF here introduced by https://chromium-review.googlesource.com/c/chromium/src/+/3625259 since std::string from UmaNameForDestination goes out of scope after UmaActionForDestination returns.

bwwilliams please fix asap or revert CL. Thanks.

[Monorail components: UI>Browser>Mobile>AppMenu]

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bw...@google.com (2022-05-16)

Thank you all for bringing this to my attention. This is my top priority this morning. I hope to have an update within the next 30-40 minutes.

### ro...@chromium.org (2022-05-16)

@harrysouders FYI. I'd like to have this in 103 before we push to Beta, and ideally fix in the next Dev channel release too.

### bw...@google.com (2022-05-16)

Hi all, 30 min ago I sent out crbug.com/3644982, which should fix this issue. 

### ha...@google.com (2022-05-16)

Thanks bwwilliams@

I think the CL link should be: crrev.com/c/3644982

If this lands on main today it should go out in M104 Dev tomorrow. Can you request a Merge to M103 as soon as you've verified the fix on main? We'll need to merge to M103 tomorrow to ship in Beta on Wednesday?

### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/81c144ba9b976e90914584e880685d9a86f35006

commit 81c144ba9b976e90914584e880685d9a86f35006
Author: Benjamin Williams <bwwilliams@google.com>
Date: Mon May 16 17:56:20 2022

Consolidate UMA RecordAction logic into the handler.

It's been discovered that crbug.com/3625259 merged code with improper
use of RecordAction(UmaActionForDestination(...)). Per the
documentation, these helper functions should be used with string
literals, whereas the merged CL uses a string variable.

This CL fixes this improper usage of
RecordAction(UmaActionForDestination(...)) by consolidating the existing
helper functions, UmaActionForDestination and UmaNameForDestination,
introduced by crbug.com/3644982 into a new function,
RecordUmaActionForDestination.

Change-Id: I671f054ce862c0e51a5225508d51f058bf89f19b
Bug: 1325615
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3644982
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Commit-Queue: Benjamin Williams <bwwilliams@google.com>
Cr-Commit-Position: refs/heads/main@{#1003836}

[modify] https://crrev.com/81c144ba9b976e90914584e880685d9a86f35006/ios/chrome/browser/ui/popup_menu/overflow_menu/overflow_menu_mediator.mm


### bw...@google.com (2022-05-16)

[Empty comment from Monorail migration]

### ha...@google.com (2022-05-17)

Not 100% sure if sheriffbot will pick this up in today's run... so adding the questionnaire manually.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

### bw...@google.com (2022-05-17)

1. Why does your merge fit within the merge criteria for these milestones?
This branch is shipping to dev (currently M103), and fixes a crucial UAF bug. This work fixes both a security issue and regression.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3644982/
(Needs a cherry-pick CL.)

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, this is not a new feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No; rohitrao@ approved and LGTM. wfh@ added as reviewer.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No manual verification needed.

### ha...@google.com (2022-05-17)

Merge approved M103 branch 5060. Please merge today.

Also just for clarification - CL landed in M104 and will ship to M104 dev later today (pending TE qualification). After the merge to M103, this will ship to M103 tomorrow.

### bw...@google.com (2022-05-17)

Cherry pick CL created: https://chromium-review.googlesource.com/c/chromium/src/+/3649958

### gi...@appspot.gserviceaccount.com (2022-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/48a8d9a052dc7e7b96a37ded43752bcdc3b30163

commit 48a8d9a052dc7e7b96a37ded43752bcdc3b30163
Author: Benjamin Williams <bwwilliams@google.com>
Date: Wed May 18 01:33:41 2022

Consolidate UMA RecordAction logic into the handler.

It's been discovered that crbug.com/3625259 merged code with improper
use of RecordAction(UmaActionForDestination(...)). Per the
documentation, these helper functions should be used with string
literals, whereas the merged CL uses a string variable.

This CL fixes this improper usage of
RecordAction(UmaActionForDestination(...)) by consolidating the existing
helper functions, UmaActionForDestination and UmaNameForDestination,
introduced by crbug.com/3644982 into a new function,
RecordUmaActionForDestination.

(cherry picked from commit 81c144ba9b976e90914584e880685d9a86f35006)

Change-Id: I671f054ce862c0e51a5225508d51f058bf89f19b
Bug: 1325615
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3644982
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Commit-Queue: Benjamin Williams <bwwilliams@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1003836}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3649958
Cr-Commit-Position: refs/branch-heads/5060@{#69}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/48a8d9a052dc7e7b96a37ded43752bcdc3b30163/ios/chrome/browser/ui/popup_menu/overflow_menu/overflow_menu_mediator.mm


### ha...@google.com (2022-05-18)

kicking off a new build to get this into tomorrow's beta release

### ha...@google.com (2022-05-18)

Marking this as fixed since it's fixed on main and has been CPd to 103. This will get released in 103.0.5060.10 beta today

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this user information disclosure/aslr defeat issue. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1325615?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059668)*
