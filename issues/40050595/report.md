# Security: Roll expat to patch CVE-2019-18197, CVE-2019-13117, CVE-2019-13118

| Field | Value |
|-------|-------|
| **Issue ID** | [40050595](https://issues.chromium.org/issues/40050595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-13117, CVE-2019-13118, CVE-2019-18197 |
| **Reporter** | [Deleted User] |
| **Assignee** | sc...@chromium.org |
| **Created** | 2019-11-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chromium has not rolled libxslt since CVE-2019-18197 [1], CVE-2019-13117 [2], CVE-2019-13118 [3] were published.  

The first vulnerability listed was published as a use-after-free with an unknown impact but likely results in out-of-bounds memory read/write.  

The other two are stack memory information disclosures.

See <https://bugs.chromium.org/p/chromium/issues/detail?id=934413> for a public issue related to rolling libxslt.  

The upstream patch is <https://gitlab.gnome.org/GNOME/libxslt/commit/2232473733b7313d67de8836ea3b29eec6e8e285>

[1] <https://nvd.nist.gov/vuln/detail/CVE-2019-18197> <https://gitlab.gnome.org/GNOME/libxslt/commit/2232473733b7313d67de8836ea3b29eec6e8e285>  

[2] <https://nvd.nist.gov/vuln/detail/CVE-2019-13117> <https://gitlab.gnome.org/GNOME/libxslt/commit/c5eb6cf3aba0af048596106ed839b4ae17ecbcb1>  

[3] <https://nvd.nist.gov/vuln/detail/CVE-2019-13118> <https://gitlab.gnome.org/GNOME/libxslt/commit/6ce8de69330783977dd14f6569419489875fb71b>

**VERSION**  

Chrome Version: 78.0.3904.87 Stable (via code inspection of <https://cs.chromium.org/chromium/src/third_party/libxslt/src/libxslt/transform.c?rcl=4d8fe5d313405d01306fbaf3d06ae424e1d287e7>)  

Operating System: code inspection / binary Analysis with internal tool. Affected object, obj/third\_party/libxslt/libxslt/transform.o, was confirmed to be linked in our downstream Chromium based browsers (BlackBerry Access - Android, Windows, Mac).

**REPRODUCTION CASE**

See oss-fuzz bugs:

- <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=15746>
- <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=15768>
- <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=15914>
- <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=14471>
- <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=15069>

**CREDIT INFORMATION**  

Reporter credit: BlackBerry Security Incident Response Team ([secure@blackberry.com](mailto:secure@blackberry.com))

## Timeline

### li...@chromium.org (2019-11-01)

schenney@, are you able to address https://crbug.com/chromium/934413 soon so that we can patch these security issues? Thanks!

[Monorail components: Blink>XML]

### sc...@chromium.org (2019-11-02)

Yes. I'll get it done early next week. Sorry for the delay.

### sh...@chromium.org (2019-11-16)

schenney: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-01)

schenney: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2019-12-19)

hi schenney I wonder if you could take a look at this bug and roll expat to the latest version? Thanks.

### sc...@chromium.org (2019-12-20)

I'm stalled due to badly written tests that I need to understand and update. Target is early January in time for M-81.

### sh...@chromium.org (2020-01-01)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6718c0cd782a6360f819133a945b898fe9e4859f

commit 6718c0cd782a6360f819133a945b898fe9e4859f
Author: Stephen Chenney <schenney@chromium.org>
Date: Fri Jan 10 20:30:37 2020

Roll libxml2 and libxslt

The new libxml git hash is a7fe7ee45938c53a8dd028dd40baa461191a2fd2
The new libxslt git hash is 3653123f992db24cec417d12600f4c67388025e3

Unfortunately we don't have the old hashes.

