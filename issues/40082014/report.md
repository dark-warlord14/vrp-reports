# An integer overflow in libskia could be used to escalate from Chrome's sandbox in Android

| Field | Value |
|-------|-------|
| **Issue ID** | [40082014](https://issues.chromium.org/issues/40082014) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android |
| **CVE IDs** | CVE-2015-3849 |
| **Reporter** | hi...@gmail.com |
| **Assignee** | dj...@chromium.org |
| **Created** | 2015-05-06 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Actually, It's a vulnerability of Android system, but it's can be used for Chrome's sandbox escalation.  

The integer overflow occur at  

62 static RunHead\* Alloc(int count) {  

63 //SkDEBUGCODE(sk\_atomic\_inc(&gRgnAllocCounter);)  

64 //SkDEBUGF(("\*\*\*\*\*\*\*\*\*\*\*\*\*\* gRgnAllocCounter::alloc %d\n", gRgnAllocCounter));  

65  

66 SkASSERT(count >= SkRegion::kRectRegionRuns);  

67  

68 RunHead\* head = (RunHead\*)sk\_malloc\_throw(sizeof(RunHead) + count \* sizeof(RunType)); --------------> there's no check for the overflow of the allocated size  

69 head->fRefCnt = 1;  

70 head->fRunCount = count;  

71 // these must be filled in later, otherwise we will be invalid  

72 head->fYSpanCount = 0;  

73 head->fIntervalCount = 0;  

74 return head;  

75 }

1130size\_t SkRegion::readFromMemory(const void\* storage, size\_t length) {  

1131 SkRBufferWithSizeCheck buffer(storage, length);  

1132 SkRegion tmp;  

1133 int32\_t count;  

1134  

1135 if (buffer.readS32(&count) && (count >= 0) && buffer.read(&tmp.fBounds, sizeof(tmp.fBounds))) {  

1136 if (count == 0) {  

1137 tmp.fRunHead = SkRegion\_gRectRunHeadPtr;  

1138 } else {  

1139 int32\_t ySpanCount, intervalCount;  

1140 if (buffer.readS32(&ySpanCount) && buffer.readS32(&intervalCount)) {  

1141 tmp.allocateRuns(count, ySpanCount, intervalCount); -------------->the vulnerable Alloc will be call here, we can trigger an integer overflow by controlling count  

1142 buffer.read(tmp.fRunHead->writable\_runs(), count \* sizeof(RunType)); ---------> the allocated buffer with the wrong size will be written here, which will cause heap corruption.  

1143 }  

1144 }  

1145 }  

1146 size\_t sizeRead = 0;  

1147 if (buffer.isValid()) {  

1148 this->swap(tmp);  

1149 sizeRead = buffer.pos();  

1150 }  

1151 return sizeRead;  

1152}

Because Region\_createFromParcel call SkRegion::readFromMemory, we can put a mal-formatted Region object in the bundle and send this bundle to system\_server by a binder call in IActivityManager, the transaction code of the binder call is CONVERT\_TO\_TRANSLUCENT\_TRANSACTION. when system\_server unparcel the bundle, the vulnerability will be trigger and the heap of system\_server will be corrupted. sandboxed Chrome render process have access to IActivityManager, so we can corrupt system\_server's heap from render processes, which could be used to escalate from sandbox.

the backtrace of trigger integer overflow is as flowers:  

(gdb) bt  

#0 SkRegion::RunHead::Alloc (count=1073741823) at external/skia/src/core/SkRegionPriv.h:68  

#1 0xb5a492f8 in Alloc (intervalCount=-858993460, yspancount=-858993460, count=<optimized out>) at external/skia/src/core/SkRegionPriv.h:81  

#2 SkRegion::allocateRuns (this=this@entry=0xa34ed1dc, count=<optimized out>, ySpanCount=-858993460, intervalCount=-858993460) at external/skia/src/core/SkRegion.cpp:104  

#3 0xb5a49f74 in SkRegion::readFromMemory (this=this@entry=0x9cd101d8, storage=<optimized out>, length=length@entry=100) at external/skia/src/core/SkRegion.cpp:1141  

#4 0xb6e60244 in android::Region\_createFromParcel (env=<optimized out>, clazz=<optimized out>, parcel=<optimized out>) at frameworks/base/core/jni/android/graphics/Region.cpp:217  

#5 0x72b9197e in ?? ()  

#6 0x72b9197e in ?? ()  

Backtrace stopped: previous frame identical to this frame (corrupt stack?)

the heap corruption backtrace is as follows:  

Program received signal SIGBUS, Bus error.  

[Switching to Thread 16519]  

\_\_memcpy\_base () at bionic/libc/arch-arm/krait/bionic/memcpy\_base.S:83  

83 vst1.8 {d0 - d3}, [r0, :128]!  

(gdb) bt  

#0 \_\_memcpy\_base () at bionic/libc/arch-arm/krait/bionic/memcpy\_base.S:83  

#1 0xb5a920bc in memcpy (copy\_amount=4294967292, src=<optimized out>, dest=<optimized out>) at bionic/libc/include/../include/string.h:104  

#2 SkRBuffer::readNoSizeCheck (this=this@entry=0xa34d21c8, buffer=<optimized out>, size=4294967292) at external/skia/src/core/SkBuffer.cpp:18  

#3 0xb5a920f6 in SkRBufferWithSizeCheck::read (this=this@entry=0xa34d21c8, buffer=<optimized out>, size=size@entry=4294967292) at external/skia/src/core/SkBuffer.cpp:40  

#4 0xb5abaf82 in SkRegion::readFromMemory (this=this@entry=0x9a3d0460, storage=<optimized out>, length=length@entry=100) at external/skia/src/core/SkRegion.cpp:1142  

#5 0xb6ed1244 in android::Region\_createFromParcel (env=<optimized out>, clazz=<optimized out>, parcel=<optimized out>) at frameworks/base/core/jni/android/graphics/Region.cpp:217  

#6 0x72b9197e in ?? ()  

#7 0x72b9197e in ?? ()  

Backtrace stopped: previous frame identical to this frame (corrupt stack?)

the adb log of crash system\_server is as follow:  

I/DEBUG (19397): \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\* \*\*\*  

I/DEBUG (19397): Build fingerprint: 'Android/aosp\_hammerhead/hammerhead:5.0/LRX21Q/ggong11131350:userdebug/test-keys'  

I/DEBUG (19397): Revision: '11'  

I/DEBUG (19397): ABI: 'arm'  

I/DEBUG (19397): pid: 19690, tid: 19706, name: Binder\_1 >>> system\_server <<<  

I/DEBUG (19397): signal 11 (SIGSEGV), code 2 (SEGV\_ACCERR), fault addr 0xa3305000  

I/DEBUG (19397): r0 9cbd1970 r1 a3304ff0 r2 fff8a3fc r3 00000000  

I/DEBUG (19397): r4 a34021c8 r5 fffffffc r6 9cb6cb20 r7 12f48600  

I/DEBUG (19397): r8 70e6d870 r9 a3206400 sl 12f48600 fp 00000000  

I/DEBUG (19397): ip b5b208c4 sp a3402198 lr b59cf0bd pc b6e90f0a cpsr a00b0030  

I/DEBUG (19397):  

I/DEBUG (19397): backtrace:  

I/DEBUG (19397): #00 pc 00012f0a /system/lib/libc.so (\_\_memcpy\_base+77)  

I/DEBUG (19397): #01 pc 000d60b9 /system/lib/libskia.so (SkRBuffer::readNoSizeCheck(void\*, unsigned int)+12)  

I/DEBUG (19397): #02 pc 000d60f3 /system/lib/libskia.so (SkRBufferWithSizeCheck::read(void\*, unsigned int)+34)  

I/DEBUG (19397): #03 pc 000fef7f /system/lib/libskia.so (SkRegion::readFromMemory(void const\*, unsigned int)+158)  

I/DEBUG (19397): #04 pc 00092241 /system/lib/libandroid\_runtime.so  

I/DEBUG (19397): #05 pc 0004697d /data/dalvik-cache/arm/system@framework@boot.oat  

I/DEBUG (19397):  

I/DEBUG (19397): Tombstone written to: /data/tombstones/tombstone\_03  

E/DEBUG (19397): unexpected waitpid response: n=19762, status=0000000b

**VERSION**  

Chrome Version: All  

Operating System: Android, I tested in 5.0, but all versions should be affected.

**REPRODUCTION CASE**  

Please refer to the attached PoC, a binary compiled from the PoC is attached too.

Please help to assign a CVE-ID to this issue.  

Thanks

## Attachments

- [pwn](attachments/pwn) (text/plain, 43.9 KB)
- [service.cpp](attachments/service.cpp) (application/octet-stream, 2.5 KB)

## Timeline

### in...@chromium.org (2015-05-06)

[Empty comment from Monorail migration]

### se...@chromium.org (2015-05-06)

[Empty comment from Monorail migration]

### ri...@google.com (2015-05-06)

Just checking, I don't see anything Android-specific, just that Guang has repro'd it on Android.

### ri...@google.com (2015-05-06)

Nevermind, on #3, I hadn't read closely enough.

### ri...@chromium.org (2015-05-06)

Thanks for the detailed report/PoC, Guang. Can anybody from Skia team confirm whether the vulnerable code is reachable from desktop chromium or not?

### hi...@gmail.com (2015-05-07)

Could you help to assign a CVE-ID to this issue.
BTW, I wonder whether this vulnerability qualify for Chrome Rewards :)

