# AddressSanitizer: heap-use-after-free on media::SCKAudioInputStream::Start

| Field | Value |
|-------|-------|
| **Issue ID** | [346692546](https://issues.chromium.org/issues/346692546) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Audio |
| **Platforms** | Mac |
| **Chrome Version** | 125.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2024-06-12 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. host poc.html <http://localhost:8000/poc.html>
2. npm install puppeteer-core and node run.js (remember replace the launchCommand to your chromium path)

# Problem Description

0. There is an object-c block function in `SCKAudioInputStream:: Start`, and the block function uses the member `shared_helper_` of `SCKAudioInputStream`. Therefore, if you run this block function before
   This is destroyed, which means that the `SCKAudioInputStream` class is destroyed. When calling `shared_helper_ ->OnStreamError (error)`, `shared\_helper\_ will implicitly capture this dereference, causing UAF. because
   The block function will be dispatched to a separate thread in Macos.

```
void SCKAudioInputStream::Start(AudioInputCallback* callback) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  CHECK(callback);

  // Don't do anything if the stream isn't open and ignore any consecutive
  // Start() calls.
  if (!stream_ || sink_) {
    return;
  }

  sink_ = callback;

  // Sample and error callbacks are set and reset by SCKAudioInputStream when
  // starting and stopping the stream, respectively. Thus, |this| will always be
  // valid if the callback is not null.
  shared_helper_->SetStreamCallbacks(
      base::BindRepeating(&SCKAudioInputStream::OnStreamSample,
                          base::Unretained(this)),
      base::BindRepeating(&SCKAudioInputStream::OnStreamError,
                          base::Unretained(this)));

  [stream_ startCaptureWithCompletionHandler:^(NSError* error) {
    if (!error) {
      return;
    }

    shared_helper_->OnStreamError(error); //<--- uaf here
  }];
}

