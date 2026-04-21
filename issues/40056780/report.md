# Security: BigInt ToStringFormatter Crash 

| Field | Value |
|-------|-------|
| **Issue ID** | [40056780](https://issues.chromium.org/issues/40056780) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@yahoo.de |
| **Assignee** | jk...@chromium.org |
| **Created** | 2021-08-04 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Hello, I found this crash during fuzzing the current d8 version.

It crashes in this code line:  

<https://github.com/v8/v8/blob/master/src/bigint/tostring.cc#L441>

while (out != end) {  

\*(--out) = '0'; <--- here  

}

By slightly modifying the PoC a DCHECK can also be triggered instead of the crash in this line:  

<https://github.com/v8/v8/blob/master/src/objects/bigint.cc#L1068>

# Fatal error in ../../src/objects/bigint.cc, line 1068

# Debug check failed: chars[i] != bigint::kStringZapValue ('63' vs. '63').

**VERSION**  

I verified this crash in the latest v8 version (v8 9.4.0; commit hash: 185badc9122fe6274c1b2fe54e03fda5315cb80e)

I compiled it using:  

gn gen out/fuzzbuild --args='is\_debug=true dcheck\_always\_on=true v8\_static\_library=true v8\_enable\_slow\_dchecks=true v8\_enable\_v8\_checks=true v8\_enable\_verify\_heap=true v8\_enable\_verify\_csa=true v8\_fuzzilli=true v8\_enable\_verify\_predictable=true target\_cpu="x64"'

And I started d8 with:  

./d8 --expose-gc --single-threaded --predictable --allow-natives-syntax --interrupt-budget=1024 --fuzzing /path/to/crash.js

Please note: I also tested it in the current Chrome version and Chrome didn't crash.

**REPRODUCTION CASE**

eval('1000000000000000000000000000000000000000000000'.repeat(20)+'0n').toLocaleString();

The above PoC crashes d8. If you remove one of the zeros you can trigger the DCHECK instead:

eval('100000000000000000000000000000000000000000000'.repeat(20)+'0n').toLocaleString();

**CREDIT INFORMATION**  

Reporter credit: Rene Freingruber (@ReneFreingruber)

## Timeline

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-04)

Thanks for the report. 

I haven't been able to reproduce but jkummerow@ can you PTAL?

[Monorail components: Blink>JavaScript]

### jk...@chromium.org (2021-08-05)

Thanks for the report!

I can repro. Investigating.

### jk...@chromium.org (2021-08-05)

Turns out the two variants of the repro hit two separate bugs :-)

The first bug is a silly off-by-one: an integer division A/B is a no-op (i.e. result 0, remainder A) only if A is *strictly* less than B; the code erroneously used `<=` to check for applicability of this shortcut. This wrong condition later on causes the out-of-bounds write that causes the crash. I don't think that's a security issue, because (1) the written data is not controllable, it's always the '0' character, and (2) more importantly, the write happens with the loop mentioned in the report because `out` erroneously starts out beyond `end` already, so the `while (out != end)` condition never stops the loop until the process segfaults -- which makes it impossible to do anything nefarious with the corruption caused by the wild write.

The second bug is that there are three cases of returning early in that recursive function, and only one of them contained the logic to ensure that enough '0' characters have been written to fill in the entire range of the result string that the current recursive step is responsible for. This is what's causing the DCHECK failures about some characters of the result string never having been written. In Release mode, those characters would leak random bits that happened to previously be stored in those memory bytes. That's not dangerous per se, but could potentially be used as part of some other exploit that needs to find valid heap data for some reason. So to be extra careful, I'll leave this marked as a Security bug.

Fix: https://chromium-review.googlesource.com/c/v8/v8/+/3075365

Only Chrome M94 (currently on the Dev channel) is affected, no back merges required.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/dcc6bd76a9d8681b49f7aafd53cce315e74b7772

commit dcc6bd76a9d8681b49f7aafd53cce315e74b7772
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Fri Aug 06 11:21:38 2021

[bigint] Two more fixes for fast .toString()

Firstly, the fast path checking for applicability of the equality
"A/B = 0 with remainder A" must use the condition "A<B", not "A<=B".
Secondly, *all* early return paths must ensure that enough padding
'0' characters are written.

Fixed: chromium:1236694
Bug: v8:11515
Change-Id: I3fa7e17f5f3969ddbb5417b53abf3bff3fc1355b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3075365
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#76139}

[modify] https://crrev.com/dcc6bd76a9d8681b49f7aafd53cce315e74b7772/src/bigint/tostring.cc
[add] https://crrev.com/dcc6bd76a9d8681b49f7aafd53cce315e74b7772/test/mjsunit/harmony/bigint/regress-tostring-2.js


### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### sa...@google.com (2021-08-11)

FWIW I think the severity should be raised from Severity-Low. It's likely that a wild write could be exploited for RCE (see e.g. https://googleprojectzero.blogspot.com/2015/03/taming-wild-copy-parallel-thread.html and https://googleprojectzero.blogspot.com/2014/08/the-poisoned-nul-byte-2014-edition.html), especially given that in Chrome, the attacker effectively gets near unlimited attempts by spawning new renderer processes.

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Congratulations, Rene! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be contacting you soon to arrange payment. Thank you for this report and nice finding! 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-11-12)

This issue was migrated from crbug.com/chromium/1236694?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1236995]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056780)*
