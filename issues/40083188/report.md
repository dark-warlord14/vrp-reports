# Security: Pwn2Own mobile case, out-of-bound access in json stringifier

| Field | Value |
|-------|-------|
| **Issue ID** | [40083188](https://issues.chromium.org/issues/40083188) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2015-11-12 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The vulnerable code is at BasicJsonStringifier::SerializeJSArray

BasicJsonStringifier::Result BasicJsonStringifier::SerializeJSArray(  

Handle<JSArray> object) {  

HandleScope handle\_scope(isolate\_);  

Result stack\_push = StackPush(object);  

if (stack\_push != SUCCESS) return stack\_push;  

uint32\_t length = 0;  

CHECK(object->length()->ToArrayLength(&length)); ---------------> initialized length here.  

builder\_.AppendCharacter('[');  

switch (object->GetElementsKind()) {  

case FAST\_SMI\_ELEMENTS: {  

Handle<FixedArray> elements(  

FixedArray::cast(object->elements()), isolate\_);  

for (uint32\_t i = 0; i < length; i++) {  

if (i > 0) builder\_.AppendCharacter(',');  

SerializeSmi(Smi::cast(elements->get(i)));  

}  

break;  

}  

case FAST\_DOUBLE\_ELEMENTS: {  

// Empty array is FixedArray but not FixedDoubleArray.  

if (length == 0) break;  

Handle<FixedDoubleArray> elements(  

FixedDoubleArray::cast(object->elements()), isolate\_);  

for (uint32\_t i = 0; i < length; i++) {  

if (i > 0) builder\_.AppendCharacter(',');  

SerializeDouble(elements->get\_scalar(i));  

}  

break;  

}  

case FAST\_ELEMENTS: {  

Handle<FixedArray> elements(  

FixedArray::cast(object->elements()), isolate\_);  

for (uint32\_t i = 0; i < length; i++) { ------------------>iterate the array here, but the length can be modified while iterating because there is javascript callbacks, such as toJSON.  

if (i > 0) builder\_.AppendCharacter(',');  

Result result =  

SerializeElement(isolate\_,  

Handle<Object>(elements->get(i), isolate\_), ------> element->get(i) will serialize out-of-bound elements  

i);  

if (result == SUCCESS) continue;  

if (result == UNCHANGED) {  

builder\_.AppendCString("null");  

} else {  

return result;  

}  

}  

break;  

}  

// TODO(yangguo): The FAST\_HOLEY\_\* cases could be handled in a faster way.  

// They resemble the non-holey cases except that a prototype chain lookup  

// is necessary for holes.  

default: {  

Result result = SerializeJSArraySlow(object, length);  

if (result != SUCCESS) return result;  

break;  

}  

}  

builder\_.AppendCharacter(']');  

StackPop();  

return SUCCESS;  

}

Chrome Version: [46.0.2490.76] + [stabe]  

to exploit this bug, we can fake a JSArrayBuffer object in the out-of-bound memory, when SerializeElement handle this faked arraybuffer, we can get a javascript object when code is called back to javascript by toJSON.

How to install an App without user interaction.  

1.get remote code execution with this bug.  

2.need a Google account signed in the Nexus devices, convert the rce to a uxss and inject javascript code into play.google.com to execute.

the full exploit is attached as a.html. you can test it with the latest Chrome in a Nexus 6 device.  

the rce2uxss code is attached as service.cpp, I inline hooked function executeScript to append some javascript.

## Attachments

- [service.cpp](attachments/service.cpp) (application/octet-stream, 5.8 KB)
- [a.html](attachments/a.html) (text/html, 50.4 KB)

## Timeline

### rs...@chromium.org (2015-11-12)

Thanks for the report!

### hi...@gmail.com (2015-11-12)

one thing more, I didn't launcher the installed App in the exploit, but I think their are several ways to do this, such as use intent schema, by receiving some broadcast receiver. 

### rs...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-11-12)

v8 renderer execution bugs are severity High.

The part of the chain where UXSS can be used to control Play Store are covered by https://crbug.com/chromium/554518.

### ha...@google.com (2015-11-12)

[Empty comment from Monorail migration]

### jk...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/6df9a1db8c85ab63dee63879456b6027df53fabc

commit 6df9a1db8c85ab63dee63879456b6027df53fabc
Author: yangguo <yangguo@chromium.org>
Date: Thu Nov 12 19:30:09 2015

[JSON stringifier] Correctly load array elements.

BUG=chromium:554946
LOG=y
R=jkummerow@chromium.org, jochen@chromium.org

Review URL: https://codereview.chromium.org/1435083003

Cr-Commit-Position: refs/heads/master@{#31968}

[modify] http://crrev.com/6df9a1db8c85ab63dee63879456b6027df53fabc/src/json-stringifier.h
[add] http://crrev.com/6df9a1db8c85ab63dee63879456b6027df53fabc/test/mjsunit/regress/regress-crbug-554946.js


### jo...@chromium.org (2015-11-12)

not marking as fixed yet, while we discuss whether to embargo the play stuff or not

### ti...@google.com (2015-11-12)

Adding Security-Embargo label so you can mark this as fixed and then we can decide when to manually release it to security-notify (noting the PoC in the OP)

### jo...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### hi...@gmail.com (2015-11-12)

it seems like the issue is fixed at the expensive of performence,  it's a little pity.

### rs...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### ya...@chromium.org (2015-11-13)

I do have a plan to fix the performance regression. Just didnt have time to implement right away.

### ha...@google.com (2015-11-13)

[Empty comment from Monorail migration]

### ya...@chromium.org (2015-11-13)

Looks like the fix won't make M48.

### ha...@google.com (2015-11-13)

Correct. It will probably be on the second M48 built if nothing shows up on Canary.

### ti...@google.com (2015-11-13)

[Automated comment] Request affecting a post-stable build (M46), manual review required.

### ti...@google.com (2015-11-13)

Congrats your change is auto-approved for M47 (branch: 2526)

### ti...@google.com (2015-11-13)

[Automated comment] Commit may have occurred before M48 branch point (11/13/2015), needs manual review.

### pa...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### kc...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### kc...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-14)

Assigning CVE in advance of release notes for easier referencing.

### ss...@google.com (2015-11-16)

This merge has been approved for M47 and stable cut is coming up soon. Reminder to please merge this in, if we want it on M47.

### in...@chromium.org (2015-11-16)

sshruthi@, please don't release until this bug fix is merged.

### ha...@chromium.org (2015-11-16)

First Canary with the fix should go live today. If everything goes right we can merge it Wednesday. This should be sufficient isn't it?

### ss...@google.com (2015-11-16)

Got it! What's the latest on this? Is the fix in trunk, needs to be merged into M47? Or, is there still investigation pending?

### ss...@google.com (2015-11-16)

hablich@, we cross-commented. Yup, that is sufficient.

### in...@chromium.org (2015-11-16)

Fix is in https://code.google.com/p/chromium/issues/detail?id=554946#c12. We are just waiting on Yangguo@ to merge this to M47, M48 asap (Yang is in Munich time zone).

### ss...@google.com (2015-11-16)

Ok thanks! I wasn't sure if that's the only fix we were talking about, since there was also talk about fixing the performance cost. yangguo@, if we are not waiting on anything else, can we merge this in tomorrow so it's in this week's beta push?

### ya...@chromium.org (2015-11-16)

There is indeed a performance fix that I landed half a day after. I will merge both tomorrow morning (in about 12 hours) if that's alright. Both should have gotten Canary coverage. The performance fix is important, as the first one is a quiclfix that tanks performance a lot.

This is the performance fix btw:https://codereview.chromium.org/1440223002/

For some reason bugdroid overlooked it.

### ya...@chromium.org (2015-11-16)

Correction: this is the actual CL for the performance fix. https://codereview.chromium.org/1442963002/

### ha...@chromium.org (2015-11-16)

I wouldn't count on today's Canary to be representative . It is not yet released because of some infrastructure problems related to this weekend's outage. A merge on Wednesday seems to be enough, so let's do that.

### ha...@chromium.org (2015-11-16)

There seemed to some confusion. That is now cleared up. Beta build is started Tuesday evening which means this needs to be merged on Tuesday. IMO one day of Canary is not a lot (not enough) coverage. After talking with sshruthi@ we have the following options:

1.) Delay Beta build for one day
2.) Merge anyway

