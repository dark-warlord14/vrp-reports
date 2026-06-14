# heap-use-after-free heap-use-after-free media\audio\audio_renderer_mixer_manager.cc:228 in blink::AudioRendererMixerManager::ReturnMixer

| Field | Value |
|-------|-------|
| **Issue ID** | [328918906](https://issues.chromium.org/issues/328918906) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2024-03-11 |
| **Bounty** | $8,000.00 |

## Description

#TESTON
asan-win32-release\_x64-1267730

#REPRODUCTION CASE
chrome --no-sandbox --user-data-dir=test --enable-logging=stderr poc.html

#NOTE
testharnessreport.js and testharness.js are from the WPT test suite, and you can replace them yourself.

#RCA
DCHECK is only working on Debug version

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc;drc=35bdb2d7ebf66673ed376cb2a7214cab10ee9a92;l=223
  // If a mixer isn't in the normal map, check the map for mixers w/ errors.
  bool dead_mixer = false;
  if (it == mixers_.end()) {
    it = base::ranges::find(
        dead_mixers_, mixer,
        [](const std::pair<MixerKey, AudioRendererMixerReference>& val) {
          return val.second.mixer;
        });
    DCHECK(it != dead_mixers_.end());
    dead_mixer = true;
  }

```

## Attachments

- [abe.png](attachments/abe.png) (image/png, 12.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 19.1 KB)
- [poc.html](attachments/poc.html) (text/html, 3.4 KB)
- [test.ogv](attachments/test.ogv) (video/ogg, 143.1 KB)
- [testharness.js](attachments/testharness.js) (text/javascript, 181.6 KB)
- [testharnessreport.js](attachments/testharnessreport.js) (text/javascript, 2.2 KB)
- [fixpatch.diff](attachments/fixpatch.diff) (text/x-diff, 715 B)

## Timeline

### m....@gmail.com (2024-03-11)

Please delete my previous report（[https://issues.chromium.org/issues/329003647）](https://issues.chromium.org/issues/329003647%EF%BC%89). I have modified the affected component, and its bug type has changed to default. I didn't pay attention to that.

### m....@gmail.com (2024-03-11)

Bisct:
<https://chromium-review.googlesource.com/c/chromium/src/+/5331283>

### m....@gmail.com (2024-03-11)

#FIX PATCH
It seems like triggering DCHECK should be an extreme exceptional case, so I think the patch can either change DCHECK to CHECK or simply return without any processing, and both options are acceptable.

```
diff --git a/third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc b/third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc
index 0e0229c0c3c4..a6e57ed45d24 100644
--- a/third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc
+++ b/third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc
@@ -220,7 +220,7 @@ void AudioRendererMixerManager::ReturnMixer(media::AudioRendererMixer* mixer) {
         [](const std::pair<MixerKey, AudioRendererMixerReference>& val) {
           return val.second.mixer;
         });
-    DCHECK(it != dead_mixers_.end());
+    CHECK(it != dead_mixers_.end());
     dead_mixer = true;
   }

```

### m....@gmail.com (2024-03-11)

Correcting the reproduction steps provided earlier, the poc need to be loaded via HTTP serve.
python -m http.server 8000
chrome --no-sandbox --user-data-dir=test --enable-logging=stderr http://localhost:8000/poc.html

### cl...@appspot.gserviceaccount.com (2024-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5166882306326528.

### pe...@google.com (2024-03-12)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-12)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mf...@chromium.org (2024-03-12)

The repro case uses --no-sandbox, which is not a configuration we ship to end users. I don't think this is a P1.

### da...@chromium.org (2024-03-12)

Thanks, this patch has already been reverted from 123. I'll take a look and ensure this is fixed in 124.

### ap...@google.com (2024-03-12)

Project: chromium/src
Branch: main

commit 5d2c44cd485e4593beec1842953b154d547208cd
Author: Dale Curtis <dalecurtis@chromium.org>
Date:   Tue Mar 12 23:57:46 2024

    Fix collision issues when mixers w/ the same key have errors.
    
    The code was using a map, but we may end up with many mixers with
    the same key having errors, which would cause the wrong one to be
    leaked. We instead need to keep a list of these.
    
    R=tguilbert
    
    Fixed: 328918906
    Change-Id: I4936d88f02dfde3187e0bccf19cd82dafe678161
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5368316
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1271889}

M       third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.cc
M       third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager.h
M       third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_manager_test.cc

https://chromium-review.googlesource.com/5368316


### pe...@google.com (2024-03-20)

Not requesting merge to dev (M124) because latest trunk commit (1271889) appears to be prior to dev branch point (1274542). If this is incorrect please remove NA-124 from the 'Merge' field and add 124 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of renderer process memory corruption + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### pe...@google.com (2024-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328918906)*