Bug: 1020745
Change-Id: I04ca286b3d9f880f970296c6f6e6b63d6df58267
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1906950
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/master@{#730286}

[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/blink/web_tests/fast/xsl/resources/xslt-enc-cyr.xsl
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/blink/web_tests/fast/xsl/resources/xslt-enc.xsl
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/blink/web_tests/fast/xsl/resources/xslt-enc16.xsl
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/blink/web_tests/fast/xsl/resources/xslt-text.xsl
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/blink/web_tests/fast/xsl/xslt-processor-expected.txt
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxml/README.chromium
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxml/src/libxml2.spec
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxml/src/parser.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxml/src/xmlreader.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/README.chromium
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/linux/config.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/linux/libexslt/exsltconfig.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/linux/libxslt/xsltwin32config.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/mac/config.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/Makefile.am
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/config.h.in
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/configure.ac
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt.pc.in
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt/crypto.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt/date.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt/dynamic.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt/functions.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libexslt/saxon.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt.pc.in
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt.spec.in
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/attrvt.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/functions.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/keys.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/libxslt.syms
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/numbers.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/pattern.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/pattern.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/templates.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/transform.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/variables.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xslt.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xsltInternals.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xsltconfig.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xsltconfig.h.in
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xsltutils.c
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/libxslt/xsltutils.h
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/win32/libxslt.def.src
[modify] https://crrev.com/6718c0cd782a6360f819133a945b898fe9e4859f/third_party/libxslt/src/xsltConf.sh.in


### sc...@chromium.org (2020-01-11)

Requesting merge back to M-80, once we have had it in Canary for a couple of days. Setting a next action.

### sh...@chromium.org (2020-01-11)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2020-01-11)

This is a P1 security issue, hence the merge request.
I am waiting on Canary roll-out to make sure it's safe.
It doesn't add any functionality - it is fixing bugs and security issue in a third_party library. The code has been present in that library for 2 months at least.

### sc...@chromium.org (2020-01-11)

Also:
1. Fits in Merge Decision Guidelines because it's a security issue originally targeted at M-79.
2. CL from https://crbug.com/chromium/1020745#c8 https://chromium.googlesource.com/chromium/src.git/+/6718c0cd782a6360f819133a945b898fe9e4859f
3. Waiting for NextAction date
4. Security issue, so needs a post Beta fix
5. Not a new feature
6 NA

### sh...@chromium.org (2020-01-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-12)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-13)

The CL seems to have effected lot of files , Can you pls clarify it is safe to merge to branch at this point. can this wait for M81?

### sc...@chromium.org (2020-01-13)

It affects a lot of files because it is an entire third_party code roll.

I definitely think it is safe to merge thanks to upstream testing, lots of fuzzer coverage of the code in question, and no changes on the chromium code size. We've merged these kinds of things before for security and functionality reasons. e.g. https://bugs.chromium.org/p/chromium/issues/detail?id=820163

### ad...@chromium.org (2020-01-13)

I'm going to suggest that this be merged into M80, but not M79.

There's high-severity security consequences here but there is some stability risk with a diff this big (even if that risk is minimal, we don't want to break the web for stable users of M79). So M80 seems like the right choice.

### sc...@chromium.org (2020-01-13)

Yes, I was only considering M-80. I do not believe an M-79 merge is justified at this point.

### sr...@google.com (2020-01-13)

Approved for M80 branch: 3987

Please merge to branch asap so this can be included this weeks beta release

### go...@chromium.org (2020-01-14)

Please merge your change to M80 branch 3987 ASAP so we can pick it up for this week beta release. Thank you.

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-01-14)

Please merge your change to M80 branch 3987 ASAP so we can pick it up for tomorrow's beta release, we're cutting Beta RC soon. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd

commit eb6f34c37c24533f4d93aa20bd7383bda9ce38bd
Author: Stephen Chenney <schenney@chromium.org>
Date: Tue Jan 14 20:18:03 2020

Roll libxml2 and libxslt

M-80 merge

The new libxml git hash is a7fe7ee45938c53a8dd028dd40baa461191a2fd2
The new libxslt git hash is 3653123f992db24cec417d12600f4c67388025e3

Unfortunately we don't have the old hashes.

Some xslt template's were updated because the new version of libxslt
requires a MATCH or TEST attribute for a template tag. This is per spec.

(cherry picked from commit 6718c0cd782a6360f819133a945b898fe9e4859f)

Bug: 1020745
Change-Id: I04ca286b3d9f880f970296c6f6e6b63d6df58267
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1906950
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#730286}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1998984
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#528}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/blink/web_tests/fast/xsl/resources/xslt-enc-cyr.xsl
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/blink/web_tests/fast/xsl/resources/xslt-enc.xsl
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/blink/web_tests/fast/xsl/resources/xslt-enc16.xsl
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/blink/web_tests/fast/xsl/resources/xslt-text.xsl
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/blink/web_tests/fast/xsl/xslt-processor-expected.txt
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxml/README.chromium
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxml/src/libxml2.spec
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxml/src/parser.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxml/src/xmlreader.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/README.chromium
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/linux/config.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/linux/libexslt/exsltconfig.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/linux/libxslt/xsltwin32config.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/mac/config.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/Makefile.am
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/config.h.in
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/configure.ac
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt.pc.in
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt/crypto.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt/date.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt/dynamic.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt/functions.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libexslt/saxon.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt.pc.in
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt.spec.in
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/attrvt.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/functions.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/keys.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/libxslt.syms
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/numbers.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/pattern.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/pattern.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/templates.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/transform.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/variables.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xslt.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xsltInternals.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xsltconfig.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xsltconfig.h.in
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xsltutils.c
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/libxslt/xsltutils.h
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/win32/libxslt.def.src
[modify] https://crrev.com/eb6f34c37c24533f4d93aa20bd7383bda9ce38bd/third_party/libxslt/src/xsltConf.sh.in


### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $500 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-01-23)

Thanks Natasha, our team will reach out to the VRP program shortly.
Just a note for your release note publication (i.e. https://chromereleases.googleblog.com/), the issue title/summary is wrong. For whatever reason, I typed "expat" instead of "libxslt" to roll. The library was correctly noted in the description.

### ad...@google.com (2020-01-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-13)

Hello @natashapabrai, in discussions with my team they mentioned that the release note credit should include my full name, similar to that of the other reports this cycle.

Please change it to, "Reported by Jordan Pryde from the BlackBerry Security Incident Response Team" or a similar construction.
We will also be contacting security-vrp@ shortly to determine the rest of the particulars in regards to the awarded bounty.

### na...@google.com (2020-02-18)

 jpryde@blackberry.com - processing this reward as a donation 

### na...@google.com (2020-02-18)

 jpryde@blackberry.com - processing this reward as a donation 

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-18)

This issue was migrated from crbug.com/chromium/1020745?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050595)*
