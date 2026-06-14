# Security: Upgrade expat to 2.2.8

| Field | Value |
|-------|-------|
| **Issue ID** | [40050134](https://issues.chromium.org/issues/40050134) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-15903 |
| **Reporter** | ad...@google.com |
| **Assignee** | bu...@chromium.org |
| **Created** | 2019-09-16 |
| **Bounty** | $500.00 |

## Description

The following e-mail came into security@chromium.org. It looks like we currently have expat 2.2.6: https://cs.chromium.org/chromium/src/third_party/expat/README.chromium?sq=package:chromium&dr=C&g=0

===


I would like to let you know that Expat 2.2.8 [1] has been released.  It
fixes heap buffer over-read CVE-2019-15903 [2] and other issues [3].

If you happen to have patches for Expat that are still required with
2.2.8, please send them my way.

Thank you!

Best



Sebastian


[1] https://github.com/libexpat/libexpat/releases/tag/R_2_2_8
[2] https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-15903
[3] https://github.com/libexpat/libexpat/blob/R_2_2_8/expat/Changes

## Timeline

### dr...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-09-19)

I feel like this might be considered for a reward, the original author is: Sebastian Pipping <sebastian@pipping.org>.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1

commit fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1
Author: Ben Wagner <bungeman@chromium.org>
Date: Thu Sep 19 13:49:24 2019

Roll expat to R_2_2_8-5-g4f23e05

Diffs here should match those at
https://github.com/libexpat/libexpat/compare/39e487da353b20bb3a724311d179ba0fddffc65b..4f23e05a33a66c5962589a32c87df4fe68144fce

Bug: chromium:1004341
Change-Id: I23df3fea3c246e4948a7f548bde8a2b06d7305fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1808428
Commit-Queue: Ben Wagner <bungeman@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#698002}

[add] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/0001-Do-not-claim-getrandom.patch
[delete] https://crrev.com/6eb7d1c327521f12343a33993771b4602fe6db37/third_party/expat/0001-Do-not-redefine-lean-and-mean.patch
[delete] https://crrev.com/6eb7d1c327521f12343a33993771b4602fe6db37/third_party/expat/0002-Add-missing-include-for-malloc-free.patch
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/BUILD.gn
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/README.chromium
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/Changes
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/README.md
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/asciitab.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/expat.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/expat_config.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/expat_external.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/iasciitab.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/internal.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/latin1tab.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/libexpat.def
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/libexpatw.def
[delete] https://crrev.com/6eb7d1c327521f12343a33993771b4602fe6db37/third_party/expat/files/lib/loadlibrary.c
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/nametab.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/siphash.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/utf8tab.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/winconfig.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmlparse.c
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmlrole.c
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmlrole.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmltok.c
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmltok.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmltok_impl.c
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmltok_impl.h
[modify] https://crrev.com/fbe897c5c6d13b0cbac94eb0e20fccf9cdfbc3b1/third_party/expat/files/lib/xmltok_ns.c


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3743d53901ed28e3649295a3430e066953e14050

commit 3743d53901ed28e3649295a3430e066953e14050
Author: Ben Wagner <bungeman@chromium.org>
Date: Thu Sep 26 19:20:36 2019

Move expat to DEPS.

The third_party/expat directory has had a checked in copy of bits of
libexpat. This has make updating quite difficult and blame more or less
impossible. Move to using expat from DEPS to make rolling easier and
more verifiable. This change should be build only and is not expected to
actually change the source compiled.

Bug: chromium:1004341
Change-Id: I7fd74ddb97e8f5302bd4dfe9b24a1bd20821cf55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1822703
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Ben Wagner <bungeman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#700374}

[modify] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/DEPS
[modify] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/third_party/expat/0001-Do-not-claim-getrandom.patch
[modify] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/third_party/expat/BUILD.gn
[modify] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/third_party/expat/README.chromium
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/AUTHORS
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/COPYING
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/Changes
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/MANIFEST
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/README.md
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/ascii.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/asciitab.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/expat.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/expat_external.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/iasciitab.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/internal.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/latin1tab.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/libexpat.def
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/libexpatw.def
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/nametab.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/siphash.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/utf8tab.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/winconfig.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmlparse.c
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmlrole.c
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmlrole.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmltok.c
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmltok.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmltok_impl.c
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmltok_impl.h
[delete] https://crrev.com/2b4d9f869295b837d2a32b4d5d928630ca689c59/third_party/expat/files/lib/xmltok_ns.c
[modify] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/third_party/expat/fuzz/expat_xml_parse_fuzzer.cc
[rename] https://crrev.com/3743d53901ed28e3649295a3430e066953e14050/third_party/expat/include/expat_config/expat_config.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/938b5960d2b4a7bf2ccaedbd624fccc1f9d64df0

commit 938b5960d2b4a7bf2ccaedbd624fccc1f9d64df0
Author: Ben Wagner <bungeman@chromium.org>
Date: Fri Sep 27 17:59:34 2019

Add expat/src to third_party/.gitignore.

This directory is brought in through DEPS and needs to be added to the
.gitignore like all the others.

Bug: chromium:1008695,chromium:1004341
Change-Id: I0be8ff319656036f14a6e06a5e677029252b938d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1829941
Reviewed-by: Florin Malita <fmalita@chromium.org>
Commit-Queue: Ben Wagner <bungeman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#700782}

[modify] https://crrev.com/938b5960d2b4a7bf2ccaedbd624fccc1f9d64df0/third_party/.gitignore


### sh...@chromium.org (2019-10-01)

bungeman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2019-10-01)

