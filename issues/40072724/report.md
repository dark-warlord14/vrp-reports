# GPU failure in blink::AXObject::RepairMissingParent

| Field | Value |
|-------|-------|
| **Issue ID** | [40072724](https://issues.chromium.org/issues/40072724) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Accessibility |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-09-19 |
| **Bounty** | $7,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5548591573303296

Fuzzer: b0ring_webidl_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: GPU failure
Crash Address: 
Crash State:
  blink::AXObject::RepairMissingParent
  blink::AXObject::SetAncestorsHaveDirtyDescendants
  blink::AXObject::RepairMissingParent
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=windows_asan_chrome&revision=1197668

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5548591573303296

Issue filed automatically.



## Timeline

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2023-09-20)

aleventhal: Could you PTAL? This is apparently a GPU crash, though I don't know if an axobject can cause that, or that there are two different issues here.

[Monorail components: Blink>Accessibility]

### al...@chromium.org (2023-09-21)

I don't see why this is high severity -- it's hitting a rare CHECK(), which is a controlled crash in the renderer.
There are a lot of other more high priority crashes than this one -- it took a 131k file for Clusterfuzz to managed to hit this, and as a controlled crash, I certainly hope it's not exploitable.

4856:3536:0921/024225.764:FATAL:ax_object.cc(936)] Check failed: !parent_ || parent_->RoleValue() != ax::mojom::blink::Role::kIframe || RoleValue() == ax::mojom::blink::Role::kDocument. An iframe can only have a document child.
* Child = "\"GenericContainer\" axid#961 <acronym#id223> needsToUpdateCachedValues isIgnored isRemovedFromTree needsToUpdateChildren parentHasDirtyDescendants missingLayout"
* Parent =  "\"Iframe\" axid#666 <fencedframe#id221> needsToUpdateCachedValues isIgnored needsToUpdateChildren parentHasDirtyDescendants"


### [Deleted User] (2023-10-05)

aleventhal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-19)

aleventhal: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-11-01)

CHECK failures are not security bugs. However they do block the fuzzers from making progress and finding actual security bugs.

However in this case it is hitting a DCHECK which will not exist in production, indicating that we can produce AX trees in invalid states, which can have undesirable outcomes as the AX tree has complex parsing machinery in privileged processes.

Can we convert this DCHECK to a CHECK or handle the situation explicitly/correctly?

### al...@chromium.org (2023-11-01)

WIP: https://chromium-review.googlesource.com/c/chromium/src/+/4873421

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0953e5a0ef7748af2c932568ec9d9bbdbc480f11

commit 0953e5a0ef7748af2c932568ec9d9bbdbc480f11
Author: Aaron Leventhal <aleventhal@google.com>
Date: Fri Nov 10 22:22:21 2023

[A11y] Do not allow asymmetrical parent-child relations in tree

Design doc:
https://docs.google.com/document/d/1PnjhlWqTtivmsUVTF0kqMAUIsO9a_eTp32pRY4KJh_U/edit#heading=h.wlgzk7gh4m76

Fix failures brought to light by the Eager AX Tree Updates project and related checks, so that serialization operates on a truly frozen, complete AX Tree, and does not lead to changes to the underlying data at unsafe times. After landing this CL and any follow-ups, the goal is to have a vastly more stable, predictable Blink accessibility engine.

The current implementation can lead to processing the tree when there
are "holes" in the data structure, such as missing parents or children,
which can lead to crashes, checks and unpredictability.