### su...@chromium.org (2015-05-07)

I looked at this quickly:

1) The only way to create an SkRegion over IPC would be to use SkValidatingReadBuffer::readRegion().
2) The only way to call this is to call SkAlphaThresholdFilterImpl::CreateProc().

So there is an SkRegion serialized in every SkAlphaThresholdFilter object.

### su...@chromium.org (2015-05-07)

Oh, sorry, but the SkAlphaThresholdFilter can't be serialized. Only filters declared in SkGlobalInitialization_chromium.cpp can be serialized and SkAlphaThresholdFilter isn't one of them.

### cl...@chromium.org (2015-05-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-11)

tracking bug - https://b.corp.google.com/u/0/issues/20883006

### [Deleted User] (2015-05-11)

From what I can tell we could also call readRegion if we called clipRegion on an SkCanvas from an SkPictureRecorder, which does not appear to happen anywhere.

So no, I do not see how this could be reachable from desktop Chromium.

### in...@chromium.org (2015-05-11)

We can close this chromium bug then. Is that reachable through android stack ? If yes, please fix as part of https://b.corp.google.com/u/0/issues/20883006.

### [Deleted User] (2015-05-11)

Yes. I'll follow up on the Android bug.

### hi...@gmail.com (2015-05-12)

[Comment Deleted]

