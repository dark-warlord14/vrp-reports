# Security: Video streams sourced from cross-origin videos aren't tainted	

| Field | Value |
|-------|-------|
| **Issue ID** | [40088907](https://issues.chromium.org/issues/40088907) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CaptureFromElement, Blink>Media>Video, Blink>SecurityFeature>SameOriginPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mc...@chromium.org |
| **Assignee** | gu...@chromium.org |
| **Created** | 2017-09-02 |
| **Bounty** | $4,000.00 |

## Description

Spin off of https://crbug.com756877 to track the potential cross-origin
violation.

Original issue description: --------------------------------------------

VULNERABILITY DETAILS
The content of cross-origin <video>s are not supposed to be accessible. 
In discussing a Firefox bug Maarten Breddels noted that if you captured the stream of the cross origin video and placed it into a second <video> then it appears to no longer be tainted. He was able to draw that into a canvas and get the image data out without a security exception, and could send the second video stream (but not the first) over webRTC. This affects Chrome 62. In Chrome 60 you need to set the flag to enable stream capture; I didn't try Chrome 61 to see what the default for the flag was in that version.

For more information see https://bugzilla.mozilla.org/show_bug.cgi?id=1177793#c24 and following (mail me or security@mozilla.org to be added to that bug)

VERSION
Chrome Version: 62.0.3188.0 (Official Build) canary (64-bit)
Operating System: macOS 10.11.6 (also on 10.12) plus whatever Maarten and Jan-Ivar use. Doesn't seem to be relevant.

REPRODUCTION CASE
My attempt to combine the fiddles into a stand-alone testcase resulted in a consistent tab crash so all I have for you are jsfiddle links

Getting image data from a cross-origin video:
https://jsfiddle.net/j5yxec3b/

Sending cross-origin video over webRTC:
https://jsfiddle.net/jib1/1kz9hfaL/9/

WebGL:
https://www.astro.rug.nl/~breddels/ipyvolume/tainted/

I will attach my crashing testcase here because it's basically the testcase for this same-origin violation security bug, but the crash itself is probably unrelated.
Tab crash, Crash ID: crash/a976ba002102678a
 

More info ------------------------------------------------------------

The original bug report also included a crash that had to be addressed
first. This issue tracks the cross-origin part. 

## Timeline

### mc...@chromium.org (2017-09-02)

dveditz@mozilla.com can you please provide a reproduceable use case?
Probably an iteration of the first fiddle would do, i.e.
<video> --> MediaStream --> <video> crossing an origin bounday
would do.

 awhalley@ please add the necessary labels to this bug, thanks !

### el...@chromium.org (2017-09-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-03)

[Empty comment from Monorail migration]

### dv...@mozilla.com (2017-09-05)

All three fiddle testcases demonstrate the problem -- on 62! There is no problem on stable (60) because the feature isn't supported without turning on a flag.

The bad behavior in each case follows clicking the "Snap!" button.

### aw...@google.com (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### mc...@chromium.org (2017-09-06)

I won't have time to work on this, so let me pass it over to guidou@
for retriaging.

As a guess, we could check explicitly for |element|'s and the current
security origin to be compatible [1] in the vicinity of [2].


[1] https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/HTMLVideoElement.cpp?sq=package:chromium&dr&l=466
[1] https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/mediacapturefromelement/HTMLMediaElementCapture.cpp?sq=package:chromium&dr&l=120

### gu...@chromium.org (2017-09-07)

Marking this bug as Untriaged so that the relevant component owners can re-triage.

[Monorail components: -Blink>WebRTC]

### me...@chromium.org (2017-09-14)

Can anyone from the relevant components please triage this bug? It's gone unnoticed for a full week now. Thanks.

### pa...@chromium.org (2017-09-19)

Blink team: We need to get some movement on this security bug.

### pa...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-09-21)

Assigning to the most recent author of HTMLMediaElement::IsMediaDataCORSSameOrigin. We can't let straightforward SOP bypasses go un-owned for so long.

### sh...@chromium.org (2017-09-22)

jrummell: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jr...@chromium.org (2017-09-25)

Looks like I got picked as last person to touch HTMLMediaElement::IsMediaDataCORSSameOrigin. All I did was move the function out of HTMLVideoElement.cpp into HTMLMediaElement.cpp so that EME could call it (https://codereview.chromium.org/893123004). The code was originally part of HTMLVideoElement::WouldTaintOrigin().

Using the first jsfiddle line, in Chrome 61 only canvas1 gets something. Current ToT has everything except video3 gets a copy. I added logging to IsMediaDataCORSSameOrigin(), and it's only called twice.

origin: "https://fiddle.jshell.net"
currentSrc: "https://webrtc.github.io/samples/src/video/chrome.mp4"
IsMediaDataCORSSameOrigin() fails.

origin: "https://fiddle.jshell.net"
currentSrc: <null>
IsMediaDataCORSSameOrigin() passes. It calls MultibufferDataSource::DidPassCORSAccessCheck() (in webmediaplayer_impl.cc), so adding dalecurtis/hubbe in case they have additional ideas.

### dv...@mozilla.com (2017-09-25)

> in Chrome 61 only canvas1 gets something.

Stream capture isn't enabled by default until 62, but you can turn it on using chrome://flags if you want to reproduce the bug.

### da...@chromium.org (2017-09-25)

This is MediaStreams, so I thought guidou@ was the right owner here. guidou@ are you not working on MediaStreams anymore?

From looking through the code it seems there's no current mechanism for tainting a MediaStream unless the origin returns true for taintsCanvas(); which I'm not sure will ever happen with a blob:// URL. WebMediaPlayerMS always returns true for HasSingleSecurityOrigin() and DidPassCORSAccessCheck().

+olka for help routing, -acolwell since he's not on the project anymore.

### ol...@chromium.org (2017-09-25)

hbos - is it for you maybe?

### da...@chromium.org (2017-09-25)

Dropping jrummell@ since this is requires some extensive MediaStream changes to accomplish if we want to do anything other than outright block cross origin captureStream(). If we just want to do that, it's easy (caveat,  http://knowyourmeme.com/memes/i-have-no-idea-what-im-doing):

  if (!element.IsMediaDataCORSSameOrigin(
          element.GetExecutionContext()->GetSecurityOrigin())) {
    // TODO(crbug.com/761622): Support proper tainting across MediaStreams.
    exception_state.ThrowDOMException(kNotSupportedError,
                                      "Stream capture not supported with CORS");
    return nullptr;
  }

Probably we want something like this or to disable the API entirely for M62 until this is properly resolved. I trivially plumbed HasSingleSecurityOrigin and DidPassCORSAccessCheck bits into the created WebMediaStream and that was insufficient for the final WebMediaPlayerMS to indicate tainting. Probably a proper approach would build tainting into the MediaStreamDescriptor somehow.

### da...@chromium.org (2017-09-25)

Actually +emircan should probably take this, since he's listed as an OWNER for the capture code along with mcasas@. Taking a look at the spec, the fix I propose in c#19 seems okay. Spec says cross-origin access is not allowed at all, not that it will invoke tainting. 

### em...@chromium.org (2017-09-25)

Assigning to mcasas@ for input. It doesn't seem like a proper fix can be landed for 62. Can you disable rolling the API as suggested in #19?

### da...@chromium.org (2017-09-25)

One note with my comment in c#19 is it also needs to be applied in the MediaElementEventListener for loadedmetadata, otherwise a empty media element could pass the initial check in captureStream(). I wasn't sure how to throw an exception from the listener though.

### gu...@chromium.org (2017-09-26)

I was under the impression that the security issue was not a general MediaStreams issue, but specific to capture from element and security.

Since it has become clear that general mediastream changes are required, I can take it.
However, it's too late for a proper fix for 62, so I think the best course of action is to unship this.

### gu...@chromium.org (2017-09-26)

After taking a closer look at the specs involved, I think emircan@ would indeed be a better owner to get this started, as indicated in #20.
Of course, I can help with changes to the general MediaStreams code in order to provide tainting support if needed.

### mc...@chromium.org (2017-09-26)

IIUC the issue is that 
<video> --> captureStream() --> <video>2 --> captureStream

works across CORS when it shouldn't, because <video>2 is a 
WebMediaPlayerMs and it has no info on CORS [1].

What we can do, while [1] is being addressed, is to disable
captureStream() from <video> elements that are fed by 
MediaStreams [2].

I discussed this morning with guidou@ and it sounds like we
agree on that.

Security reviewers in CC: is this OK for y'all ?? :-)



[1] https://cs.chromium.org/chromium/src/content/renderer/media/webmediaplayer_ms.cc?type=cs&q=webmediaplayerms+cors&sq=package:chromium&l=657

[2] https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/mediacapturefromelement/HTMLMediaElementCapture.cpp?q=htmlvideoelementcapture&sq=package:chromium&dr=C&l=128

### da...@chromium.org (2017-09-26)

Isn't the core problem that capture stream can be used on a cross-origin media element w/o invoking any kind of tainting? I.e. captureStream => MediaRecorder would be just as bad? 

### mc...@chromium.org (2017-09-26)

#26: correct, what I meant is that
<video>1 ---> captureStream() ---> <video>2 ---> captureStream()
          1                    2             3
 
Assuming 1 and 2 are correct CORS-wise, the issue at hand IIUC
is on the second captureStream(), i.e. 3, which at the moment 
succeeds because <video>2 is a WebMediaPlayerMS (and not a 
WebMediaPlayerImpl like <video>1) that always says true which
makes WouldTaintOrigin() false etc.

### gu...@chromium.org (2017-09-26)

I sent crrev.com/c/685239 for review, which adds tainting information to MediaStreams (implemented for HTML video capture only atm).


### gu...@chromium.org (2017-09-26)

#27: You are correct, but feeding <video>2 to a canvas would be wrong too. This case wouldn't be covered by preventing HTML capture from MediaStream since there isn't any.

crrev.com/c/685239 makes the mediaplayer for <video>2 return the same values for CORS checks as <video>1.

### hu...@chromium.org (2017-09-26)

Is it possible for video2 to be in a different origin than video1?
From the quick peek I took at the CL, it seems to just return a bool, which could be insufficient if the media stream is crossing origins.

(What happens if you plug your mediastream into a cast or webrtc session?)



### dv...@mozilla.com (2017-09-26)

The second example (https://jsfiddle.net/jib1/1kz9hfaL/9/) shows plugging the media stream into webrtc. The 3rd shows it being handed off to WebGL.

### dv...@mozilla.com (2017-09-26)

Can someone please add maartenbreddels (at) gmail.com to the access list of this bug? He's the original reporter of this issue as part of the Firefox bug mentioned in the initial comment.

### gu...@chromium.org (2017-09-26)

#30: Since there is currently no tainting information on mediastreams, cast or webrtc are currently not checking any tainting directly on mediastreams. 

The CL attempts to solve the problem for things that query the mediaplayer to check tainting of media elements playing mediastreams, but not things that should check the MediaStream directly. 
The methods added to MediaStreamSource are good enough to check if a stream playing content from a media element is tainted, but the checks need to be added to the respective places. 

Perhaps we should indeed unship capture from element until cast and webrtc perform those checks?

Also, the API to check tainting of mediastreams might need to change to support mediastreams that are tainted in a way different from grabbing data from a cross-origin element, but that would be a separate bug.


### da...@chromium.org (2017-09-26)

+original reporter per c#32

### tr...@gmail.com (2017-09-27)

c#25 MediaStream resulting from UnsafeMediaElement#captureStream should be muted.
Doing this only for MediaElements fed by MediaStream is useless: https://jsfiddle.net/zta30g9n/
The inverse would make more sense.

One note since I'm here, Firefox team is also facing a similar issue: https://bugzilla.mozilla.org/show_bug.cgi?id=1341016
Except that in their case, they are overprotective (they block all cross-origin MediaStreams, whatever the CORS headers.
The discussion there might help you determine the best way to handle this case. 
(In my user's mind it would be to mark the MediaElement element itself as safe or unsafe at load and make all the consumer APIs only ask for the source element's safety).

### gu...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### gu...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### gu...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0

commit 4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Sep 29 12:34:32 2017

Stop media-element capturers if the element has cross-origin data.

BUG=761622

Change-Id: I9428919041a0c5a0779bec18b911b253c82fece3
Reviewed-on: https://chromium-review.googlesource.com/690377
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Emircan Uysaler <emircan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#505353}
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media/media_stream_center.cc
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media/media_stream_center.h
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media_capture_from_element/html_audio_element_capturer_source.cc
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media_capture_from_element/html_audio_element_capturer_source.h
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media_capture_from_element/html_audio_element_capturer_source_unittest.cc
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/content/renderer/media_capture_from_element/html_video_element_capturer_source_unittest.cc
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/third_party/WebKit/Source/modules/mediacapturefromelement/HTMLMediaElementCapture.cpp
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/third_party/WebKit/Source/platform/mediastream/MediaStreamCenter.cpp
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/third_party/WebKit/Source/platform/mediastream/MediaStreamCenter.h
[modify] https://crrev.com/4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0/third_party/WebKit/public/platform/WebMediaStreamCenter.h


### ma...@gmail.com (2017-09-29)

Hi,

I'm afraid this commit disables captureStream completely from a tained element? 

Let me give a bit of background, I originally requested Firefox to be more like Chrome here:
https://bugzilla.mozilla.org/show_bug.cgi?id=1177793#c24
i.e. to take a tainted mediaStream and show it on another video element using .srcObject. This bugreport/feature request led to the realization that *that* videoelement's videostream wasn't being marked as tainted in Chrome, which it should, but the visualization *should* work from a developers point of view.

I also gave some background on why here:
https://bugzilla.mozilla.org/show_bug.cgi?id=1177793#c27
I also mentioned a silly workaround, which would be to manually draw the video frame on a canvas (which would be marked as tainted, but it would work although wasting cpu cycles), although it would work.

So to summarize, I think it should be possible to show a tainted mediastream using video.srcObject or on a WebGL canvas savely (by marking it tainted). It would be sad if both firefox and chrome don't allow this, and would make the webrtc/mediastream api crippled. 
I understand if this is technically difficult to implement now that it would be temporary disabled, I just hope it is temporary :)

Regards,

Maarten




### gu...@chromium.org (2017-09-29)

Maarten: The purpose of the patch is to eliminate the security issue of removing the tainting of a captured cross-origin video element.

Please file a new bug for allowing the visualization of tainted streams, so that the team can work on a secure way of supporting that in all the Chrome code that deals with MediaStreams.  It would be good if you re-state your rationale in the new Chromium bug, since the Firefox bug is restricted and we do not have access to it.

### gu...@chromium.org (2017-09-29)

At the moment, we cannot allow capturing a cross-origin element to a MediaStream, The reason is that MediaStreams in Chromium currently do not support tainting and the features that deal with MediaStreams, such as RTCPeerConnection are implemented without taking tainting into account.
So we need to:
1. Define a tainting interface for MediaStreams.
2. Patch all features that deal with MediaStreams so that they handle tainting in a secure way.
3. Enable the production of tainted MediaStreams such as allowing capture of cross-origin media elements.

### gu...@chromium.org (2017-10-02)

The problem of proper tainting of MediaStreams and their handling by various consumers is still not fixed, but closing this bug anyway since the important security issue was fixed in r505353, which prevents capture from cross-origin elements. 


### gu...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-02)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### dv...@mozilla.com (2017-10-02)

> It would be good if you re-state ... since the Firefox bug is restricted and we do not have access to it.

Offer from https://crbug.com/chromium/761622#c0 still stands to CC anyone on this bug who has an account over there. Guido doesn't seem to have an account though.

### gu...@chromium.org (2017-10-02)

dveditz@: Just created an account.

### aw...@google.com (2017-10-02)

guidou@ - just wanted to check that merging r505353 to M62 is preferable to not enabling (per #23). Is canary coverage OK for shaking out any problems with the change in #39? Cheers!

### cm...@chromium.org (2017-10-03)

Any results from Canary? Has this been tested on canary?

### gu...@chromium.org (2017-10-03)

The patch has been on canary for a few days and is working as intended.

### gu...@chromium.org (2017-10-03)

I think merging is preferrable tp disabling, given that this feature has already been advertised for 62: https://blog.chromium.org/2017/09/chrome-62-beta-network-quality.html

### aw...@chromium.org (2017-10-03)

Thanks guidou@. abdulsyed@ - good for M62 merge. This has also made it into today's Dev.

### sh...@chromium.org (2017-10-03)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-10-03)

Thanks - approving r505353 for merge to M62. Branch:3202

### bu...@chromium.org (2017-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c46fd4bff255cd4f1c87d8899499f306c15c8148

commit c46fd4bff255cd4f1c87d8899499f306c15c8148
Author: Guido Urdaneta <guidou@chromium.org>
Date: Tue Oct 03 23:16:24 2017

Stop media-element capturers if the element has cross-origin data.

BUG=761622

Change-Id: I9428919041a0c5a0779bec18b911b253c82fece3
Reviewed-on: https://chromium-review.googlesource.com/690377
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Emircan Uysaler <emircan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#505353}(cherry picked from commit 4f61ad37e42d20afdcc6442b18b617f7e5f7a2a0)
Reviewed-on: https://chromium-review.googlesource.com/698847
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#570}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media/media_stream_center.cc
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media/media_stream_center.h
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media_capture_from_element/html_audio_element_capturer_source.cc
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media_capture_from_element/html_audio_element_capturer_source.h
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media_capture_from_element/html_audio_element_capturer_source_unittest.cc
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/content/renderer/media_capture_from_element/html_video_element_capturer_source_unittest.cc
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/third_party/WebKit/Source/modules/mediacapturefromelement/HTMLMediaElementCapture.cpp
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/third_party/WebKit/Source/platform/mediastream/MediaStreamCenter.cpp
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/third_party/WebKit/Source/platform/mediastream/MediaStreamCenter.h
[modify] https://crrev.com/c46fd4bff255cd4f1c87d8899499f306c15c8148/third_party/WebKit/public/platform/WebMediaStreamCenter.h


### aw...@chromium.org (2017-10-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-10-06)

Given #42 and #43, it sounds like there will be more changes in the future. Is it possible to write a LayoutTest or similar test to ensure that media assets don't leak across origins (without appropriate CORS opt-in, or whatever) in the future?

I also propose that we consider rewarding the original bug reporter, maartenbreddels (#32).

Mega-thanks to dveditz for your help, too. :)

### aw...@chromium.org (2017-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-11)

Congratulations, the Chrome VRP panel decided to award $4,000 for this report.

### tr...@gmail.com (2017-10-11)

Just to know, there is nothing for duplicates in this case, right?

### ma...@gmail.com (2017-10-12)

Whow, I didn't expect that since I did not request for this, but I'm honored and it's very welcome. For some background; this is a by product of digging into webrtc for a small open source library (https://github.com/maartenbreddels/ipywebrtc) that I wrote for the Jupyter notebook/lab ecosystem.

### aw...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2020-11-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>CaptureFromElement]

### is...@google.com (2020-11-05)

This issue was migrated from crbug.com/chromium/761622?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>CaptureFromElement, Blink>Media>Video, Blink>SecurityFeature>SameOriginPolicy]
[Monorail mergedwith: crbug.com/chromium/766384]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088907)*
