# Security: Cross-origin scripting possible via native functions

| Field | Value |
|-------|-------|
| **Issue ID** | [40082234](https://issues.chromium.org/issues/40082234) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Reporter** | pi...@live.nl |
| **Assignee** | yu...@chromium.org |
| **Created** | 2015-06-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to run JavaScript in a different context (e.g. in a different origin) via certain extension functions exposed to regular webpages (see <https://crbug.com/chromium/468931>). I am filing this as a separate issue since I think this particular exploit is worth fixing as soon as possible (the general case, <https://crbug.com/chromium/468931>, appears hard to fix).

For this issue I was inspired by [1].

The idea is to leak the function "runWithModuleSystem" inside "test\_custom\_bindings.js". This exposes the "requireNative" function to the attacker's web page, which can be used to leak the JavaScript wrapper for the function "TakeBrowserProcessBlob" in "blob\_native\_handler.cc". The problem is that this function sets the return value using "args.Holder()" as the creation context. This can be faked as in [1] to get the return value object in a different context. The technique from [1] (see the test there) can then be used to run JavaScript code cross-origin.

**VERSION**  

Chrome Version: 43.0.2357.81 m stable, also 45.0.2424.0 downloaded from [2] (r333129)  

Operating System: Stable on Windows 8.1, trunk on Windows Vista

**REPRODUCTION CASE**  

See the attachments. I based them on the ones in <https://crbug.com/chromium/468931>. Save both files in the same directory and open "parent.html". The sandboxed iframe "child.html" is able to modify the parent's background color.

[1] <https://codereview.chromium.org/1163893002>  

[2] <https://commondatastorage.googleapis.com/chromium-browser-syzyasan/index.html?prefix=win32-release/>

## Attachments

- [child.html](attachments/child.html) (text/html, 2.6 KB)
- [parent.html](attachments/parent.html) (text/html, 117 B)

## Timeline

### oc...@chromium.org (2015-06-06)

CCing the same people in the original bug.

### cl...@chromium.org (2015-06-06)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-06-07)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-06-08)

The cause is at line 37 of blob_native_handler.cc:
https://code.google.com/p/chromium/codesearch#chromium/src/extensions/renderer/blob_native_handler.cc&l=37
where |args.Holder()| is passed as the creation context, but it could be faked by user script.  We should pass |args.GetIsolate()->GetCurrentContext()->Global()| instead as the current context where the script is running.

Having said that, the fix on this line fixes the reported case only, but also there are many similar extension APIs.  So one line change doesn't fix all the cases.

I'm now trying a fix on Blink's side as https://codereview.chromium.org/1166793006/ .  The CL makes Blink ignore the creation context given from the API callers, and always use the current context.  If this change doesn't break anything, we may land the CL.

However, please remember that the use cases of Blink's public APIs in Chromium is wrong.  The current public APIs of Blink trust the caller to pass the right creation context.

### bu...@chromium.org (2015-06-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196755

------------------------------------------------------------------
r196755 | yukishiino@chromium.org | 2015-06-09T11:34:24.477498Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebBlob.cpp?r1=196755&r2=196754&pathrev=196755
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebArrayBufferConverter.cpp?r1=196755&r2=196754&pathrev=196755
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDOMFileSystem.cpp?r1=196755&r2=196754&pathrev=196755
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDOMError.cpp?r1=196755&r2=196754&pathrev=196755

bindings: Stop using the given creationContext in public APIs.

The creation context passed through the public APIs may be unsafe
and faked by user script.  The callers of the APIs often do not
check if the context is safe and valid or not.  Plus, there shouldn't
be a case that a caller needs to handle cross-origin cases, so let us
always use the current context instead of the creation context given
through the callers, which are not reliable.

BUG=497507

Review URL: https://codereview.chromium.org/1166793006
-----------------------------------------------------------------

### yu...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-06-10)

Lets keep bug in fixed state. merges are tracked via merge labels.

### cl...@chromium.org (2015-06-10)

[Empty comment from Monorail migration]

### pe...@google.com (2015-06-10)

[Automated comment] Request affecting a post-stable build (M43), manual review required.

### pe...@google.com (2015-06-10)

Approved for M44 (branch: 2403)

### bu...@chromium.org (2015-06-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196863

------------------------------------------------------------------
r196863 | yukishiino@chromium.org | 2015-06-10T12:57:48.066987Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/WebBlob.cpp?r1=196863&r2=196862&pathrev=196863
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/WebArrayBufferConverter.cpp?r1=196863&r2=196862&pathrev=196863
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/WebDOMFileSystem.cpp?r1=196863&r2=196862&pathrev=196863
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/WebDOMError.cpp?r1=196863&r2=196862&pathrev=196863

Merge 196755 "bindings: Stop using the given creationContext in ..."

> bindings: Stop using the given creationContext in public APIs.
> 
> The creation context passed through the public APIs may be unsafe
> and faked by user script.  The callers of the APIs often do not
> check if the context is safe and valid or not.  Plus, there shouldn't
> be a case that a caller needs to handle cross-origin cases, so let us
> always use the current context instead of the creation context given
> through the callers, which are not reliable.
> 
> BUG=497507
> 
> Review URL: https://codereview.chromium.org/1166793006

TBR=yukishiino@chromium.org

Review URL: https://codereview.chromium.org/1168973003
-----------------------------------------------------------------

### bu...@chromium.org (2015-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/42bd05a2bf4260f500687a2457d01e298033f2bb

commit 42bd05a2bf4260f500687a2457d01e298033f2bb
Author: yukishiino <yukishiino@chromium.org>
Date: Mon Jun 15 08:17:08 2015

blink:bindings: Passes the global context instead of |this| in JS.

|this| in JS (args.Holder() in C++ code) is not a reliable object.  User
script can pass any object as |this|.  So we shouldn't use it as creation
context when calling Blink APIs to create a new DOM wrapper.

We should instead use the current context where the user script is running
as creation context.

BUG=497507

Review URL: https://codereview.chromium.org/1174343003

Cr-Commit-Position: refs/heads/master@{#334366}

[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/chrome/renderer/extensions/file_manager_private_custom_bindings.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/chrome/renderer/extensions/media_galleries_custom_bindings.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/chrome/renderer/extensions/media_galleries_custom_bindings.h
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/chrome/renderer/extensions/page_capture_custom_bindings.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/chrome/renderer/extensions/sync_file_system_custom_bindings.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/extensions/renderer/app_runtime_custom_bindings.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/extensions/renderer/app_runtime_custom_bindings.h
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/extensions/renderer/blob_native_handler.cc
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/extensions/renderer/blob_native_handler.h
[modify] http://crrev.com/42bd05a2bf4260f500687a2457d01e298033f2bb/extensions/renderer/file_system_natives.cc


### bu...@chromium.org (2015-06-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197105

------------------------------------------------------------------
r197105 | yukishiino@chromium.org | 2015-06-15T09:36:25.161207Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebBlob.cpp?r1=197105&r2=197104&pathrev=197105
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebArrayBufferConverter.cpp?r1=197105&r2=197104&pathrev=197105
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDOMFileSystem.cpp?r1=197105&r2=197104&pathrev=197105
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDOMError.cpp?r1=197105&r2=197104&pathrev=197105

bindings: Adds ASSERTs to check the creation context passed to public APIs.

As a follow up of http://crrev.com/1166793006 , adds check if the creation
context passed to public API is the same as the global context.

BUG=497507

Review URL: https://codereview.chromium.org/1181943005
-----------------------------------------------------------------

### la...@google.com (2015-06-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-06-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197234

------------------------------------------------------------------
r197234 | yukishiino@chromium.org | 2015-06-17T05:52:19.530673Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/web/WebDOMError.cpp?r1=197234&r2=197233&pathrev=197234
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/web/WebBlob.cpp?r1=197234&r2=197233&pathrev=197234
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/web/WebArrayBufferConverter.cpp?r1=197234&r2=197233&pathrev=197234
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/web/WebDOMFileSystem.cpp?r1=197234&r2=197233&pathrev=197234

Merge 196755 "bindings: Stop using the given creationContext in ..."

> bindings: Stop using the given creationContext in public APIs.
> 
> The creation context passed through the public APIs may be unsafe
> and faked by user script.  The callers of the APIs often do not
> check if the context is safe and valid or not.  Plus, there shouldn't
> be a case that a caller needs to handle cross-origin cases, so let us
> always use the current context instead of the creation context given
> through the callers, which are not reliable.
> 
> BUG=497507
> 
> Review URL: https://codereview.chromium.org/1166793006

TBR=yukishiino@chromium.org

Review URL: https://codereview.chromium.org/1186023004
-----------------------------------------------------------------

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-16)

Bulk update: removing view restriction from closed bugs.

### as...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-28)

Hey Pim - found this old bug in a cleanup that hadn't been voted on. 

Pleased to let you know that our reward panel decided in $7,500 for this report. Congrats! We'll start payment processing next week.

### aw...@chromium.org (2016-07-01)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/497507?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082234)*
