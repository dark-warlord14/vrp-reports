# Heap overflow and integer overflow in ICU library

| Field | Value |
|-------|-------|
| **Issue ID** | [40081262](https://issues.chromium.org/issues/40081262) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2014-8146, CVE-2014-8147 |
| **Reporter** | pe...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2015-01-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36

Steps to reproduce the problem:
This is a code level problem which I found while fuzzing LibreOffice, but has been confirmed to be a underlying issue in ICU 52 to 54 - therefore it affects Chrome, although I'm not sure how to trigger it.

Open any of the two files (fuzzed-168-7-542405652.xls or  fuzzed-18-95-602621340.xls) in LibreOffice Calc 4.3.3.2 or 4.4.0-beta2. See the analysis file for more details.

What is the expected behavior?
The file is opened.

What went wrong?
fuzzed-18-95-602621340.xls:
Calc crashes with a SIGSEGV on free caused by an invalid pointer. The backtrace can be seen in [1] but this only shows when the actual blowup happens.
The integer overflow can be traced to a call in resolveImplicitLevels in the ICU library (itself called from ubidi_setPara which is called in core/editeng/source/editeng/impedit2.cxx:1895). With the proof of concept file, the overflow happens on the 18th call to ubidi_setPara.

Integer overflow in resolveImplicitLevels (ubidi.c:2248):

        pBiDi->isolates[pBiDi->isolateCount].state=levState.state;

pBiDi->isolates[].state is a int16, while levState.state is a int32.
The overflow causes an error when performing a malloc on pBiDi->insertPoints->points because insertPoints is adjacent in memory to isolates[].

The Isolate struct is defined in ubidiimp.h:184
typedef struct Isolate {
    int32_t startON;
    int32_t start1;
    int16_t stateImp;
    int16_t state;
} Isolate;

LevState is defined in ubidi.c:1748
typedef struct {
    const ImpTab * pImpTab;             /* level table pointer          */
    const ImpAct * pImpAct;             /* action map array             */
    int32_t startON;                    /* start of ON sequence         */
    int32_t startL2EN;                  /* start of level 2 sequence    */
    int32_t lastStrongRTL;              /* index of last found R or AL  */
    int32_t state;                      /* current state                */
    int32_t runStart;                   /* start position of the run    */
    UBiDiLevel runLevel;                /* run level before implicit solving */
} LevState;

My view on this is that it is hard to exploit (as all integer overflows are), but might be possible to do so - I'm won't put my hands in the fire and say no. No guarantees on this one.

fuzzed-168-7-542405652.xls:
The code to blame is the following (from ubidi.c:2148 in ICU 52):
    dirProp=dirProps[limit-1];
    if((dirProp==LRI || dirProp==RLI) && limit<pBiDi->length) {
        pBiDi->isolateCount++;
        pBiDi->isolates[pBiDi->isolateCount].stateImp=stateImp;
        pBiDi->isolates[pBiDi->isolateCount].state=levState.state;
        pBiDi->isolates[pBiDi->isolateCount].start1=start1;
    }
    else
        processPropertySeq(pBiDi, &levState, eor, limit, limit);

From my investigation below, I'm guessing that isolateCount is increased by one and the following writes are out of bounds, causing valgrind to throw the errors below and finally killing it. Again I'm not sure but this might be exploitable - I'm not putting my hands in the fire. No guarantees either.

There are 3 out of bound writes: one of 2 bytes, then 4 bytes, then 2 bytes again.

Stack traces and more detail are in the analysis.txt of the attached 7z file.

Did this work before? N/A 

Chrome version: 39.0.2171.71  Channel: n/a
OS Version: 
Flash Version: Shockwave Flash 16.0 r0

Why I am reporting this to you - two reasons.

First, I just realised that somebody was received $1000 for reporting an unitialised value in the ICU library in the latest Chrome release. It's worth trying? I bet it is widely used for other Google Apps, and even the Android core! :)

Second, I am a bit annoyed at the way this is being handled - it was disclosed to ICU and LibreOffice on the 18th of December and I have heard little from them except that the target release date is for "end of quarter" (when the new version of 55.1 comes out). Maybe with a little push from you then can fix it quicker.

This is being tracked as:
CVE-2014-8146 ICU: pedrib@gmail.com heap overflow
CVE-2014-8147 ICU: pedrib@gmail.com integer overflow

The vulnerabilities are still under wraps, only ICU, libreoffice-security the distro-security mailing lists know about it.

## Attachments

- [sorted.7z](attachments/sorted.7z) (application/octet-stream, 26.0 KB)

## Timeline

### pe...@gmail.com (2015-01-25)

Also this is being tracked in the ICU bug tracker as:
#11451: ubidi_setpara issues

(with restricted view at the moment)

Also another reason I am reporting to you - you can use your "power" to coordinate the release. I expect ICU will just drop this on everyone's lap once they fix it and release 55.1.

### ri...@chromium.org (2015-01-26)

Thanks for the detailed analysis. Adding jshin@, who might be more familiar with ICU stuff. Do you think this is reachable from chromium? I see a call to ubidi_setPara at https://code.google.com/p/chromium/codesearch#chromium/src/base/i18n/bidi_line_iterator.cc&l=32, which I assume can be run with a user-controlled input? For the purposes of triaging, I'm going to assume that we're affected.

Unfortunately I'm not sure whether there is much we can do to nudge them to fix this earlier, but it's definitely helpful to be aware of this if we are affected - thanks!

### pe...@gmail.com (2015-01-26)

I'll be honest with you, I have no idea if it's reachable from chromium. I'm only reporting this to you because of the reasons listed above. 
I know you guys don't necessarily work for Google, but I assume it's easy for you to contact the Android team? I'm sure they might be interested in this. Otherwise I will just contact them directly. 

### cl...@chromium.org (2015-01-27)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-01-27)

I chatted with some android security folks, and they suggested reporting it to them separately since they use a different bug tracking system - thanks!

### pe...@gmail.com (2015-02-01)

It's been reported to Android via their security@android.com and encrypted it with their PGP key.
Please keep me posted on your progress, and let me know if you need any help.

### cl...@chromium.org (2015-02-08)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-02-09)

Sorry that I missed this one. Blink does not use ICU's Bidi implementation, but RenderText (for Chrome's UI) may use ubidi* API. So, Chrome can be affected. 