The decision will be made on Tuesday.



### ha...@chromium.org (2015-11-17)

Yang and I reconciled today. There was no Monday Canary and today is the first day with the two fixes in it. Especially for the second check-in we want to have proper Canary coverage before we merge it.

I propose delaying the Beta build for one day. If we don't get crashers reported connected to the fixes we are going to merge them on Wednesday.

Btw, is there any value merging this to M46?



### ss...@google.com (2015-11-17)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-17)

Leaving this as open till we merge into M47, for tracking purposes.

### cl...@chromium.org (2015-11-17)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ha...@google.com (2015-11-18)

Let's merge this to 46 too. Just in case you also want to do another 46 push.

### [Deleted User] (2015-11-18)

Opera will also take in these patches and release as soon as possible. Is there any estimates for when the details of this issue will be disclosed?

### ha...@chromium.org (2015-11-18)

Merged to 4.8:
 https://chromium.googlesource.com/v8/v8.git/+/971564a9c539700b38e1201f28526b9adc9dc422

4.7: https://chromium.googlesource.com/v8/v8.git/+/a10202d1aa3cbaa3b550401bebbe34119b2d20b2

4.6: https://chromium.googlesource.com/v8/v8.git/+/06c0a54bf476fcf6aa133078f50ca63634f91965

### ss...@google.com (2015-11-18)

Changing labels to show that this has been merged into 46, 47, 48 as per hablich@ comment. Please change if that is incorrect.

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-11-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Thanks for reporting this issue to us - our reward panel awarded you $7,500 for your report. I'll start the payment process shortly. 

We'll list you in our release notes for M47 as "Guang Gong" and reference this issue and the CVE ID. 

Thanks again for your research and hope to hear from you again soon!


### hi...@gmail.com (2015-12-01)

Could you kindly add my company in your release notes?
such as "Guang Gong of Qihoo 360", thanks.

### ti...@google.com (2015-12-01)

Done! Should be published in about 12 hours.

### ya...@chromium.org (2015-12-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### kc...@chromium.org (2015-12-15)

Is it possible to write a target function for libfuzzer
(https://sites.google.com/a/chromium.org/dev/developers/testing/libfuzzer)
that will trigger this bug with a proper input?

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-11)

Removing view restrictions as the fix pushed with M47 and there's public interest in this mobile pwn2own submission.

### rs...@chromium.org (2016-01-11)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/554946?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/554518]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083188)*
