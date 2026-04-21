# Security: heap-use-after-free on AudioManagerWin

| Field | Value |
|-------|-------|
| **Issue ID** | [40065022](https://issues.chromium.org/issues/40065022) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>Audio |
| **Platforms** | Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | tg...@chromium.org |
| **Created** | 2023-05-30 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DETAILS
## Bisect
Based on the analysis with bisect, it was determined that the vulnerability was introduced by this commit: https://source.chromium.org/chromium/chromium/src/+/0b4125c58738e6fc1339a5ffffc4fb4e644d9e5a
```
Handle audio device changes on Windows.

Uses the new AudioDeviceListener framework to notify of device
changes.  Handles only default device changes at the moment,
e.g., not manually changing the sample rate, etc on a current
default device.

This all works well enough that I can connect / disconnect remote
desktop sessions with and without audio and everything continues
to play seamlessly and in sync!

BUG=153056
TEST=Unplug... Plug... Unplug! Plug!

Review URL: https://codereview.chromium.org/11233023
```

## RCA
This vulnerability was discovered by my fuzzer, so although I provided some patches and UI interactions for reproduction purposes, it is clearly a non-interactive out-of-sandbox Use-After-Free vulnerability. 
The detailed root cause is as follows:

### Allocation

The allocation process of AudioManager is as follows, and it is created in the UI thread (T0).
The Service holds an OwningAudioManagerAccessor, and the OwningAudioManagerAccessor holds the AudioManager.

```text
#1 media::CreateAudioManager \src\media\audio\win\audio_manager_win.cc:434
#2 media::AudioManager::Create \src\media\audio\audio_manager.cc:116
#3 audio::OwningAudioManagerAccessor::GetAudioManager \src\services\audio\owning_audio_manager_accessor.cc:139
#4 audio::Service::Service \src\services\audio\service.cc:58
#5 audio::CreateStandaloneService \src\services\audio\service_factory.cc:32
#6 content::`anonymous namespace'::RunAudio \src\content\utility\services.cc:249
#7 mojo::ServiceFactory::RunService \src\mojo\public\cpp\bindings\service_factory.cc:35
#8 content::UtilityThreadImpl::HandleServiceRequest \src\content\utility\utility_thread_impl.cc:219
```

### Free

When the browser is closed, the `Service` will be destructed, and the corresponding `OwningAudioManagerAccessor` will also be released.

Therefore, AudioManagerWin will be freed at the end of `Service::~Service`.

The destruction process of AudioManager is as follows.

```text
#0 operator delete+0x8d (\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004ef7d)
#1 media::AudioManagerWin::~AudioManagerWin \src\media\audio\win\audio_manager_win.cc:116
#2 audio::OwningAudioManagerAccessor::~OwningAudioManagerAccessor \src\services\audio\owning_audio_manager_accessor.cc:128
#3 audio::OwningAudioManagerAccessor::~OwningAudioManagerAccessor \src\services\audio\owning_audio_manager_accessor.cc:125
#4 audio::Service::~Service \src\services\audio\service.cc:86
#5 audio::Service::~Service \src\services\audio\service.cc:72
#8 mojo::ServiceFactory::OnInstanceDisconnected \src\mojo\public\cpp\bindings\service_factory.cc:52
#9 mojo::ServiceFactory::InstanceHolderBase::OnPipeSignaled \src\mojo\public\cpp\bindings\service_factory.cc:83
#10 mojo::SimpleWatcher::OnHandleReady \src\mojo\public\cpp\system\simple_watcher.cc:278
```

More specifically, when the `Service` is destructing, it sequentially performs [1][2][3].
It would reset the `output_device_listener_` on the `AudioManager`, and then immediately releases the `AudioManager` in [4].

```cpp
Service::~Service() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  TRACE_EVENT0("audio", "audio::Service::~Service");

  // Stop all streams cleanly before shutting down the audio manager.
  stream_factory_.reset();

  // Reset |debug_recording_| to disable debug recording before AudioManager
  // shutdown.
  debug_recording_.reset();

  audio_manager_accessor_->Shutdown();   // <-------------- [1] 
}                                       // <--------------- [4]
void OwningAudioManagerAccessor::Shutdown() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  if (audio_manager_)
    audio_manager_->Shutdown();
  audio_manager_factory_cb_ = AudioManagerFactoryCallback();
}

bool AudioManager::Shutdown() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);

  if (audio_thread_->GetTaskRunner()->BelongsToCurrentThread()) {
    // If this is the audio thread, there is no need to check if it's hung
    // (since it's clearly not). https://crbug.com/919854.
    ShutdownOnAudioThread();  // <------------------ [2]
  } else {
    ...
  }
  audio_thread_->Stop();
  shutdown_ = true;
  return true;
}