I'll talk to ICU folks as to what they have done or will do. I'll also talk to Android folks dealing with ICU if necessary. 

### js...@chromium.org (2015-02-10)

http://bugs.icu-project.org/trac/ticket/11451 : CVE-2014-814[67]  : not yet fixed. 



### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-24)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-03-02)

There's a post-commit-review CL in the upstream  : 
http://bugs.icu-project.org/trac/changeset/37080

Once reviewed, I'll cherry-pick it. 


### cl...@chromium.org (2015-03-17)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-03-19)

@pedrib : can you apply the following two changes to ICU and see if LibreOffice issues are resolved? 

http://bugs.icu-project.org/trac/changeset/37080
http://bugs.icu-project.org/trac/changeset/37162

### bu...@chromium.org (2015-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu.git/+/7c81740601355556e630da515b74d889ba2f8d08

commit 7c81740601355556e630da515b74d889ba2f8d08
Author: Jungshik Shin (jungshik at google) <jshin@chromium.org>
Date: Sat Mar 21 07:26:40 2015

Cherry-pick security patches and clean up

1. Cherry-pick security patches from the upstream.
  a. BiDi: integer overflow
    http://bugs.icu-project.org/trac/ticket/11451
    http://crbug.com/451799
    bidi.patch was updated to include patches for this issue.
  b. data race in cmemory; remove an unnecessary check with a global variable.
    http://bugs.icu-project.org/trac/ticket/11538
    http://crbug.com/223352
    cmemory.patch was added
  c. Locale::getBaseName() thread-safety
    http://bugs.icu-project.org/trac/ticket/11547
    http://crbug.com/467836
    locid.patch was updated to include patches for this issue.

2. Add UCONFIG_NO_NON_HTML5_CONVERSION=1 to BUILD.gn

3. Clean up
  a. Update README.chromium to flag patches that are already in the upstream.
  b. Split pkg_gen.patch from data.build.patch. pkg_gen.patch was already
     in the upstream while the rest of data.build.patch is Chromium-specific.
  c. Delete an unused converters.patch.

BUG=223352,451799,467836
TEST=See bugs 223352, 467836, 468716, and 466838
R=jyasskin@chromium.org, mark@chromium.org

Review URL: https://codereview.chromium.org/1020303002

