# Android Chrome: Out of bound in Vulkan Samsung driver

| Field | Value |
|-------|-------|
| **Issue ID** | [401546699](https://issues.chromium.org/issues/401546699) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Android |
| **Chrome Version** | 133.0.0.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2025-03-08 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Run chrome browser in android
2. Open poc.html
3. Check crash log using "adb logcat -b crash"

# Problem Description

When Android Chrome compiles a shader using the Vulkan driver, a crash occurs in the vulkan.samsung.so driver. Specifically, the function `sub_185855C` seems to trigger an overflow under certain conditions. Below is the relevant code snippet:

```
__int64 __fastcall sub_185855C(__int64 a1, __int64 a2, _QWORD *a3, const void *a4, __int64 a5, size_t length)
{
  ...
    if ( length ) // [1]
    {
      v39 = (void *)(*(__int64 (__fastcall **)(_QWORD, size_t, __int64, __int64))(a1 + 16))( // [2]
                      *(_QWORD *)(a1 + 8),
                      length,
                      16LL,
                      0x80000001LL);
      if ( !v39 )
      {
        (*(void (__fastcall **)(_QWORD, __int64))(a1 + 24))(*(_QWORD *)(a1 + 8), v38);
        return (unsigned int)-4;
      }
      v40 = v39;
      if ( a4 )
        memcpy(v39, a4, length); // [3]
    }
  ...
}

```

- The function `sub_185855C` takes length as its final parameter. The first parameter appears to be similar to a this pointer.
- At [1], it checks if `length` is nonzero.
- At [2], it allocates `length` bytes of memory and stores the pointer in `v39`.
- At [3], it calls `memcpy(v39, a4, length)`. However, `v39` is always allocated length bytes, while the source buffer `a4` might not actually have that many bytes available. If `a4` is smaller than length, reading beyond `a4` can cause an overflow.
  This behavior can lead to a crash in the driver. The issue arises because there is no check to ensure that `a4` has at least length bytes of valid data before calling memcpy.

There is code in the same function that exhibits similar behavior:

```
__int64 __fastcall sub_185855C(__int64 a1, __int64 a2, _QWORD *a3, const void *a4, __int64 a5, size_t length)
{
  ...
LABEL_13:
    ...
    if ( !*(_QWORD *)(v22 + 48) )
    {
      if ( a4 && a5 )
      {
        v47 = (void *)(*(__int64 (__fastcall **)(_QWORD, size_t, __int64, __int64))(*(_QWORD *)v22 + 8LL))(
                        **(_QWORD **)v22,
                        length,
                        16LL,
                        2147483649LL);
        *(_QWORD *)(v22 + 48) = v47;
        if ( !v47 )
        {
          v9 = -4;
          goto LABEL_64;
        }
        memcpy(v47, a4, length);
        *(_QWORD *)(v22 + 56) = a5;
        *(_QWORD *)(v22 + 64) = length;
        *(_QWORD *)(a1 + 128) += length;
      }
      pthread_cond_broadcast((pthread_cond_t *)(a1 + 796));
      ...
    }
    ...
}

```
## Version

Chrome: 135.0.7048.0
OS: Android 14

# Summary

Android Chrome: Out of bound in Vulkan Samsung driver

# Custom Questions

#### Type of crash:

GPU

#### Reporter credit:

GF, un3xploitable

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 8.6 KB)
- [poc.html](attachments/poc.html) (text/html, 5.3 KB)
- [about-gpu-2025-03-11T07-46-33-989Z.txt.phps](attachments/about-gpu-2025-03-11T07-46-33-989Z.txt.phps) (application/x-httpd-php-source, 59.7 KB)
- [about-gpu-2025-02-11T06-09-25-759Z.txt (1).phps](attachments/about-gpu-2025-02-11T06-09-25-759Z.txt (1).phps) (application/x-httpd-php-source, 50.9 KB)
- [KakaoTalk_20250406_233640323.jpg](attachments/KakaoTalk_20250406_233640323.jpg) (image/jpeg, 444.8 KB)