void AudioManagerWin::ShutdownOnAudioThread() {
  AudioManagerBase::ShutdownOnAudioThread();

  // Destroy AudioDeviceListenerWin instance on the audio thread because it
  // expects to be constructed and destroyed on the same thread.
  output_device_listener_.reset();  // <------------------ [3]
}
```

### Use

However, there is a race window here.

If we switch the audio output device before executing `audio_manager_accessor_->Shutdown()` [1], causing the UI thread to create an `AudioManager::NotifyAllOutputDeviceChangeListeners` callback task and allowing the UI thread to execute this callback task after the `AudioManager` was destructed, it will result in a Use after free vulnerability.

```text
#0 base::ObserverList<media::AudioManager::AudioDeviceListener,0,1,base::internal::UncheckedObserverAdapter>::begin \src\base\observer_list.h:246
#1 media::AudioManagerBase::NotifyAllOutputDeviceChangeListeners \src\media\audio\audio_manager_base.cc:499
#2 base::TaskAnnotator::RunTaskImpl \src\base\task\common\task_annotator.cc:186
```

Specifically, when we click on the audio output device on the Windows taskbar and switch it, the AudioDeviceListenerWin::OnDefaultDeviceChanged callback will be immediately executed on the UI thread through the MMDeviceAPI:

```c++
HRESULT AudioDeviceListenerWin::OnDefaultDeviceChanged(
    EDataFlow flow,
    ERole role,
    LPCWSTR new_default_device_id) {
  ...

  // Only output device changes should be forwarded.  Do not attempt to filter
  // changes based on device id since some devices may not change their device
  // id and instead trigger some internal flow change: http://crbug.com/506712
  //
  // We rate limit device changes to avoid a single device change causing back
  // to back changes for eCommunications and eConsole; this is worth doing as
  // it provides a substantially faster resumption of playback.
  bool did_run_listener_cb = false;
  const base::TimeTicks now = tick_clock_->NowTicks();
  if (flow == eRender && (now - last_device_change_time_ > kDeviceChangeLimit ||
                          new_device_id.compare(last_device_id_) != 0)) {
    last_device_change_time_ = now;
    last_device_id_ = new_device_id;

    listener_cb_.Run();  // <---------------- [5]
    
    did_run_listener_cb = true;
  }

  ...
  return S_OK;
}
```

The UI thread will immediately execute the aforementioned function and call `listener_cb_.Run()` [5], where `listener_cb_` actually refers to `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` registed in [6].

```cpp
void AudioManagerWin::InitializeOnAudioThread() {
  DCHECK(GetTaskRunner()->BelongsToCurrentThread());

  // AudioDeviceListenerWin must be initialized on a COM thread.
  output_device_listener_ = std::make_unique<AudioDeviceListenerWin>(
      base::BindPostTaskToCurrentDefault(base::BindRepeating(
          &AudioManagerWin::NotifyAllOutputDeviceChangeListeners,   // <---------- [6]
          base::Unretained(this))));
}
```

However, executing `listener_cb_.Run()` immediately **does not necessarily mean** that `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` will be executed immediately.
There may be an implicit effect similar to `PostTask`, where the actual function to be executed will be scheduled to run on the UI thread when it becomes idle.

Therefore, as long as `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` is executed by the UI thread after `AudioManagerWin` is freed, it can trigger a Use After Free (UAF) vulnerability.

VERSION
Chrome Version: 116.0.5800.0 + [stable, dev, and canary]
Operating System: only Windows

TestOn: asan-win32-release_x64-1150200, Version 116.0.5800.0 (Developer Build) (64-bit), Window 10
Download From Here: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-1150200

REPRODUCTION CASE
1. Apply repro.diff in chromium src and compile (tested commit: c9dbb548a945f7dbd4e8f41ff9e7da9cfe638bd7)
2. Run `chrome.exe --user-data-dir=userdir --no-sandbox D:\poc.html` and wait for the output of `Debug in AudioManagerWin::ShutdownOnAudioThread before sleep`
3. Upon seeing that output, within 10 seconds, click on the Windows taskbar to switch the audio output device. After a successful switch, Chrome will output "Debug in AudioDeviceListenerWin::OnDefaultDeviceChanged before cb."
4. Wait for a few seconds, and the ASAN log will occurs.

FOR GIT DIFF FILE
The diff file contains three parts:
1. The first part modifies `build/config/clang/clang.gni` by changing `enable_check_raw_ptr_fields`. This modification is made to **avoid Chrome compilation errors** and has **no impact on the vulnerability**.
2. The second part adds a significant amount of LOG(ERROR) output for debugging and understanding the vulnerability.
3. The final part **adds Sleep(10s) in the AudioManagerWin::ShutdownOnAudioThread() function**. This is done to increase the race window, making it easier to switch the audio output device and trigger the vulnerability.

OTHER
Since this vulnerability was discovered by the fuzzer, it should not need to switch the sound card in the reproduction, but only need to trigger the event of changing the default output device in other ways.
I'm not sure whether the browser must be closed to trigger the release of the audio service, I leave it to you to judge.
Since it happens in a audio process outside the sandbox, this should be a high-severity bug.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 1.4 MB)
- [repro.diff](attachments/repro.diff) (text/plain, 12.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 332 B)
- [execution_and_asan_log_in_c9dbb5.txt](attachments/execution_and_asan_log_in_c9dbb5.txt) (text/plain, 18.9 KB)
- [asan_log_in_asan-win32-release_x64-1150200.txt](attachments/asan_log_in_asan-win32-release_x64-1150200.txt) (text/plain, 10.9 KB)
- [asan_log_in_asan-win32-release_x64-1150200.txt](attachments/asan_log_in_asan-win32-release_x64-1150200.txt) (text/plain, 10.9 KB)
- [execution_and_asan_log_in_c9dbb5.txt](attachments/execution_and_asan_log_in_c9dbb5.txt) (text/plain, 18.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 332 B)
- [repro.diff](attachments/repro.diff) (text/plain, 12.2 KB)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 1.4 MB)
- [asan.log](attachments/asan.log) (text/plain, 10.9 KB)

## Timeline

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-05-30)

VULNERABILITY DETAILS
## Bisect
Based on the analysis with bisect, it was determined that the vulnerability was introduced by this commit: https://source.chromium.org/chromium/chromium/src/+/0b4125c58738e6fc1339a5ffffc4fb4e644d9e5a
```
Handle audio device changes on Windows.

