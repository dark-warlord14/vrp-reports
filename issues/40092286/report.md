# CSP media-src bypass with HLS

| Field | Value |
|-------|-------|
| **Issue ID** | [40092286](https://issues.chromium.org/issues/40092286) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>Video, Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android |
| **Reporter** | s....@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2018-08-27 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/hls/csp.php

What is the expected behavior?
Video and audio shouldn't be loaded

What went wrong?
https://test.shhnjk.com/hls/csp.php specifies following CSP header.
Content-Security-Policy: media-src 'self'

But https://test.shhnjk.com/hls/testa.m3u8 fetches media content from vuln.shhnjk.com which should be blocked.

Did this work before? N/A 

Chrome version: 68.0.3440.91  Channel: stable
OS Version: 6.0.1
Flash Version:

## Timeline

### bu...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### va...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-27)

OP -- can you please paste the contents of the PHP files here for the assignee to test locally?

### s....@gmail.com (2018-08-27)

<?php
header("Content-Security-Policy: media-src 'self'");
?>

<video controls autoplay>
  <source src="testa.m3u8">
</video>

### sh...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-10)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-24)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-04-30)

I do not work on CSP anymore so leaving this for someone else to pick up

### ad...@google.com (2019-05-02)

Assigning CSP bugs to mkwst@ after discussion.

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 687 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 701 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ar...@google.com (2020-11-25)

FYI, the video URL "https://test.shhnjk.com/hls/testa.m3u8"
contains:

```
#EXTM3U
#EXT-X-VERSION:5

#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="English stereo",LANGUAGE="en",AUTOSELECT=YES,URI="https://vuln.shhnjk.com/audio.m3u8"

#EXT-X-STREAM-INF:BANDWIDTH=628000,CODECS="avc1.42c00d,mp4a.40.2",RESOLUTION=320x180,AUDIO="audio"
https://vuln.shhnjk.com/video.m3u8
```

The video's URL passes the CSP check. So far, so good.

Its content, contains EXT-X-STREAM, which are alternative media playlist, which can fetch other URLs. I am not fully sure this is implemented in Chrome (this doesn't seems to load).

I don't think CSP is meant to apply to this extent, but maybe Mike have an opinion about this?

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@google.com (2021-03-01)

In theory, CSP should apply to resources loaded by other resources (like images loaded via CSS). If Chromium doesn't implement the alternative media playlist mechanism, then it's not a critical question to answer.

Jun, does this work today? Or is Arthur correct above?

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### s....@gmail.com (2021-03-11)

I was able to repro the PoC.

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2021-05-18)

The video does not play on desktop, but it does on Android. We should probably have a look and fix.

This is a partial CSP bypass. Lowering the priority according to the guidelines (https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md).

### an...@chromium.org (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2021-07-12)

I tried to investigate more but when running this with a debug version I run into a DCHECK

07-12 04:38:46.047 21849 21974 F chromium: [FATAL:sequence_checker.h(136)] Check failed: checker.CalledOnValidSequence(&bound_at).

From:

07-12 04:38:46.047 21849 21974 F chromium:   logging::CheckError::~CheckError()                                                ../../base/check.cc:106:3
07-12 04:38:46.047 21849 21974 F chromium:   base::ScopedValidateSequenceChecker::ScopedValidateSequenceChecker(base::SequenceCheckerImpl const&)  ../../base/sequence_checker.h:136:5
07-12 04:38:46.048 21849 21974 F chromium:   mojo::InterfaceEndpointClient::SendMessage(mojo::Message*, bool)                  ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:537:3
07-12 04:38:46.048 21849 21974 F chromium:   mojo::InterfaceEndpointClient::Accept(mojo::Message*)                             ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:524:10
07-12 04:38:46.048 21849 21974 F chromium:   gpu::mojom::StreamTextureProxy::ForwardForSurfaceRequest(base::UnguessableToken const&)  gen/gpu/ipc/common/gpu_channel.mojom.cc:6390:28
07-12 04:38:46.048 21849 21974 F chromium:   content::StreamTextureHost::ForwardStreamTextureForSurfaceRequest(base::UnguessableToken const&)  ../../content/renderer/stream_texture_host_android.cc:78:22
07-12 04:38:46.048 21849 21974 F chromium:   content::StreamTextureProxy::ForwardStreamTextureForSurfaceRequest(base::UnguessableToken const&)  ../../content/renderer/media/android/stream_texture_factory.cc:105:10
07-12 04:38:46.048 21849 21974 F chromium:   content::StreamTextureWrapperImpl::ForwardStreamTextureForSurfaceRequest(base::UnguessableToken const&)  ../../content/renderer/media/android/stream_texture_wrapper_impl.cc:99:26
07-12 04:38:46.048 21849 21974 F chromium:   content::MediaPlayerRendererClient::OnScopedSurfaceRequested(base::UnguessableToken const&)  ../../content/renderer/media/android/media_player_renderer_client.cc:93:28

Reassigning this to media component for further investigation.

dalecurtis@ could you have a look and/or forward to someone who has more background here?

[Monorail components: Blink>Media>Video]

### an...@chromium.org (2021-07-12)

(Some additional information: the network request downloading the video is not tracked in devtools, so I guess there is something wrong in setting that up)

### da...@chromium.org (2021-07-12)

The reported issue isn't fixable until we ship our own HLS stack or Android adds CSP support unfortunately. Network loading is done by the Android MediaPlayer API, not Chrome. 

As for the DCHECK, +vikassoni,liberato

+cassew who is investigating our own HLS stack which would allow us to obey CSP.

### vi...@chromium.org (2021-07-12)

assigning it to Ken who recently moved all legacy ipc messages over to mojom.

Ken can you please take a look.

### ro...@google.com (2021-07-12)

I think StreamTextureHostAndroid is unintentionally called in a thread-unsafe way. The Mojo conversion incidentally exposes this through a thread-safety DCHECK within Mojo, but looking back at history this unsafe behavior appears to have been possible before the conversion as well.

### ro...@google.com (2021-07-12)

I will send out a fix for the thread-unsafe behavior anyway and then reassign since I'm guessing that's not the root of whatever issue is being investigated here.

### gi...@appspot.gserviceaccount.com (2021-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad048cced2706fb70c0ae6c3fb943422df06065e

commit ad048cced2706fb70c0ae6c3fb943422df06065e
Author: Ken Rockot <rockot@google.com>
Date: Mon Jul 12 23:47:58 2021

fix threading issue in StreamTextureProxy

It seems MediaPlayerRendererClient can invoke
ForwardStreamTextureForSurfaceRequest from an arbitrary thread.
Make it safe.

Bug: 877856
Change-Id: I1a645145bf0fd0a90339ecdb4bb77d720ee5ac10
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3021691
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/master@{#900719}

[modify] https://crrev.com/ad048cced2706fb70c0ae6c3fb943422df06065e/content/renderer/media/android/stream_texture_factory.cc


### ro...@google.com (2021-07-12)

DCHECK should be fixed. Not sure who the right owner for this is, but returning to dalecurtis@ for now.

### da...@chromium.org (2021-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-09-08)

No target on this at this time, it's a large undertaking but design is underway.

### [Deleted User] (2021-10-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2022-09-27)

Per https://crbug.com/chromium/877856#c60, this is not a fixit-sized issue.

### ca...@google.com (2022-09-28)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### da...@chromium.org (2023-02-16)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-03-10)

Did anything come out of cassew@'s investigation of HLS and CSP?

### da...@chromium.org (2023-03-10)

In what way? Android doesn't support it, but switching to Chrome's network stack will support it implicitly.

### ti...@chromium.org (2023-03-29)

I see, thanks! Are there any plans to make the switch?

### tm...@chromium.org (2023-03-29)

Yes. The implementation is being tracked here: https://bugs.chromium.org/p/chromium/issues/detail?id=1266991

### tm...@chromium.org (2023-04-07)

[Empty comment from Monorail migration]

### tm...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-05)

This issue was migrated from crbug.com/chromium/877856?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Media>Video, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail blocked-on: crbug.com/chromium/1266991]
[Monorail mergedwith: crbug.com/chromium/1441321]
[Monorail components added to Component Tags custom field.]

### da...@chromium.org (2025-04-01)

As of <https://crrev.com/a6e3765baaa2e2f09b52527ea60db304355d9a9d> (M135) this should be finally fixed.

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Congratulations Jun! Thank you for your efforts reporting this issue to us back in 2018.

### s....@gmail.com (2025-04-10)

Thanks!

### ch...@google.com (2025-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092286)*
