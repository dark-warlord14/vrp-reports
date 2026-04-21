# Security: UAF in RawClipboardHostImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40052742](https://issues.chromium.org/issues/40052742) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-07-01 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

when the renderer bind RawClipboardHost Service, the RawClipboardHostImpl object take render\_frame\_host ptr. [1]  

but the RawClipboardHostImpl object's lifetime is independent on render\_frame\_host.  

So if render\_frame\_host is deleted, the RawClipboardHostImpl object take invalid pointer and use it[2]

i think that RawClipboardHostImpl should inherit WebContentsObserver to observer frame lifetime using RenderFrameDeleted function.

[1] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/frame_host/raw_clipboard_host_impl.cc;drc=f5c26dea72747aa434da84c57655cac5272d5ad4;l=65?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[2] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/frame_host/raw_clipboard_host_impl.cc;drc=f5c26dea72747aa434da84c57655cac5272d5ad4;l=158?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

**VERSION**  

Chrome Version: 84+  

Operating System: All

**REPRODUCTION CASE**

unzip repo.zip

it should be launched on "https" server becuase Clipboard R/W Permission must be accepted on https server  

and you should turn on chrome://flags/#raw-clipboard.

Poc :  

Run chrome with --enable-blink-features=MojoJS,MojoJSTest and visit <http://localhost:8080/poc.html>

Exploit:  

the exploit can work on 84.0.4147.68 (Official Build) beta (64-bit), Windows 10 1909 x64.  

And you should change chrome.dll, kernel.dll base address in exploit.html. (Note that this base address could be acquired from a compromised renderer)

```
Run chrome with --enable-blink-features=MojoJS,MojoJSTest and visit http://localhost:8080/exploit.html  

As a result, it swpan Calculator.  

```

**CREDIT INFORMATION**  

Reporter credit: Woojin Oh(@pwn\_expoit) of STEALIEN on 2020-04-21

## Attachments

- [repo.zip](attachments/repo.zip) (application/octet-stream, 2.5 MB)

## Timeline

### cl...@chromium.org (2020-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5702009501581312.

### cl...@chromium.org (2020-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5645057832583168.

### ra...@gmail.com (2020-07-02)

+allow permission when poc work


### ad...@google.com (2020-07-06)

carlosil@ I had a try at reproducing this in a redshell and have failed. FWIW here's what I tried:

1. Fetching 84.0.4147.68 and building all targets of a 64-bit release build in order to get the correct mojoJS bindings. Replacing those in the exploit with those built this way. (That said, I did not use is_official_build=true so it's conceivable there was still some difference). Obviously I didn't do the build on the redshell.
2. Fetching the Chrome beta on the redshell which is currerntly 84.0.414 7.68.
3. Launching with google-chrome-beta --enable-blink-features=MojoJS,MojoJSTest --allow-insecure-localhost --unsafely-treat-insecure-origin-as-secure
4. Enabling raw clipboard and relaunching
5. I tried loading over both http and https. (Both python3 -m http.server 8000, and putting together a simple https python3 server, which obviously didn't chain to a proper root certificate so I'm not sure if that affects the raw clipboard permissions situation.
6. Loading poc.html.
7. Clicking Click Me.
8. Nothing...

I don't know if the failure to reproduce is because I didn't have a "real" https server, or because of some MojoJS mismatch, or something else.

Still, if this is real, it's a high severity sandbox escape introduced in M84. As such I think we need to ensure raw clipboard is at 0% of users in M84, unless we want to recut the initial M84 release to include a fix.

Darwin - normally we wouldn't pass this to you until we'd been able to reproduce, but perhaps you can comment on the status of raw clipboard? And whether the diagnosis i the report makes sense?

### ad...@google.com (2020-07-06)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-07-06)

the poc could be unreliable. did you refresh many time? or i  recommend to run poc on asan build. but in 84.0.4147.68 (Official Build) beta (64-bit), the Exploit will be triggered very well.

### [Deleted User] (2020-07-06)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-07-07)

I didn't try repro'ing, since I'm not immediately sure how to change chrome/kernel .dll base addresses. 

That said, this code hasn't changed much since launched in M84 (including the code referenced by rapid.pwn@), so I suspect that if this is reproducible in M84, that it is also reproducible on canary.

The premise of this bug is that Chrome assumes the input render_frame_host_ to be valid, as documented in [1], but on non-debug builds this is not verified after that DCHECK, and it's also not verified to continue to be valid after that first DCHECK in [2] (in case its lifetime expires). My understanding was that this mojo host should be destructed when the frame expires, so that the lifetime should be connected. That said, rapid.pwn@ says that the lifetimes are not connected, so if this is the case, I could easily believe that this should repro.

To verify UaF on the line in question, without using an asan build, we could likely also run the POC with a CHECK(render_frame_host_);. at [2], and if there's a crash, then the UaF is verified. 

[1]: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/frame_host/raw_clipboard_host_impl.cc;l=27;drc=f5c26dea72747aa434da84c57655cac5272d5ad4
[2]: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/frame_host/raw_clipboard_host_impl.cc;l=162;drc=f5c26dea72747aa434da84c57655cac5272d5ad4

### hu...@chromium.org (2020-07-07)

Regarding impact:

I'm unsure how to tell the % of users using the raw clipboard flag. Do you know if there's a way to see how many people have turned it on? (chrome://flags/#raw-clipboard). That said, this number should be very small, as use of this flag triggers a display noting "You are using an unsupported feature flag: RawClipboard. Stability and security will suffer"[1], and the flag is off by default.

[1]: https://crrev.com/c/2086011

### ra...@gmail.com (2020-07-07)

 CHECK(render_frame_host_); can't verify UAF because render_frame_host_ is raw pointer and dangling pointer when vulnerability is triggered. 
as you refresh page, it's sure that the chrome do crash.
but the best of verifier is asan build :D

### ra...@gmail.com (2020-07-07)

* as you refresh page many time, it's sure that the chrome do crash. but in normal environment, the poc will be triggered at once. and see developer console  to confirm that poc_child.html and poc.html is both loaded.

### ad...@chromium.org (2020-07-07)

Thanks Darwin and rapid.pwn for the additional information.

Darwin:
I only tried to reproduce using the poc not the exploit. If you are able to reproduce using the poc then you shouldn't need to fiddle with DLL base addresses, AIUI. Per https://crbug.com/chromium/1101509#c4 though I couldn't manage to reproduce. I strongly suspect that this is because I don't know the correct ways to enable an origin to have permission to use raw clipboard, and I probably didn't get that quite right - if there are command line flags which you can use to allow the origin of a test webserver to have raw clipboard permission, then you may find this "just works". (You'll have to use the exact same build in order that the mojojs bindings match though).

Re https://crbug.com/chromium/1101509#c9 - can you confirm that the only users affected here are those who have chosen to turn on raw clipboard? There's no percentage of stable users who have raw clipboard turned on via Finch? If that's the case, then this is likely Security_Severity-High Security_Impact-None.

Incidentally it would be AMAZING to create a mojolpm fuzzer for this interface. This is newly possible! -- https://chromium.googlesource.com/chromium/src/+/master/mojo/docs/mojolpm.md. It's beyond the scope of fixing this bug; perhaps you could file another crbug for it? I've actually been trying to create a mojolpm fuzzer myself (for the filesystemmanager interface) and I've got quite stuck on the permissions stuff, so it'd be interesting to see how you would programmatically ensure it has permission to do raw clipboard stuff. In the context of this bug, it also raises interesting questions about whether the mojolpm framework can adequately simulate lifetime quirks of fundamental infrastructure objects like renderframehost.

### hu...@chromium.org (2020-07-07)

Re: https://crbug.com/chromium/1101509#c10 Oops yes, my bad. We do need an asan build to verify this.

Re: https://crbug.com/chromium/1101509#c12. Yes, the only users affected here are those who have explicitly chosen to turn on raw clipboard. Chrome doesn't turn this flag on by default for anyone (via Finch or otherwise).

Thanks, I've also filed https://crbug.com/1102720 to track a mojolpm fuzzer.

[Monorail components: Blink>DataTransfer]

### ad...@chromium.org (2020-07-07)

Aha, yes, my mistake was also likely that I didn't have an ASAN build for the poc.

### ra...@gmail.com (2020-07-29)

is doing patch?


### ra...@gmail.com (2020-08-20)

hello?


### ad...@chromium.org (2020-08-21)

My expectation is that this would be fixed before raw clipboard is enabled by default, but that this is not going to be the most urgent thing to fix mean while.

### ts...@chromium.org (2020-08-25)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-09-10)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-09-15)

I tried repro'ing this and wasn't able to successfully repro. My steps were:
1) ASAN build, by adding to the GN args: `is_asan=true` and `is_debug=false`, per https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md#configuring-the-build
2) navigating to the unzip'ed repo folder, and calling `python -m SimpleHTTPServer`.
3) opening chrome via `ASAN_OPTIONS=detect_odr_violation=0 out/Default/chrome --enable-blink-features=MojoJS,MojoJSTest --enable-features=RawClipboard http://localhost:8000/poc.html`.
4) confirmed that poc.html and poc_child.html are both loaded in dev console, and allowed clipboard via site settings.
5) refreshed and clicked the button many times (>20 each?).

