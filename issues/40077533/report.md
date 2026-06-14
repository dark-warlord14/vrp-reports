# Tab crashes when changing <audio> element source when used with Web Audio API

| Field | Value |
|-------|-------|
| **Issue ID** | [40077533](https://issues.chromium.org/issues/40077533) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Reporter** | cd...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-05-10 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1499.0 Safari/537.36

Example URL:
http://jsfiddle.net/TT9pf/

Steps to reproduce the problem:
1. Place an <audio> element on a page.
2. Create a webkitAudioContext.
3. Use the webkitAudioContext to create a MediaElementAudioSourceNode from the <audio> element.
4. Programmatically change the source of the <audio> element by removing its child <source> node(s) and replacing it(them). This can also be done via direct modification of the <source> element's 'src' attribute.
5. Use the load() method of the <audio> element to load the new audio source.

What is the expected behavior?
The new source should be loaded by the <audio> element in place.

What went wrong?
Replacing the source of an <audio> element which is the target of a MedilaElementAudioSourceNode results in a crash of the browser tab in which it is hosted.  This does not occur when the <audio> element has not been used in conjunction with the Web Audio API.

Did this work before? No 

Is it a problem with Flash or HTML5? HTML5

Does this work in other browsers? N/A 

Chrome version: 28.0.1499.0  Channel: canary
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)

This issue only occurs when the <audio> element is being used, via MediaElementAudioSourceNode, in a Web Audio API AudioContext, therefore it seems likely that the media element source node implementation is not prepared to handle source switching after instantiation.

An attempt to destroy the source node and re-initialize it fails with DOMException 11.  Disconnecting the source node from the rest of the audio context filtergraph does not appear to have any effect.

Removing the <audio> element in its entirety and replacing it with a new element does appear to be a workaround to this issue, though it is not ideal as it requires the filtergraph to be rebuilt.  A MediaElementAudioSourceNode should tolerate changes to the underlying <audio> element.

An example of the workaround can be found here: http://jsfiddle.net/KbCsG/1/

I have tested this on Chrome 26.0.1410.64 (Stable) as well, wherein the crash will not occur until playback is initiated after audio source replacement.

## Timeline

### aj...@chromium.org (2013-05-11)

Hi Anand, can you look at this?

### cd...@gmail.com (2013-05-13)

Update: Bug remains present in Chrome 29.0.1506.0 (Canary).

### da...@chromium.org (2013-05-13)

Hi, do you have a crash id for this? I.e. does chrome://crashes show something?

### cd...@gmail.com (2013-05-13)

Sorry for not including that - wasn't aware crashes were tracked that way.  Here's the ID of a crash I induced just now using the jsfiddle bug example referenced above: 6721f3025ae7807e

### da...@chromium.org (2013-05-13)

Ah! Thanks! I think this is the same as https://crbug.com/chromium/233026. I'll play around a bit.  In the meantime can you try Chrome Canary and see if it still crashes?  I landed a fix recently for the other bug.

### cd...@gmail.com (2013-05-13)

The crash does still occur on Canary, build 1506, though it doesn't happen immediately upon the <audio> element load() call.  The crash does not take place until one attempts to begin playback of the <audio> element with the new source.  The crash ID I posted was from 29.0.1506.

### da...@chromium.org (2013-05-13)

+crogers: It looks like WebAudio is still using the WebAudioSourceProviderImpl even before it has called setClient appropriately.  This an be confirmed by running the test case above with --enable-dcheck on a local build, or in this method trace:

[10287:10287:0513/142111:ERROR:audio_renderer_mixer_input.cc(24)] AudioRendererMixerInput(0x60d000009aa0)::AudioRendererMixerInput()
[10287:10287:0513/142111:ERROR:webaudiosourceprovider_impl.cc(55)] WebAudioSourceProviderImpl(0x60c000032140)::WebAudioSourceProviderImpl()
[10287:10287:0513/142111:ERROR:webaudiosourceprovider_impl.cc(67)] WebAudioSourceProviderImpl(0x60c000032140)::setClient(0)
[10287:10287:0513/142111:ERROR:webaudiosourceprovider_impl.cc(67)] WebAudioSourceProviderImpl(0x60c000032140)::setClient(0x60200004c530)
[10287:10287:0513/142111:ERROR:audio_renderer_mixer_input.cc(54)] AudioRendererMixerInput(0x60d000009aa0)::Stop()
[10287:10299:0513/142111:ERROR:webaudiosourceprovider_impl.cc(176)] WebAudioSourceProviderImpl(0x60c000032140)::Initialize()
[10287:10299:0513/142111:ERROR:webaudiosourceprovider_impl.cc(127)] WebAudioSourceProviderImpl(0x60c000032140)::Start()
[10287:10299:0513/142111:ERROR:webaudiosourceprovider_impl.cc(156)] WebAudioSourceProviderImpl(0x60c000032140)::Pause()
[10287:10299:0513/142113:ERROR:webaudiosourceprovider_impl.cc(137)] WebAudioSourceProviderImpl(0x60c000032140)::Stop()
[10287:10287:0513/142113:ERROR:webaudiosourceprovider_impl.cc(60)] WebAudioSourceProviderImpl(0x60c000032140)::~WebAudioSourceProviderImpl()
[10287:10287:0513/142113:ERROR:audio_renderer_mixer_input.cc(32)] AudioRendererMixerInput(0x60d000009aa0)::~AudioRendererMixerInput()
[10287:10287:0513/142113:ERROR:audio_renderer_mixer_input.cc(24)] AudioRendererMixerInput(0x60d0000091b0)::AudioRendererMixerInput()
[10287:10287:0513/142113:ERROR:webaudiosourceprovider_impl.cc(55)] WebAudioSourceProviderImpl(0x60c00002b000)::WebAudioSourceProviderImpl()
[10287:10287:0513/142113:ERROR:webaudiosourceprovider_impl.cc(67)] WebAudioSourceProviderImpl(0x60c00002b000)::setClient(0)
[10287:10307:0513/142113:ERROR:webaudiosourceprovider_impl.cc(176)] WebAudioSourceProviderImpl(0x60c00002b000)::Initialize()
[10287:10307:0513/142113:ERROR:webaudiosourceprovider_impl.cc(127)] WebAudioSourceProviderImpl(0x60c00002b000)::Start()
[10287:10307:0513/142113:ERROR:audio_renderer_mixer_input.cc(47)] AudioRendererMixerInput(0x60d0000091b0)::Start()
[10287:10307:0513/142113:ERROR:webaudiosourceprovider_impl.cc(156)] WebAudioSourceProviderImpl(0x60c00002b000)::Pause()
[10287:10307:0513/142113:ERROR:audio_renderer_mixer_input.cc(79)] AudioRendererMixerInput(0x60d0000091b0)::Pause()
[10287:10307:0513/142113:ERROR:webaudiosourceprovider_impl.cc(146)] WebAudioSourceProviderImpl(0x60c00002b000)::Play()
[10287:10307:0513/142113:ERROR:audio_renderer_mixer_input.cc(67)] AudioRendererMixerInput(0x60d0000091b0)::Play()
[10287:10304:0513/142113:ERROR:webaudiosourceprovider_impl.cc(115)] WebAudioSourceProviderImpl(0x60c00002b000)::provideInput()
[10287:10304:0513/142113:FATAL:webaudiosourceprovider_impl.cc(119)] Check failed: client_.


### da...@chromium.org (2013-05-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2013-05-13)

That this leads to a use after free == security bug. +Type-Bug-Security.  Impacts stable+.

### pa...@chromium.org (2013-05-13)

Thank you Dale.

And thank you, cdel921! This bug may be eligible for reward under Chrome's Vulnerability Rewards Program: http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program. Here is some legalese:

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### bu...@chromium.org (2013-05-14)

------------------------------------------------------------------------
r150330 | crogers@google.com | 2013-05-14T19:02:54.640935Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp?r1=150330&r2=150329&pathrev=150330
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.h?r1=150330&r2=150329&pathrev=150330

Add safety when the .src attribute of an <audio> or <video> element is changed and it's used with the Web Audio API

When this happens, the underlying WebMediaPlayer is changed, with the old one destroyed and the new one created.
We need to take care to synchronize this destruction of the old WebMediaPlayer.

Part of this change involves making sure WebMediaPlayerClientImpl::AudioSourceProviderImpl::wrap(0)
calls WebAudioSourceProvider::setClient(0) for the old WebAudioSourceProvider.

We also add locking in the WebMediaPlayerClientImpl::AudioSourceProviderImpl methods.

BUG=239897
R=abarth@chromium.org, dalecurtis@chromium.org, kbr@chromium.org

Review URL: https://codereview.chromium.org/15077011
------------------------------------------------------------------------

### in...@chromium.org (2013-05-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-28)

M27 is r151284
M28 is r151285

### sc...@gmail.com (2013-06-03)

@cdel921: thanks for the report! Although not originally reported as a security issue, it qualifies for a $500 Chromium Security Reward since it enabled us to improve security for our users.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issue.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---


### cd...@gmail.com (2013-06-04)

Thank you very much! I am quite pleasantly surprised - I was entirely unaware of the reward program when I reported this bug.  At your convenience, please let me know what is required of me to accept.

I would note that I am impressed how quickly this issue was dealt with and resolved. You have an efficient operation running here.

### pa...@chromium.org (2013-06-24)

We aim to act fast on security bugs, so thanks for the complement :)

I just initiated payment for this with our finance team. Someone should be in touch with you this/next week to get personal details so we can transfer the reward.

Thanks again for helping make Chrome secure!

### da...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/239897?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077533)*
