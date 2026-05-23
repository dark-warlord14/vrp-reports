# heap-use-after-free in wl_proxy_marshal_array_flags

| Field | Value |
|-------|-------|
| **Issue ID** | [433027577](https://issues.chromium.org/issues/433027577) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Ozone |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 138.0.0.0 |
| **Reporter** | yu...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2025-07-20 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

The crash occasionally occurs in my fuzzing system and there is currently no stable reproduction case. You can refer to the RCA to fix the issue.

# Problem Description

BISECT
<https://chromium-review.googlesource.com/c/chromium/src/+/3008414>

RCA

1. When Chrome opens on Ubuntu, a ui::WaylandConnection object is created, and display\_ is initialized in WaylandConnection::Initialize().

```
bool WaylandConnection::Initialize(bool use_threaded_polling) {
  ...
  display_.reset(wl_display_connect(nullptr));      // [1]
  if (!display_) {
    PLOG(ERROR) << "Failed to connect to Wayland display";
    return false;
  }
  ...
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_connection.cc;l=195;drc=5c47d5e475326944a7be161b049c73c831cb830e;bpv=1;bpt=1>

2. When a screen saver view is created and suspended, a WaylandScreen object is also created and owned by that view.
   The idle\_inhibitor\_ member of WaylandScreen will be initialized, holding a proxy pointer to ui::WaylandConnection's
   zwp\_idle\_inhibit\_manager. This proxy pointer will be used in Wayland to interact with the display in [1].

```
bool WaylandScreen::SetScreenSaverSuspended(bool suspend) {
  if (!connection_->zwp_idle_inhibit_manager())
    return false;

  if (suspend) {
    ...
    idle_inhibitor_ = connection_->zwp_idle_inhibit_manager()->CreateInhibitor(
        current_window->root_surface()->surface());     // [2]
  } else {
    idle_inhibitor_.reset();
  }

  return true;
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_screen.cc;l=451;drc=5c47d5e475326944a7be161b049c73c831cb830e;bpv=1;bpt=1>

3. If the above two conditions are met, when Chrome closes, the WaylandConnection and its display\_ (which points to a
   wl\_display) may be destroyed before ChromeBrowserMainExtraPartsViews. As a result, a heap-use-after-free will
   occur when the WaylandScreen is destroyed and try to interact the display object [3].

```
WL_EXPORT struct wl_proxy *
wl_proxy_marshal_array_flags(struct wl_proxy *proxy, uint32_t opcode,
			     const struct wl_interface *interface, uint32_t version,
			     uint32_t flags, union wl_argument *args)
{
    ...
	if (proxy->display->last_error) {       // [3]
		goto err_unlock;
	}
    ...
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/wayland/src/src/wayland-client.c;l=911;drc=5c47d5e475326944a7be161b049c73c831cb830e;bpv=1;bpt=1>

# Summary

heap-use-after-free in wl\_proxy\_marshal\_array\_flags

# Custom Questions

#### Type of crash:

browser

#### Crash state:

heap-use-after-free

#### Reporter credit:

V0

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 12.9 KB)
- [full.log](attachments/full.log) (text/plain, 70.5 KB)

## Timeline

### yu...@gmail.com (2025-07-20)

Fuzz target: 	asan-linux-release-1477656
OS system: Ubuntu 24.04
Flags: --no-sandbox --enable-logging=stderr --v=0 

Since the bisect code was submitted on July 13, 2021, this issue may affect the stable channel.

### nh...@chromium.org (2025-07-21)

Thank you for the report. Based on the lack of reproduction steps and the described no stable reproduction case, I'm treating this as a speculative report. If you're able to provide additional information on on conditions to reproduce, that would be appreciated in being able to resolve this bug.

Owner – the Security Team is unable to reproduce this issue based on information provided. If you can diagnose and fix the issue based on information provided, please proceed accordingly. 


### ch...@google.com (2025-07-22)

Setting milestone because of s2 severity.

### ch...@google.com (2025-07-22)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yu...@gmail.com (2025-07-22)

After taking a deeper look into this issue, here are some additional findings:
The root cause appears to be that |chrome.power.requestKeepAwake| triggers [2] in #1. However, when WaylandScreen::WaylandScreenSaverSuspender is destroyed, screen_->SetScreenSaverSuspended(false) is not reached and reset idle_inhibitor_ correctly.
https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_screen.cc;l=422;drc=3e66f7744b7c99572ab6e2c61b259545574688b5

I’m still confusing about how this state reached. Here is the full log of my fuzz output, hope it is useful.

### ch...@google.com (2025-08-05)

fangzhoug: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-20)

fangzhoug: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-13)

fangzhoug: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Kramer Ge [fangzhoug@chromium.org](mailto:fangzhoug@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6979565>

[Ozone/Wayland]Remove idle\_inhibitor\_ object from WaylandScreen

---


Expand for full commit details
```
     
    ..to prevent UAF on chrome shutdown. Unlike most objects created by 
    WaylandConnection, WaylandScreen is owned by ChromeBrowserMainExtraParts 
    and outlives WaylandConnection. 
     
    To prevent accessing wl_display internals after destruction of 
    WaylandConnection, WaylandScreen should either destroy wl::Object when 
    connection resets, or reference wl::Object indirectly. 
     
    Manage inhibitor in zwp_idle_inhibit_manager. Also fix a logic in 
    IsScreenSaverActive() where `inhibitor` mean screen saver is blocked. 
     
    Bug: 433027577, 433643249 
    Change-Id: If02755ddced08f8cf795ac21ed144387d0aa4077 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6979565 
    Commit-Queue: Kramer Ge <fangzhoug@chromium.org> 
    Reviewed-by: Thomas Anderson <thomasanderson@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1520174}

```

---

Files:

- M `ui/ozone/platform/wayland/host/wayland_screen.cc`
- M `ui/ozone/platform/wayland/host/wayland_screen.h`
- M `ui/ozone/platform/wayland/host/zwp_idle_inhibit_manager.cc`
- M `ui/ozone/platform/wayland/host/zwp_idle_inhibit_manager.h`

---

Hash: [454dc266cc0437da6371c65720b722322ef8eecc](https://chromiumdash.appspot.com/commit/454dc266cc0437da6371c65720b722322ef8eecc)  

Date: Thu Sep 25 02:20:27 2025


---

### ch...@google.com (2025-09-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
very highly mitigated memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> very highly mitigated memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/433027577)*