### hi...@gmail.com (2015-05-12)

[Comment Deleted]

### ri...@chromium.org (2015-05-12)

Hi, according to http://www.google.com/about/appsecurity/chrome-rewards/, this should qualify if it affects Chrome on Android 4.4+. I expect a CVE would be assigned, but not sure who is in charge of doing this. Adding timwillis@ in case he might be familiar.

### hi...@gmail.com (2015-05-12)

Thanks for you reply ric....
Yes this vulnerability do affect chrome on Android 4.4+, include on the latest Android 5.1.
Hope someone can help me to answer my question.

### hi...@gmail.com (2015-05-12)

Is there an email address(such as security@chromium.org?) I can contact about chrome security vulnerability? 


### ri...@chromium.org (2015-05-12)

This is the correct place to file this and someone should reply with more details shortly. You can also contact us at that email.

### hi...@gmail.com (2015-05-12)

Thanks, ric...
one more question, when can i disclose it?

### ri...@chromium.org (2015-05-12)

Ah, I'm not as familiar about Chrome on Android's policies and update cycle. Perhaps riggle@ or timwillis@ might have a good answer about when a fix for this can be pushed.

### ti...@chromium.org (2015-05-12)

I'm adding the reward-topanel label so that this issue is considered under the reward program. We also determine during the reward panel meeting whether or not a bug is issued a CVE (based on the severity of the issue).

Answers to your other questions and more info here: http://www.google.com/about/appsecurity/chrome-rewards/index.html#faq

### hi...@gmail.com (2015-05-13)

If this issue is exploited successfully, it can break two layers of sandboxes. one is the sandbox of chrome and the other is the application sandbox in Android. It could be used to get system privilege directly from sandbox-ed render process. So, it should be a high severity vulnerability and I hope it deserve a CVE.

### [Deleted User] (2015-05-13)

[Empty comment from Monorail migration]

### hi...@gmail.com (2015-05-15)

[Comment Deleted]

### ti...@google.com (2015-05-16)

Our panel doesn't meet every week. I'll update as soon as we have a decision here.

### hi...@gmail.com (2015-05-25)

[Comment Deleted]

### ti...@google.com (2015-05-27)

This report is on the panel list for this week, which means that you should have a decision by late next week.

### hi...@gmail.com (2015-06-08)

Any update?

### [Deleted User] (2015-06-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-08)

[Empty comment from Monorail migration]

### hi...@gmail.com (2015-06-11)

Hi, is there any feedback? two weeks have passed. 

### ti...@google.com (2015-06-11)

We decided on a $3,000 reward for this bug, noting that although the issue wasn't in the Chrome codebase, it could manifest through Chrome. 

Reward panel notes: "$3,000 for wild copy. Higher amount would be provided if control of registers was demonstrated". 

Congratulations! Please note the terms and conditions below. You'll be contacted for payment details from someone in our finance team within two weeks.

Regarding the question on CVE, as discussed via email, this request should go through Android.

riggle@ - what's the process for an Android CVE? Does this issue meet the threshold?


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-06-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-25)

Starting payment process - you should hear from someone in our finance department within a week to collect your payment details.

### ti...@google.com (2015-06-25)

Merge requested for M-44 (branch 2403)

### pe...@google.com (2015-06-25)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@chromium.org (2015-06-26)

Could someone please verify what CL is being requested for merge?

### ti...@google.com (2015-07-01)

@reed: Is https://codereview.chromium.org/1143603003 the only CL that needs merging here? Grateful for your advice.

### ke...@google.com (2015-07-06)

Ping?

### dj...@chromium.org (2015-07-06)

The issue was how Chrome interacted with the Android framework. The bug was fixed in the framework and I'm not aware of any codepaths in Chromium that exercise this particular code so I don't think there is anything to merge.

### pe...@chromium.org (2015-07-07)

Ok, removing merge labels for now.

### hi...@gmail.com (2015-07-10)

The CVE is assigned to this issue by Android security team, which is CVE-2015-3849

### ti...@google.com (2015-08-04)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2015-08-17)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-26)

I've "undeleted" these attachments. If someone has good reason to delete them, please update the bug when you're deleting them so that we can easily track.

### ti...@google.com (2016-04-26)

#47:... where "these attachments" refer to the POC attached in the OP.

### hi...@gmail.com (2016-04-27)

ah, the attachments was deleted by me as I want to keep it secret for a short time, now it's OK for me .

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/484998?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082014)*