Expat has been updated to 2.2.8 and moved to DEPS. The plan is to create a roll script to better document how the roll process works and roll to 2.2.9 with it. Once the roll script documentation has proven itself to generally work, the logic can be translated into go and made into an dryrun autoroller.

### sh...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-01)

Requesting merge to beta M78 because latest trunk commit (700782) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-10-01)

+adetaylor@ (Security TPM)  for M78 merge review

### ad...@chromium.org (2019-10-01)

We ought to merge this to M78 if we can, yes.

### sr...@google.com (2019-10-01)

bungerman@ which CL's are you requesting to merge to branch? The CL's in https://crbug.com/chromium/1004341#c4 and #5 seems like quite a bit of code change for a merge to branch,  What is the confidence level of merging a new version of parser while milestone is in beta.

### bu...@chromium.org (2019-10-01)

I didn't request the merge myself, I think that came from the security team which would like to see expat get updated. On the pro side, while this looks like a really big diff, the reality is 7/8ths of the line diffs are from a single reformatting change, there are cve related changes we want as quickly as possible, the code is exactly what was upstream, and the roll has been in Canary and Dev for a bit. On the nay side, this is a big change late in the cycle for a beta (~350 upstream git commits) and this code hasn't been updated for a long time and we've lived with the issues for a while.

I can do a clean cherry-pick of just the change in https://crbug.com/chromium/1004341#c4, which would bring the 78 branch up to where master has been for a few weeks now. I would not recommend any of the other changes here (such as the changes in https://crbug.com/chromium/1004341#c5 and https://crbug.com/chromium/1004341#c6 which go together) as there is no need to move expat to DEPS on the branch.

### ad...@google.com (2019-10-01)

I agree with everything in https://crbug.com/chromium/1004341#c14. The reason we'd like to merge is that we know attackers will be monitoring not only our git repo, but also expat's CVE disclosures, so - to the extent that this is actually exploitable - there is no doubt that attackers will be having a crack at it right now. It's an OOB read, rather than a write, which is why I'm asking to merge it only to beta.

### sr...@google.com (2019-10-01)

bungeman@ clean cherry-pick of change from https://crbug.com/chromium/1004341#c4 sgtm. pls get the CL ready for review 

### bu...@chromium.org (2019-10-01)

Cherry-pick change up at https://chromium-review.googlesource.com/c/chromium/src/+/1832736 . I can land when I see this go to Merge-Approved-78, or you can mark this Merge-Approved-78 and just land it if you prefer.

### bu...@chromium.org (2019-10-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-10-02)

Approving merge to M78 branch 3904 based on comments #12 to #17.  Please merge ASAP. Thank you.

### sr...@google.com (2019-10-02)

CL in https://crbug.com/chromium/1004341#c17 has landed on branch 3904, so removing the merge-approved-label .

### na...@google.com (2019-10-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-09)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-10-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

Hi sebastian@pipping.org, you would normally get a credit in the release notes for this. How would you like to be credited? e.g. "Sebastian Pipping" or whatever brief text you like. Thanks again!

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

Using expat CVE instead of allocating one.

### sh...@chromium.org (2020-01-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-07)

This issue was migrated from crbug.com/chromium/1004341?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050134)*