```

1. `SCKAudioInputStream` is created in `AudioManagerBase:: MakeAudioInputStream`, then insert into `input_streams_`, and `MakeAudioInputStrea` returns this stream.

```
AudioInputStream* AudioManagerBase::MakeAudioInputStream(
    const AudioParameters& input_params,
    const std::string& device_id,
    const LogCallback& log_callback) {
...

  AudioInputStream* stream;
  switch (params.format()) {
    case AudioParameters::AUDIO_PCM_LINEAR:
      stream = MakeLinearInputStream(params, device_id, log_callback);
      break;
    case AudioParameters::AUDIO_PCM_LOW_LATENCY:
      stream = MakeLowLatencyInputStream(params, device_id, log_callback); // <---- create
      break;
    case AudioParameters::AUDIO_FAKE:
      stream = FakeAudioInputStream::MakeFakeStream(this, params);
      break;
    default:
      stream = nullptr;
      break;
  }

  if (stream) {
    input_streams_.insert(stream); // insert
    if (!log_callback.is_null()) {
      SendLogMessage(log_callback, "%s => (number of streams=%d)", __func__,
                     input_stream_count());
    }

...
}

```

2. Closed in `InputStream::~InputStream`

```
InputStream::~InputStream()
    InputController::Close()
        SCKAudioInputStream::Close()

```

3. Call `close_callback` in `SCKAudioInputStream:: Close()`, and the close\_callback is passed in when `SCKAudioInputStream` is created

```
AudioInputStream* AudioManagerMac::MakeLowLatencyInputStream(
    const AudioParameters& params,
    const std::string& device_id,
    const LogCallback& log_callback) {
  DCHECK(GetTaskRunner()->BelongsToCurrentThread());
  DCHECK_EQ(AudioParameters::AUDIO_PCM_LOW_LATENCY, params.format());

  if (AudioDeviceDescription::IsLoopbackDevice(device_id)) {
    screen_capture_kit_swizzler_ = SwizzleScreenCaptureKit();

    return CreateSCKAudioInputStream(
        params, device_id, log_callback,
        base::BindRepeating(&AudioManagerBase::ReleaseInputStream,
                            base::Unretained(this))); 
  }

```

4. `AudioManagerBase::ReleaseInputStream` Erase `this` and then delete this(stream)

```
void AudioManagerBase::ReleaseInputStream(AudioInputStream* stream) {
  CHECK(GetTaskRunner()->BelongsToCurrentThread());
  DCHECK(stream);
  // TODO(xians) : Have a clearer destruction path for the AudioInputStream.
  CHECK_EQ(1u, input_streams_.erase(stream));
  delete stream;
}

```

5. `InputStream` is created and held by `StreamFactory`.

```
void StreamFactory::CreateInputStream(
...

  input_streams_.insert(std::make_unique<InputStream>(
      std::move(created_callback), std::move(deleter_callback),
      std::move(stream_receiver), std::move(client), std::move(observer),
      std::move(pending_log), audio_manager_, aecdump_recording_manager_,
      UserInputMonitor::Create(std::move(key_press_count_buffer)),
#if BUILDFLAG(CHROME_WIDE_ECHO_CANCELLATION)
      output_device_mixer_manager_.get(), std::move(processing_config),
#else
      nullptr, nullptr,
#endif
      device_id, params, shared_memory_count, enable_agc));
}

```

6. So when `StreamFactory` is destroyed, the destruction of `StreamFactory` ultimately leads to the destruction of `SCKAudioInputStream`. And the `StreamFactory` lifecycle is bound to one endpoint of the browser. So when the browser disconnects one end of Mojo, the Service is destroyed.

bitset: <https://source.chromium.org/chromium/chromium/src/+/eed1c5f6d99764cf0eb93b0108a14af9e287ccda>

Note: The reason for the patch is that I don't know how to sign and how to attach TCC permissions to the programme

# Summary

AddressSanitizer: heap-use-after-free on media::SCKAudioInputStream::Start

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see asan.txt

#### Reporter credit:

lime(limeSe) and fmyy(@binary\_fmyy) From TIANGONG Team of Legendsec at QI-ANXIN Group

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 19.4 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 683 B)
- [uaf-asan.txt](attachments/uaf-asan.txt) (text/plain, 25.8 KB)
- [run.js](attachments/run.js) (text/javascript, 990 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.6 KB)
- [main.html](attachments/main.html) (text/html, 622 B)
- main.html (text/html, 622 B)

## Timeline

### li...@gmail.com (2024-06-13)

Sorry , it seems that i forget to upload poc named `main.html` , and make a mistake upload the asan.txt ,it not related with this bug, so could you please delete it ? thanks.

### li...@gmail.com (2024-06-13)

and update the credit to : lime(@limeSec\_) and fmyy(@binary\_fmyy) From TIANGONG Team of Legendsec at QI-ANXIN Group, thanks.

### da...@chromium.org (2024-06-13)

The ASAN stack is clear. The objc block function needs to hold a WeakPtr on `this` as there's nothing notifying it when `this` is destroyed.

The function block was introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/4727729> in September. So FoundIn includes extended stable.

### da...@chromium.org (2024-06-13)

Attempting to see what process this UAF is happening in, I see that CreateInputStream() is called from the browser process over mojo, and looks to be in a sandboxed process with `RequireContext=sandbox.mojom.Context.kPrivilegedUtility` if `IsAudioServiceOutOfProcess()` is true: <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/audio/audio_service.cc;l=148;drc=90cac1911508d3d682a67c97aa62483eb712f69a> On mac, it should be true by default: <https://source.chromium.org/chromium/chromium/src/+/main:content/public/common/content_features.cc;l=40;drc=90cac1911508d3d682a67c97aa62483eb712f69a>

So that makes this S1 instead of S0.

### li...@gmail.com (2024-06-13)

Hi, team ,
From the patch point of view, I think the key to this Vulnerability is that the block implicitly captures this. If we don't use this member, this problem will be solved very well. Refer to my patch, which works well.

### li...@gmail.com (2024-06-13)

Because this block is currently almost asynchronous, we are not sure whether WeakPtr is competing with the main thread. If it is in the same thread, then WeakPtr will play a good role.

### pe...@google.com (2024-06-13)

Setting milestone because of s0/s1 severity.

### av...@chromium.org (2024-06-13)

The block refers to `shared_helper_`, which is implicitly `this->shared_helper_`, so it captures `this_` which might be out of scope, as the OP correctly notes.

However, `shared_helper_` is a `scoped_refptr`, so if the function containing the block were to make a local copy:

```
  // ...

  auto local_shared_helper = shared_helper_;

  [stream_ startCaptureWithCompletionHandler:^(NSError* error) {
    if (!error) {
      return;
    }

    local_shared_helper->OnStreamError(error);
  }];

```

then the local `scoped_refptr` variable would be copied by the block, not the `this`.

I don’t know this code in order to say if the block holding a shared ref to the helper would lead to an OK situation, but making local copies of class-owned variables for capture by blocks is a common Objective-C pattern.

### ap...@google.com (2024-06-17)

Project: chromium/src
Branch: main

commit d54105311590b41164bcd8e8d81edac187cf5690
Author: mark a. foltz <mfoltz@chromium.org>
Date:   Mon Jun 17 23:07:32 2024

    [SCK] Retain refptr to shared helper to prevent UAF.
    
    Capture a reference to the shared helper in the onerror handler to
    prevent a UAF that can occur when the browser drops the mojo
    connection.
    
    Bug: 346692546
    Change-Id: Ifb264488a6fa8417c134a34d902605d2c141720b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5634908
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1316145}

M       media/audio/mac/audio_loopback_input_mac_impl.mm

https://chromium-review.googlesource.com/5634908


### li...@gmail.com (2024-06-20)

Hi，team，i see that this vulnerability has been fixed, so can it be marked as `fixed` asap? thanks. :)

### pe...@google.com (2024-06-21)

Requesting merge to stable (M126) because latest trunk commit (1316145) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1316145) appears to be after beta branch point (1313161).
Merge review required: M126 is already shipping to stable.

Merge review required: M127 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-06-25)

https://crrev.com/c/5634908 approved for merges to M126 and M127
please merge this fix to M127 branch 5633 by EOD today so this fix can be included in tomorrow's update of M127 beta 

M126 Stable update for this week has already shipped and we are entering into a two week release freeze; please merge this fix to M126 Stable (branch 6478) at your convenience so this fix can be included in the next M126 Stable update following release freeze

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$2,000 for moderately mitigated security bug in sandboxed process + $1,000 patch bonus, + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations lime and fmyy --thank you for your efforts and reporting this issue to us as well as a patch! 

### li...@gmail.com (2024-06-27)

Thank you, Amy.

### pe...@google.com (2024-07-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-07-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2024-07-08)

Please land your merges before COP Tuesday to ensure it is included in this weeks Beta release.

For gitwatcher to update your merge request to Merge-Merged you will need to **include the bug id in the commit message**.


### mf...@chromium.org (2024-07-10)

I'm not sure who requested the merges here, but it wasn't me :)

### am...@chromium.org (2024-07-12)

It's automated for security issues. Since this is fix for a security bug, the fix needs to be backmerged to Beta M127 (which is being cut for Stable RC for release the following week on 15 July) and Stable M126, which has a planned respin being released on 16 July. Please ensure these merges are completed by EOD tomorrow (Friday, 12 July ) so this fix can be included in both.

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 904d41df7e2347fe9655702a1ff4a1fdc433c613
Author: mark a. foltz <mfoltz@chromium.org>
Date:   Mon Jul 15 10:15:43 2024

    [SCK] Retain refptr to shared helper to prevent UAF.
    
    Capture a reference to the shared helper in the onerror handler to
    prevent a UAF that can occur when the browser drops the mojo
    connection.
    
    (cherry picked from commit d54105311590b41164bcd8e8d81edac187cf5690)
    
    Bug: 346692546
    Change-Id: Ifb264488a6fa8417c134a34d902605d2c141720b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5634908
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316145}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5704440
    Reviewed-by: Daniel Yip <danielyip@google.com>
    Commit-Queue: Daniel Yip <danielyip@google.com>
    Cr-Commit-Position: refs/branch-heads/6533@{#1468}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       media/audio/mac/audio_loopback_input_mac_impl.mm

https://chromium-review.googlesource.com/5704440


### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: refs/branch-heads/6478

commit b81363139f411f8fe3ec42ece0847cddd460dca4
Author: mark a. foltz <mfoltz@chromium.org>
Date:   Mon Jul 15 10:28:34 2024

    [SCK] Retain refptr to shared helper to prevent UAF.
    
    Capture a reference to the shared helper in the onerror handler to
    prevent a UAF that can occur when the browser drops the mojo
    connection.
    
    (cherry picked from commit d54105311590b41164bcd8e8d81edac187cf5690)
    
    Bug: 346692546
    Change-Id: Ifb264488a6fa8417c134a34d902605d2c141720b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5634908
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316145}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5704253
    Reviewed-by: Daniel Yip <danielyip@google.com>
    Commit-Queue: Daniel Yip <danielyip@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1769}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       media/audio/mac/audio_loopback_input_mac_impl.mm

https://chromium-review.googlesource.com/5704253


### pe...@google.com (2024-09-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346692546)*