1. Avoid holes in the first place: do not call AXObject::ClearChildren() immediately when calling AXObject::SetNeedsToUpdateChildren(), so that missing parent and missing child holes are not created for unchanged siblings. These holes tended to sit around and cause problems when downstream operations did not expect them. Only call ClearChildren() right before rebuilding the children, in UpdateChildrenIfNecessary().
2. More complete repairs: Instead of only repairing missing parents, when a parentless ensure a complete subtree structure around the child, starting with the included parent. The new method to accomplish this is called AXObjectCacheImpl::RepairIncludedParentsChildren(). It makes sure that every parent up to the included parent has a complete set of children.
3. More timely repairs: instead of waiting for a hole to be discovered while tree walking, eagerly ensure that objects up to their included parent have repairs, whenever an object is being retrieved for deferred event processing, or when an object is being created in the middle of a tree. If the necessary parents do not exist, and thus the AXObject itself is not viable, make sure any stale AXObjects in that subtree are eagerly removed, because they are also not viable.
4. More complete tree structure checks in AXObjectCacheImpl::CheckTreeIsUpdated(), which ensure symmetrical included parent-child relationships are complete. This helps guarantee that no lazy computations try to alter the tree while it’s being serialized (in a frozen state). The new checks do not pass without the other code changes, which are in service of the new checks.

Future work: attempt to avoid any tree repairs and guarantee completeness in more places, providing even more predictability, for example, by handling CSS display changes similarly to role changes.

Fixed: 1422755,1483877,1482591,1481940,1480442,1488246,1486249,1484029,1353205,1480627,1480429,1494849,1493953,1484394,1489027,1491163
Change-Id: Ied4258680ffe4099caaf4c5e614c59c70c61a013
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4873421
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1223164}

[add] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/web_tests/external/wpt/accessibility/crashtests/illegal-optgroup-structure.html
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_position_test.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_node_object.cc
[add] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/test/data/accessibility/html/img-link-empty-alt-set.html
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/testing/buildbot/filters/accessibility-linux.interactive_ui_tests.filter
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_object.cc
[add] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/test/data/accessibility/html/img-link-empty-alt-set-expected-blink.txt
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/test/data/accessibility/event/visibility-hidden-changed-expected-auralinux.txt
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/renderer/accessibility/render_accessibility_impl_browsertest.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_relation_cache.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_menu_list_popup.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_relation_cache.h
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/ax_object.h
[modify] https://crrev.com/0953e5a0ef7748af2c932568ec9d9bbdbc480f11/third_party/blink/renderer/modules/accessibility/testing/accessibility_test.cc


### cl...@chromium.org (2023-11-11)

ClusterFuzz testcase 5548591573303296 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1223122:1223165

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

Requesting merge to extended stable M118 because latest trunk commit (1223164) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1223164) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1223164) appears to be after beta branch point (1217362).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

Merge review required: M120 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

Merge review required: M119 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

Merge review required: M118 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/809d0117b1481d72f26368b6f29b08d91c08055f

commit 809d0117b1481d72f26368b6f29b08d91c08055f
Author: Aaron Leventhal <aleventhal@chromium.org>
Date: Sun Nov 12 20:08:12 2023

Revert "[A11y] Do not allow asymmetrical parent-child relations in tree"

This reverts commit 0953e5a0ef7748af2c932568ec9d9bbdbc480f11.

Reason for revert: https://crbug.com/chromium/1501535 (crashes on google.com when a11y active)