Uses the new AudioDeviceListener framework to notify of device
changes.  Handles only default device changes at the moment,
e.g., not manually changing the sample rate, etc on a current
default device.

This all works well enough that I can connect / disconnect remote
desktop sessions with and without audio and everything continues
to play seamlessly and in sync!

BUG=153056
TEST=Unplug... Plug... Unplug! Plug!

Review URL: https://codereview.chromium.org/11233023
```

## RCA
This vulnerability was discovered by my fuzzer, so although I provided some patches and UI interactions for reproduction purposes, it is clearly a non-interactive out-of-sandbox Use-After-Free vulnerability. 
The detailed root cause is as follows:

### Allocation

The allocation process of AudioManager is as follows, and it is created in the UI thread (T0).
The Service holds an OwningAudioManagerAccessor, and the OwningAudioManagerAccessor holds the AudioManager.

```text
#1 media::CreateAudioManager \src\media\audio\win\audio_manager_win.cc:434
#2 media::AudioManager::Create \src\media\audio\audio_manager.cc:116
#3 audio::OwningAudioManagerAccessor::GetAudioManager \src\services\audio\owning_audio_manager_accessor.cc:139
#4 audio::Service::Service \src\services\audio\service.cc:58
#5 audio::CreateStandaloneService \src\services\audio\service_factory.cc:32
#6 content::`anonymous namespace'::RunAudio \src\content\utility\services.cc:249
#7 mojo::ServiceFactory::RunService \src\mojo\public\cpp\bindings\service_factory.cc:35
#8 content::UtilityThreadImpl::HandleServiceRequest \src\content\utility\utility_thread_impl.cc:219
```

### Free

When the browser is closed, the `Service` will be destructed, and the corresponding `OwningAudioManagerAccessor` will also be released.

Therefore, AudioManagerWin will be freed at the end of `Service::~Service`.

The destruction process of AudioManager is as follows.

```text
#0 operator delete+0x8d (\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004ef7d)
#1 media::AudioManagerWin::~AudioManagerWin \src\media\audio\win\audio_manager_win.cc:116
#2 audio::OwningAudioManagerAccessor::~OwningAudioManagerAccessor \src\services\audio\owning_audio_manager_accessor.cc:128
#3 audio::OwningAudioManagerAccessor::~OwningAudioManagerAccessor \src\services\audio\owning_audio_manager_accessor.cc:125
#4 audio::Service::~Service \src\services\audio\service.cc:86
#5 audio::Service::~Service \src\services\audio\service.cc:72
#8 mojo::ServiceFactory::OnInstanceDisconnected \src\mojo\public\cpp\bindings\service_factory.cc:52
#9 mojo::ServiceFactory::InstanceHolderBase::OnPipeSignaled \src\mojo\public\cpp\bindings\service_factory.cc:83
#10 mojo::SimpleWatcher::OnHandleReady \src\mojo\public\cpp\system\simple_watcher.cc:278
```

More specifically, when the `Service` is destructing, it sequentially performs [1][2][3].
It would reset the `output_device_listener_` on the `AudioManager`, and then immediately releases the `AudioManager` in [4].

```cpp
Service::~Service() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  TRACE_EVENT0("audio", "audio::Service::~Service");

  // Stop all streams cleanly before shutting down the audio manager.
  stream_factory_.reset();

  // Reset |debug_recording_| to disable debug recording before AudioManager
  // shutdown.
  debug_recording_.reset();

  audio_manager_accessor_->Shutdown();   // <-------------- [1] 
}                                       // <--------------- [4]
void OwningAudioManagerAccessor::Shutdown() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  if (audio_manager_)
    audio_manager_->Shutdown();
  audio_manager_factory_cb_ = AudioManagerFactoryCallback();
}

