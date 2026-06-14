# Heap-use-after-free in WebCore::HRTFElevation::calculateKernelsForAzimuthElevation

| Field | Value |
|-------|-------|
| **Issue ID** | [40077912](https://issues.chromium.org/issues/40077912) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-08-09 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6133378520711168

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x603000050db0
Crash State:
  - crash stack -
  WTF::HashTableAddResult<WTF::HashTableIterator<WTF::String, WTF::KeyValuePair<WTF::String, WTF::RefP
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  - free stack -
  WTF::HashTableAddResult<WTF::HashTableIterator<WTF::String, WTF::KeyValuePair<WTF::String, WTF::RefP
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).

## Attachments

- [fuzz-185.html](attachments/fuzz-185.html) (text/html; charset=us-ascii, 91.6 KB)

## Timeline

### in...@chromium.org (2013-08-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5954860553863168

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x04371b6b
Crash State:
  - crash stack -
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  - free stack -
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  




### cl...@chromium.org (2013-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6171464344535040

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x04f046a3
Crash State:
  - crash stack -
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::OwnPtr<WebCore::ScopedPersistent<v8::S
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  WTF::HashTable<WTF::String,WTF::KeyValuePair<WTF::String,WTF::RefPtr<WebCore::AudioBus> >,WTF::KeyVa
  




### in...@chromium.org (2013-08-15)

Chris, can you please take a look. This is an important high severity bug that is hitting a lot on the bots. If you are not free, please disable HRTFElevation functionality.

### in...@chromium.org (2013-08-15)

Chris is no longer in team. Assigning to Ray for help with triage.

### ka...@google.com (2013-08-26)

ping?

### js...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### rt...@chromium.org (2013-08-29)

I cannot reproduce this with my local asan build.  Can someone help me to reproduce this?

### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4626741238693888

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x606000053f00
Crash State:
  - crash stack -
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  WebCore::HRTFElevation::createForSubject
  - free stack -
  WTF::HashMap<WTF::String, WTF::RefPtr<WebCore::AudioBus>, WTF::StringHash, WTF::HashTraits<WTF::Stri
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  




### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6291334197411840

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x606000056f08
Crash State:
  - crash stack -
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  WebCore::HRTFElevation::createForSubject
  - free stack -
  WebCore::AudioBus::create
  WebKit::WebAudioBus::initialize
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5531180283723776

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x6060000554c0
Crash State:
  - crash stack -
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  WebCore::HRTFElevation::createForSubject
  - free stack -
  WebCore::HRTFElevation::calculateKernelsForAzimuthElevation
  WebCore::HRTFElevation::createForSubject
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### rt...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### gr...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-03)

This is also a threading issue.

READ of size 8 at 0x603000050db0 thread T5
  #1 0x7f7a7f98ac68 in WebCore::HRTFElevation::calculateKernelsForAzimuthElevation(int, int, float, WTF::String const&, WTF::RefPtr<WebCore::HRTFKernel>&, WTF::RefPtr<WebCore::HRTFKernel>&) src/third_party/WebKit/Source/wtf/HashMap.h:342

freed by thread T7 here:
  #2 0x7f7a7f98ac68 in WebCore::HRTFElevation::calculateKernelsForAzimuthElevation(int, int, float, WTF::String const&, WTF::RefPtr<WebCore::HRTFKernel>&, WTF::RefPtr<WebCore::HRTFKernel>&) src/third_party/WebKit/Source/wtf/HashMap.h:342

Two threads call calculateKernelsForAzimuthElevation(). The first thread clears some data in the method. The second thread touches the data and crashes.


### ha...@chromium.org (2013-09-03)

I think the core issue is that the access to AudioBusMap is not thread-safe.

static PassRefPtr<AudioBus> getConcatenatedImpulseResponsesForSubject(const String& subjectName) {
  typedef HashMap<String, RefPtr<AudioBus> > AudioBusMap;
    DEFINE_STATIC_LOCAL(AudioBusMap, audioBusMap, ());
    RefPtr<AudioBus> bus;
    AudioBusMap::iterator iterator = audioBusMap.find(subjectName); // (A)
    if (iterator == audioBusMap.end()) {
        ...;
        audioBusMap.set(subjectName, bus);  // (B)
    }
}

It's possible that:

- Thread 1 executes (A)
- Thread 2 executes (A)
- Thread 1 executes (B)
- Thread 2 executes (B) and crashes.

I'll write a CL soon.

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157273

------------------------------------------------------------------------
r157273 | haraken@chromium.org | 2013-09-05T04:59:19.902020Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/HRTFElevation.cpp?r1=157273&r2=157272&pathrev=157273

Fix threading races on HRTFElevation::audioBusMap

According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6291334197411840),
there is a threading race in HRTFElevation::getConcatenatedImpulseResponsesForSubject.

static PassRefPtr<AudioBus> getConcatenatedImpulseResponsesForSubject(...) {
    typedef HashMap<String, RefPtr<AudioBus> > AudioBusMap;
    DEFINE_STATIC_LOCAL(AudioBusMap, audioBusMap, ());
    RefPtr<AudioBus> bus;
    AudioBusMap::iterator iterator = audioBusMap.find(subjectName); // (A)
    if (iterator == audioBusMap.end()) {
        ...;
        audioBusMap.set(subjectName, bus);  // (B)
    }
}

It's possible that:

(1) Thread 1 executes (A)
(2) Thread 2 executes (A)
(3) Thread 1 executes (B)
(4) Thread 2 executes (B) and crashes.

This CL protects accesses to the AudioBusMap with mutex.

BUG=270758
No tests because the crash depends on threading races and thus not reproducible.

Review URL: https://chromiumcodereview.appspot.com/23613007
------------------------------------------------------------------------

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157691

------------------------------------------------------------------------
r157691 | haraken@chromium.org | 2013-09-12T19:22:42.991190Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/platform/audio/HRTFElevation.cpp?r1=157691&r2=157690&pathrev=157691

Merge 157273 "Fix threading races on HRTFElevation::audioBusMap"

> Fix threading races on HRTFElevation::audioBusMap
> 
> According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6291334197411840),
> there is a threading race in HRTFElevation::getConcatenatedImpulseResponsesForSubject.
> 
> static PassRefPtr<AudioBus> getConcatenatedImpulseResponsesForSubject(...) {
>     typedef HashMap<String, RefPtr<AudioBus> > AudioBusMap;
>     DEFINE_STATIC_LOCAL(AudioBusMap, audioBusMap, ());
>     RefPtr<AudioBus> bus;
>     AudioBusMap::iterator iterator = audioBusMap.find(subjectName); // (A)
>     if (iterator == audioBusMap.end()) {
>         ...;
>         audioBusMap.set(subjectName, bus);  // (B)
>     }
> }
> 
> It's possible that:
> 
> (1) Thread 1 executes (A)
> (2) Thread 2 executes (A)
> (3) Thread 1 executes (B)
> (4) Thread 2 executes (B) and crashes.
> 
> This CL protects accesses to the AudioBusMap with mutex.
> 
> BUG=270758
> No tests because the crash depends on threading races and thus not reproducible.
> 
> Review URL: https://chromiumcodereview.appspot.com/23613007

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/23437031
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-12)

Merged into M30.

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### la...@google.com (2013-09-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$500

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

This issue was migrated from crbug.com/chromium/270758?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077912)*