Original change's description:
> [A11y] Do not allow asymmetrical parent-child relations in tree
>
> Design doc:
> https://docs.google.com/document/d/1PnjhlWqTtivmsUVTF0kqMAUIsO9a_eTp32pRY4KJh_U/edit#heading=h.wlgzk7gh4m76
>
> Fix failures brought to light by the Eager AX Tree Updates project and related checks, so that serialization operates on a truly frozen, complete AX Tree, and does not lead to changes to the underlying data at unsafe times. After landing this CL and any follow-ups, the goal is to have a vastly more stable, predictable Blink accessibility engine.
>
> The current implementation can lead to processing the tree when there
> are "holes" in the data structure, such as missing parents or children,
> which can lead to crashes, checks and unpredictability.
>
> 1. Avoid holes in the first place: do not call AXObject::ClearChildren() immediately when calling AXObject::SetNeedsToUpdateChildren(), so that missing parent and missing child holes are not created for unchanged siblings. These holes tended to sit around and cause problems when downstream operations did not expect them. Only call ClearChildren() right before rebuilding the children, in UpdateChildrenIfNecessary().
> 2. More complete repairs: Instead of only repairing missing parents, when a parentless ensure a complete subtree structure around the child, starting with the included parent. The new method to accomplish this is called AXObjectCacheImpl::RepairIncludedParentsChildren(). It makes sure that every parent up to the included parent has a complete set of children.
> 3. More timely repairs: instead of waiting for a hole to be discovered while tree walking, eagerly ensure that objects up to their included parent have repairs, whenever an object is being retrieved for deferred event processing, or when an object is being created in the middle of a tree. If the necessary parents do not exist, and thus the AXObject itself is not viable, make sure any stale AXObjects in that subtree are eagerly removed, because they are also not viable.
> 4. More complete tree structure checks in AXObjectCacheImpl::CheckTreeIsUpdated(), which ensure symmetrical included parent-child relationships are complete. This helps guarantee that no lazy computations try to alter the tree while it’s being serialized (in a frozen state). The new checks do not pass without the other code changes, which are in service of the new checks.
>
> Future work: attempt to avoid any tree repairs and guarantee completeness in more places, providing even more predictability, for example, by handling CSS display changes similarly to role changes.
>
> Fixed: 1422755,1483877,1482591,1481940,1480442,1488246,1486249,1484029,1353205,1480627,1480429,1494849,1493953,1484394,1489027,1491163
> Change-Id: Ied4258680ffe4099caaf4c5e614c59c70c61a013
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4873421
> Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1223164}

Fixed: 1501535
Change-Id: I33d7aab81edacb151cadffeee0969df4591bd947
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021416
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1223407}

[delete] https://crrev.com/762bbab70d93a24334aca9fd2ce1e47367183167/third_party/blink/web_tests/external/wpt/accessibility/crashtests/illegal-optgroup-structure.html
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_position_test.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_node_object.cc
[delete] https://crrev.com/762bbab70d93a24334aca9fd2ce1e47367183167/content/test/data/accessibility/html/img-link-empty-alt-set.html
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/testing/buildbot/filters/accessibility-linux.interactive_ui_tests.filter
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_object.cc
[delete] https://crrev.com/762bbab70d93a24334aca9fd2ce1e47367183167/content/test/data/accessibility/html/img-link-empty-alt-set-expected-blink.txt
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/content/renderer/accessibility/render_accessibility_impl_browsertest.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/content/test/data/accessibility/event/visibility-hidden-changed-expected-auralinux.txt
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_menu_list_popup.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_relation_cache.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_relation_cache.h
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/ax_object.h
[modify] https://crrev.com/809d0117b1481d72f26368b6f29b08d91c08055f/third_party/blink/renderer/modules/accessibility/testing/accessibility_test.cc


### pg...@google.com (2023-11-13)

Re-opening as the fix was reverted.
Keeping merge labels on for tracking.

### gi...@appspot.gserviceaccount.com (2023-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fda0f8317a6f861c97c413d1deecb8c4f998481

commit 8fda0f8317a6f861c97c413d1deecb8c4f998481
Author: Aaron Leventhal <aleventhal@google.com>
Date: Fri Nov 17 04:00:20 2023

Reland "[A11y] Do not allow asymmetrical parent-child relations in tree"

This is a reland of commit 0953e5a0ef7748af2c932568ec9d9bbdbc480f11

Two new tests have been added since the original CL:
1. content/test/data/regression/aria-owns-from-textarea.html, which
induces the same crash as google.com, which caused the revert via https://crbug.com/chromium/1501535. The fix for this one is to not assume the owned child had
previously been unignored.
2. web_tests/accessibility/aria-owns-dynamic-changes-2.html, to show that the consequences of the error Chris found in the original landing as discussed in this review thread: https://chromium-review.googlesource.com/c/chromium/src/+/4873421/72..77/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc#b1418
The fix for this one was already in the original landing.

