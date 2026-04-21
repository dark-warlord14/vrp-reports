# Security: UAF in Ozone Clipboard

| Field | Value |
|-------|-------|
| **Issue ID** | [40054968](https://issues.chromium.org/issues/40054968) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Linux |
| **Reporter** | le...@gmail.com |
| **Assignee** | ni...@igalia.com |
| **Created** | 2021-02-24 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

Same as the X11 clipboard bugs I submitted before[1], the ozone clipboard also has this problem. Take ContextMenu as an example in asan and poc.

[1]. 1161141,1161143,1161145,1161146,1161147,1161149,1161151,1161152

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS

**REPRODUCTION CASE**  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --use-system-clipboard "<http://localhost:8000/poc.html>"  

Copy a lot of content and right click the textarea field.

or use the trick mentioned in [crbug.com/1161146](https://crbug.com/1161146)#c5

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 19.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 238 B)

## Timeline

### [Deleted User] (2021-02-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-02-24)

I was also unable to reproduce this one. 
How much should I copy into the clipboard?
When I try to repro, the Chromium inside the ChromeOS window closes/crashes but i didn't see any stacktrace. Does it go somewhere abnormal or should it print to stderr like normal?

### me...@chromium.org (2021-02-24)

This time I used the same build as I mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1181676#c2

### le...@gmail.com (2021-02-24)

Yes, there should be an Asan crash backtrace printed on the terminal. I copied about 30M of data, but this can also be bypassed by the trick mentioned in crbug.com/1161146#c5.

### le...@gmail.com (2021-02-25)

After the test, it can be triggered on the build[1] you mentioned in crbug.com/1181676#c2.

[1]. https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-827102.zip

### me...@chromium.org (2021-02-25)

OK, I was able to repro this on the build you provided above.
avi@ or lazyboy@ do you know who might be the right owner for this issue?

[Monorail components: UI>Browser]

### me...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### av...@chromium.org (2021-02-25)

No idea.

Rob, Thomas, do either of you know who’d be good to look at this?

### th...@chromium.org (2021-02-25)

This is a known issue [1] [2].  Also, ozone/X11 is currently in development and officially not supported yet.  However, fixing the clipboard issue is a requirement to be able to ship.

+igalia folks.  FYI this issue is a hard requirement before enabling ozone/X11 due to the security UAF bugs it causes (1161141,1161143,1161145,1161146,1161147,1161149,1161151,1161152).

[1] https://crbug.com/913422
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/clipboard/clipboard_ozone.cc;drc=a6a4d2061067b182ca70c8ca9d2b214d6a3e9528;l=197


### aa...@google.com (2021-02-25)

Should we switch this to Security_Impact-None based on https://crbug.com/chromium/1181688#c9?

### ad...@igalia.com (2021-02-26)

The OP doesn't use Ozone (given the command line mentioned in https://crbug.com/chromium/1181688#c1) so I'm afraid this issue impacts the supported version of Chrome.

### ad...@igalia.com (2021-02-26)

Adding Nick as he is one of contributors in Ozone clipboard.

### ni...@igalia.com (2021-02-26)

OP: I am a bit confused, the bug description mentions ChromeOS and some comments Ozone/X11. What binary exacly are you running (or the GN args in case you're running a devel binary)? So we can say for sure if it affects ChromeOS' Chrome browser.

As Tom said, ozone/linux (x11 and wayland) is still under devel. I recently landed the first of series of fixes ozone's clipboard issues https://crrev.com/c/2676322 (tracked in crbug.com/1165466), which is in dev. Could you check with Chrome in dev channel?

### le...@gmail.com (2021-02-26)

I tested on both the local build and the chrome provided by the DataStorage[1].

The GN args used in local:

# Build arguments go here.
# See "gn args <out_dir> --list" for available build arguments.
is_debug = false
enable_nacl = false
is_asan = true
target_os = "chromeos"
is_component_build = true

The chrome provided by the datastorage:

1. https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-827102.zip
M88 Stable with http://crrev.com/827102

2. https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-843807.zip
M89 Beta with http://crrev.com/843807 that will be released in the next few days.

3. https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-858040.zip
The latest dev version with http://crrev.com/858040 updated in 2021-02-26T06:41:26.941Z(seems after https://crrev.com/c/2676322)

command line : ./chrome --user-data-dir=/tmp/xxxx --use-system-clipboard "http://localhost:8000/poc.html"

All the above versions can trigger the bug.

[1] https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release-chromeos/

### [Deleted User] (2021-02-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2021-03-01)

IIUC as far as Chrome OS is concerned - this bug requires running chrome with --use-system-clipboard which we currently don't do at stable. Is that accurate?

### ni...@igalia.com (2021-03-01)

Re #c 16: Precisely. AFAIK, use-system-clipboard is meant for development, so I think this does apply to ChromeOS (will try to compile out that flag in non linux-chromeos builds). That said, this bug is actually targeted at Linux Desktop Ozone builds (linux builds with use_ozone=true), which is still experimental and under development. Regardless, I'll look into it soon.

### aa...@google.com (2021-03-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7e17583da19cb8ef1bbaf6555666b641daff6d6b

commit 7e17583da19cb8ef1bbaf6555666b641daff6d6b
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Tue Mar 02 13:18:28 2021

clipboard: ozone: Simplify clipboard factories

Clipboard factory code for Ozone, NonBacked and X11 variants became
confusing and hard to follow, especially with Linux Desktop hybrid
builds (use_ozone=true &&use_x11=true) support in place. This CL
simplifies and unifies it into a single and cleaner source file.

As nice side effect, --use-system-clipboard runtime flag is no
longer exposed in non linux ash-chrome builds (as it was originally
intended), preventing ClipboardOzone-specific issues being reported as
ChromeOS issues, such as crbug.com/1181688.

Bug: 1181688
Test: Manually tested with different ozone build variants.
Change-Id: I5c7b68725d5520fc606897e78cd24d8beae1e44b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2728218
Auto-Submit: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Maksim Sisov <msisov@igalia.com>
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Cr-Commit-Position: refs/heads/master@{#858972}

[modify] https://crrev.com/7e17583da19cb8ef1bbaf6555666b641daff6d6b/ui/base/clipboard/clipboard_non_backed.cc
[modify] https://crrev.com/7e17583da19cb8ef1bbaf6555666b641daff6d6b/ui/base/clipboard/clipboard_ozone.cc
[modify] https://crrev.com/7e17583da19cb8ef1bbaf6555666b641daff6d6b/ui/base/clipboard/BUILD.gn
[delete] https://crrev.com/daaf5308f6aa940d3febdf88e618c52d1003f9dc/ui/base/clipboard/clipboard_linux.cc
[add] https://crrev.com/7e17583da19cb8ef1bbaf6555666b641daff6d6b/ui/base/clipboard/clipboard_factory_ozone.cc


### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ad...@igalia.com (2021-03-18)

[Empty comment from Monorail migration]

### ni...@igalia.com (2021-03-30)

OP: Just verified with a Desktop Linux Ozone build, developer build (head commit hash: ) and couldn't reproduce it with neither X11 nor Wayland backend. Could you please re-check it ?

Marking this as fixed, please re-open if it still happens.

Thanks

### ni...@igalia.com (2021-03-30)

Oops, forgot to add the tip of tree commit hash: 03b14178cbbd.

GN flags:

enable_nacl = false
is_asan = true
is_debug = false
dcheck_is_configurable = true
is_component_build = true

Command line args:

X11: 

ASAN_OPTIONS=detect_odr_violation=0 out/asan/chrome --enable-features=UseOzonePlatform --ozone-platform=x11 --enable-logging=stderr --no-sandbox --user-data-dir=/tmp/chr_tmp_ozone http://localhost:8000/poc.html

Wayland:

ASAN_OPTIONS=detect_odr_violation=0 out/asan/chrome --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-logging=stderr --no-sandbox --user-data-dir=/tmp/chr_tmp_ozone http://localhost:8000/poc.html


### le...@gmail.com (2021-03-31)

Re #23: Unfortunately, I could reproduce the UAF with the build you mentioned (commit hash: 03b14178cbbd). 

I used https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-865466.zip with:
{
  "kind": "storage#object",
  "mediaLink": "https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release-chromeos%2Fasan-linux-release-865466.zip?generation=1616467486110322&alt=media",
  "name": "linux-release-chromeos/asan-linux-release-865466.zip",
  "size": "3953415118",
  "updated": "2021-03-23T02:44:46.147Z",
  "metadata": {
    "cr-commit-position": "refs/heads/master@{#865466}",
    "cr-commit-position-number": "865466",
    "cr-git-commit": "03b14178cbbd290f77e378664663720891e4b98b"
  }
}

I think the root cause is that we could destroy some instances, which are involved to maintain the context of the message loop[1][2] while the loop is still running, and the UAF will be triggered after the loop exits if there is no check.

It is as same as the bug related to the X11 clipboard I reported before[3]. Just that the protagonist is changed to ozone-clipboard. And in order to use ozone-clipboard I used --use-system-clipboard.

thomasanderson@ changed the X11 clipboard to be asynchronous to fix those issues, he might be able to give you some advice.

[1]. https://source.chromium.org/chromium/chromium/src/+/master:ui/base/clipboard/clipboard_ozone.cc;l=119;drc=b031326bf3f27000c6462dae672cf781f47c417e
[2]. https://source.chromium.org/chromium/chromium/src/+/master:ui/base/clipboard/clipboard_ozone.cc;l=200;drc=b031326bf3f27000c6462dae672cf781f47c417e
[3]. crbug.com/[1161141|1161143|1161145|1161146|1161147|1161149|1161151|1161152]

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### ni...@igalia.com (2021-04-05)

Hi leecraso@, thanks for checking. Though, as mentioned in https://crbug.com/chromium/1181688#c16 and https://crbug.com/chromium/1181688#c17, this issue shouldn't affect ChromeOS, as `--use-system-clipboard` is meant only for development (ie: not used in production builds). I'm aware of Tom's fixes for Chrome/X11 and my idea is to re-use them in Ozone path (next step) in Linux Desktop builds. Please notice that Chrome/Ozone for Linux Desktop is a different product from what you're using to report issues. Could you please check if it's reproducible using the binary downloaded from the URL below, for example:

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-debug%2Fasan-linux-debug-867332.zip?generation=1617062100983934&alt=media

As I mentioned in my last comments, I couldn't repro this locally, and it would be helpful to be able to do it, so I can validate my fix before landing.

### le...@gmail.com (2021-04-07)

Get it! Yes, it's irrelevant to the ChromeOS. The ozone-clipboard could also be enabled with "--enable-features=UseOzonePlatform --ozone-platform=x11". And I could reproduce the UAF with it in https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-867333.zip

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/22b15de44d400f6d83caafb61927403135b7b107

commit 22b15de44d400f6d83caafb61927403135b7b107
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Wed Apr 07 23:20:36 2021

x11: Move selection_requestor.{h,cc} into the correct build target

R=thomasanderson@chromium.org

Bug: 1165466, 1181688
Change-Id: I157cf4e733518797bb871a6297c933d33fe8544f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2809000
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Cr-Commit-Position: refs/heads/master@{#870261}

[modify] https://crrev.com/22b15de44d400f6d83caafb61927403135b7b107/ui/base/BUILD.gn
[modify] https://crrev.com/22b15de44d400f6d83caafb61927403135b7b107/ui/base/x/BUILD.gn
[modify] https://crrev.com/22b15de44d400f6d83caafb61927403135b7b107/ui/base/x/selection_requestor.cc
[modify] https://crrev.com/22b15de44d400f6d83caafb61927403135b7b107/ui/base/x/selection_requestor.h
[modify] https://crrev.com/22b15de44d400f6d83caafb61927403135b7b107/ui/base/x/selection_requestor_unittest.cc


### ni...@igalia.com (2021-04-07)

Re https://crbug.com/chromium/1181688#c29: Right, could you provide more info on the env you're reproducing it? E.g: which DE/WM and xorg? versions? thanks

### gi...@appspot.gserviceaccount.com (2021-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737

commit c2dcc7f6637bc41d9285bb8b4413d3fa15e28737
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Thu Apr 08 00:50:46 2021

x11: Factor XClipboardHelper out of ClipboardX11

Extract X11 clipboard integration code from clipboard_x11.cc into a
common place ui/base/x/x11_clipboard_helper.{h,cc}, so that it can be
re-used in Ozone/X11 platform clipboard implementation. Which will be
done in a followup CL.

R=thomasanderson@chromium.org

Bug: 1165466, 1181688
Change-Id: I073b7468c32d11ddf46bcad25ea78cdf44501c9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2809535
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870305}

[modify] https://crrev.com/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737/ui/base/clipboard/clipboard_x11.cc
[modify] https://crrev.com/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737/ui/base/clipboard/clipboard_x11.h
[modify] https://crrev.com/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737/ui/base/x/BUILD.gn
[add] https://crrev.com/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737/ui/base/x/x11_clipboard_helper.cc
[add] https://crrev.com/c2dcc7f6637bc41d9285bb8b4413d3fa15e28737/ui/base/x/x11_clipboard_helper.h


### le...@gmail.com (2021-04-08)

GNOME 3.18.3
X.Org X Server 1.19.6

I think the environment has a little effect. You can try the following steps to trigger it more easily:
Prepare about 10M data in a non-chrome window, visit the POC page, press ctrl-c multiple times to copy the data, and right-click the textarea.

### gi...@appspot.gserviceaccount.com (2021-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7fc5b32bff620d62a068fe0a0812eeb326978996

commit 7fc5b32bff620d62a068fe0a0812eeb326978996
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Thu Apr 08 12:32:57 2021

x11: XClipboardHelper: Encapsulate target/atom list handling

Clean up and improve XClipboardHelper public API, mainly parts that deal
with "target lists" and how they translate into mime type strings, so
that it can more easily re-used by ozone/x11 clipboard implementation.
This does not imply in any functional change.

Next step is to refactor X11ClipboardOzone to start using
XClipboardHelper, which will be done in a separate CL.

R=thomasanderson@chromium.org

Bug: 1165466, 1181688
Change-Id: I367e444d8e9c29cffa8fa76cde53b04373181897
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2809959
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870481}

[modify] https://crrev.com/7fc5b32bff620d62a068fe0a0812eeb326978996/ui/base/clipboard/clipboard_x11.cc
[modify] https://crrev.com/7fc5b32bff620d62a068fe0a0812eeb326978996/ui/base/x/x11_clipboard_helper.cc
[modify] https://crrev.com/7fc5b32bff620d62a068fe0a0812eeb326978996/ui/base/x/x11_clipboard_helper.h


### gi...@appspot.gserviceaccount.com (2021-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef

commit b4444bdbcd40a1b2357ccc3c5ddc6040245655ef
Author: Nick Diego Yamane <nickdiego@igalia.com>
Date: Thu Apr 08 19:15:57 2021

ozone/x11: Refactor clipboard to re-use XClipboardHelper

...so that Ozone/X11 Clipboard implementation leverage the same
underlying component used in the legacy X11 backend. So, now the Ozone
path shares/inherits:

- Feature parity: The previous implementation was lacking, for example,
incremental content reading, re-entrancy handling, etc.

- Security fixes: No nested message loops used while requesting/reading
data from the X server [1].

R=thomasanderson@chromium.org

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2622521

Bug: 1165466, 1181688
Change-Id: I28f8fc1f4ec7a01d50244b82ff61daeaa73341f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2814459
Commit-Queue: Nick Yamane <nickdiego@igalia.com>
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870643}

[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/base/x/selection_utils.cc
[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/base/x/selection_utils.h
[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/base/x/x11_clipboard_helper.cc
[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/base/x/x11_clipboard_helper.h
[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/ozone/platform/x11/x11_clipboard_ozone.cc
[modify] https://crrev.com/b4444bdbcd40a1b2357ccc3c5ddc6040245655ef/ui/ozone/platform/x11/x11_clipboard_ozone.h


### ni...@igalia.com (2021-04-13)

This should be fixed now.

OP: Appreciate if you can double-check it.

Thanks

### le...@gmail.com (2021-04-13)

Thanks for your patience to fix it. After the test with https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-870643.zip and 871846, the bug seems to have been fixed. But when the browser is launched with "--enable-features=UseOzonePlatform --ozone-platform=x11", the page will be hung, and will print lots of logs as follows:

[17274:17274:0413/191346.038673:ERROR:gl_surface_egl.cc(780)] EGL Driver message (Error) eglCreateContext: eglCreateContext
[17274:17274:0413/191346.038753:ERROR:gl_context_egl.cc(279)] eglCreateContext failed with error EGL_BAD_ATTRIBUTE
[17274:17274:0413/191346.038817:ERROR:gpu_channel_manager.cc(746)] ContextResult::kFatalFailure: Failed to create shared context for virtualization.
[17274:17274:0413/191346.038883:ERROR:shared_image_stub.cc(460)] SharedImageStub: unable to create context
[17274:17274:0413/191346.038957:ERROR:gpu_channel.cc(449)] GpuChannel: Failed to create SharedImageStub
[17274:17274:0413/191346.039717:ERROR:gl_surface_egl.cc(780)] EGL Driver message (Error) eglCreateContext: eglCreateContext
[17274:17274:0413/191346.039808:ERROR:gl_context_egl.cc(279)] eglCreateContext failed with error EGL_BAD_ATTRIBUTE
[17274:17274:0413/191346.039884:ERROR:gpu_channel_manager.cc(746)] ContextResult::kFatalFailure: Failed to create shared context for virtualization.
[17274:17274:0413/191346.039948:ERROR:shared_image_stub.cc(460)] SharedImageStub: unable to create context
[17274:17274:0413/191346.040021:ERROR:gpu_channel.cc(449)] GpuChannel: Failed to create SharedImageStub


### ni...@igalia.com (2021-04-13)

Seems like a different issue. Please file a new bug and attach your GPU info, etc. Thanks for checking. 
On my env it hangs a bit as well (reading clipboard data >= 15MB) but then gets back after some millisecs/secs.

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, leecraso@! The VRP Panel has decided to award you $20,000 for this report. Awesome work!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-20)

This issue was migrated from crbug.com/chromium/1181688?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1165466]
[Monorail blocking: crbug.com/chromium/1022722]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054968)*
