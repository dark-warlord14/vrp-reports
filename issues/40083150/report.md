# window.crypto.getRandomValues() uses a weak CSPRNG

| Field | Value |
|-------|-------|
| **Issue ID** | [40083150](https://issues.chromium.org/issues/40083150) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL |
| **CVE IDs** | CVE-2016-1618 |
| **Reporter** | aa...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2015-11-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36

Steps to reproduce the problem:
window.crypto.getRandomValues() is no longer a "cryptographically strong" pseudorandom number generator.

What is the expected behavior?

What went wrong?
The cryptographic primitive that window.crypto.getRandomValues() is based on is no longer secure.  It is using the OpenBSD implementation of RC4 called Arc4. See https://chromium.googlesource.com/chromium/blink/+/master/Source/wtf/CryptographicallyRandomNumber.cpp. RC4 is no longer considered secure, and as such, window.crypto.getRandomValues() can no longer be considered a "cryptographically strong" pseudorandom number generator. See analysis of RC4 at:

* https://en.wikipedia.org/wiki/RC4#Security
* https://www.usenix.org/conference/usenixsecurity13/technical-sessions/paper/alFardan
* http://www.imperva.com/docs/hii_attacking_ssl_when_using_rc4.pdf
* http://www.securityweek.com/new-attack-rc4-based-ssltls-leverages-13-year-old-vulnerability
* http://www.infoworld.com/article/2979527/security/google-mozilla-microsoft-browsers-dump-rc4-encryption.html
* https://www.schneier.com/blog/archives/2015/07/new_rc4_attack_1.html
* etc.

The TLSv1.3 draft will also drop RC4 negotiation entirely. See https://tools.ietf.org/html/draft-ietf-tls-tls13-10.

Many of those issues have to do with TLS, of which window.crypto.getRandomValues() does not depend on, but the attacks are generic enough, that they are still applicable here. RC4, and thus arc4random, is no longer secure.

OpenBSD dropped arc4random for its kernel-space CSPRNG and implemented ChaCha20 (which is in BoringSSL, LibreSSL, and proposed for the stream cipher in TLSv1.3). See http://cvsweb.openbsd.org/cgi-bin/cvsweb/src/lib/libc/crypt/arc4random.c revision 1.25. It seems like a direct replacement of arc4random with ChaCha20 would also be applicable here.

Firefox seems to be reading from the operating system's CSPRNG directly. That could be another alternative. GNU/Linux uses SHA-1, Mac OS X uses Yarrow, and Windows uses AES-CTR:

* https://github.com/torvalds/linux/blob/master/drivers/char/random.c
* https://opensource.apple.com/source/xnu/xnu-1456.1.26/bsd/dev/random/
* https://msdn.microsoft.com/en-us/library/windows/desktop/aa375534(v=vs.85).aspx#BCRYPT_RNG_ALGORITHM

Did this work before? N/A 

Chrome version: 46.0.2490.71  Channel: stable
OS Version: Debian Sid
Flash Version: Shockwave Flash 18.0 r0

## Timeline

### in...@chromium.org (2015-11-08)

Ryan, can you please help to triage this.

### sl...@google.com (2015-11-08)

[Empty comment from Monorail migration]

### er...@chromium.org (2015-11-08)

I expect we can use BoringSSL's RAND_bytes() directly here.

I'll dig into this next week, but I believe RAND_bytes() basically reads from urand, and should be safe to use for this purpose. In fact if there is concern with it exhausting entropy we already have a problem since RAND_bytes() it is already being exposed via WebCrypto's key generation...

### in...@chromium.org (2015-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-11-09)

[Empty comment from Monorail migration]

### ag...@chromium.org (2015-11-09)

third_party/WebKit/Source/modules/crypto/Crypto.cpp makes me think that the report might be valid. Even if not, that RC4 code is used, for example to create MIME boundaries in WebKit. It should just call RAND_bytes so that we don't need to worry about it.

### aa...@gmail.com (2015-11-09)

If I'm understanding correctly, does RAND_bytes in BoringSSL read from the system CSPRNG directly? Would window.crypto.getRandomValues() use RAND_bytes as the generator then?

### aa...@gmail.com (2015-11-09)

In fact, more importantly, if RAND_bytes() in BoringSSL uses the operating system's CSPRNG, and that isn't available, what does RAND_bytes() fall back on for a cryptographic generator?

### da...@chromium.org (2015-11-09)

https://crbug.com/chromium/552749#c7: Looks like that code calls into here:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/wtf/CryptographicallyRandomNumber.cpp&sq=package:chromium&type=cs&l=180&rcl=1447072180
Which does call into ARC4RandomNumberGenerator.

https://crbug.com/chromium/552749#c9: It doesn't fallback. If the system one doesn't work, it aborts. I don't think I've ever seen a crash report from this.

I think what we'd want is just to delete everything in that file and call sourceFunction directly. This,in non-test code, points to Blink's Platform::cryptographicallyRandomValues which, in Chromium, routes to base::RandBytes[*]. That, like BoringSSL[**], reads from the system CSPRNG and aborts on failure.

[*] That is documented to not be okay, but actually is. There's crypto::RandBytes which just calls base::RandBytes. But we should switch that call to crypto::RandBytes per this comment:
https://code.google.com/p/chromium/codesearch#chromium/src/crypto/random.cc&l=11

[**] BoringSSL also has an RDRAND + system mode which is used when RDRAND is available which this doesn't have. Still similarly requires that the system CSPRNG not fail though.

### er...@chromium.org (2015-11-10)

My initial benchmarking (on Linux) suggests that removing the ARC4 PNRG and just consuming crypto::RandBytes() directly results in about a 5x slowdown for generating random bytes (measured by generating 256 MB of random data, 256 bytes at a time).

Provided this doesn't regress any of our benchmarks, I will pursue this approach:

https://codereview.chromium.org/1419293005/
https://codereview.chromium.org/1431233002/

### aa...@gmail.com (2015-11-10)

Would dropping in ChaCha20 in place of RC4 be a better performer?

### da...@chromium.org (2015-11-10)

I don't think we need to be worried about the performance of this microbenchmark. If we did care, we could resolve the silly layering concerns between crypto::RandBytes and base::RandBytes using BoringSSL's RAND_bytes. BoringSSL has some modes which are slightly cleverer than /dev/urandom, but those weren't added for Chrome anyway.

### rs...@chromium.org (2015-11-10)

No problems using RAND_bytes

(For a separate bug) We can also remove crypto::RandBytes now that we're clearer on where the direction of FIPS is going.

### bu...@chromium.org (2015-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9224aa4826d29930a8194a58dfd7170411bfc672

commit 9224aa4826d29930a8194a58dfd7170411bfc672
Author: eroman <eroman@chromium.org>
Date: Tue Nov 10 07:43:35 2015

Remove blink's use of RC4 for random value generation.

This re-implements Blink's random number generator (wtf::cryptographicallyRandomValues) in terms of calling crypto::RandomBytes() directly, rather than using an ARC4 keystream that periodically stirs in system randomness.

Reason: RC4 (ARC4) has known weaknesses and has already been disabled as an accepted TLS cipher for Chrome M48. It should not be used internally for generating random numbers in Blink.

The way cryptographically random number generation worked in Blink prior to this patch is that wtf::cryptographicallyRandomValues() would generate random bytes using an ARC4 keystream. Every 1.6MB of generated data it would stir in randomness obtained via Platform::current()->cryptographicallyRandomValues().

The way it works after this patchset is that wtf::cryptographicallyRandomValues() directly calls Platform::current()->cryptographicallyRandomValues(), without layering on its own PRNG. The concrete implementation of Platform::cryptographicallyRandomValues() now calls crypto::RandBytes() [1], which provides good cryptographically secure random numbers by reading from hardware/system randomness sources.

The consequences of this change are:

 * The fixed sequence of random numbers seen by certain tests will have changed. I haven't observed this to be a problem with any of the tests though.

 * The performance characteristics of cryptographicallyRandomValues() have changed, for the worse. Measured using a microbenchmark, window.crypto.getRandomValues() is almost 5x slower now. This is not all that surprising since RC4 was pretty fast, and was only mixing in system randomness every 1.6MB (my test generated 256MB).

[1] Technically it is calling base::RandBytes(), but under the hood that calls crypto::RandBytes(). Will fix that dependency separately.

BUG=552749

Review URL: https://codereview.chromium.org/1431233002

Cr-Commit-Position: refs/heads/master@{#358803}

[modify] http://crrev.com/9224aa4826d29930a8194a58dfd7170411bfc672/third_party/WebKit/Source/wtf/CryptographicallyRandomNumber.cpp


### er...@chromium.org (2015-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d151e09e13a704e9738ea913d117df7282e6c7d

commit 0d151e09e13a704e9738ea913d117df7282e6c7d
Author: eroman <eroman@chromium.org>
Date: Thu Nov 12 03:18:08 2015

Add assertions that the empty Platform::cryptographicallyRandomValues() overrides are not being used.

These implementations are not safe and look scary if not accompanied by an assertion. Also one of the comments was incorrect.

BUG=552749

Review URL: https://codereview.chromium.org/1419293005

Cr-Commit-Position: refs/heads/master@{#359229}

[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/components/test_runner/test_common.cc
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/media/blink/run_all_unittests.cc
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/core/dom/ScriptRunnerTest.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/core/fetch/CachingCorrectnessTest.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/platform/TestingPlatformSupport.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/platform/fonts/FontCacheTest.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/platform/graphics/RecordingImageBufferSurfaceTest.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/platform/heap/RunAllTests.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/platform/weborigin/OriginAccessEntryTest.cpp
[modify] http://crrev.com/0d151e09e13a704e9738ea913d117df7282e6c7d/third_party/WebKit/Source/web/ImageDecodeBench.cpp


### ti...@google.com (2015-11-23)

I'm assuming that we want this change to bake and go with M48. Please update if you want this to be considered for a patch release for M47 (remove Merge-NA and Release-0-M48 labels, then add Merge-Request-47).

### er...@chromium.org (2015-11-23)

Correct. My intent is to:

 * Merge the fix to M48 (next-next stable, which just branched last week)
 * Don't do anything for M46 (current stable) or M47 (current beta)

Justification below.

------------------
Patch to merge
------------------

https://chromium.googlesource.com/chromium/src.git/+/9224aa4826d29930a8194a58dfd7170411bfc672

------------------
Risks of the bugfix (low)
------------------

Pro:
 * The code change is small and simple
 * Has been on the three dev-channel releases already
 * No obvious crashes from it
 * Haven't received any user/developer bug reports about it (but to be fair, it is unlikely these will be noticed until it hits beta/stable)
 * The same mechanism has been used by crypto.generateKey() for a long time (order of years), so is fairly well tested code.

Con:
 * The performance of cryptographicallyRandomValues() has been reduced by as much as 5x (when measured on Linux).

... So the main concern is a risk of performance regression on particular pages, that are heavy consumers of randomness.

I haven't observed any regressions on top-level page load metrics. But it is possible to construct pages that have heavy usage of window.crypto.getRandomValues() by generating many bytes of random values. For such pages there could be a user-visible slowdown.

As an upper bound, according to https://www.chromestatus.com/metrics/feature/popularity#CryptoGetRandomValues window.crypto.getRandomValues(), is used on 9.7% of page loads. This doesn't measure though whether random number generation is on the critical path, or if they generate enough random bytes to become slow. My expectation is these top consumers are generating only small amounts of randomness and hence will not be impacted by the slowdown.

Lastly, (I believe) Firefox is using a comparably slow random number generation.

------------------
Risks of not fixing the bug on M46/M47
------------------

I am not a crypto expert, but my understanding is the issue here is known bias in the RC4 keystream.

Chrome 46 and Chrome 47 currently accept RC4 as a valid TLS cipher (albeit de-prioritized), with a plan to kill RC4 in TLS for Chrome 48 [1]

Given that RC4 is "good-enough" for us to allow on stable and beta for TLS, it is congruent  that we similarly kill it in cryptographicallyRandomValues() for M48.

[1] https://groups.google.com/a/chromium.org/forum/#!msg/security-dev/kVfCywocUO8/vgi_rQuhKgAJ

### rs...@chromium.org (2015-11-23)

And as for threat model:

This doesn't affect .generateKey() or the .deriveKey()/.deriveBits() APIs of Web Crypto, which still use strong sources of entropy (RAND_bytes, which is either urandom or urandom + RDRAND + ChaCha20). So the primary affect would be polyfilled crypto algorithms, which have a much more complicated security story anyways.

### ti...@google.com (2015-11-23)

[Automated comment] Commit may have occurred before M48 branch point (11/13/2015), needs manual review.

### ti...@google.com (2015-11-23)

Thanks for the detail and the threat model - M48 SGTM. 

By my reading, the patches in #18 and #20 landed as r358803, which was before the M48 branch point (hence why I labelled as Merge-NA as the fix is already in M48). That said, no harm in tinazh@ double checking here.

### er...@chromium.org (2015-11-24)

D'oh you are right, I messed up on the M48 branch calculation. Thanks for catching that :)

Yes, in that case no action necessary.

This change is already part of M48, and we are not requesting merge to any other branch (per justification above).

### er...@chromium.org (2015-11-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-28)

Adding reward-topanel for consideration under the Chrome Reward Program. Details here: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-01-20)

Hi Aaron - our reward panel reviewed this issue and decided to award you $500 for bringing this issue to our attention. 

Notes from the reward panel: $500 for spotting a weakness, though reward would be larger if combined with a practical attack.

We'll list your name in the Chrome release notes as "Aaron Toponce". If you'd like me to update it to another name, please let me know.

Someone from our finance team should be in contact within 7 days to collect some details for payment. If that doesn't happen, please either update the bug or contact me at timwillis@

I'll update this bug shortly with a CVE ID for your records. Thanks again for helping secure chrome and happy bug hunting!

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1618

### aa...@gmail.com (2016-01-21)

This was quite the surprise when you labeled it in Nov. I didn't expect this, needless to say. Thanks for the reward!

### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-17)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

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

This issue was migrated from crbug.com/chromium/552749?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083150)*