## Timeline

### pw...@gmail.com (2025-03-08)

Issue: 401615064 Could you closed this case(401615064)? I intend to report it with this account.

### ph...@chromium.org (2025-03-10)

I don't have any Samsung device that I can repro this with, but the described bug and the asan log looks legit. Since this is an OOB read which is not clearly exploitable, assigning severity medium, and provisional found-in M134.

egdaniel@: Would you please help triage this bug?

### eg...@google.com (2025-03-10)

IIUC the poc provided by TC is a custom shader they wrote. Is this actually an issue with a shader Chrome is compiling? If not I think this bug should be closed as this is simply a bug that should be filed with samsung.

### va...@chromium.org (2025-03-10)

Looking at the asan logs:

- It's Device with Exynos GPU, they don't have real GL driver, device internally uses Angle/Vulkan. From a stack trace it seems chrome thinks it uses GL, but it's not obvious.
- Stack trace has libbase.so / liggl\_init.so, which suggests it's a component build. I don't think we ship component builds anywhere, is it a local build? If so could you help symbolizing that fully? If not, could you provide contents of chrome://version and chrome://gpu?
- Crash is on the worker thread, I'm not sure what we can be calling from the worker thread.

### eg...@google.com (2025-03-10)

passing over to vasilyt because this seems to be unrelated to Skia's usage of Vulkan. Is this a WebGL shader?

### va...@chromium.org (2025-03-10)

poc.html is webgl app, yeah. With an empty vertex shader, fragment shader and a draw without vertex buffer.

### pw...@gmail.com (2025-03-11)

