# Heap-use-after-free in content::WebAudioSourceProviderImpl::provideInput

| Field | Value |
|-------|-------|
| **Issue ID** | [40078042](https://issues.chromium.org/issues/40078042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-09-03 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4697390229487616

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x605000115378
Crash State:
  - crash stack -
  content::WebAudioSourceProviderImpl::provideInput
  WebKit::WebMediaPlayerClientImpl::AudioSourceProviderImpl::provideInput
  - free stack -
  content::WebAudioSourceProviderImpl::~WebAudioSourceProviderImpl
  non-virtual thunk to content::WebAudioSourceProviderImpl::~WebAudioSourceProviderImpl
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).

## Timeline

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-04)

This is due to threading races on WebAudioSourceProviderImpl::bus_wrapper_ in WebAudioSourceProviderImpl::provideInput. I'll write a CL soon.

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157259

------------------------------------------------------------------------
r157259 | haraken@chromium.org | 2013-09-05T02:06:57.884260Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=157259&r2=157258&pathrev=157259

Fix threading races on WebAudioSourceProviderImpl::provideInput

Fix threading races on WebAudioSourceProviderImpl::provideInput 

According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=4697390229487616), 
there is a threading race. Specifically, WebAudioSourceProviderImpl can be destructed by the main thread while WebAudioSourceProviderImpl::Stop() is being called by the audio thread. 

The core problem is that we're not calling WebAudioSourceProviderImpl::setClient(NULL) when HTMLMediaElement clears the audio source provider. 

BUG=284786
No tests because the crash depends on threading races and thus not reproducible.

Review URL: https://chromiumcodereview.appspot.com/23969007
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### ha...@chromium.org (2013-09-12)

Merged into M30.

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157694

------------------------------------------------------------------------
r157694 | haraken@chromium.org | 2013-09-12T19:25:42.497379Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLMediaElement.cpp?r1=157694&r2=157693&pathrev=157694

Merge 157259 "Fix threading races on WebAudioSourceProviderImpl:..."

> Fix threading races on WebAudioSourceProviderImpl::provideInput
> 
> Fix threading races on WebAudioSourceProviderImpl::provideInput 
> 
> According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=4697390229487616), 
> there is a threading race. Specifically, WebAudioSourceProviderImpl can be destructed by the main thread while WebAudioSourceProviderImpl::Stop() is being called by the audio thread. 
> 
> The core problem is that we're not calling WebAudioSourceProviderImpl::setClient(NULL) when HTMLMediaElement clears the audio source provider. 
> 
> BUG=284786
> No tests because the crash depends on threading races and thus not reproducible.
> 
> Review URL: https://chromiumcodereview.appspot.com/23969007

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/23658042
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

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

This issue was migrated from crbug.com/chromium/284786?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078042)*
