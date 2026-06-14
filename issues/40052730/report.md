# Security: UAF Read in Content process

| Field | Value |
|-------|-------|
| **Issue ID** | [40052730](https://issues.chromium.org/issues/40052730) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tm...@acu.edu |
| **Assignee** | mc...@chromium.org |
| **Created** | 2020-06-30 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

We found a UAF while fuzzing chrome with the portals enabled flag on (chrome://flags#enable-portals)

**VERSION**  

Chrome Version: 86.0.4187.0 (Developer Build) (64-bit)  

Operating System: 5.3.0-61-generic #55~18.04.1-Ubuntu (Ubuntu 18.04.2 LTS x86\_64)  

\* Note: Did not test on chromiumOS/Windows, I would suspect it works there too

**REPRODUCTION CASE**

1. Enable portals in chrome://flags
2. Install our extension
3. Run "python -m SimpleHTTPServer 8081" (So that is serves the TryMe.html file for the extension)
4. Open chrome, click on our extension icon, and select "Crash remote"
5. You might have to try a few times, but we are currently crashing a majority of the time  
   
   \* Note: We appear to sometimes crash outside of the extension process, however I assume that's some sort of weird cache issue we run into (As the stack traces are pretty similar and I've only seen it once or twice)

FILES  

ASAN.txt - Asan output  

extension\_poc\_PortalUAF.zip - our extension to install  

TryMe.html - reproduction case

NOTE:  

We were told to submit this before completely minimizing the file, and we should have it completely minimized in the next 24hrs or so. That said; the key parts I've identified so far have been noted in the TryMe.html file

ROOT CAUSE ANALYSIS:  

The host implementation pointer is freed during the portal being activated while the window is being torn down; however we are still running javascript that references the dangling pointer. We can see here: <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_widget_targeter.cc;l=381;drc=0ca01450b41850d09069055f1df5d1eafe6167f6;bpv=1;bpt=1?q=FoundFrameSinkId&originalUrl=https:%2F%2Fcs.chromium.org%2F> that once host\_ is freed, controlling it allows us to immediately dereference the pointer, giving us a way to gain %RIP control

**CREDIT INFORMATION**  

Tim Michaud(@TimGMichaud) of Leviathan Security Group and  

Gary Nield (@monobehaviour) of ECSC Group plc

## Attachments

- [ASAN.txt](attachments/ASAN.txt) (text/plain, 16.9 KB)
- [extension_poc_PortalUAF.zip](attachments/extension_poc_PortalUAF.zip) (application/octet-stream, 3.5 KB)
- [TryMe.html](attachments/TryMe.html) (text/plain, 82.5 KB)
- TryMe.html (text/plain, 55.2 KB)

## Timeline

### ca...@chromium.org (2020-06-30)

Assigning low severity since this requires a custom extension to be installed, and the user to interact with the extension.
Devlin: Can you triage this from the extensions side? I also cc'd lfg for thoughts from the portal side. Feel free to reassign as appropriate.

[Monorail components: Blink>HTML>Portal Platform>Extensions]

### ca...@chromium.org (2020-06-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-06-30)

Actually, from https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md it looks like this should be a Medium severity ("Memory corruption that requires a specific extension to be installed"), I'm also changing the impact to None, since portals are enabled by default only on Android, where there are no extensions.

### rd...@chromium.org (2020-06-30)

Thanks for the report!

From a quick scan, it doesn't look like the extension is really needed here - it just seems to be a convenient way to package it.  It seems like the real crash is all from the TryMe.html.  Tentatively removing extensions label; please re-add it if I'm missing something.

Over to jbroman@ for portals triage.

[Monorail components: -Platform>Extensions]

### tm...@acu.edu (2020-06-30)

Any extension that is allowed to open a new tab would be exploitable by this vulnerability, or leveraging a vulnerability in an extension (IE: overwrite the URL used by an extension to open up this malicious webpage / potentially re-using a page opened by an extension [I didn't fully explore this angle]). We've also seen malicious actors buy popular extensions to exploit the user base, and this vulnerability would work for that as well. 

### tm...@acu.edu (2020-06-30)

Forgot to add: Extension is here as it made this the most reliable way to crash the process; I left a note in the Reproduction case as to what I was somewhat seeing without, but it wasn't very reliable. 

### jb...@chromium.org (2020-06-30)

This smells related to d29952586bbb178782a3050fa5dc128e7a3a527f; bouncing to lfg@.

If this is Aura-specific, then yeah, this code is unshipped. If this affects Android, then it may have non-zero impact because we just went into origin trial in M85 beta.

### lf...@chromium.org (2020-06-30)

[Empty comment from Monorail migration]

### lf...@chromium.org (2020-06-30)

I haven't been able to repro, tried both Windows and Linux, including ASAN versions.

I'll keep looking, but if someone has better repro steps please post on the bug.


### tm...@acu.edu (2020-06-30)

Is the extension loading the tab with the repro file and it's just not crashing on your machine? Happy to hop on a call to help sort it out if that's helpful 

### tm...@acu.edu (2020-07-01)

Also not sure if it helps #9, but I'm currently minimizing using the build ya'll publish (gs://chromium-browser-asan/linux-release/asan-linux-release-783710.zip)

### tm...@acu.edu (2020-07-01)

Got it down to around ~56kb (Attached); there appears to be a timing component that I can't *really* nail down with a smaller reproduction file

It appears to be reliant on racing the setting of the portal's source component, activating the portal, and updating a DOM object. My gut says that as Portal is activated the underlying window (which was opened by the Extension) is freed (Since it's no longer considered an extension's window) as it's redirected to the portal source.

### tm...@acu.edu (2020-07-01)

One more thing regarding #9 - The tab has to be active to crash

### tm...@acu.edu (2020-07-02)

Not sure if it helps but here is a crash-id for the bug: 408f6e5c55157343

Used with the following version of chrome (Linux-dev):

Google Chrome	85.0.4181.8 (Official Build) unknown (64-bit)
Revision	7efa53d4db96fc6acaa6fef9318d6f5d8857d0fe-refs/branch-heads/4181@{#15}

### lf...@google.com (2020-07-02)

Thanks, I managed to repro!

Working on a fix now.

### lf...@chromium.org (2020-07-06)

I got a fix out for review, but this is not a UaF. This is a nullptr dereference, and the dereference happens on the base::WeakPtr<>.

The ASAN build reports it as a UaF, but the UaF seems to happen on the ASAN instrumentation.

### lf...@chromium.org (2020-07-06)

+mmoroz Do you know why ASAN would report a UaF here or can you point someone else that could look?

### mm...@chromium.org (2020-07-06)

lfg@ I've just checked the log from c#0 and it looks reasonable to me:

1) new object created https://source.chromium.org/chromium/chromium/src/+/master:content/browser/web_contents/web_contents_view_aura.cc;l=952;drc=e8bf9226f71b98431aa19de59809a6b170b9a1f1?originalUrl=https:%2F%2Fcs.chromium.org%2F

2) it gets deleted 

0x61b0002b6590 is located 16 bytes inside of 1488-byte region [0x61b0002b6580,0x61b0002b6b50)
freed by thread T0 (chrome) here:
    #0 0x55f2637a02bd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55f272c89f3b in aura::Window::~Window() ui/aura/window.cc:164:16
    #2 0x55f272c8b69d in aura::Window::~Window() ui/aura/window.cc:119:19
    #3 0x55f2679fe70a in content::Portal::Activate(blink::TransferableMessage, base::TimeTicks, base::OnceCallback<void (blink::mojom::PortalActivateResult)>) content/browser/portal/portal.cc:442:37


3) but then it gets accessed: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_widget_host_view_base.h;l=496;drc=c135bf157b76215b7c7cac8c110cb9259c11ce33?originalUrl=https:%2F%2Fcs.chromium.org%2F


Sorry I'm a bit out of context here. What makes you think that there is no UaF? Do you see another error while reproducing this locally?

### lf...@chromium.org (2020-07-07)

The access to host() happens here: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_widget_targeter.cc;l=381;drc=e62845d45e7391e9aea92f2892eefb7e3e4f8b32

This is done through a base::WeakPtr that has already been invalidated. See the fixing CL here: https://chromium-review.googlesource.com/c/chromium/src/+/2283824

So, either:

1. There's a problem with the ASAN instrumentation.
2. base::WeakPtr does not work as expected.
3. My CL doesn't fix the issue (since it is only a nullptr check) and there is still a UaF around.



### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6fa7135014c118fa029f3781986c63f8170cc4bc

commit 6fa7135014c118fa029f3781986c63f8170cc4bc
Author: Lucas Gadani <lfg@chromium.org>
Date: Tue Jul 07 18:13:27 2020

Fix crash when processing input.

This CL fixes a  crash when a RenderWidgetHostView is already destroyed
by the time the query IPC is processed.

Bug: 1101001
Change-Id: I046abacf6334fcfd56e3ea2bca07fdb24b5fff4e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2283824
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#785873}

[modify] https://crrev.com/6fa7135014c118fa029f3781986c63f8170cc4bc/content/browser/renderer_host/render_widget_host_input_event_router_unittest.cc
[modify] https://crrev.com/6fa7135014c118fa029f3781986c63f8170cc4bc/content/browser/renderer_host/render_widget_host_view_base.h
[modify] https://crrev.com/6fa7135014c118fa029f3781986c63f8170cc4bc/content/browser/renderer_host/render_widget_targeter.cc


### mm...@chromium.org (2020-07-07)

Are you able to reproduce the issue without applying the fix?

### lf...@chromium.org (2020-07-08)

Re#21: Yes, I can reproduce if I revert the fix. Only on Linux.


### mm...@google.com (2020-07-08)

Well that's indeed weird. I still hardly believe that ASan is working incorrectly. Perhaps more debugging could shed some light, e.g. printing `target` value before

target->host()->input_target_client().set_disconnect_handler(
      base::OnceClosure());

could it be so that this code is executed several times? If `target` was really `nullptr`, then ASan would complain about null-deref rather than UaF.

Another guess: any chance there is a race condition being involved and `target` value isn't always the same across different attempts to reproduce?

### tm...@acu.edu (2020-07-09)

Per #23: From playing around with this last night I typically have three calls into FrameSinkId - with the 2nd one causing the ASAN output linked above. It's super racey and target isn't the same for me across reproduction attempts. I am not seeing target as a nullptr but given how many times I have to run this to get an ASAN crash it wouldn't surprise me if it reproduces as a null-deref in some instances. 

### lf...@chromium.org (2020-07-09)

Re#24: Can you still reproduce in the latest ASAN build (86.0.4196.0 or later)?

### lf...@chromium.org (2020-07-09)

Re#23 I tried printing target.get() as well as target->host(). It'll print null for the first one, and it doesn't print the second line, reporting a UaF.


### tm...@acu.edu (2020-07-09)

Ref#25: I am not - I think this fixes this issue as per #26 (The null check happening before the host check prevents the UAF, though I believe this would mean that other uses of target->host() might also be vulnerable). I will let it run for another hour or so on d9b3fdc3340fb59b7e1ed61a0bb06317005d563e and report back if I can get a crash. 

### lf...@chromium.org (2020-07-09)

If the null check prevents the UaF, then either there was no UaF in the first place (ASAN working incorrectly), or there's a bug in base::WeakPtr<>.

+ajwong as base OWNER, can you take a look?


### tm...@acu.edu (2020-07-09)

After ~1.5 hours of re running the POC it isn't crashing (See C#27). It's possible the race is unwinnable now since it was already a tight race when initially submitted.

### lf...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### tm...@acu.edu (2020-08-21)

Any update on this?

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-05-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-02-14)

