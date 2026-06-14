# Security: CheckDuplicateHandle (BreakDebugger) browser crash with (Web) Workers and WebSQL

| Field | Value |
|-------|-------|
| **Issue ID** | [40077590](https://issues.chromium.org/issues/40077590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2013-05-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome (browser process) crashes with a CheckDuplicateHandle (BreakDebugger) crash when:

1. Minimized script:  
   
   The browser's history is erased (minimized case) while (multiple) webworkers are triggering a reload from their onmessage event.
2. Extended script:  
   
   Same as 1, but does not require erasing history

The log is the same in both cases:

...  

[3612:3504:0523/165945:FATAL:sandbox\_win.cc(426)] Check failed: !(basic\_info.GrantedAccess & kDangerousMask). You are attempting to duplicate a privileged handle into a sandboxed process.  

Please use the sandbox::BrokerDuplicateHandle API or contact [security@chromium.org](mailto:security@chromium.org) for assistance.

**VERSION**  

Chrome Version: all (29.0.1517.0 used), issue may be more reliable on recent ToT versions  

Operating System: Windows XP SP3 (and others)

**REPRODUCTION CASE**

1. Launch the minimized script with a clean profile and (fully) erase history
2. Launch the extended script with a clean profile

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see added trace/log files

## Attachments

- [WebSQL_breakdebugger_browser_crash__extended_trace_&_log.txt](attachments/WebSQL_breakdebugger_browser_crash_extended_trace_&_log.txt) (text/x-c++; charset=us-ascii, 69.4 KB)
- [WebSQL_breakdebugger_browser_crash__minimized_repro.html](attachments/WebSQL_breakdebugger_browser_crash_minimized_repro.html) (text/plain; charset=us-ascii, 287 B)
- [WebSQL_breakdebugger_browser_crash__extended_repro.html](attachments/WebSQL_breakdebugger_browser_crash_extended_repro.html) (text/plain; charset=us-ascii, 1.5 KB)
- [WebSQL_breakdebugger_browser_crash__minimized_trace_&_log.txt](attachments/WebSQL_breakdebugger_browser_crash_minimized_trace_&_log.txt) (text/x-c++; charset=us-ascii, 97.0 KB)

## Timeline

### js...@chromium.org (2013-05-23)

Ugh... we have a race in the browser process and we're duping a stale file handle that turns out to be reused as a process handle. That's just ugly.

### me...@google.com (2013-05-23)

It looks like the race is in DatabaseMessageFilter::OnDatabaseOpenFile where there is a check for db_tracker_->IsDatabaseScheduledForDeletion(...).

### jl...@chromium.org (2013-05-23)

Michael: would you be a good owner for this? Otherwise, could you help in finding an owner?

I'm tentatively assigning Medium severity: looks like a potential sandbox escape, but probably requires arbitrary code execution in the renderer to do something useful. But this could be High.


### mi...@chromium.org (2013-05-23)

@jschuh, what do you mean "a file handle that resuled as a process handle"? And how is it stale?

@meacer, what is the IsDatabaseScheduledForDeletion test racing with?

### me...@google.com (2013-05-23)

> @meacer, what is the IsDatabaseScheduledForDeletion test racing with?

The repro says to erase the history while running the test case. I guess the database is scheduled for deletion after IsDatabaseScheduledForDeletion check is done, and gets deleted before the handle is duplicated. I didn't try to reproduce or look closely into this though, so take this with a grain of salt :)

### mi...@chromium.org (2013-05-23)

The deletion of websql database files occurs on the same thread of control that this code executes on, so shouldn't be racey.

According to the log, we're trying to dup an INVALID_HANDLE_VALUE in this call...
IPC::GetFileHandleForProcess(void * handle = 0xffffffff, void * process = 0x00000740, bool close_source_handle = true)
... big deal? I don't see why that ultimately warrants a CRASH in sandbox_win.cc (wtf)?

PlatformFileForTransit GetFileHandleForProcess(base::PlatformFile handle,
                                               base::ProcessHandle process,
                                               bool close_source_handle)
...should just return IPC::InvalidPlatformFileForTransit() if 'handle' == kInvalidPlatformFileValue.

Maybe somebody on the security team can tone down the black ice?

### js...@chromium.org (2013-05-24)

Ah, there's no race. INVALID_HANDLE_VALUE is -1, and so is the pseudo handle handle for the current process (thanks Windows). So, this would copy a full privilege handle for the browser into the sandboxed process, effectively shutting off the sandbox. It's pretty much the worst thing the browser process could ever do on Windows.

### js...@chromium.org (2013-05-24)

Didn't realize this doesn't require user intervention. So, upping the severity and priority since it's an arbitrary sandbox escape on Windows.

On reflection, I should consider making CheckDuplicateHandle fire in official builds as well.

### me...@google.com (2013-05-24)

FYI, it looks like MHTMLGenerationManager::CreateFile has the same pattern: GetFileHandleForProcess can potentially be called with INVALID_HANDLE_VALUE.

### in...@chromium.org (2013-05-24)

Assigning to Justin for this part "I should consider making CheckDuplicateHandle fire in official builds as well." :)

### js...@chromium.org (2013-05-24)

Yeah, I don't think I'm gonna do that. As an immediate mitigation I'm just going to have GetFileHandleForProcess check for INVALID_HANDLE_VALUE. The rationale here is that only the file and pipe functions use INVALID_HANDLE_VALUE, so it's easy enough to catch this there.

More broadly, I'll have to think about longer term solutions to this pattern. CheckDuplicateHandle was supposed to make it easy to catch these early, but it relies on us having sufficient code coverage.

### pa...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-05-24)

Can we make CheckDuplicateHandle explicitly check for -1 in release + debug ? And the rest of the check could stay DEBUG only.

### js...@chromium.org (2013-05-24)

Browser process hooks in official builds are almost always a bad idea.

### js...@chromium.org (2013-05-24)

This is a trivial merge that we'll want to pick up for the next release.

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-05-28)

Fixed: https://src.chromium.org/viewvc/chrome?revision=202207&view=revision

### sc...@gmail.com (2013-05-28)

M27 is r202611
M28 is r202612

### sc...@gmail.com (2013-06-03)

@therealholden: great find. We'll reward this one at the $2000 level.

### th...@gmail.com (2013-06-03)

Thanks!

### sc...@gmail.com (2013-06-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2021-10-08)

At some point Microsoft added warning text relevant to this bug, so just leaving a copy here for reference:
https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights#:~:text=Warning

### gi...@appspot.gserviceaccount.com (2021-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e62b54cfb3111a1911d866c73f01877e14a3c655

commit e62b54cfb3111a1911d866c73f01877e14a3c655
Author: Justin Schuh <jschuh@chromium.org>
Date: Sat Oct 09 00:53:27 2021

Add check to prevent privileged process handle duplication

This is a defense-in-depth measure to prevent a process from copying
its fully privileged pseudo-handle into a lesser privileged process.

BUG=243339

Change-Id: I3c905073e0c6931034028680c7098e94d8f8ff95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3214578
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Justin Schuh <jschuh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#929941}

[modify] https://crrev.com/e62b54cfb3111a1911d866c73f01877e14a3c655/mojo/public/cpp/platform/platform_handle.cc


### is...@google.com (2021-10-09)

This issue was migrated from crbug.com/chromium/243339?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077590)*
