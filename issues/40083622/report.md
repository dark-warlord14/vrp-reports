# Security: Buffer overflow in Brotli decompression

| Field | Value |
|-------|-------|
| **Issue ID** | [40083622](https://issues.chromium.org/issues/40083622) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebFonts |
| **CVE IDs** | CVE-2016-1624 |
| **Reporter** | lu...@yahoo.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2016-02-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

A heap-based buffer overflow in brotli decompression.  

We found the vulnerability while fuzzing with AFL.

**VERSION**  

Chrome Version: [48.0.2564.97] + [stable]  

Operating System: [Ubuntu 15.04]

**REPRODUCTION CASE**

Decompressing crash.compressed with Chrome's brotli (<https://src.chromium.org/viewvc/chrome/trunk/src/third_party/brotli/>)  

causes a segmentation fault. Decompressing crash.compressed with brotli source on GitHub (<https://github.com/google/brotli>) causes a segmentation fault. To deterministically reproduce the segfault, ASLR can be disabled. Even when ASLR is enabled, segfaults still occur with ~1/10 probability through repeated attempted decompressions. We are attaching two patch files for the brotli Github repo and the Chromium source.

Investigation on the segmentation fault show that it is caused by a heap-based buffer overflow. In decode.c:1755 (Chromium version, under the postSelfintersecting label), we write past the end of s->ringbuffer. For our test case, i is extremely large, causing pos to grow to a size much larger than s->ringbuffer\_size.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Brotli is already deployed on Chrome to decompress woff files and due to its impending larger rollout, we wanted to bring this to your attention as soon as possible. Currently, we have only caused crashes on the brotli library and command line tool, but we strongly believe this vulnerability can manifest in Chrome and we are working on an proof-of-concept. Let us know if you want more information.

Also, we noticed that Firefox uses brotli as well. Would it be ok to report this vulnerability to Mozilla?

## Attachments

- [crash.compressed](attachments/crash.compressed) (application/octet-stream, 20 B)
- [chromium-fix](attachments/chromium-fix) (text/plain, 373 B)
- [brotli-fix](attachments/brotli-fix) (text/plain, 399 B)

## Timeline

### ke...@chromium.org (2016-02-03)

CCing Tim to answer the question about reporting this vulnerability to Mozilla as well.

### ke...@chromium.org (2016-02-03)

Thanks for the report, I am sending this to the brotli owners to take a look. Meanwhile a crash report would be helpful if the original reporter can provide one.

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### ks...@chromium.org (2016-02-04)

Eugene, could you handle this?

### lu...@yahoo.com (2016-02-04)

We've been able to produce test cases that write past the end of the ringbuffer in Chromium, so we have very good reason to believe that this can lead to remote code execution. We have done this in Chromium built from the latest source. We'll try to get one that causes a crash soon.

Any updates on Firefox?

By the way, here is the commit that introduced the bug into brotli: https://github.com/google/brotli/commit/94cd7085f79a707f5ba3d93086796e695b495975

### eu...@chromium.org (2016-02-04)

Started investigation.

### eu...@chromium.org (2016-02-04)

We've found the actual problem. Proposed fix won't fix the problem.
Investigating further.

### eu...@chromium.org (2016-02-04)

We've got a proper fix. Going to create a Chromium patch soon.
It looks that we need to merge it to M49 also.

### lu...@yahoo.com (2016-02-04)

Thanks for the update Eugene, kudos to the Chrome team for a quick response!

Still looking for clarity about Firefox. Can we notify them? Their brotli decompression algorithm was branched after the bug was introduced, so they are similarly vulnerable.

### eu...@chromium.org (2016-02-04)

Fix in upstream: https://github.com/google/brotli/pull/309

CL (waiting for review): https://codereview.chromium.org/1662313002/

This bug was introduced in brotli upstream on 10 Aug 2015.
It was picked up to chrome on 07 Nov 2015 - revision 358538 (https://codereview.chromium.org/1411573011)

So M48-M50 has this issue.

### ks...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7716418a27d561ee295a99f11fd3865580748de2

commit 7716418a27d561ee295a99f11fd3865580748de2
Author: eustas <eustas@chromium.org>
Date: Fri Feb 05 03:17:46 2016

Cherry pick underflow fix.

BUG=583607

Review URL: https://codereview.chromium.org/1662313002

Cr-Commit-Position: refs/heads/master@{#373736}

[modify] http://crrev.com/7716418a27d561ee295a99f11fd3865580748de2/third_party/brotli/README.chromium
[modify] http://crrev.com/7716418a27d561ee295a99f11fd3865580748de2/third_party/brotli/dec/decode.c


### eu...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-02-05)

This issue can happen only if certain malloc (ringbuffer) returns address less than 0x1000845 (~16MiB). Is it possible in browser environment?

### cl...@chromium.org (2016-02-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### eu...@chromium.org (2016-02-05)

If process has standard memory layout (0 - Text - Data - Heap - Free Space - Stack - Kernel), then malloc result is never less than Text + Data. For big enough binaries this would mean impossibility to cause this issue.

### cl...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-05)

Merge approved for M48 (branch 2564). Pls merge asap - by 4pm this Fri to catch up with next stable refresh. Thanks.

### eu...@chromium.org (2016-02-05)

4PM PST, I hope?

### eu...@chromium.org (2016-02-05)

Merge CL to M48: https://codereview.chromium.org/1672793002/

### go...@chromium.org (2016-02-05)

Reply to #19, Yes, by 4:00 PM PST.

### eu...@chromium.org (2016-02-05)

Waiting for LGTM. Supposedly any committer's LGTM will be enough.

### eu...@chromium.org (2016-02-05)

CQ responds with "Failed to commit the patch."
Need help!

### th...@chromium.org (2016-02-05)

Do we have a bug somewhere to write a fuzzer for brotli?

### eu...@chromium.org (2016-02-05)

Yes: https://code.google.com/p/chromium/issues/detail?id=530417

Unfortunatelly, libfuzzer can't detect this problem (due to memory allocation patterns).

### kc...@chromium.org (2016-02-05)

eustas, can you tell more? 
do you mean that asan can not find this problem because the underflow happens within
the same heap memory region? 
Is it possible to use asan annotations in the brotli code to be able to find this bug? 

I would very much want to see a target function for fuzzing that is able to detect this bug with asan. 


### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/117526af102e81e910bb2005b3ba7bac9d4b7265

commit 117526af102e81e910bb2005b3ba7bac9d4b7265
Author: eustas <eustas@chromium.org>
Date: Fri Feb 05 21:40:19 2016

Cherry pick underflow fix.

BUG=583607

Review URL: https://codereview.chromium.org/1662313002

Cr-Commit-Position: refs/heads/master@{#373736}
(cherry picked from commit 7716418a27d561ee295a99f11fd3865580748de2)

NOTRY=true
NOPRESUBMIT=true
TBR=ksakamoto@chromium.org

Review URL: https://codereview.chromium.org/1672793002

Cr-Commit-Position: refs/branch-heads/2564@{#677}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/117526af102e81e910bb2005b3ba7bac9d4b7265/third_party/brotli/README.chromium
[modify] http://crrev.com/117526af102e81e910bb2005b3ba7bac9d4b7265/third_party/brotli/dec/decode.c


### eu...@chromium.org (2016-02-05)

This issue can happen only if certain malloc (ringbuffer) returns address less than 0x1000845 (~16MiB).
My guess is that libfuzzer either generates large binary (Text + Data > 16 MiB) or allocates large picese of memory before running test.

AFL, perhaps, uses different approach -> finds the bug

### in...@chromium.org (2016-02-05)

Did you seed the corpus in AFL ? Or you started with an empty one ?

### kc...@chromium.org (2016-02-05)

libfuzzer does not allocate memory, asan does. 
what's the ringbuffer in this case? 

### lu...@yahoo.com (2016-02-05)

We agree with eustas's assessment. Large text/data sections push the location of the heap higher, so underflow does not occur. When running AFL with a -fsanitize build, the bug is never triggered. Similarly, the bug is never triggered when running with valgrind, as the ringbuffer has too high of a memory address.

### lu...@yahoo.com (2016-02-05)

In the same vein, underflow may not occur depending on the location of the start of the heap due to ASLR (if s->ringbuffer has too high of a memory address)

### lu...@yahoo.com (2016-02-05)

We (the original issue authors) seeded AFL using testcases in brotli/testcases/tests, using the 4 smallest files and truncating random_chunks to 30 bytes

### in...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### kc...@chromium.org (2016-02-05)

Also, could someone post the exact reproduction steps? 
This is what I did, and got no crash: 

git clone https://github.com/google/brotli.git
cd brotli/tools/
make -j 
setarch x86_64 -R  ./bro --decompress --input  ~/Downloads/crash.compressed  > /dev/null 
corrupt input


### lu...@yahoo.com (2016-02-05)

@kcc, ASLR should be turned off to reproduce reliably, otherwise it is only triggered when heap offset is low enough to cause underflow

### kc...@chromium.org (2016-02-05)

scratch that, I needed to undo the fix. 
Now I can see the crash. 

### bu...@chromium.org (2016-02-06)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/117526af102e81e910bb2005b3ba7bac9d4b7265

commit 117526af102e81e910bb2005b3ba7bac9d4b7265
Author: eustas <eustas@chromium.org>
Date: Fri Feb 05 21:40:19 2016


### ti...@google.com (2016-02-06)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ti...@google.com (2016-02-08)

Sorry for the delay - I was travelling! By all means report the issue to Mozilla, but please make sure you follow their published security bug submission process so that it's handled appropriately.

@tinazh - can you please approve for M49 as well? Want to make sure we land this now to M49 as it's already on M48. 

### eu...@chromium.org (2016-02-08)

Still waiting for Merge-Approved-49 flag.

### ti...@google.com (2016-02-08)

#40, s/tinazh/sshruthi/g

sshruthi@ - can you please approve for M49?

### ss...@google.com (2016-02-08)

Merge approved for M49 (branch 2623)

### eu...@chromium.org (2016-02-08)

CL: https://codereview.chromium.org/1676323002/
Needs committer LGTM to land.

### in...@chromium.org (2016-02-08)

There is no cq for merge branch. Oliver, can you land c#44.

### bu...@chromium.org (2016-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e10d1d07fe7c3ac81977033d40261d65319686d6

commit e10d1d07fe7c3ac81977033d40261d65319686d6
Author: eustas <eustas@chromium.org>
Date: Mon Feb 08 17:41:04 2016

Cherry pick underflow fix.

BUG=583607

Review URL: https://codereview.chromium.org/1662313002

Cr-Commit-Position: refs/heads/master@{#373736}
(cherry picked from commit 7716418a27d561ee295a99f11fd3865580748de2)

NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1676323002

Cr-Commit-Position: refs/branch-heads/2623@{#295}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/e10d1d07fe7c3ac81977033d40261d65319686d6/third_party/brotli/README.chromium
[modify] http://crrev.com/e10d1d07fe7c3ac81977033d40261d65319686d6/third_party/brotli/dec/decode.c


### bu...@chromium.org (2016-02-08)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/e10d1d07fe7c3ac81977033d40261d65319686d6

commit e10d1d07fe7c3ac81977033d40261d65319686d6
Author: eustas <eustas@chromium.org>
Date: Mon Feb 08 17:41:04 2016


### md...@chromium.org (2016-02-08)

"p < (const char *)0 + i" is undefined behavior per ISO C.  Is it possible to detect this overflow some other way?

### kc...@chromium.org (2016-02-08)

Not trivial. 
We considered this checker and even had a prototype, but it was quite hard to use
and noisy. https://llvm.org/bugs/show_bug.cgi?id=18989

### ri...@chromium.org (2016-02-09)

Perhaps we could check that copy_len (i) is in [0, s->ringbuffer_size] instead (or is it intentional that i can be outside of this range)?

Then checks can look like (with checks for overflow if needed):

if (pos + copy_len > s->ringbuffer_size)

and

if (src_pos + copy_len > s->ringbuffer_size)

### ri...@chromium.org (2016-02-09)

Oops, actually:

if (pos > s->ringbuffer_size - copy_len)

and similar avoids the possibility of overflow for free (assuming copy_len is validated above).

### eu...@chromium.org (2016-02-09)

It is legal for copy_len to be large. pos is unrelated.
ringbuffer_end_minus_copy_length is a "guard" value to switch between fast execution path and slow one.

### eu...@chromium.org (2016-02-09)

In upstream we've developed more ISO compatible fix. Will publish in GitHub soon and then pull to Chromium.

### ti...@google.com (2016-02-09)

Hey lukezli,

Thanks again for your report! The fix is shipping in a patch release of chrome (likely later today) and you'll be credited in our release notes as "lukezli". Please let me know if you want me to update the credit name to something else. 

The CVE ID for your report is CVE-2016-1624

We took your report to our reward panel and couldn't decide if this meets the threshold for a monetary reward. Considering c#16 above and some comments from the panel, we couldn't immediately determine how this bug could be used in a practical attack. If you can think of a way this bug could be used in practice, please let us know! 

If you can't see a way this could be used in practice, that's fine as well - we just wanted to give you an opportunity to present another angle we might not be considering before making a determination at the reward panel.

Tim

### lu...@yahoo.com (2016-02-09)

Hi Tim,

Can you change the credit name to reflect my collaborator, "Luke Li and Jonathan Metzman"? A change in the CVE notes to this would be great as well.

Re: use of the bug in a practical attack:

The underflow is definitely a vulnerability in brotli (which Google does develop). So for people running brotli independently (e.g. the command line tool), its definitely actionable, although I understand that the reward consideration is for Chrome. We've run up against the 16MB limitation too (e.g. the heap address of the ringbuffer needs to be below ~2^16 ish to cause the underflow), a fair point. I'm guessing none of Chrome's products (32 bit browser, Android, iOS) would have binaries of smaller size?

Another point is that the 2^24 limitation for the underflow isn't an enforcement from C (the operand causing the underflow, i, is presumably 32 bits), but rather an invariant brotli claims to enforce. While it seems like this invariant is respected, theoretically a bug in that enforcement could be chained with this underflow to cause a practical attack in Chrome, since 2^32 is a lot bigger (particularly in 32 bit browsers).

I'd also like to note that Chrome does seem to decode (and in fact display) 9MB worth of I's with the input I provided you guys (even in the patched brotli), even though the input is still malformed (e.g. if its run from the command line, brotli will print out 9MB of I's followed by a "corrupt input" to stderr. Is the expected behavior to decode/display a partially decoded file even if the file is malformed?

In general, I do want to note that it doesn't seem apparent to us to how to use this bug functionally in Chrome for an exploit (although anyone using the library with a smaller binary could be relatively easily exploited via the resulting buffer overflow). We found it pretty fascinating regardless, particularly since the use of ASan in fact hid a memory bug, presumably why Google's army of fuzzers didn't find this before. Will Google additionally try fuzzing without ASan in the future to catch bugs like these?

Thanks for the quick fix and consideration from Google. Let me know if the reward panel deems it eligible for a reward!



### lu...@yahoo.com (2016-02-09)

Sorry, a typo: I meant to say

(e.g. the heap address of the ringbuffer needs to be below ~2^24 ish to cause the underflow)

### eu...@chromium.org (2016-02-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

Thanks for the additional comments Luke - I'll take your additional comments back through the panel. There's no doubt that there's a bug here and we fixed it, though the fact that it's not apparent on how you could use this as a functional exploit in chrome will likely play a significant factor in the decision to reward. 

I should have an answer for you later this week. Feel free to ping me if you don't hear back.

Also in case you didn't notice, the credit name is now updated to Luke Li and Jonathan Metzman: https://googlechromereleases.blogspot.com/2016/02/stable-channel-update_9.html

### lu...@yahoo.com (2016-03-10)

Thanks for the update Tim. I'm wondering if the reward panel has come to a conclusion yet? Also, would it be ok to write about this bug?

### sh...@chromium.org (2016-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

#59 - my apologies for the long delay here. There were bugs in some older releases that kept getting cut off the reward panel agenda. We've now cleared out the backlog, so thanks for your patience.

We decided to award you $1,000 for this report. Congratulations!

Our finance team should be in touch within 7 days. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!

### aw...@chromium.org (2016-07-01)

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/583607?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/539572]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083622)*
