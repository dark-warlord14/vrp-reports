# SPAKE password-scalar not multiplied by 8

| Field | Value |
|-------|-------|
| **Issue ID** | [40089401](https://issues.chromium.org/issues/40089401) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gh...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2017-10-25 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

The M and N constants used by the BoringSSL SPAKE code (crypto/curve25519/spake25519.c) do not appear to be in the prime-order subgroup of the generator:

$ python -i ed25519.py 
>>> N = decodepoint('10e3df0ae37d8e7a99b5fe74b44672103dbddcbd06af680d71329a11693bc778'.decode('hex'))
>>> M = decodepoint('5ada7e4bf6ddd9adb6626d32131c6b5c51a1e347a3478f53cfcf441b88eed12e'.decode('hex'))
>>> scalarmult(N, l) == [0, 1]
False
>>> scalarmult(N, 2 * l) == [0, 1]
False
>>> scalarmult(N, 4 * l) == [0, 1]
False
>>> scalarmult(N, 8 * l) == [0, 1]
True
>>> scalarmult(M, l) == [0, 1]
False
>>> scalarmult(M, 2 * l) == [0, 1]
True

As a result, the order of the points used in protocol messages will depend on the low-order bits of SHA512(password).  An attacker could use that information to filter password candidates by a factor of 8 before conducting an online password attack.  That's not a very interesting attack, but there might be other ramifications which I'm not aware of, so I'm going through the security reporting channel for now.  At some point soon I will want to talk about replacing the M and N values in draft-ietf-kitten-krb-spake-preauth on the kitten list, which will make this issue more public.

After modifying the Python code (currently misformatted after the comment conversion, incidentally; the first few lines were converted to // comments and the rest is in a /* */ block comment) to check the point order, I get:

N = d3bfb518f44f3430f29d0c92af503865a1ed3281dc69b35dd868ba85f886c4ab
M = d048032c6ea0b6d697ddc2e86bda85a33adac920f1bf18e1b0c6d166a5cecdaf

after 7 iterations for N and 21 iterations for M.  Changing to these values is obviously an incompatible protocol change.

VERSION

All Chromium versions which use the SPAKE code.

REPRODUCTION CASE

n/a

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

n/a

## Timeline

### el...@chromium.org (2017-10-25)

[Empty comment from Monorail migration]

### da...@chromium.org (2017-10-25)

I believe the only consumer of this is Chromoting. I'm not familiar with the SPAKE stuff. Adam?

[Monorail components: Services>Chromoting]

### ag...@chromium.org (2017-10-26)

Thank you for this.

The issue isn't with the order of the points, it's that I missed left_shift_3 after reducing the password-scalar. It's included after reducing the ephemeral scalar, where it's less obviously needed, but then I missed it in the obvious case :(

That is quite an embarrassing screw up.

Thankfully, for Chromoting, the SPAKE messages are carried within TLS and you have to have sharing permissions in order to even be able to exchange them, I believe. So the impact is limited.

The correct fix would be to add the missing left-shift, but that would be incompatible and thus hard to deploy rapidly.

I think that I have a unilateral fix though, although I'll sit on it for a couple of days and see whether I can find a problem:

The ephemeral scalar *does* have the left-shift, so is a multiple of 8. Thus if we add $l$ (where $l$ is the order of the prime-order subgroup) to the password scalar, the other party will calculate

xB + (p+l)N + -pN = xB + lN

(where $x$ is Alice's ephemeral scalar and $p$ is her password-scalar)

Then, when Bob does the scalar-mult:

y(xB + lN) = xyB + ylN = xyB (because y is a multiple of 8 and adding 8*l of any point is a no-op)
 
So the resulting shared secret will be the same.

Since $l$ is prime, the LSB is 1. Thus we can add $l$ to clear the LSB of the password scalar, 2*l to clear the next bit, and 4*l to clear another bit. Thus the password scalar will be a multiple of eight, as required, without breaking anything.

As for whether the points should be in the prime-order subgroup: I didn't bother and instead decided(/failed) to clear the subgroup. Having N and M be in the prime-order subgroup slightly complicates the generation but doesn't eliminate all cofactor considerations because the peer can still send a point outside of that subgroup.

Failing to clear the subgroup would have been immediately obvious had there been any test vectors (i.e. it can't be a subtle error), but there were no other implementations to test against at the time. (Of course, I should have done a model in Python or such but hindsight is, as ever, 20/20.)

### gh...@gmail.com (2017-10-27)

> Having N and M be in the prime-order subgroup slightly complicates the generation but doesn't eliminate all cofactor considerations because the peer can still send a point outside of that subgroup.

I don't follow.  I'm going to calculate y(T-wM) (for Bob).  If T is outside of the subgroup, T-wM will also be outside of the subgroup, whether or not w is a multiple of 8.  However, as long as y is a multiple of 8, y(T-wM) will be in the subgroup.  So if M and N are in the subgroup, I'm missing the reason to force w to be a multiple of the cofactor, though I do see a reason to force x and y to be.

### ag...@chromium.org (2017-10-27)

I think you're correct in all the above:

There's nothing wrong with tweaking the point generation to put N and M in the prime-order subgroup. I didn't because:

a) it's not the case that you can ignore the co-factor in the rest of the protocol by doing that because you still need to consider the case where T is outside the subgroup. One can argue about whether x and y need to be multiples of eight but I eventually decided that SPAKE2 should follow X25519 here. So one needs the left_shift_3 function anyway so it's easy to do that with the password hash too. (Unless you copy-paste one line too few and skip it, of course.)

b) This was done during the time when the IETF was discussing what lead to https://tools.ietf.org/html/rfc7748 which involved an exhausting debate over every tiny point of curve-picking algorithms and whether we were all secret NSA agents seeking to backdoor standards. Thus adding complexity to the point-generation function seemed likely to spur more of that.

c) this isn't a subtle error: failing to multiply the password scalar leads to interop failure. Thus, in a wider ecosystem we wouldn't expect it to be a bigger problem than, say, transcribing the N and M points incorrectly or something.

I can see a counter argument that it's worth publishing point-picking algorithms that integrate the cofactor directly because people might use them on other curves and having an input called "cofactor" will make them think whilst they might otherwise just duplicate the "multiply by 8" in the code. I don't have strong feelings about it and was mostly worried about (b) at the time.

### ag...@chromium.org (2017-10-27)

(p.s. looks like https://tools.ietf.org/html/draft-irtf-cfrg-spake2-04 picked up putting M and N in the prime-order subgroup along the way. Although that draft seems to have languished, unifying with it still seems like a decent idea for other protocols.)

### mb...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-31)

The following revision refers to this bug:
  https://boringssl.googlesource.com/boringssl/+/696c13bd6ab78011adfe7b775519c8b7cc82b604

commit 696c13bd6ab78011adfe7b775519c8b7cc82b604
Author: Adam Langley <agl@google.com>
Date: Tue Oct 31 20:58:29 2017

Clear bottom three bits of password scalar in SPAKE2.

Due to a copy-paste error, the call to |left_shift_3| is missing after
reducing the password scalar in SPAKE2. This means that three bits of
the password leak in Alice's message. (Two in Bob's message as the point
N happens to have order 4l, not 8l.)

The “correct” fix is to put in the missing call to |left_shift_3|, but
that would be a breaking change. In order to fix this in a unilateral
way, we add points of small order to the masking point to bring it into
prime-order subgroup.

BUG=chromium:778101

Change-Id: I440931a3df7f009b324d2a3e3af2d893a101804f
Reviewed-on: https://boringssl-review.googlesource.com/22445
Reviewed-by: Adam Langley <agl@google.com>
Reviewed-by: David Benjamin <davidben@google.com>
Commit-Queue: Adam Langley <agl@google.com>
CQ-Verified: CQ bot account: commit-bot@chromium.org <commit-bot@chromium.org>

[modify] https://crrev.com/696c13bd6ab78011adfe7b775519c8b7cc82b604/crypto/curve25519/spake25519_test.cc
[modify] https://crrev.com/696c13bd6ab78011adfe7b775519c8b7cc82b604/crypto/curve25519/spake25519.c
[modify] https://crrev.com/696c13bd6ab78011adfe7b775519c8b7cc82b604/crypto/curve25519/internal.h


### ag...@chromium.org (2017-10-31)

(Will let this fix proof in the tree for about a week before starting merges.)

### ag...@chromium.org (2017-10-31)

(And the timer doesn't start until another change rolls BoringSSL into Chromium.)

### bu...@chromium.org (2017-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2

commit a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2
Author: Adam Langley <agl@chromium.org>
Date: Fri Nov 03 15:08:25 2017

Roll src/third_party/boringssl/src 664e99a64..696c13bd6

https://boringssl.googlesource.com/boringssl/+log/664e99a6486c293728097c661332f92bf2d847c6..696c13bd6ab78011adfe7b775519c8b7cc82b604

BUG=778101

Change-Id: I8dda4f3db952597148e3c7937319584698d00e1c
Reviewed-on: https://chromium-review.googlesource.com/747941
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: David Benjamin <davidben@chromium.org>
Commit-Queue: Steven Valdez <svaldez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#513774}
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/DEPS
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/content/browser/browser_main_loop.cc
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/content/public/common/content_features.cc
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/content/public/common/content_features.h
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/content/renderer/render_thread_impl.cc
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/third_party/boringssl/BUILD.generated.gni
[modify] https://crrev.com/a263d1cf62a9c75be6aaafdec88aacfcef1e8fd2/third_party/boringssl/BUILD.generated_tests.gni


### ag...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-10)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-11-10)

+awhalley@ for M63 merge revivew

### go...@chromium.org (2017-11-10)

Also pls apply appropriate milestone labels. Adding M63 per https://crbug.com/chromium/778101#c13 for now.

### sh...@chromium.org (2017-11-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-11-12)

govind@ - good for 63 (for a cherrypick of the SPAKE2 changes in #9, rather than the full roll in #12)

### sh...@chromium.org (2017-11-12)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-11-13)

Approving merge for cl listed at #9 to M63 branch 3239 based on https://crbug.com/chromium/778101#c18.

Cl listed at #12 is not approved for merge per https://crbug.com/chromium/778101#c18.

### sh...@chromium.org (2017-11-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-11-16)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/cab9ce4c11edf393672dfed492deed665dca9015

commit cab9ce4c11edf393672dfed492deed665dca9015
Author: Adam Langley <agl@google.com>
Date: Thu Nov 16 18:20:46 2017


### go...@chromium.org (2017-11-16)

Please merge your change to M63 branch 3239 by 4:00 PM PT, tomorrow (Friday) so we can pick it up for next week Beta release. Thank you.

### aw...@google.com (2017-11-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-11-16)

Thanks for the report, ghudson@! The Chrome VRP panel decided to award $500 for this. A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

+ghudson@gmail.com - please claim your reward by 1/31/2020. Otherwise it will be donated to charity. 

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-04)

Processing this as a donation 

### is...@google.com (2020-02-04)

This issue was migrated from crbug.com/chromium/778101?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089401)*