Original change's description:
> [A11y] Do not allow asymmetrical parent-child relations in tree
>
> Design doc:
> https://docs.google.com/document/d/1PnjhlWqTtivmsUVTF0kqMAUIsO9a_eTp32pRY4KJh_U/edit#heading=h.wlgzk7gh4m76
>
> Fix failures brought to light by the Eager AX Tree Updates project and related checks, so that serialization operates on a truly frozen, complete AX Tree, and does not lead to changes to the underlying data at unsafe times. After landing this CL and any follow-ups, the goal is to have a vastly more stable, predictable Blink accessibility engine.
>
> The current implementation can lead to processing the tree when there
> are "holes" in the data structure, such as missing parents or children,
> which can lead to crashes, checks and unpredictability.
>
> 1. Avoid holes in the first place: do not call AXObject::ClearChildren() immediately when calling AXObject::SetNeedsToUpdateChildren(), so that missing parent and missing child holes are not created for unchanged siblings. These holes tended to sit around and cause problems when downstream operations did not expect them. Only call ClearChildren() right before rebuilding the children, in UpdateChildrenIfNecessary().
> 2. More complete repairs: Instead of only repairing missing parents, when a parentless ensure a complete subtree structure around the child, starting with the included parent. The new method to accomplish this is called AXObjectCacheImpl::RepairIncludedParentsChildren(). It makes sure that every parent up to the included parent has a complete set of children.
> 3. More timely repairs: instead of waiting for a hole to be discovered while tree walking, eagerly ensure that objects up to their included parent have repairs, whenever an object is being retrieved for deferred event processing, or when an object is being created in the middle of a tree. If the necessary parents do not exist, and thus the AXObject itself is not viable, make sure any stale AXObjects in that subtree are eagerly removed, because they are also not viable.
> 4. More complete tree structure checks in AXObjectCacheImpl::CheckTreeIsUpdated(), which ensure symmetrical included parent-child relationships are complete. This helps guarantee that no lazy computations try to alter the tree while it’s being serialized (in a frozen state). The new checks do not pass without the other code changes, which are in service of the new checks.
>
> Future work: attempt to avoid any tree repairs and guarantee completeness in more places, providing even more predictability, for example, by handling CSS display changes similarly to role changes.
>
> Fixed: 1422755,1483877,1482591,1481940,1480442,1488246,1486249,1484029,1353205,1480627,1494849,1493953,1484394,1489027,1491163,1501723
> Change-Id: Ied4258680ffe4099caaf4c5e614c59c70c61a013
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4873421
> Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1223164}

Change-Id: I96fcc71601842ea7b38de70ee24f77df1f011f24
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019353
Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1225907}

[add] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/web_tests/external/wpt/accessibility/crashtests/illegal-optgroup-structure.html
[add] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/test/data/accessibility/regression/aria-owns-from-textarea.html
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_position_test.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_node_object.cc
[add] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/test/data/accessibility/html/img-link-empty-alt-set.html
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/testing/buildbot/filters/accessibility-linux.interactive_ui_tests.filter
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_object.cc
[add] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/test/data/accessibility/html/img-link-empty-alt-set-expected-blink.txt
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/renderer/accessibility/render_accessibility_impl_browsertest.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/test/data/accessibility/event/visibility-hidden-changed-expected-auralinux.txt
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_menu_list_popup.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_relation_cache.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_relation_cache.h
[add] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/web_tests/accessibility/aria-owns-dynamic-changes-2.html
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/ax_object.h
[modify] https://crrev.com/8fda0f8317a6f861c97c413d1deecb8c4f998481/third_party/blink/renderer/modules/accessibility/testing/accessibility_test.cc


### gi...@appspot.gserviceaccount.com (2023-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d71be73ff6ae1e26559634149c729b41de71836

commit 7d71be73ff6ae1e26559634149c729b41de71836
Author: Yifan Luo <lyf@chromium.org>
Date: Fri Nov 17 09:53:09 2023

Revert "Reland "[A11y] Do not allow asymmetrical parent-child relations in tree""

This reverts commit 8fda0f8317a6f861c97c413d1deecb8c4f998481.

Reason for revert: Test failure on Linux MSan Tests: https://ci.chromium.org/ui/b/8764197885202278033