I noticed a console error: "navigator.permissions.request is not a function".


### hu...@chromium.org (2020-09-15)

Note regarding repro attempt in https://crbug.com/chromium/1101509#c21. This was on Linux rather than Windows, so swopen of Calculator understandably didn't occur, but I was expecting some ASAN-related crash, which never occurred.

### hu...@chromium.org (2020-09-15)

That said, this bug should be valid if the lifetimes aren't connected, and there's been 3 duplicate bugs filed since for this same root cause, so I'm fairly certain this is probably a valid, reproducible bug that adetaylor@ and I simply haven't been able to repro yet.

I have a fix ready at https://crrev.com/c/2411673. 

(I also noticed there were no other users of HasTransientUserActivation() who simply took in a render_frame_host without checking it was still active via `RenderFrameHostImpl::FromID` or otherwise, so I guess that's more validation that the RenderFrameHost really shouldn't have been assumed to be alive throughout the lifetime of RawClipboardHostImpl).

### hu...@chromium.org (2020-09-15)

+sky, for visibility when reviewing.

Also, +dcheng for heads up (no action needed)

### hu...@chromium.org (2020-09-15)

+pwnall for heads up too (no action needed)

### ra...@gmail.com (2020-09-16)

[Comment Deleted]

### ra...@gmail.com (2020-09-16)

i think navigator.permissions.request work on windows.


### hu...@chromium.org (2020-09-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/70af807c10e12296c8caab0886a790e55be64fc4

commit 70af807c10e12296c8caab0886a790e55be64fc4
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Tue Sep 22 06:04:39 2020

Raw Clipboard: Ensure Renderer is still active before use.

Ensure the RenderFrameHost is still active before use. Previously,
RawClipboardHostImpl incorrectly assumed that the RenderFrameHost was
guaranteed to outlive the RawClipboardHostImpl, and didn't check that
the renderer was always still active.

Bug: 1101509
Change-Id: I3e503634be50b1ca60e4c00131546c2337e4176a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2411673
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#809201}

[modify] https://crrev.com/70af807c10e12296c8caab0886a790e55be64fc4/content/browser/renderer_host/raw_clipboard_host_impl.cc
[modify] https://crrev.com/70af807c10e12296c8caab0886a790e55be64fc4/content/browser/renderer_host/raw_clipboard_host_impl.h


### hu...@chromium.org (2020-09-22)

Sorry rapid.pwn@, could you please confirm that this no longer repro's with https://crrev.com/c/2411673 applied (the updated ToT/main branch should reflect this now)? I'm fairly certain this should be fixed now, but wasn't able to repro the bug, so can't confirm that this is fixed now.

### ra...@gmail.com (2020-09-23)

it seem to be good :D

### hu...@chromium.org (2020-09-23)

I'll mark this bug as fixed now. I won't be asking for mergeback to previous releases, because this was Security_Impact-None. Thank you for reporting and confirming the fixing of this bug, rapid.pwn@! :)

### [Deleted User] (2020-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-28)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-29)

huangdarwin@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-30)

Congratulations! The VRP panel has decided to award $30,000 for this bug. Nice work.

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-12-30)

This issue was migrated from crbug.com/chromium/1101509?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1117348, crbug.com/chromium/1121548, crbug.com/chromium/1125949, crbug.com/chromium/1129862]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052742)*
