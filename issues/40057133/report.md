# AddressSanitizer: use-after-poison execution_context_lifecycle_observer.cc:40 in blink::ExecutionContextLifecycleObserver::GetExecutionContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40057133](https://issues.chromium.org/issues/40057133) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GetDisplayMedia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-09-02 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4624.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-916705.zip

#Reproduce
This problem is difficult to reproduce manually. I wrote an automated script here through puppeteer, which is easier to reproduce, but nodejs needs to be installed.
The automated tool fails to give the minicase, I will try to make the minicase by hand.

1. install nodejs
2. unzip poc.zip,sudo python -m http.server 80
3. node ch.test.js D:\chrome_asan\asan-win32-release_x64-916705\chrome.exe http://localhost/fuzz-00015.html
4. wait asan report

What is the expected behavior?

What went wrong?
Type of crash
render tab

Did this work before? N/A 

Chrome version: 95.0.4624.0  Channel: dev
OS Version: 10.0

#Analysis
Come soon

```

#Patch
Not yet

#asan
=================================================================
==15312==ERROR: AddressSanitizer: use-after-poison on address 0x7e8b00314770 at pc 0x7ffcd24010f4 bp 0x00b620dfe530 sp 0x00b620dfe578
READ of size 8 at 0x7e8b00314770 thread T0
==15312==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffcd24010f3 in blink::ExecutionContextLifecycleObserver::GetExecutionContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\execution_context\execution_context_lifecycle_observer.cc:40
    #1 0x7ffcdaf40adb in blink::MediaDevices::CloseFocusWindowOfOpportunity C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\mediastream\media_devices.cc:579
    #2 0x7ffcd23b1ee4 in blink::MicrotaskFunctionCallback C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\bindings\microtask.cc:50
    #3 0x7ffcc759f0c7 in v8::internal::Runtime_RunMicrotaskCallback C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-promise.cc:95
    #4 0x7ee8000bdf1b  (<unknown module>)

Address 0x7e8b00314770 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\execution_context\execution_context_lifecycle_observer.cc:40 in blink::ExecutionContextLifecycleObserver::GetExecutionContext
Shadow bytes around the buggy address:
  0x124b19e62890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e628a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e628b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7
  0x124b19e628c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e628d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7
=>0x124b19e628e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7
  0x124b19e628f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e62900: f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e62910: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e62920: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x124b19e62930: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==15312==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan.txt](attachments/asan.txt) (text/plain, 2.7 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-02)

eladon: PTAL for blink::MediaDevices::CloseFocusWindowOfOpportunity.

[Monorail components: Blink>GetDisplayMedia]

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

~/Desktop/media_devices_bug:$ node ch.test.js ~/chromium/src/out/Release/chrome  http://127.0.0.1:5500/fuzz-00015.html
=================================================================
==2913399==ERROR: AddressSanitizer: odr-violation (0x7fcfd8b70c60):
  [1] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
  [2] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
These globals were registered at these points:
  [1]:
^C~/Desktop/media_devices_bug:$ node ch.test.js ~/chromium/src/out/Release/chrome  http://127.0.0.1:5500/fuzz-00015.html
=================================================================
==2913447==ERROR: AddressSanitizer: odr-violation (0x7faeb8e82c60):
  [1] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
  [2] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
These globals were registered at these points:
  [1]:
    #0 0x560bab5aa837 in __asan_register_globals /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_globals.cpp:360:3
    #1 0x7fae922b83ae in asan.module_ctor concurrent-marker.cc
    #2 0x7faf27e9afe1 in call_init elf/dl-init.c:72:3

  [2]:
    #0 0x560bab5aa837 in __asan_register_globals /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_globals.cpp:360:3
    #1 0x7faeb7e6e5ce in asan.module_ctor concurrent-marker.cc
    #2 0x7faf27e9afe1 in call_init elf/dl-init.c:72:3

==2913447==HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_odr_violation=0
SUMMARY: AddressSanitizer: odr-violation: global 'vtable for cppgc::internal::ConcurrentMarkerBase' at ../../v8/src/heap/cppgc/concurrent-marker.cc
==2913447==ABORTING
(node:2913440) UnhandledPromiseRejectionWarning: Error: Failed to launch the browser process!
=================================================================
==2913447==ERROR: AddressSanitizer: odr-violation (0x7faeb8e82c60):
  [1] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
  [2] size=40 'vtable for cppgc::internal::ConcurrentMarkerBase' ../../v8/src/heap/cppgc/concurrent-marker.cc
These globals were registered at these points:
  [1]:
    #0 0x560bab5aa837 in __asan_register_globals /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_globals.cpp:360:3
    #1 0x7fae922b83ae in asan.module_ctor concurrent-marker.cc
    #2 0x7faf27e9afe1 in call_init elf/dl-init.c:72:3

  [2]:
    #0 0x560bab5aa837 in __asan_register_globals /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_globals.cpp:360:3
    #1 0x7faeb7e6e5ce in asan.module_ctor concurrent-marker.cc
    #2 0x7faf27e9afe1 in call_init elf/dl-init.c:72:3

==2913447==HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_odr_violation=0
SUMMARY: AddressSanitizer: odr-violation: global 'vtable for cppgc::internal::ConcurrentMarkerBase' at ../../v8/src/heap/cppgc/concurrent-marker.cc
==2913447==ABORTING


TROUBLESHOOTING: https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md

    at onClose (/usr/local/google/home/eladalon/Desktop/media_devices_bug/node_modules/puppeteer-core/lib/cjs/puppeteer/node/BrowserRunner.js:197:20)
    at ChildProcess.<anonymous> (/usr/local/google/home/eladalon/Desktop/media_devices_bug/node_modules/puppeteer-core/lib/cjs/puppeteer/node/BrowserRunner.js:188:79)
    at ChildProcess.emit (events.js:326:22)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:276:12)
(node:2913440) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). To terminate the node process on unhandled promise rejection, use the CLI flag `--unhandled-rejections=strict` (see https://nodejs.org/api/cli.html#cli_unhandled_rejections_mode). (rejection id: 1)
(node:2913440) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.


### el...@chromium.org (2021-09-02)

Hi m.coolie@. I am trying to reproduce this on my Linux workstation.
1. Could you check the error in https://crbug.com/chromium/1245881#c4 and let me know if it stems from your script?
2. Could you mention your exact gn-args so that we can make sure I'm on the same page? (As much as possible given the different operating systems.)

### m....@gmail.com (2021-09-02)

I think the problem you are encountering should be the liunx asan version. You try to set the environment variable ASAN_OPTIONS=detect_odr_violation=0 and try again. In addition, I tested it on window10.

### el...@chromium.org (2021-09-02)

I believe ASAN_OPTIONS=detect_odr_violation=0 refers only to the warnings, no the UnhandledPromiseRejectionWarning.

### m....@gmail.com (2021-09-02)

warnings will cause browser process exit Finally lead to UnhandledPromiseRejectionWarning.
I have encountered other problems on linux to reproduce, I provide a windows reproduce video here.


### el...@chromium.org (2021-09-02)

Could you please provide your GN args?

### m....@gmail.com (2021-09-02)

I downloaded it directly from gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-917187.zip


### [Deleted User] (2021-09-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-09-02)

I'm still looking into this.

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05c33c873af11f6c7a8034dff07ff2bff9958014

commit 05c33c873af11f6c7a8034dff07ff2bff9958014
Author: Elad Alon <eladalon@chromium.org>
Date: Fri Sep 03 17:29:24 2021

[Conditional Focus] Use WeakPersistent for MediaDevices reference

Bug: 1245881
Change-Id: I032a63ff38cd16da3054fda5a6e8b6387439133f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3141555
Commit-Queue: Elad Alon <eladalon@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#918157}

[modify] https://crrev.com/05c33c873af11f6c7a8034dff07ff2bff9958014/third_party/blink/renderer/modules/mediastream/media_devices.cc
[modify] https://crrev.com/05c33c873af11f6c7a8034dff07ff2bff9958014/third_party/blink/renderer/modules/mediastream/media_devices.h


### el...@chromium.org (2021-09-06)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-06)

CL #3141555 should have fixed this, but I have not yet verified, as I don't have a Windows machine on hand. I am working to remedy/bypass this.

### el...@chromium.org (2021-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-09)

I don't have a Windows machine on which to verify the fix. I've requested a Cloudtop machine but I've not received it yet.
Chrome trunk sheriffs, do you happen to have access to a Windows machine or know someone who can verify this bug is properly fixed?

### re...@chromium.org (2021-09-09)

I should be able to try verifying the fix on Windows tomorrow.

Reporter, since this change has landed in HEAD there should be an updated build in the gs://chromium-browser-asan bucket as well you can verify with. 

### m....@gmail.com (2021-09-10)

re c22

No longer reproduce on asan-win32-release_x64-920053

### [Deleted User] (2021-09-11)

Not requesting merge to dev (M95) because latest trunk commit (918157) appears to be prior to dev branch point (920003). If this is incorrect, please replace the Merge-NA-95 label with Merge-Request-95. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

And another one! Congratulations - the VRP Panel has decided to award you $5000 for this report. Thank you for your efforts! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245881?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057133)*
