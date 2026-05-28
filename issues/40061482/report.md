# Security: UAF in MultiplexEncoderFactory

| Field | Value |
|-------|-------|
| **Issue ID** | [40061482](https://issues.chromium.org/issues/40061482) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2022-10-26 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**

Typical iterator invalidation bug. If a reallocation happens[a], all iterators, pointers and references related to the container are invalidated. Then access to the iterators will trigger the UAF[b].

```
std::vector<SdpVideoFormat> MultiplexEncoderFactory::GetSupportedFormats()  
    const {  
  std::vector<SdpVideoFormat> formats = factory_->GetSupportedFormats();  
  for (const auto& format : formats) {        // ------------------------>> [b]  
    if (absl::EqualsIgnoreCase(format.name, kMultiplexAssociatedCodecName)) {  
      SdpVideoFormat multiplex_format = format;  
      multiplex_format.parameters[cricket::kCodecParamAssociatedCodecName] =  
          format.name;  
      multiplex_format.name = cricket::kMultiplexCodecName;  
      formats.push_back(multiplex_format);    // ------------------------>> [a]  
      break;  
    }  
  }  
  return formats;  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/media/engine/multiplex_codec_factory.cc;l=53;drc=2b781bf9080ab7070b67f8ce8429ce7191e200ef>

**VERSION**  

Chrome Version: stable with WebRTC-MultiplexCodec feature  

Operating System: test on Win & linux

Bisect:  

<https://source.chromium.org/chromium/chromium/src/+/501897f108fb1a191103f309be78e7b853a572fb>  

<https://source.chromium.org/chromium/_/webrtc/src.git/+/0a375470334181d13f78f249b34351a418450ffd>

**REPRODUCTION CASE**

$ python3 -m http.server 8000  

$ out/asan/chrome.exe --user-data-dir=xxxx --enable-features=WebRTC-MultiplexCodec "<http://localhost:8000/poc.html>" --no-sandbox

(use no-sandbox to log renderer process asan trace)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer process  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 40.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 73 B)

## Timeline

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5293014416293888.

### me...@chromium.org (2022-10-26)

ilnik, could you PTAL?

[Monorail components: Blink>WebRTC]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### il...@chromium.org (2022-10-28)

Yes, this looks like a real bug.

The impact is minimal, since it requires an experimental, not rolled anywhere feature.
I'm working on a fix.

### il...@chromium.org (2022-10-28)

The report has link to a wrong piece of code.

This is happening in MultiplexDecoderFactory [1], not MultiplexEncoderFactory.

The latter doesn't have the UAF, because there's a |break| after new entry is pushed into the |format| vector.


[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/media/engine/multiplex_codec_factory.cc;l=82;drc=2b781bf9080ab7070b67f8ce8429ce7191e200ef

### il...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### il...@chromium.org (2022-10-28)

Updating severity and impact accordingly. 

meacer@, Am I understanding the guildelines [1] correctly here?
The code in question is executed only behind a disabled feature, so the impact is none.
The bug is read UAF, so I believe it's a medium severity.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

### le...@gmail.com (2022-10-28)

c7:
Yes, it is happening in MultiplexDecoderFactory. The code structure is somewhat similar, sorry I confused them when I wrote this issue.

### gi...@appspot.gserviceaccount.com (2022-10-28)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/aa8f28d082bfb33b9e6464aee329678510772d7a

commit aa8f28d082bfb33b9e6464aee329678510772d7a
Author: Ilya Nikolaevskiy <ilnik@webrtc.org>
Date: Fri Oct 28 09:07:45 2022

Fix UAF in MultiplexDecoderFactory::GetSupportedFormats

Bug: chromium:1378571
Change-Id: I01f105a2f2820af440cf64c654b321f34186d7e0
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/280961
Commit-Queue: Ilya Nikolaevskiy <ilnik@webrtc.org>
Auto-Submit: Ilya Nikolaevskiy <ilnik@webrtc.org>
Reviewed-by: Erik Språng <sprang@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#38493}

[modify] https://crrev.com/aa8f28d082bfb33b9e6464aee329678510772d7a/media/engine/multiplex_codec_factory.cc


### il...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e93ebed39efd2f30646b4318de6a7f11cc59c733

commit e93ebed39efd2f30646b4318de6a7f11cc59c733
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Oct 28 16:53:25 2022

Roll WebRTC from d393543110cb to 8fe5579136c8 (3 revisions)

https://webrtc.googlesource.com/src.git/+log/d393543110cb..8fe5579136c8

2022-10-28 eshr@webrtc.org Ensure video frame buffer is still decodable before decoding
2022-10-28 ilnik@webrtc.org Fix UAF in MultiplexDecoderFactory::GetSupportedFormats
2022-10-28 eshr@webrtc.org Remove "Using FrameBuffer3" log

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

Bug: chromium:1361623,chromium:1378253,chromium:1378571
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Iec56563bcd3e39c026d2d241cb4ecc01a908165e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3988582
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1064886}

[modify] https://crrev.com/e93ebed39efd2f30646b4318de6a7f11cc59c733/DEPS


### [Deleted User] (2022-10-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Leecraso! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1378571?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061482)*
