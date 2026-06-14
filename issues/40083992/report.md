# Heap-use-after-free in blink::LayoutBoxModelObject::invalidateStickyConstraints

| Field | Value |
|-------|-------|
| **Issue ID** | [40083992](https://issues.chromium.org/issues/40083992) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-04-01 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4893865365995520

Fuzzer: attekett_dom_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7d340000b000
Crash State:
  blink::LayoutBoxModelObject::invalidateStickyConstraints
  blink::LayoutBlock::updateAfterLayout
  blink::LayoutFlexibleBox::layoutBlock
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=384213:384232

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv962gi8VyabVMhXiClu5gqygSWmTAPSi_Kgbp1yh4Zfa_44h9zgGglk5vbdlwiHJDTukJ5mme624YLg7N7eEasf2LDbmIy4xTWQ2nk-dQHfK6LKGN0zlSwTiLVBeRvpa-e7Bc1so9rxhdnnds1xQ7f1DM8D5eQ
<style>
a:hover {
}
.face {
    overflow: hidden;
    top: 155px;
</style>
    <div class="face left">
    <video>  
<script> 
setTimeout(function(){
document.styleSheets[0].disabled=true;;
})
</script>


Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-04-01)

dsinclair@, could you please take a look or suggest another owner?

### mm...@chromium.org (2016-04-01)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout]

### cl...@chromium.org (2016-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-02)

ClusterFuzz has detected this issue as fixed in range 384282:384380.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4893865365995520

Fuzzer: attekett_dom_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7d340000b000
Crash State:
  blink::LayoutBoxModelObject::invalidateStickyConstraints
  blink::LayoutBlock::updateAfterLayout
  blink::LayoutFlexibleBox::layoutBlock
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=384213:384232
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=384282:384380

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv962gi8VyabVMhXiClu5gqygSWmTAPSi_Kgbp1yh4Zfa_44h9zgGglk5vbdlwiHJDTukJ5mme624YLg7N7eEasf2LDbmIy4xTWQ2nk-dQHfK6LKGN0zlSwTiLVBeRvpa-e7Bc1so9rxhdnnds1xQ7f1DM8D5eQ
<style>
a:hover {
}
.face {
    overflow: hidden;
    top: 155px;
</style>
    <div class="face left">
    <video>  
<script> 
setTimeout(function(){
document.styleSheets[0].disabled=true;;
})
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-02)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ds...@chromium.org (2016-04-04)

Closing as per clusterfuzz in #4.

### cl...@chromium.org (2016-04-05)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-30)

Atte - another $3,500 for you here ($3k for the report, $500 for the fuzzer).

### aw...@chromium.org (2016-06-30)

[Comment Deleted]

### aw...@chromium.org (2016-06-30)

[Comment Deleted]

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-12)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/599849?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083992)*
