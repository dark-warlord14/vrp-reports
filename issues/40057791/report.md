# Security: webrtc: out-of-bounds write in audio channel processing

| Field | Value |
|-------|-------|
| **Issue ID** | [40057791](https://issues.chromium.org/issues/40057791) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Audio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | iv...@chromium.org |
| **Created** | 2021-11-02 |
| **Bounty** | $8,500.00 |

## Description

**VULNERABILITY DETAILS**

WebRTC handles audio packets that are sent from other RTC clients in GetAudioInternal [1]. In the case where the channel is muted the `audio_frame->num_channels_` is set to `sync_buffer->Channles()`.

```
  if (enable_muted_state_ && expand_->Muted() && packet_buffer_->Empty()) {  
      ...  
    audio_frame->num_channels_ = sync_buffer_->Channels();  
      ...  
    return 0;  
  }  
  

```

The sync buffer is initialized in SetSampleRateAndChannels [2]. This sets the sync\_buffer\_ and many other buffers to size `channels`.

```
void NetEqImpl::SetSampleRateAndChannels(int fs_hz, size_t channels) {  
    ...  
  algorithm_buffer_.reset(new AudioMultiVector(channels));  
  sync_buffer_.reset(new SyncBuffer(channels, kSyncBufferSize \* fs_mult_));  
  background_noise_.reset(new BackgroundNoise(channels));  
  UpdatePlcComponents(fs_hz, channels);  
    ...  

```

`SetSampleRateAndChannels` is passed channels and sample rate from a specific encoder/decoder [3]. Decoder's channel number and sample rate are inititalized using SDP and SDP is completely controllable by the client. The PCMU codec can be set to have an arbitrary number of codecs [4]. For example, to set `num_channels_` to 1000 add this line to an SDP config.

```
a=rtpmap:116 PCMU/8000/1000  

```

In the attached Javascript I use SDP munging to accomplish this in the browser:

```
const answer = await pc.createAnswer()  
  
let munge = answer.sdp.replace("a=rtpmap:9 G722/8000\r\n", "a=rtpmap:9 G722/8000\r\na=rtpmap:116 PCMU/8000/1000\r\n");  
    
munge = munge.replace(  
    "m=audio 9 UDP/TLS/RTP/SAVPF 111 103 104 9 0 8 106 105 13 110 112 113 126",   
    "m=audio 9 UDP/TLS/RTP/SAVPF 111 103 104 9 0 8 106 105 13 110 112 113 126 116");  
answer.sdp = munge;  
setLocalAndSendMessage(answer);  

```

Now `audio_frame->samples_per_channel_ \* audio_frame->num_channels_ \* sizeof(int16_t)` will exceed `AudioFrame::kMaxDataSizeSamples` which will cause a slew of overflows when the victim browser receives a packet on channel 116 and the channel is set to mute. For example shortly after GetAudioInternal WebRTC will resample the the audio frame and allocate a buffer of size `AudioFrame::kMaxDataSizeSamples` for the ouput [5].

or shortly after that in the more simple exploit primitive, memcpy into `last_audio_buffer_` [6].

```
  last_audio_buffer_(new int16_t[AudioFrame::kMaxDataSizeSamples]),  
  ...  
  // Store current audio in `last_audio_buffer_` for next time.  
  memcpy(last_audio_buffer_.get(), audio_frame->data(),  
         sizeof(int16_t) \* audio_frame->samples_per_channel_ \*  
             audio_frame->num_channels_);  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/audio_coding/neteq/neteq_impl.cc;l=834;drc=7af7400d03766f76cdc34b9ffee27178dc9430c6>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/audio_coding/neteq/neteq_impl.cc;l=2148;drc=7af7400d03766f76cdc34b9ffee27178dc9430c6>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/audio_coding/neteq/neteq_impl.cc;l=1417;drc=fd8802b593110ea18a97ef044f8a40dd24a622ec>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/audio_codecs/g711/audio_decoder_g711.cc;l=51;drc=fd8802b593110ea18a97ef044f8a40dd24a622ec>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/audio_coding/acm2/acm_receiver.cc;l=167;drc=fd8802b593110ea18a97ef044f8a40dd24a622ec>  

[6] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/audio_coding/acm2/acm_receiver.cc;l=205;drc=28a2c63526f471558bc93cdcae9fab42b84b10a5>

**VERSION**  

Chromium 95.0.4638.69 (x64.asan Build) (x86\_64)  

Chromium head cf0b23fa66619b63b2212606cd225be15f04fe05 (x64.asan Build) (x86\_64)  

Chrome 95.0.4638.69 (Release Build)(x86\_64)  

OS: Ubuntu 18.04

**REPRODUCTION CASE**

Note: Triggering this vulnerability requires an attacker client that sends malicious packets. I'm using another build of chromium as my attacker client for simplicity. The attacker client requires a renderer process patch to send malicious packers to the victim browser. No changes are required to the victim browser.

Building a VICTIM browser (chromium):

1. Build chromium with asan

Setting up the ATTACKER client:

1. fetch chromium
2. cd src && git reset --hard 95.0.4638.69
3. gclient sync
4. cd third\_party/webrtc # NOTE YOU MUST APPLY THE PATCH TO THE WEBRTC LIBRARY
5. git apply attacker.patch
6. build the release build

Setting up the webserver:

1. tar xvf server.tar.gz && cd server
2. npm install .
3. node index.js

Final Steps:

1. Run the webserver
2. Navigate the attacker browser to <http://localhost:8080/#attacker=1> and run with the flag (--autoplay-policy=no-user-gesture-required)  
   
   (attacker browser) ./out/x64.release/chrome --disk-cache-dir=/dev/null --disk-cache-size=1 --ignore-certificate-errors --user-data-dir=/home/n/.datadir/attacker --window-size=900,900 --autoplay-policy=no-user-gesture-required <http://localhost:8080/#attacker=1>  
   
   NOTE: The only flag that really matters here in the attacker browser is  `--autoplay-policy=no-user-gesture-required`. This allows the malicious client to do `.play()` on the audio element without clicking.

3.Navigate the victim browser to <http://localhost:8080/> (no flags required)  

(victim browser) ASAN\_OPTIONS=detect\_odr\_violation=0 ./out/x64.asan/chrome --ignore-certificate-errors --user-data-dir=/home/n/.datadir/victim --disable-gpu --window-size=600,800 <http://localhost:8080> 2>&1 | tools/valgrind/asan/asan\_symbolize.py  

NOTE: None of the flags here really matter. If you're running the malicious client on the same host as the victim client then you need to set --user-data-dir so they are different browser instances. However, the attacker client obviously does not need to be on the same host.

PATCH RECOMMENDATION

1. Handle the muted state in the same way we handle the unmuted state. i.e. if the number of out samples exceeds AudioFrame::kMaxDataSizeSamples set audio\_frame->num\_channels to `AudioFrame::kMaxDataSizeSamples / sync_buffer_->Channels();`

```
  // Extract data from `sync_buffer_` to `output`.  
  size_t num_output_samples_per_channel = output_size_samples_;  
  size_t num_output_samples = output_size_samples_ \* sync_buffer_->Channels();  
  if (num_output_samples > AudioFrame::kMaxDataSizeSamples) {  
    RTC_LOG(LS_WARNING) << "Output array is too short. "  
                        << AudioFrame::kMaxDataSizeSamples << " < "  
                        << output_size_samples_ << " \* "  
                        << sync_buffer_->Channels();  
    num_output_samples = AudioFrame::kMaxDataSizeSamples;  
    num_output_samples_per_channel =  
        AudioFrame::kMaxDataSizeSamples / sync_buffer_->Channels();  
  }  

```

2. Maybe add a num\_channels restriction to the PCMU decoder. However, I'm not sure if this breaks valid use cases

## Attachments

- [attacker.patch](attachments/attacker.patch) (text/plain, 3.8 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 38.9 KB)
- [server.tar.gz](attachments/server.tar.gz) (application/octet-stream, 3.8 MB)
- [asan1.txt](attachments/asan1.txt) (text/plain, 42.2 KB)
- [tmp.mp4](attachments/tmp.mp4) (video/mp4, 960.0 KB)

## Timeline

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-11-02)

[Comment Deleted]

### bt...@gmail.com (2021-11-02)

Attached a second asan stacktrace that shows the OOB write as well. This vulnerability leads to both an  OOB read and OOB write as both `last_audio_buffer_` and `audio_frame->data()` are initialized to be AudioFrame::kMaxDataSizeSamples

```
  memcpy(last_audio_buffer_.get() /* OOB WRITE */, audio_frame->data() /* OOB READ */,
         sizeof(int16_t) * audio_frame->samples_per_channel_ *
             audio_frame->num_channels_);
```

### va...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>Audio]

### va...@chromium.org (2021-11-03)

henrika@ -- can you please help triage this bug better? I'm unable to find a good owner myself. Thanks.

### he...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### hl...@chromium.org (2021-11-03)

Thanks for the excellent report!

Minyue, please assign a suitable owner.

### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-05)

Could you also help identify the earliest milestone (94+) that bug this affects? Thanks.

### bt...@gmail.com (2021-11-05)

vakh@ This bug has been in the codebase for at least 3 years. Also it appears to affect almost every other browser I've tried that uses libwebrtc.

### ad...@google.com (2021-11-11)

Setting FoundIn to the earliest relevant milesstone per https://crbug.com/chromium/1265806#c10, thanks Brendan.


### ad...@google.com (2021-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@google.com (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/4cbfe4192cd5b8289f7896ce14e0bd8c4ae41a97

commit 4cbfe4192cd5b8289f7896ce14e0bd8c4ae41a97
Author: Ivo Creusen <ivoc@webrtc.org>
Date: Tue Nov 16 11:18:10 2021

Fix out-of-bounds memory access due to large number of audio channels.

The number of audio channels can be configured in SDP, and can thus be
set to arbitrary values by an attacker. This CL fixes an out-of-bounds
memory access that could occur when the number of channels is set to a
large number.

Bug: chromium:1265806
Change-Id: Ic88ff6d85b978b8eb99bf03cc52457a4552e8c24
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/237808
Reviewed-by: Jakob Ivarsson <jakobi@webrtc.org>
Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#35354}

[modify] https://crrev.com/4cbfe4192cd5b8289f7896ce14e0bd8c4ae41a97/modules/audio_coding/neteq/neteq_impl.cc


### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd

commit d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd
Author: Ivo Creusen <ivoc@webrtc.org>
Date: Tue Nov 16 15:11:28 2021

Set the maximum number of audio channels to 24

The number of audio channels can be configured in SDP, and can thus be
set to arbitrary values. However, the audio code has limitations that
prevent a high number of channels from working well in practice.

Bug: chromium:1265806
Change-Id: I6f6c3f68a3791bb189a614eece6bd0ed7874f252
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/237807
Reviewed-by: Jakob Ivarsson <jakobi@webrtc.org>
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#35359}

[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/audio_encoder.cc
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/L16/audio_decoder_L16.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/modules/audio_coding/codecs/builtin_audio_decoder_factory_unittest.cc
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/audio_encoder.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/g711/audio_decoder_g711.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/modules/audio_coding/codecs/builtin_audio_encoder_factory_unittest.cc
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/audio_decoder.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/g711/audio_encoder_g711.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/opus/audio_decoder_multi_channel_opus_config.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/audio_decoder.cc
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/g722/audio_encoder_g722_config.h
[modify] https://crrev.com/d823259c7f1de9ceb2a79cb4e8e2d8ea043b75dd/api/audio_codecs/L16/audio_encoder_L16.h


### [Deleted User] (2021-11-16)

ivoc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### iv...@chromium.org (2021-11-16)

[Empty comment from Monorail migration]

### iv...@chromium.org (2021-11-16)

Thanks a lot for reporting this issue, and the detailed repro instructions. I have followed both of your recommendations in the CLs above, so I'm considering this fixed.

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1716b97db65bb88a0babc8c3f568e99ad4182e20

commit 1716b97db65bb88a0babc8c3f568e99ad4182e20
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 17 00:05:36 2021

Roll WebRTC from efe46b6beea9 to c09b14c3c57d (3 revisions)

https://webrtc.googlesource.com/src.git/+log/efe46b6beea9..c09b14c3c57d

2021-11-16 orphis@webrtc.org Use a FQDN hostname as an invalid hostname
2021-11-16 ivoc@webrtc.org Fix out-of-bounds memory access due to large number of audio channels.
2021-11-16 nisse@webrtc.org Delete support for has_internal_source

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Id11ead329c319d10164b925d3aaf54b23f578859
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285303
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#942341}

[modify] https://crrev.com/1716b97db65bb88a0babc8c3f568e99ad4182e20/DEPS


### [Deleted User] (2021-11-17)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### iv...@chromium.org (2021-11-17)

1. This is a high-severity security issue, so it fits the criteria for merging to stable.
2. Only this CL needs to be merged: https://webrtc-review.googlesource.com/c/src/+/237808
3. The change is included in the current canary on windows, however I don't have access to a windows machine so I'll wait for it to reach canary on mac before verifying that the solution works. This will probably happen tomorrow (I'll post an update on this bug).
4. No.
6. No manual testing necessary.

### [Deleted User] (2021-11-17)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/55248ea9aaf1f6f4c67cf3ae4004f3d424a50f1f

commit 55248ea9aaf1f6f4c67cf3ae4004f3d424a50f1f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 17 11:14:40 2021

Roll WebRTC from c09b14c3c57d to 2ae54b921b5b (7 revisions)

https://webrtc.googlesource.com/src.git/+log/c09b14c3c57d..2ae54b921b5b

2021-11-17 mbonadei@webrtc.org Make Chromium DEPS autoroller set Bot-Commit+1
2021-11-17 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision b56d8868f3..f1aab63b8b (941610:942294)
2021-11-16 orphis@webrtc.org Add more usrsctp TSAN suppressions
2021-11-16 ivoc@webrtc.org Set the maximum number of audio channels to 24
2021-11-16 philipp.hancke@googlemail.com stats collector test: remove is_remote expectations
2021-11-16 orphis@webrtc.org VSS: Fix TSAN error related to internal variables
2021-11-16 titovartem@webrtc.org Remove old definition of the macro RTC_NOTREACHED

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1260482,chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I4e66a25312f94a58c4ac3e65d20562ce06c5c853
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289052
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#942546}

[modify] https://crrev.com/55248ea9aaf1f6f4c67cf3ae4004f3d424a50f1f/DEPS


### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-11-19)

Adding some context to this issue after a conversation with ivoc@. It's still possible to trigger this even with the patches above due to a couple of peculiarities in these webrtc codepaths:

* The `IsOk()` method, used to check if the number of channels is below 24 in the patch above, is only ever DCHECKED [1]. `IsOk` failing should probably be a legitimate failure case. [1] [2] [3]

* Resampling and copying from the current audio_frame into the last_audio_buffer_ do not take audio_frame->samples_per_channel_ into consideration so we should probably just return `kFail` if `num_output_samples > AudioFrame::kMaxDataSizeSamples` in the muted codepath.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/audio_codecs/g711/audio_encoder_g711.cc;l=41;drc=59bdabfb96e4c7a0de476b24c34ff197d1fa2ce4
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/audio_codecs/g711/audio_encoder_g711.cc;l=56;drc=59bdabfb96e4c7a0de476b24c34ff197d1fa2ce4
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/audio_codecs/g711/audio_encoder_g711.cc;l=65;drc=59bdabfb96e4c7a0de476b24c34ff197d1fa2ce4

### am...@chromium.org (2021-11-19)

hi ivoc@, just checking in about item 3 in https://crbug.com/chromium/1265806#c26 
>> The change is included in the current canary on windows, however I don't have access to a windows machine so I'll wait for it to reach canary on mac before verifying that the solution works. This will probably happen tomorrow (I'll post an update on this bug).


### am...@chromium.org (2021-11-19)

Ignore my last in https://crbug.com/chromium/1265806#c31 as I was not working on an updated version of this bug; going to go ahead and reopen this issue as the issue appears to still be reproducible 

### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/624fb67bbc785cd35b78b8dc6c053d2b1874f6eb

commit 624fb67bbc785cd35b78b8dc6c053d2b1874f6eb
Author: Ivo Creusen <ivoc@webrtc.org>
Date: Tue Nov 23 17:00:51 2021

Revert "Fix out-of-bounds memory access due to large number of audio channels."

This reverts commit 4cbfe4192cd5b8289f7896ce14e0bd8c4ae41a97.

Reason for revert: The fix in this CL is ineffective. A better one has been created here: https://webrtc-review.googlesource.com/c/src/+/238666

Original change's description:
> Fix out-of-bounds memory access due to large number of audio channels.
>
> The number of audio channels can be configured in SDP, and can thus be
> set to arbitrary values by an attacker. This CL fixes an out-of-bounds
> memory access that could occur when the number of channels is set to a
> large number.
>
> Bug: chromium:1265806
> Change-Id: Ic88ff6d85b978b8eb99bf03cc52457a4552e8c24
> Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/237808
> Reviewed-by: Jakob Ivarsson <jakobi@webrtc.org>
> Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
> Cr-Commit-Position: refs/heads/main@{#35354}

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: chromium:1265806
Change-Id: If695ed92f831c2a9631efdf47f1568f5a15c1841
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238803
Reviewed-by: Ivo Creusen <ivoc@webrtc.org>
Reviewed-by: Jakob Ivarsson <jakobi@webrtc.org>
Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#35413}

[modify] https://crrev.com/624fb67bbc785cd35b78b8dc6c053d2b1874f6eb/modules/audio_coding/neteq/neteq_impl.cc


### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91f7a656fe28a6fe286ce0d3fa613b09c097b348

commit 91f7a656fe28a6fe286ce0d3fa613b09c097b348
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 24 15:43:42 2021

Roll WebRTC from a18cad9c099d to a018e677f247 (3 revisions)

https://webrtc.googlesource.com/src.git/+log/a18cad9c099d..a018e677f247

2021-11-24 cschuldt@google.com Optimize block_delay_buffer.
2021-11-24 ivoc@webrtc.org Revert "Fix out-of-bounds memory access due to large number of audio channels."
2021-11-24 phancke@nvidia.com dcsctp: assert that CreateTimeout returns a usable pointer

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I578510cb0de6299509c9a2e8ea800f4881b50aaf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3300346
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#944971}

[modify] https://crrev.com/91f7a656fe28a6fe286ce0d3fa613b09c097b348/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-26)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/deb1b1bc70e479a375dc2b0cf71d03d71719874c

commit deb1b1bc70e479a375dc2b0cf71d03d71719874c
Author: Ivo Creusen <ivoc@webrtc.org>
Date: Wed Nov 24 19:29:10 2021

Always call IsOk() to ensure audio codec configuration is valid when negotiating.

We should avoid creating codecs with invalid parameters, since this can
expose security issues. For many codecs the IsOk() method to check the
codec config is only called in DCHECKs. This CL ensures IsOk() is always
called, also in non-debug builds.

Bug: chromium:1265806
Change-Id: Ibd3c6c65d3bb547cd2603e11808ac40ac693a8b1
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238801
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#35422}

[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/isac/audio_decoder_isac_fix.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/modules/audio_coding/codecs/opus/audio_encoder_multi_channel_opus_impl.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/isac/audio_encoder_isac_float.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/modules/audio_coding/codecs/opus/audio_encoder_opus.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/L16/audio_encoder_L16.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/L16/audio_decoder_L16.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/modules/audio_coding/codecs/opus/audio_decoder_multi_channel_opus_unittest.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/g722/audio_decoder_g722.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/g722/audio_encoder_g722.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/modules/audio_coding/codecs/opus/audio_encoder_multi_channel_opus_unittest.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/g711/audio_decoder_g711.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/g711/audio_encoder_g711.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/isac/audio_encoder_isac_fix.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/isac/audio_decoder_isac_float.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/ilbc/audio_decoder_ilbc.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/ilbc/audio_encoder_ilbc.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/opus/audio_decoder_opus.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/api/audio_codecs/opus/audio_encoder_opus.cc
[modify] https://crrev.com/deb1b1bc70e479a375dc2b0cf71d03d71719874c/modules/audio_coding/codecs/opus/audio_decoder_multi_channel_opus_impl.cc


### gi...@appspot.gserviceaccount.com (2021-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab7ab73dcfbf83caa4d0a63a5ee3ed580bb71252

commit ab7ab73dcfbf83caa4d0a63a5ee3ed580bb71252
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 26 13:08:02 2021

Roll WebRTC from 789a0f361f42 to deb1b1bc70e4 (1 revision)

https://webrtc.googlesource.com/src.git/+log/789a0f361f42..deb1b1bc70e4

2021-11-26 ivoc@webrtc.org Always call IsOk() to ensure audio codec configuration is valid when negotiating.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Ifdc6be422f22a09268f7e5453488be90e8c48bf0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3303147
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#945606}

[modify] https://crrev.com/ab7ab73dcfbf83caa4d0a63a5ee3ed580bb71252/DEPS


### am...@chromium.org (2021-11-29)

hi ivoc@, please update as fixed if this issue has been resolved by the latest commit, thank you

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/d58ac5adf887a2bc96d75b1c0fb6fef17889ac80

commit d58ac5adf887a2bc96d75b1c0fb6fef17889ac80
Author: Philipp Hancke <phancke@nvidia.com>
Date: Thu Nov 25 07:57:54 2021

sdp: reject large number of channels

the maximum used in practice is multiopus with
6 or 8 channels. 24 is the maximum number of channels
supported in the audio decoder.

BUG=chromium:1265806

Change-Id: Iba8e3185a1f235b846fed9c154e66fb3983664ed
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238980
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Philipp Hancke <phancke@nvidia.com>
Cr-Commit-Position: refs/heads/main@{#35440}

[modify] https://crrev.com/d58ac5adf887a2bc96d75b1c0fb6fef17889ac80/pc/webrtc_sdp_unittest.cc
[modify] https://crrev.com/d58ac5adf887a2bc96d75b1c0fb6fef17889ac80/pc/webrtc_sdp.cc


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e29115c06f518667454262c4ec6d3f47505b0e41

commit e29115c06f518667454262c4ec6d3f47505b0e41
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 30 16:05:42 2021

Roll WebRTC from 6c167d8278a2 to d58ac5adf887 (1 revision)

https://webrtc.googlesource.com/src.git/+log/6c167d8278a2..d58ac5adf887

2021-11-30 phancke@nvidia.com sdp: reject large number of channels

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I8dbb5ff3e7dc5a5676eac29d1319f2517b160ab1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3308863
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#946473}

[modify] https://crrev.com/e29115c06f518667454262c4ec6d3f47505b0e41/DEPS


### iv...@chromium.org (2021-11-30)

I have applied 2 new fixes, both of them stop this issue from occurring (in my testing). Philipp has also updated the SDP code to reflect the new restriction on the number of audio channels. I'm going to mark this as fixed now, I will try to verify that the issue is fixed on canary tomorrow.

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/500d6e7f142fddbcc2a6e04a76471eed15efa988

commit 500d6e7f142fddbcc2a6e04a76471eed15efa988
Author: Ivo Creusen <ivoc@webrtc.org>
Date: Wed Nov 24 12:32:07 2021

Return kSampleUnderrun if the number of samples does not fit in an AudioFrame.

If the number of samples does not fit in an AudioFrame, we should return
kSampleUnderrun to avoid crashes further downstream.

Bug: chromium:1265806
Change-Id: Ie94e1de53810167fd9b52ade72b3cb669a2a4f06
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238666
Reviewed-by: Jakob Ivarsson <jakobi@webrtc.org>
Reviewed-by: Ivo Creusen <ivoc@webrtc.org>
Commit-Queue: Ivo Creusen <ivoc@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#35459}

[modify] https://crrev.com/500d6e7f142fddbcc2a6e04a76471eed15efa988/modules/audio_coding/neteq/neteq_impl.cc
[modify] https://crrev.com/500d6e7f142fddbcc2a6e04a76471eed15efa988/modules/audio_coding/neteq/neteq_impl_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc853f9f44892e8808993c724d30d0ef5f4ba804

commit cc853f9f44892e8808993c724d30d0ef5f4ba804
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 02 15:19:51 2021

Roll WebRTC from 258ed1a38ad9 to 4ad09762daa9 (2 revisions)

https://webrtc.googlesource.com/src.git/+log/258ed1a38ad9..4ad09762daa9

2021-12-02 danilchap@webrtc.org Delete legacy RtpPacketSendInfo::ssrc field
2021-12-02 ivoc@webrtc.org Return kSampleUnderrun if the number of samples does not fit in an AudioFrame.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1265806
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I2e9bb531dbc0930fca14c07b01136a19c23eaac6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3313192
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#947480}

[modify] https://crrev.com/cc853f9f44892e8808993c724d30d0ef5f4ba804/DEPS


### am...@chromium.org (2021-12-02)

hi ivoc@ re: https://crbug.com/chromium/1265806#c40: have you verified these fixes on canary? I don't see any issues these on canary (in terms of crashes/stability issues) based on my queries, but want to ensure that this issue is resolve and would like to approve this for merge for 96, which would need to occur by EOD today so these fixes can be included in next week's stable channel refresh. Thanks! 

### ph...@googlemail.com (2021-12-02)

i've verified the CL from https://crbug.com/chromium/1265806#c38 on 98.0.4740.0 -- applies cleanly to the M96 branch too.

### iv...@chromium.org (2021-12-02)

I haven't been able to test canary, since I only have access to a linux machine, and there is no canary for linux. I tried to reproduce the issue with one party remotely, but was not able to do this. 

I have been able to reproduce the issue locally with my own Chromium builds, where I can reproduce the crash on stable, and cannot reproduce the crash with either of these patches applied.

### bt...@gmail.com (2021-12-02)

[Comment Deleted]

### bt...@gmail.com (2021-12-02)

I checked and the fix appears to have worked on Canary. Here's a video of what happens on stable vs canary from a remote host.

### am...@chromium.org (2021-12-02)

Thanks, ivoc@ and Brendon!
Since the most complicated set of fixes has been on canary presumably for at least six days now (commit deb1b1bc70e479a375dc2b0cf71d03d71719874c) and I'm not seeing anything on Canary that is indicating any stability issues or other concerns with any of these commits, I'm going to go ahead and approve merge to M96. 
ivoc@, if you can confirm and if there are no issues or concerns from your end, let's go ahead and get this merged into M96, branch 4664, ASAP/by EOD today (Thursday) so this set of fixes can be included in tomorrow's stable cut and ship in next week's stable refresh. 
Please let me know if there are any issues with this. 


### am...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-02)

forgot to add to above, once you confirm is set for M96, also can get this into M97, branch 4692, at your earliest convenience, but M96 is the priority right now given the deadlines for stable cut. Thanks! 

### ph...@googlemail.com (2021-12-02)

amyressler: given timezone constraints that seems unlikely.
https://webrtc-review.googlesource.com/c/src/+/239740
is reasonably small and should disable the attack vector. Shall I (with my nvidia hat on)?

### iv...@chromium.org (2021-12-03)

I think it makes sense to merge Philipp's CL to stable, instead of mine, since it is fairly small and simple. I've verified earlier today that just Philipp's CL by itself fixes the issue, so this should be fine.

### am...@chromium.org (2021-12-03)

Hi Philipp, apologies I didn't see your earlier message yesterday. ivoc@ I concur with merging https://webrtc-review.googlesource.com/c/src/+/239740 to stable/m96, please go ahead and get this into the web-rtc autoroll so this can get into M96 stable cut which should be happening soon. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/809830f1b39f9d0933dd979c9e8f32a4a922b71c

commit 809830f1b39f9d0933dd979c9e8f32a4a922b71c
Author: Philipp Hancke <phancke@nvidia.com>
Date: Thu Nov 25 07:57:54 2021

[merge to M96] sdp: reject large number of channels

the maximum used in practice is multiopus with
6 or 8 channels. 24 is the maximum number of channels
supported in the audio decoder.

BUG=chromium:1265806
(cherry picked from commit d58ac5adf887a2bc96d75b1c0fb6fef17889ac80)

No-Try: True
Change-Id: Iba8e3185a1f235b846fed9c154e66fb3983664ed
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238980
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Philipp Hancke <phancke@nvidia.com>
Cr-Original-Commit-Position: refs/heads/main@{#35440}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/239740
Commit-Queue: Mirko Bonadei <mbonadei@webrtc.org>
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4664@{#3}
Cr-Branched-From: 40abb7d8ff6ebdb8095d372c18949940c5fcecb5-refs/heads/main@{#35164}

[modify] https://crrev.com/809830f1b39f9d0933dd979c9e8f32a4a922b71c/pc/webrtc_sdp_unittest.cc
[modify] https://crrev.com/809830f1b39f9d0933dd979c9e8f32a4a922b71c/pc/webrtc_sdp.cc


### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, Brendon! The VRP Panel has decided to award you $8500 for this report, including a suggested patch bonus. Thank you for this excellent report and your efforts!

### ad...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### pb...@google.com (2021-12-07)

Your change has been approved for M97 branch 4692,please go ahead and merge the CL's to M97 branch manually asap so that they would be part of tomorrows Beta release.thank you

### [Deleted User] (2021-12-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/8ad555b18228a1e667578d04c5e52c067b3cd1e7

commit 8ad555b18228a1e667578d04c5e52c067b3cd1e7
Author: Philipp Hancke <phancke@nvidia.com>
Date: Thu Nov 25 07:57:54 2021

[merge to M97] sdp: reject large number of channels

the maximum used in practice is multiopus with
6 or 8 channels. 24 is the maximum number of channels
supported in the audio decoder.

BUG=chromium:1265806
(cherry picked from commit d58ac5adf887a2bc96d75b1c0fb6fef17889ac80)

No-Try: True
Change-Id: Iba8e3185a1f235b846fed9c154e66fb3983664ed
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/238980
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Philipp Hancke <phancke@nvidia.com>
Cr-Original-Commit-Position: refs/heads/main@{#35440}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/240180
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4692@{#2}
Cr-Branched-From: c276aee4eda7b1a466b139838f20e790bd746309-refs/heads/main@{#35313}

[modify] https://crrev.com/8ad555b18228a1e667578d04c5e52c067b3cd1e7/pc/webrtc_sdp_unittest.cc
[modify] https://crrev.com/8ad555b18228a1e667578d04c5e52c067b3cd1e7/pc/webrtc_sdp.cc


### he...@chromium.org (2021-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### bt...@gmail.com (2022-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1265806?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2025-05-21)

Project: src  

Branch: main  

Author: Tommi <[tommi@webrtc.org](mailto:tommi@webrtc.org)>  

Link:      <https://webrtc-review.googlesource.com/392380>

Add stricter checks for valid NetEq configs.

---


Expand for full commit details
```
Add stricter checks for valid NetEq configs. 
 
This is a step towards moving config checks away from the audio path and 
closer to the initial config/construction path. Construction of decoder 
instances is similarly more rigorously checked. 
 
* NetEq can no longer accept 1000 audio channels as a valid config. 
  (see NoCrashWith1000Channels test) 
* Improve checking for valid configurations when constructing 
  encoders/decoders. The checks are now more aligned with the 
  limits of the internal classes such as NetEqImpl and AudioFrame 
  rather than e.g. using a value of 255 for channel count. 
* Consolidate constant definitions of "max number of audio channels". 
  This CL adds one constant with a default value of 24. 
* Updating similar constants for encoders and decoders to refer to 
  that value. 
* Updating AudioFrame to use the new value for sanity checking. 
  Since AudioFrame has public member variables, those checks were 
  being, and continue to be, bypassed unfortunately, but this is 
  some progress. 
 
Bug: chromium:335805780, chromium:40057791 
Change-Id: Ib015d1223f2c3fc00c66a831b1fa851fa50a940d 
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/392380 
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
Reviewed-by: Per Åhgren <peah@webrtc.org> 
Reviewed-by: Jakob Ivarsson‎ <jakobi@webrtc.org> 
Cr-Commit-Position: refs/heads/main@{#44718}

```

---

Files:

- M `api/audio/audio_frame.cc`
- M `api/audio/audio_frame.h`
- M `api/audio/audio_view.h`
- M `api/audio_codecs/BUILD.gn`
- M `api/audio_codecs/audio_decoder.cc`
- M `api/audio_codecs/audio_decoder.h`
- M `api/audio_codecs/audio_encoder.cc`
- M `api/audio_codecs/audio_encoder.h`
- M `api/audio_codecs/opus/BUILD.gn`
- M `api/audio_codecs/opus/audio_decoder_multi_channel_opus_config.h`
- M `api/audio_codecs/opus/audio_encoder_multi_channel_opus_config.cc`
- M `api/audio_codecs/opus/audio_encoder_opus_config.cc`
- M `api/audio_codecs/test/audio_decoder_factory_template_unittest.cc`
- M `modules/audio_coding/codecs/g711/audio_decoder_pcm.h`
- M `modules/audio_coding/codecs/g711/audio_encoder_pcm.cc`
- M `modules/audio_coding/codecs/pcm16b/audio_decoder_pcm16b.cc`
- M `modules/audio_coding/neteq/audio_multi_vector.cc`
- M `modules/audio_coding/neteq/audio_multi_vector.h`
- M `modules/audio_coding/neteq/neteq_impl.cc`
- M `modules/audio_coding/neteq/neteq_impl.h`
- M `modules/audio_coding/neteq/neteq_impl_unittest.cc`
- M `modules/audio_coding/neteq/neteq_network_stats_unittest.cc`
- M `modules/audio_mixer/BUILD.gn`
- M `modules/audio_mixer/frame_combiner_unittest.cc`
- M `pc/BUILD.gn`
- M `pc/webrtc_sdp.cc`

---

Hash: 969486666bcec6690066a3e883b97081934396a7  

Date:  Wed May 21 15:55:38 2025


---

### dx...@google.com (2025-05-21)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6576987>

Roll WebRTC from ca21f9e2de5a to 1cb2ef0e0605 (10 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/ca21f9e2de5a..1cb2ef0e0605 
     
    2025-05-21 apehrson@mozilla.com Make SckPickerProxy thread-safe with a Mutex 
    2025-05-21 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision eb2ed5afec..963e5bc411 (1463392:1463586) 
    2025-05-21 danilchap@webrtc.org Remove unused mention of InitFieldTrialsFromString in media unittests 
    2025-05-21 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision c1450c64cd..eb2ed5afec (1463258:1463392) 
    2025-05-21 tommi@webrtc.org Add stricter checks for valid NetEq configs. 
    2025-05-21 tommi@webrtc.org [AudioProcessingImpl] Don't use AudioFrameView with aec dump 
    2025-05-21 phancke@meta.com Improve SDP SCTP handling 
    2025-05-21 solenberg@webrtc.org Remove system_wrappers/../sleep.* 
    2025-05-21 hta@webrtc.org Expand pc/webrtc_sdp.cc OWNERS 
    2025-05-21 danilchap@webrtc.org Avoid global field trial string in audio processing fuzzer 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:335805780,chromium:40057791,chromium:409777951,chromium:417930289 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I2c2355181c1395b779ee4dd4737ee013f2cb7b7e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6576987 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1463757}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: 8b68941ce511b35e68f9e7a2b69271c5aad2c5b2  

Date:  Wed May 21 22:24:37 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057791)*