Original change's description:
> Reland "[A11y] Do not allow asymmetrical parent-child relations in tree"
>
> This is a reland of commit 0953e5a0ef7748af2c932568ec9d9bbdbc480f11
>
> Two new tests have been added since the original CL:
> 1. content/test/data/regression/aria-owns-from-textarea.html, which
> induces the same crash as google.com, which caused the revert via https://crbug.com/chromium/1501535. The fix for this one is to not assume the owned child had
> previously been unignored.
> 2. web_tests/accessibility/aria-owns-dynamic-changes-2.html, to show that the consequences of the error Chris found in the original landing as discussed in this review thread: https://chromium-review.googlesource.com/c/chromium/src/+/4873421/72..77/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc#b1418
> The fix for this one was already in the original landing.
>
> Original change's description:
> > [A11y] Do not allow asymmetrical parent-child relations in tree
> >
> > Design doc:
> > https://docs.google.com/document/d/1PnjhlWqTtivmsUVTF0kqMAUIsO9a_eTp32pRY4KJh_U/edit#heading=h.wlgzk7gh4m76
> >
> > Fix failures brought to light by the Eager AX Tree Updates project and related checks, so that serialization operates on a truly frozen, complete AX Tree, and does not lead to changes to the underlying data at unsafe times. After landing this CL and any follow-ups, the goal is to have a vastly more stable, predictable Blink accessibility engine.
> >
> > The current implementation can lead to processing the tree when there
> > are "holes" in the data structure, such as missing parents or children,
> > which can lead to crashes, checks and unpredictability.
> >
> > 1. Avoid holes in the first place: do not call AXObject::ClearChildren() immediately when calling AXObject::SetNeedsToUpdateChildren(), so that missing parent and missing child holes are not created for unchanged siblings. These holes tended to sit around and cause problems when downstream operations did not expect them. Only call ClearChildren() right before rebuilding the children, in UpdateChildrenIfNecessary().
> > 2. More complete repairs: Instead of only repairing missing parents, when a parentless ensure a complete subtree structure around the child, starting with the included parent. The new method to accomplish this is called AXObjectCacheImpl::RepairIncludedParentsChildren(). It makes sure that every parent up to the included parent has a complete set of children.
> > 3. More timely repairs: instead of waiting for a hole to be discovered while tree walking, eagerly ensure that objects up to their included parent have repairs, whenever an object is being retrieved for deferred event processing, or when an object is being created in the middle of a tree. If the necessary parents do not exist, and thus the AXObject itself is not viable, make sure any stale AXObjects in that subtree are eagerly removed, because they are also not viable.
> > 4. More complete tree structure checks in AXObjectCacheImpl::CheckTreeIsUpdated(), which ensure symmetrical included parent-child relationships are complete. This helps guarantee that no lazy computations try to alter the tree while it’s being serialized (in a frozen state). The new checks do not pass without the other code changes, which are in service of the new checks.
> >
> > Future work: attempt to avoid any tree repairs and guarantee completeness in more places, providing even more predictability, for example, by handling CSS display changes similarly to role changes.
> >
> > Fixed: 1422755,1483877,1482591,1481940,1480442,1488246,1486249,1484029,1353205,1480627,1494849,1493953,1484394,1489027,1491163,1501723
> > Change-Id: Ied4258680ffe4099caaf4c5e614c59c70c61a013
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4873421
> > Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> > Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1223164}
>
> Change-Id: I96fcc71601842ea7b38de70ee24f77df1f011f24
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019353
> Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
> Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1225907}

Change-Id: I77f6149192a7afa697098e125900705ab43ed0f0
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 1503056
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5040555
Reviewed-by: Yifan Luo <lyf@chromium.org>
Owners-Override: Yifan Luo <lyf@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1225985}