The Chrome version uses a 135.0.7048.0 developer build. (I'm building it myself and using it.)
This is the requested Chrome://gpu.

### ch...@google.com (2025-03-11)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### va...@chromium.org (2025-03-11)

As this is local build, could you provide fully symbolized stack from asan? You should be able to symbolize it via `third_party/android_platform/development/scripts/stack` by feeding it log and output directory.

+cc syoussefi@ chrome://gpu says we run with angle/vulkan, in this case worker thread makes some sense, I guess angle compiles shaders on a pool?

### pw...@gmail.com (2025-03-11)

I need a routed phone to run asan chrome, but I'm having some difficulties at the rooting stage right now, so please wait a little bit.

### m....@samsung.com (2025-03-16)

Could we get a logcat dump of the crash?
I'm hoping to capture the SHA of vulkan.samsung.so that was used here, to reproduce the problem locally.

### pw...@gmail.com (2025-03-18)

You can see the crash logcat in the `asan.log` of my report.

Hash:

```
e1s:/ $ sha1sum /vendor/lib64/hw/vulkan.samsung.so
bf6dcaa6848b019422fb913c1d602adb78785f7f  /vendor/lib64/hw/vulkan.samsung.so
e1s:/ $ md5sum /vendor/lib64/hw/vulkan.samsung.so
673f0ffdbe7e8658d1d5bb6389169559  /vendor/lib64/hw/vulkan.samsung.so

```

Also, I am build and using Chrome directly.( Not Stable Chrome )
@samsung Are you also building and using Chrome directly?

### m....@samsung.com (2025-03-18)

Ahh `asan.log` has a snippet of the logcat with the crash log, but the driver should also print something like the following to logcat when the app starts up

```
03-17 23:40:23.810  7464  7496 V XGL     : -------------------------------------------------------
03-17 23:40:23.810  7464  7496 V XGL     : SUMD version merge SHA1      = <SHA1 commit hash>
03-17 23:40:23.810  7464  7496 V XGL     : SUMD version revision number = <SHA1 commit hash>
03-17 23:40:23.810  7464  7496 V XGL     : -------------------------------------------------------

```

This will correlate to the commit hash in our internal repo, and I can use that to try and recreate the crash.

As for chrome, I'm just using the one from playstore for now, if I cant get it to crash with the right vk driver, then I will try to match the chrome versions next.

### pw...@gmail.com (2025-03-18)

Here

```
03-19 02:19:25.885 18606 11295 V XGL     : SUMD version merge SHA1      = 893a48f7be
03-19 02:19:25.885 18606 11295 V XGL     : SUMD version revision number = 8e918d4d17

```

### m....@samsung.com (2025-03-19)

Was unable to get chrome to crash with that version of the vk driver.

Do you have any pointers on how to build the same version of chrome you are using?

### pw...@gmail.com (2025-03-19)

<https://chromium.googlesource.com/chromium/src/+/main/docs/android_build_instructions.md>

I did this as it is.

### ch...@google.com (2025-03-26)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-27)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-28)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-29)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-30)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-31)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-01)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-02)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-03)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### m....@samsung.com (2025-04-04)

Sorry about the downtime.

So I got chrome to build and with Top of tree, I was not able to reproduce the crash.
I tried running ASAN chrome but that wouldn't start.

I also tried to run it on an S24+ and wasn't able to reproduce it there either, although the VK Driver version was different and I couldn't update it.
So that's a slightly different environment.

Would it be possible to share your build of chrome as an APK, and if possible your vulkan.samsung.so?
Just to try and recreate the same runtime environment.

### pw...@gmail.com (2025-04-04)

Are you using the Korean version of s24?

As far as I know, there is a difference in gpu between the American version and the Korean version.

### ch...@google.com (2025-04-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### m....@samsung.com (2025-04-05)

I believe I was using an S24+ from the UK.
It was running our driver, but just a different version from the one you are using.

### pw...@gmail.com (2025-04-05)

As far as I know, if it's not the Korea version, the device uses a Qualcomm GPU.
However, the Korean version uses Xclipse, so the device I'm reproducing the issue on is an Xclipse device.
The reproduction issue might be due to this.

### ch...@google.com (2025-04-05)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-06)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pw...@gmail.com (2025-04-06)

1. If reproduce is not working, try changing the settings as shown in the picture. (Enabling this setting will directly call the Vulkan driver, so it might make reproduce work.)
2. Please check whether you are using an Exynos processor.

### ch...@google.com (2025-04-07)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### m....@samsung.com (2025-04-07)

Thanks!
I will give this a try.

And I just confirmed that the S24+ device I tried it on uses Xclipse. Its not the Qualcomm variant

### ch...@google.com (2025-04-08)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-09)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-10)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-11)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-12)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-13)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-14)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-15)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 34 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-16)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 35 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-17)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 36 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-18)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 37 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-19)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 38 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-20)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 39 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-21)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 40 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-22)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 41 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-23)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 42 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-24)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 43 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-25)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-26)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 45 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-27)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 46 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-28)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 47 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-29)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 48 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-30)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 49 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-01)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 50 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-02)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 51 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-03)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 52 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 53 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-05)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 54 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-06)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 55 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 56 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 56 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-08)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 57 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-23)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 72 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-07)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 87 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-22)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 102 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-07)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 117 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-22)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 132 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-06)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 147 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-21)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 162 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-05)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 177 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-20)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 192 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-05)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 207 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-20)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 222 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 237 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-19)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 252 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 267 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-19)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 282 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-03)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 297 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-18)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 312 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-02)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 327 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-17)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 342 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-04)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 357 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-19)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 372 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ds...@google.com (2026-04-20)

Was anyone able to reproduce this issue? Is it still waiting on Samsung to confirm? Should we set it as external dependency? Is there anything to do on the Chrome side?

All of the current settings seem correct, I'm going to remove this from the security triage as it all seems to be inorder.

### pw...@gmail.com (2026-05-06)

It appears that this vulnerability has already been patched by Samsung, and it is no longer reproducible.

### pe...@google.com (2026-05-06)

Based on [comment #93](https://issues.chromium.org/issues/401546699#comment93) from reported I think we should claim that this is fixed by IHV

### ch...@google.com (2026-05-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-05-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/401546699)*