bool AudioManager::Shutdown() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);

  if (audio_thread_->GetTaskRunner()->BelongsToCurrentThread()) {
    // If this is the audio thread, there is no need to check if it's hung
    // (since it's clearly not). https://crbug.com/919854.
    ShutdownOnAudioThread();  // <------------------ [2]
  } else {
    ...
  }
  audio_thread_->Stop();
  shutdown_ = true;
  return true;
}

void AudioManagerWin::ShutdownOnAudioThread() {
  AudioManagerBase::ShutdownOnAudioThread();

  // Destroy AudioDeviceListenerWin instance on the audio thread because it
  // expects to be constructed and destroyed on the same thread.
  output_device_listener_.reset();  // <------------------ [3]
}
```

### Use

However, there is a race window here.

If we switch the audio output device before executing `audio_manager_accessor_->Shutdown()` [1], causing the UI thread to create an `AudioManager::NotifyAllOutputDeviceChangeListeners` callback task and allowing the UI thread to execute this callback task after the `AudioManager` was destructed, it will result in a Use after free vulnerability.

```text
#0 base::ObserverList<media::AudioManager::AudioDeviceListener,0,1,base::internal::UncheckedObserverAdapter>::begin \src\base\observer_list.h:246
#1 media::AudioManagerBase::NotifyAllOutputDeviceChangeListeners \src\media\audio\audio_manager_base.cc:499
#2 base::TaskAnnotator::RunTaskImpl \src\base\task\common\task_annotator.cc:186
```

Specifically, when we click on the audio output device on the Windows taskbar and switch it, the AudioDeviceListenerWin::OnDefaultDeviceChanged callback will be immediately executed on the UI thread through the MMDeviceAPI:

```c++
HRESULT AudioDeviceListenerWin::OnDefaultDeviceChanged(
    EDataFlow flow,
    ERole role,
    LPCWSTR new_default_device_id) {
  ...

  // Only output device changes should be forwarded.  Do not attempt to filter
  // changes based on device id since some devices may not change their device
  // id and instead trigger some internal flow change: http://crbug.com/506712
  //
  // We rate limit device changes to avoid a single device change causing back
  // to back changes for eCommunications and eConsole; this is worth doing as
  // it provides a substantially faster resumption of playback.
  bool did_run_listener_cb = false;
  const base::TimeTicks now = tick_clock_->NowTicks();
  if (flow == eRender && (now - last_device_change_time_ > kDeviceChangeLimit ||
                          new_device_id.compare(last_device_id_) != 0)) {
    last_device_change_time_ = now;
    last_device_id_ = new_device_id;

    listener_cb_.Run();  // <---------------- [5]
    
    did_run_listener_cb = true;
  }

  ...
  return S_OK;
}
```

The UI thread will immediately execute the aforementioned function and call `listener_cb_.Run()` [5], where `listener_cb_` actually refers to `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` registed in [6].

```cpp
void AudioManagerWin::InitializeOnAudioThread() {
  DCHECK(GetTaskRunner()->BelongsToCurrentThread());

  // AudioDeviceListenerWin must be initialized on a COM thread.
  output_device_listener_ = std::make_unique<AudioDeviceListenerWin>(
      base::BindPostTaskToCurrentDefault(base::BindRepeating(
          &AudioManagerWin::NotifyAllOutputDeviceChangeListeners,   // <---------- [6]
          base::Unretained(this))));
}
```

However, executing `listener_cb_.Run()` immediately **does not necessarily mean** that `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` will be executed immediately.
There may be an implicit effect similar to `PostTask`, where the actual function to be executed will be scheduled to run on the UI thread when it becomes idle.

Therefore, as long as `AudioManagerWin::NotifyAllOutputDeviceChangeListeners` is executed by the UI thread after `AudioManagerWin` is freed, it can trigger a Use After Free (UAF) vulnerability.

VERSION
Chrome Version: 116.0.5800.0 + [stable, dev, and canary]
Operating System: only Windows

TestOn: asan-win32-release_x64-1150200, Version 116.0.5800.0 (Developer Build) (64-bit), Window 10
Download From Here: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-1150200

REPRODUCTION CASE
1. Apply repro.diff in chromium src and compile (tested commit: c9dbb548a945f7dbd4e8f41ff9e7da9cfe638bd7)
2. Run `chrome.exe --user-data-dir=userdir --no-sandbox D:\poc.html` and wait for the output of `Debug in AudioManagerWin::ShutdownOnAudioThread before sleep`
3. Upon seeing that output, within 10 seconds, click on the Windows taskbar to switch the audio output device. After a successful switch, Chrome will output "Debug in AudioDeviceListenerWin::OnDefaultDeviceChanged before cb."
4. Wait for a few seconds, and the ASAN log will occurs.

FOR GIT DIFF FILE
The diff file contains three parts:
1. The first part modifies `build/config/clang/clang.gni` by changing `enable_check_raw_ptr_fields`. This modification is made to **avoid Chrome compilation errors** and has **no impact on the vulnerability**.
2. The second part adds a significant amount of LOG(ERROR) output for debugging and understanding the vulnerability.
3. The final part **adds Sleep(10s) in the AudioManagerWin::ShutdownOnAudioThread() function**. This is done to increase the race window, making it easier to switch the audio output device and trigger the vulnerability.

OTHER
Since this vulnerability was discovered by the fuzzer, it should not need to switch the sound card in the reproduction, but only need to trigger the event of changing the default output device in other ways.
I'm not sure whether the browser must be closed to trigger the release of the audio service, I leave it to you to judge.
Since it happens in a audio process outside the sandbox, this should be a high-severity bug.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)


### ct...@chromium.org (2023-06-02)

Thanks for the report. I'm updating my windows build to be able to test out your patch and repro case and will update this bug once I've been able to reproduce.

Meanwhile a quick question: Are you able to reproduce without the `--no-sandbox` flag?

### ki...@gmail.com (2023-06-02)

re https://crbug.com/chromium/1449929#c3:
Since removing --no-sandbox will prevent the output of ASan logs, I included that parameter. However, since this vulnerability is only related to AudioManagerWin, I don't believe the sandbox will affect this vulnerability. Please leave it to the developers to make further assessments.

### ki...@gmail.com (2023-06-02)

I submitted the reproduction video as repro.mkv, but it seems that this format cannot be viewed online. Can you see it?

### ct...@chromium.org (2023-06-02)

Yeah I don't think Monorail supports displaying MKV files, but I was able to upload it to Drive to view it -- here's a private link for others on this bug: https://drive.google.com/file/d/1ghahvyZMUET8uMxyMbiGuQdoWl19filP/view?usp=sharing

### aj...@google.com (2023-06-06)

I notice in your patch that you disable raw_ptr - this is now enabled on all Chrome channels - does your poc still repro with raw_ptr enabled?

Severity: high but needs racing and user interaction -> medium but... likely protected by raw_ptr -> low

-> dalecurtis from linked CL & owners

[Monorail components: Internals>Media>Audio]

### aj...@google.com (2023-06-06)

(+ Windows as you have to click the taskbar)

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-06-06)

Hmm, IIRC the expectation is that the AudioManager should live as long as the process lives. I'm surprised the service task runner is still running tasks after destroying the service. If that's the case we probably need to use WeakPtr for quite a few cases of callbacks in the AudioManager and audio service.

cc: rockot in case this is unexpected.

### da...@chromium.org (2023-06-06)

Looks like only Mac, Win need a small fix if we need to do this:
https://source.chromium.org/search?q=file:audio_manager%20Unretained%20-mock%20-file:unittest.cc&ss=chromium

Neither Android nor Fuschia use out of process audio, so they're unaffected -- though we may want to fix their instances at the same time.

Alternatively we can just leak the audio manager accessor at service shutdown if we feel this is WAI.

### ki...@gmail.com (2023-06-06)

re https://crbug.com/chromium/1449929#c7:
Disabling the raw_ptr protection was solely because I couldn't compile it with that option enabled. I have attached the earliest ASAN log produced by the fuzzer running on the downloaded ASAN release.

The user interaction was only meant to make it easier for you to reproduce the vulnerability. Since the vulnerability was discovered by a fuzzer without any UI interaction, I believe there might be other ways to trigger this issue.

Additionally, according to https://crbug.com/chromium/1449929#c11 and https://crbug.com/chromium/1449929#c12, it seems that this is not just a single trigger point.

Perhaps you should consider marking it as a medium priority and let the developers decide whether to downgrade it.

Thank you

### ki...@gmail.com (2023-06-07)

Moreover, enable_check_raw_ptr_fields does not affect vulnerabilities because it is a compile-time check that restricts developers from using raw pointers directly and encourages the use of raw<T> instead. After the code is compiled, this check no longer has any effect, and it does not impact the chrome code logic.

The Chrome commit 2492c170cfeef2a40cb4ac1c69b293523857efc5 (dated 2023-05-30 15:21) reverted the usage of enable_check_raw_ptr_fields on the Windows platform due to build failures it caused. And our diff actually did the same thing as this commit.

### ct...@chromium.org (2023-06-07)

Bumping this to Severity-Medium as this does not appear to meet our criteria for being protected by MiraclePtr per our severity guidelines [1]. I previously managed to get the patch working without setting enable_check_raw_ptr_fields = false (iirc there was a brief period where trunk was broken when linking with raw_ptr enabled that maybe affected the reporter). As this appears to affect Stable/Extended Stable (the root cause analysis, if correct, is quite old), this should still be considered unprotected.

[1]: https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-miracleptr states that only M115 and above are protected

### ct...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-06-07)

I doubt this is exploitable or user controllable, but defer to security experts.

### aj...@google.com (2023-06-08)

re https://crbug.com/chromium/1449929#c18 - we still treat shutdown uafs as security issues but with significantly less priority than web-controllable ones - so it would be good to have the fixes outlined in https://crbug.com/chromium/1449929#c12.

### da...@chromium.org (2023-06-08)

Handing over to Thomas to make the call on leaking or fixing with a few WeakPtrs here. Olga, did you have an opinion?

### ol...@chromium.org (2023-06-09)

Theoretically WeakPtrs would be more consistent: there might be some edge cases with leaking when we have not closed devices correctly, for example. So intuitively I like it more. On the other hand, we kill the process "on hang" here and there without any clean shutdowns. So as I don't have specific pointers to back up my "intuition", I defer to Thomas.

### da...@chromium.org (2023-06-09)

In the leak case, I was thinking we'd still run the shutdown sequence which has CHECK()s which ensure streams are shutdown.

There may be other things that need WeakPtr, but the streams being CHECK()'d at least means they don't, so it might be as simple as just replacing the sites in c#12.

### da...@chromium.org (2023-06-09)

There are other comments like here that make me worried it'd be a game of whack'a'mole though:
https://source.chromium.org/chromium/chromium/src/+/main:media/audio/audio_system_impl.cc;l=16;drc=c48b37ef88433de45e376652b33904542f82ea29

### ki...@gmail.com (2023-06-13)

Hello, is there still active? Thanks!

### [Deleted User] (2023-06-13)

tguilbert: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tg...@chromium.org (2023-06-22)

RE https://crbug.com/chromium/1449929#c23 - I thought that raw_ptr offers UAF protection (or will offer when it's fully turned on). The file in https://crbug.com/chromium/1449929#c23 should be covered then? I think (but I don't know for sure) that base::Unretained(this) is also internally stored as a raw_ptr(this) and offers/will-offer the same protection.

WeakPtrs and threading is tricky, and I have to re-read their documentation every time. I think that, if it's correct, the WeakPtr solution doesn't look too bad:
https://chromium-review.googlesource.com/c/chromium/src/+/4635284

I think there is a WeakPtr threading issue with the existing code on Mac, which was never an actual issue because InitializeOnAudioThread() always completes before we attempt to destroy AudioManagerMac. `weak_ptr_factory_.GetWeakPtr()` is dereferenced on the audio thread, when `weak_ptr_factory_` is destroyed/invalidated on the owning sequence. Using base::Unretained(this) doesn't pretend to be safe at least:
https://chromium-review.googlesource.com/c/chromium/src/+/4635284/1/media/audio/mac/audio_manager_mac.cc#b526

I also think it's impossible to use WeakPtrs to remove the use of base::Unretained(this) for the InitializedOnAudioThread() calls, both on Windows and Mac. We'll never be able to invalidate the WeakPtrFactory on the audio thread before it's destroyed on the owning sequence.

Can we assume we will at least run InitializeOnAudioThread before attempting to destroy the audio managers? If the answer is no, we would need a more complicated solution to manage this lifetime.

I haven't looked into the leaking option for now, as using WeakPtrs seemed like a better starting point to me.

### ol...@chromium.org (2023-06-22)

The bug description calls the main thread of the audio process "UI", but for our purpose it's what's called "audio" thread by AudioManager, and also it's the thread receiving mojo IPC, and also it's the owning sequence of AudioManager.

When we run the audio service in a separate process, the main thread of the process is the audio thread, and 
on Win InitializeOnAudioThread() will be called in the constructor. This should be like that in all production Chrome [1]. Unfortunately we still have kAudioServiceOutOfProcess feature around, since it's used in a number of tests.

I'm not entirely sure we need to post InitializeOnAudioThread() on Mac when we run the audio process either.

>> I think there is a WeakPtr threading issue with the existing code on Mac
Probably https://crbug.com/chromium/1350414 is caused by it.

I'm thinking if we can clean up kAudioServiceOutOfProcess feature, we may stop caring about cases where the owning sequence of AudioManager and the audio thread are two different entities. And until then we can fix the audio process case using WeakPtr and probably just let AudioManager leak when kAudioServiceOutOfProcess is off (this one [2]): we do already leak it if shutdown fails [3]

WDYT?

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_main_loop.cc;l=1560
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_main_loop.h;l=370
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_main_loop.cc;drc=22201befd595c4413fdfa85df57cb5e839a42ac3;bpv=1;bpt=1;l=1226

### tg...@chromium.org (2023-06-22)

Thank you for the clarification, that is very helpful. I did not know the "main" thread was the same as the audio thread in the out of process case.

>> Probably https://crbug.com/chromium/1350414 is caused by it.
Yes, that seems very plausible.

Removing that flag seems like a good idea, if possible. I will open a tracking bug for that effort and update my CL according. I will do this work on Monday, as I ran out of time due to upcoming OOO.

Leaking seems ok, only when kAudioServiceOutOfProcess is off, which I now understand to not be the case in production often (ever?).

### ol...@chromium.org (2023-06-26)

>> Removing that flag seems like a good idea, if possible. 
We have a canary/dev experiment using this feature running on CrOS. I believe we should shut it down shortly, but Per is OOO at the moment. We can try to remove the flag on Win/Mac/Linux for now (it was a bit tricky last time I looked at it).


>> Leaking seems ok, only when kAudioServiceOutOfProcess is off, which I now understand to not be the case in production often (ever?).
The service runs in the browser process on CrOS (% that canary/dev experiment) and Android. We have not seen lifetime issues there, right? We may choose to leak only on Win/Mac/Linux, to be on the safe side.

### tg...@chromium.org (2023-06-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6363e1f7cc84dc9011fd34ede922b95783e268d0

commit 6363e1f7cc84dc9011fd34ede922b95783e268d0
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Wed Jun 28 23:22:31 2023

Use WeakPtrs with AudioDeviceListenerWin

There is a potential race condition on shutdown if there is a device
change as AudioManagerWin is destroyed.

This CL fixes the issue by using WeakPtrs. The use of WeakPtrs is nuanced and intentional here, to accommodate for different threading
situations:
- When the audio service is run out of process, there is no issue,
as there is only one thread, and WeakPtrs can be used without
afterthought.
- When the audio service is run in process, there is a main thread on
which the AudioManagerWin is created & destroyed, and the Audio thread
on which the AudioManagerWin operates. We make sure to allocate and invalidate WeakPtrs on the audio thread, before the WeakPtrFactory
is destroyed on the main thread, to avoid threading issues.

crbug.com/1458623 will aim to remove kAudioServiceOutOfProcess and
simplify this by only running audio out of process.

Bug: 1449929
Change-Id: I1d73e47cd4819dea4e154d8b5d52d59afd270171
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4635284
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1163850}

[modify] https://crrev.com/6363e1f7cc84dc9011fd34ede922b95783e268d0/media/audio/win/audio_manager_win.h
[modify] https://crrev.com/6363e1f7cc84dc9011fd34ede922b95783e268d0/media/audio/win/audio_manager_win.cc


### ki...@gmail.com (2023-07-02)

Hi, since the vulnerability has been fixed, can this report be marked as fixed. Thanks!

### tg...@chromium.org (2023-07-06)

I believe this is fixed, but I was not able to verify it.

I am unable to make ASAN crash without the change, following the instructions in https://crbug.com/chromium/1449929#c2. I do not see the "AudioDeviceListenerWin::OnDefaultDeviceChanged before cb" line appear: default device changes did not seem to be reported while we sleep in the AudioManagerWin destructor.

@kip... Could you verify that the fuzzers no longer run into this issue?

### ki...@gmail.com (2023-07-06)

Hi @tguil...

I've been running fuzzer consistently for a long time on the latest version and so far I haven't met this issue again.

I'll leave fuzzer running for a while.

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

Requesting merge to beta M115 because latest trunk commit (1163850) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1163850) appears to be after dev branch point (1160321).

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Merge review required: M115 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce56698a434b4f78dde34c943a9e6fa5159b77a6

commit ce56698a434b4f78dde34c943a9e6fa5159b77a6
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Thu Jul 06 21:13:07 2023

[M116] Use WeakPtrs with AudioDeviceListenerWin

There is a potential race condition on shutdown if there is a device
change as AudioManagerWin is destroyed.

This CL fixes the issue by using WeakPtrs. The use of WeakPtrs is nuanced and intentional here, to accommodate for different threading
situations:
- When the audio service is run out of process, there is no issue,
as there is only one thread, and WeakPtrs can be used without
afterthought.
- When the audio service is run in process, there is a main thread on
which the AudioManagerWin is created & destroyed, and the Audio thread
on which the AudioManagerWin operates. We make sure to allocate and invalidate WeakPtrs on the audio thread, before the WeakPtrFactory
is destroyed on the main thread, to avoid threading issues.

crbug.com/1458623 will aim to remove kAudioServiceOutOfProcess and
simplify this by only running audio out of process.

(cherry picked from commit 6363e1f7cc84dc9011fd34ede922b95783e268d0)

Bug: 1449929
Change-Id: I1d73e47cd4819dea4e154d8b5d52d59afd270171
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4635284
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1163850}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4670845
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Thomas Guilbert <tguilbert@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#354}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/ce56698a434b4f78dde34c943a9e6fa5159b77a6/media/audio/win/audio_manager_win.h
[modify] https://crrev.com/ce56698a434b4f78dde34c943a9e6fa5159b77a6/media/audio/win/audio_manager_win.cc


### tg...@chromium.org (2023-07-06)

I do not know if this fix is critical/impactful enough to clear the bar for being merged back to M115. That being said, answers to Sheriff bot.

1. Which CLs should be backmerged? (Please include Gerrit links.)
- https://chromium-review.googlesource.com/c/chromium/src/+/4635284

2. Has this fix been tested on Canary?
- Tested on ToT, and on ASAN fuzzers, per https://crbug.com/chromium/1449929#c35.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
- This should not pose stability risks or regressions. If there were any issues, they would happen during browser shutdown, which should not be visible to users. However, to verify this, we would need to assess the changes on a bigger population after it's released with the next M116.

4. Does this fix pose any known compatibility risks?
- No

5. Does it require manual verification by the test team? If so, please describe required testing.
- No

### am...@chromium.org (2023-07-10)

Thanks for the above tguilbert@ 
Given the preconditions and lack of attacker control and low exploitability potential of this bug + that the requested backmerge is to M115 (on which MiraclePtr is enabled across relevant platforms), this doesn't seem to meet the security bar for backmerge (the bot isn't sentient enough to understand the MiraclePtr impact here :) ...yet). Erring on the side of caution and am declining to approve this for backmerge for now. Removing M115 backmerge request label. LMK if there are any disagreements with this call. 

### tg...@chromium.org (2023-07-10)

That seems like the right call. Thanks!

### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Congratulations, Zhenghang Xiao! The VRP Panel has decided to award you $4,000 for this high-quality report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your effort in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-24)

[Description Changed]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1449929?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1458623]
[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-05-15)

deleted

### ap...@google.com (2024-05-22)

Project: chromium/src
Branch: refs/branch-heads/6478

commit f9ea2265267c653ce0c789662b527b17af022eac
Author: Olga Sharonova <olka@chromium.org>
Date:   Wed May 22 12:57:51 2024

    [M126] Use weak_ptr<AudioManagerMac> to configure AudioDeviceListenerMac
    
    See the bug and https://g-issues.chromium.org/issues/40065022#comment33
    
    (cherry picked from commit 6d95935f83b1296e45c7f4cc2b64108a81865601)
    
    Bug: 340178596,40065022
    Change-Id: I02402519d4f73d035cd3b7a0f3f04ce353f755fd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5538281
    Reviewed-by: Fredrik Hernqvist <fhernqvist@google.com>
    Commit-Queue: Fredrik Hernqvist <fhernqvist@google.com>
    Auto-Submit: Olga Sharonova <olka@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1301300}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5554599
    Commit-Queue: Olga Sharonova <olka@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#423}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       media/audio/mac/audio_manager_mac.cc

https://chromium-review.googlesource.com/5554599


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065022)*