[delete] https://crrev.com/405985e45cadcf2af8afeec06fef44b87187c74a/content/test/data/accessibility/regression/aria-owns-from-textarea.html
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_position_test.cc
[delete] https://crrev.com/405985e45cadcf2af8afeec06fef44b87187c74a/third_party/blink/web_tests/external/wpt/accessibility/crashtests/illegal-optgroup-structure.html
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_node_object.cc
[delete] https://crrev.com/405985e45cadcf2af8afeec06fef44b87187c74a/content/test/data/accessibility/html/img-link-empty-alt-set.html
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/testing/buildbot/filters/accessibility-linux.interactive_ui_tests.filter
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_object.cc
[delete] https://crrev.com/405985e45cadcf2af8afeec06fef44b87187c74a/content/test/data/accessibility/html/img-link-empty-alt-set-expected-blink.txt
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/content/renderer/accessibility/render_accessibility_impl_browsertest.cc
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/content/test/data/accessibility/event/visibility-hidden-changed-expected-auralinux.txt
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_menu_list_popup.cc
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_relation_cache.cc
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_relation_cache.h
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[delete] https://crrev.com/405985e45cadcf2af8afeec06fef44b87187c74a/third_party/blink/web_tests/accessibility/aria-owns-dynamic-changes-2.html
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/ax_object.h
[modify] https://crrev.com/7d71be73ff6ae1e26559634149c729b41de71836/third_party/blink/renderer/modules/accessibility/testing/accessibility_test.cc


### gi...@appspot.gserviceaccount.com (2023-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53ae5d8361e2b89acb8e89083016ab16d6e6273c

commit 53ae5d8361e2b89acb8e89083016ab16d6e6273c
Author: Yifan Luo <lyf@chromium.org>
Date: Fri Nov 17 11:57:13 2023

Revert^2 "Reland "[A11y] Do not allow asymmetrical parent-child relations in tree""

This reverts commit 7d71be73ff6ae1e26559634149c729b41de71836.

Reason for revert: Reverting this cl makes the failure stable. reland this.

Original change's description:
> Revert "Reland "[A11y] Do not allow asymmetrical parent-child relations in tree""
>
> This reverts commit 8fda0f8317a6f861c97c413d1deecb8c4f998481.
>
> Reason for revert: Test failure on Linux MSan Tests: https://ci.chromium.org/ui/b/8764197885202278033
>
> Original change's description:
> > Reland "[A11y] Do not allow asymmetrical parent-child relations in tree"
> >
> > This is a reland of commit 0953e5a0ef7748af2c932568ec9d9bbdbc480f11
> >
> > Two new tests have been added since the original CL:
> > 1. content/test/data/regression/aria-owns-from-textarea.html, which
> > induces the same crash as google.com, which caused the revert via https://crbug.com/chromium/1501535. The fix for this one is to not assume the owned child had
> > previously been unignored.
> > 2. web_tests/accessibility/aria-owns-dynamic-changes-2.html, to show that the consequences of the error Chris found in the original landing as discussed in this review thread: https://chromium-review.googlesource.com/c/chromium/src/+/4873421/72..77/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc#b1418
> > The fix for this one was already in the original landing.
> >
> > Original change's description:
> > > [A11y] Do not allow asymmetrical parent-child relations in tree
> > >
> > > Design doc:
> > > https://docs.google.com/document/d/1PnjhlWqTtivmsUVTF0kqMAUIsO9a_eTp32pRY4KJh_U/edit#heading=h.wlgzk7gh4m76
> > >
> > > Fix failures brought to light by the Eager AX Tree Updates project and related checks, so that serialization operates on a truly frozen, complete AX Tree, and does not lead to changes to the underlying data at unsafe times. After landing this CL and any follow-ups, the goal is to have a vastly more stable, predictable Blink accessibility engine.
> > >
> > > The current implementation can lead to processing the tree when there
> > > are "holes" in the data structure, such as missing parents or children,
> > > which can lead to crashes, checks and unpredictability.
> > >
> > > 1. Avoid holes in the first place: do not call AXObject::ClearChildren() immediately when calling AXObject::SetNeedsToUpdateChildren(), so that missing parent and missing child holes are not created for unchanged siblings. These holes tended to sit around and cause problems when downstream operations did not expect them. Only call ClearChildren() right before rebuilding the children, in UpdateChildrenIfNecessary().
> > > 2. More complete repairs: Instead of only repairing missing parents, when a parentless ensure a complete subtree structure around the child, starting with the included parent. The new method to accomplish this is called AXObjectCacheImpl::RepairIncludedParentsChildren(). It makes sure that every parent up to the included parent has a complete set of children.
> > > 3. More timely repairs: instead of waiting for a hole to be discovered while tree walking, eagerly ensure that objects up to their included parent have repairs, whenever an object is being retrieved for deferred event processing, or when an object is being created in the middle of a tree. If the necessary parents do not exist, and thus the AXObject itself is not viable, make sure any stale AXObjects in that subtree are eagerly removed, because they are also not viable.
> > > 4. More complete tree structure checks in AXObjectCacheImpl::CheckTreeIsUpdated(), which ensure symmetrical included parent-child relationships are complete. This helps guarantee that no lazy computations try to alter the tree while it’s being serialized (in a frozen state). The new checks do not pass without the other code changes, which are in service of the new checks.
> > >
> > > Future work: attempt to avoid any tree repairs and guarantee completeness in more places, providing even more predictability, for example, by handling CSS display changes similarly to role changes.
> > >
> > > Fixed: 1422755,1483877,1482591,1481940,1480442,1488246,1486249,1484029,1353205,1480627,1494849,1493953,1484394,1489027,1491163,1501723
> > > Change-Id: Ied4258680ffe4099caaf4c5e614c59c70c61a013
> > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4873421
> > > Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> > > Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> > > Cr-Commit-Position: refs/heads/main@{#1223164}
> >
> > Change-Id: I96fcc71601842ea7b38de70ee24f77df1f011f24
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019353
> > Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
> > Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
> > Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1225907}
>
> Change-Id: I77f6149192a7afa697098e125900705ab43ed0f0
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: 1503056
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5040555
> Reviewed-by: Yifan Luo <lyf@chromium.org>
> Owners-Override: Yifan Luo <lyf@chromium.org>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1225985}