jbroman@: Do you think you can retriage this? It is a Portals UAF report that got dropped on the floor a while back, and everyone who had been involved in investigating it has since left the project.

### jb...@chromium.org (2022-03-02)

mcnee@, would you mind taking a look (you were a reviewer on some of the relevant CLs)? Not super urgent because Portals is now off but it would be nice to have this bug wrapped up one way or another.

### mc...@chromium.org (2022-03-30)

I'm afraid I'm not able to reproduce this using any of the test cases, even if I revert lfg@'s CL in c#20.

I think I agree with lfg@'s comments above about this just being a case of a null dereference. From stepping through the destruction code, I don't see how the `host()` could be outlived.

So I'm not really sure how to resolve this. The CL in c#20 fixed a null pointer dereference, but it doesn't look like we have an actual UAF. I'll go ahead and mark this fixed.

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-14)

A belated congratulations and resolution, Tim and Gary. Apologies for the large time delta from report to resolution; however, the VRP Panel would like to extend a $15,000 reward for this report. Thanks for your efforts and reporting this issue to us! 

### tm...@acu.edu (2022-04-14)

Awesome, thanks a lot :)! 

### tm...@acu.edu (2022-04-14)

Is it possible to change the credits to:

Tim Michaud(@TimGMichaud) of Zoom Video Communications, Inc and
Gary Nield of ECSC Group plc

Thanks :)!

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-07-07)

This issue was migrated from crbug.com/chromium/1101001?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052730)*