[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/BUILD.gn
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/README.chromium
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/patches/bidi.patch
[add] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/patches/cmemory.patch
[delete] http://crrev.com/009e7a78d921586361bb0a14890e3e35d24edcf0/patches/converters.patch
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/patches/data.build.patch
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/patches/locid.patch
[add] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/patches/pkg_gen.patch
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/cmemory.c
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/cmemory.h
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/icuplug.cpp
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/locid.cpp
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/ubidi.c
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/ubidiimp.h
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/unicode/locid.h
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/test/cintltst/hpmufn.c
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/test/intltest/loctest.cpp
[modify] http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/test/intltest/loctest.h


### bu...@chromium.org (2015-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1d5c2ab824cb253affce1077393e969d1727e035

commit 1d5c2ab824cb253affce1077393e969d1727e035
Author: jshin <jshin@chromium.org>
Date: Sun Mar 22 12:08:20 2015

Roll ICU from 009e7a78d921586361 to 7c817406013555

See https://codereview.chromium.org/1020303002/ for the actual changes.

Besides, remove uprv_malloc fromt the tasn suppression list because
https://crbug.com/chromium/223352 is fixed in this roll.

BUG=223352, 451799, 467836
TEST=See bugs 223352, 467836, 468716, and 466838
TBR=mark@chromium.org,jyasskin@chromium.org

Review URL: https://codereview.chromium.org/1027013002

Cr-Commit-Position: refs/heads/master@{#321714}

[modify] http://crrev.com/1d5c2ab824cb253affce1077393e969d1727e035/DEPS
[modify] http://crrev.com/1d5c2ab824cb253affce1077393e969d1727e035/build/sanitizers/tsan_suppressions.cc


### js...@chromium.org (2015-03-23)

It's fixed in the trunk. 

For M41 (that uses ICU 52.1) and M42 (that uses ICU 54.1, the same as the trunk), the following two changes have to be applied. 

http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/ubidi.c
http://crrev.com/7c81740601355556e630da515b74d889ba2f8d08/source/common/ubidiimp.h

@rickyz and @jschuh, what do you want me to do about this issue for M41 and 42? 
I can cherry-pick the above two changes for M41 and M42 if necessary. We haven't made a Chrome-specific test case, but I guess it's possible. 



### js...@chromium.org (2015-03-26)

inferno@ : can you advise about M41 and M42 branches? 



### in...@chromium.org (2015-03-26)

This is too new for last m41 patch, skip m41. requesting for m42.

### am...@google.com (2015-03-26)

Approved for M42 (branch: 2311)

### js...@chromium.org (2015-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-03-30)

For the record, https://chromereviews.googleplex.com/174937013 is a CL to roll ICU in M42 to the revision with the fix. 


### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/experimental/chrome-radiance.git/+/1d5c2ab824cb253affce1077393e969d1727e035

commit 1d5c2ab824cb253affce1077393e969d1727e035
Author: jshin <jshin@chromium.org>
Date: Sun Mar 22 12:08:20 2015


### pe...@gmail.com (2015-03-31)

@jshin the bug is already fixed in LibreOffice since the last release.

Let me know if you need anything else.

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=70811

------------------------------------------------------------------
r70811 | jungshik@google.com | 2015-03-26T19:40:02.763335Z

-----------------------------------------------------------------

### ti...@google.com (2015-04-09)

Adding reward-topanel for consideration (for the record and to manage your expectations, this doesn't imply that this will be rewarded, just discussed at the panel meeting to see if it's eligible for reward).

### ti...@google.com (2015-04-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Hey pedrib - our reward panel decided to award you with a $500 reward for letting us know about the issue.

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

Cheers,
Tim


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pe...@gmail.com (2015-04-14)

Thanks Tim!
I've noticed that ICU have released a fixed version but they didn't mention the CVE numbers or the security issue at all... is there anything you can do to push them?

### ti...@google.com (2015-04-15)

You're probably going to have more luck than I would. 

The ticket is still restricted from public view (http://bugs.icu-project.org/trac/ticket/11451), so I'd imagine that they may not release details until they open the ticket to the public.

### pe...@gmail.com (2015-04-15)

What if I ask CERT to coordinate? What do you think?
There must be hundreds of software packages using ICU.

### pe...@gmail.com (2015-04-20)

Let me know your thoughts Tim - if I can disclose this to CERT and still get the reward. They can help with coordination since Android, Chromium, ICU, LibreOffice and many other packages might be affected.

### ti...@google.com (2015-04-20)

If you wish to disclose to CERT to help get this fixed, I think that's a win for everyone. It won't invalidate your Chrome reward, but thanks for checking.

### pe...@gmail.com (2015-04-20)

Reported to CERT with tracking number: VRF#I8QFIOPP

### pe...@gmail.com (2015-04-28)

[Comment Deleted]

### pe...@gmail.com (2015-04-28)

Hi,

distro-security is threatening to release the information immediately as they had a 15 day embargo that has been violated (now over 4 months). Would this affect my bounty? I still haven't been contacted by your payments team.

### ti...@google.com (2015-04-29)

That won't affect the bounty - we'll still pay in this case. 

I'll email you now about what the payment email looks like, as sometimes it ends up in spam.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-07-02)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/451799?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081262)*