Bug: 1503056
Change-Id: Id9b4319eefa91a2988adda94fb69bc1881c63600
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5038755
Auto-Submit: Yifan Luo <lyf@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Yifan Luo <lyf@chromium.org>
Reviewed-by: Yifan Luo <lyf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1226026}

[add] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/test/data/accessibility/regression/aria-owns-from-textarea.html
[add] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/web_tests/external/wpt/accessibility/crashtests/illegal-optgroup-structure.html
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_position_test.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_node_object.cc
[add] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/test/data/accessibility/html/img-link-empty-alt-set.html
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/testing/buildbot/filters/accessibility-linux.interactive_ui_tests.filter
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_object.cc
[add] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/test/data/accessibility/html/img-link-empty-alt-set-expected-blink.txt
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/test/data/accessibility/event/visibility-hidden-changed-expected-auralinux.txt
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/renderer/accessibility/render_accessibility_impl_browsertest.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_relation_cache.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_menu_list_popup.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_relation_cache.h
[add] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/web_tests/accessibility/aria-owns-dynamic-changes-2.html
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/ax_object.h
[modify] https://crrev.com/53ae5d8361e2b89acb8e89083016ab16d6e6273c/third_party/blink/renderer/modules/accessibility/testing/accessibility_test.cc


### pg...@google.com (2023-11-21)

For context (from lyf@, thank you!) on the double revert, the revert was reverted because the tests that it was failing were actually flaky (context, https://crbug.com/chromium/1503056)

Although this fix has sat in canary for a while and show no other potential issues, the fix is quite large and more of a holistic change. Hence, I'm leaning to not back merge the fix for stability concerns, and let it roll out naturally with M121, where the fix landed. aleventhal@, if you disagree, please let me know! Happy to chat about the stability risks. Removing merge labels for now.



### am...@google.com (2023-11-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-22)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of renderer process memory corruption + $2,000 fuzzer bonus. Thank you for your past fuzzing contributions that resulted in this report. Nice work! 

### am...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1484394?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072724)*
