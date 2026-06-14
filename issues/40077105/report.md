# Security: Possible path traversal in file_util::AbsolutePath (Windows XP/2K3)

| Field | Value |
|-------|-------|
| **Issue ID** | [40077105](https://issues.chromium.org/issues/40077105) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core |
| **Platforms** | Windows |
| **Reporter** | kr...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2013-03-11 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

There is a possible path traversal in implementation of file\_util::AbsolutePath under Windows (XP/2K3).  

This implementation uses \_wfullpath <http://msdn.microsoft.com/en-us/library/506720ff(v=vs.80).aspx>  

which internally calls GetFullPathNameW <http://msdn.microsoft.com/en-us/library/windows/desktop/aa364963(v=vs.85).aspx>  

However this function (on WinXP/2K3) incorrectly translates dot-dot-dot path sequences into dot-dot,

**VERSION**  

Chrome Version: [Revision: 722 and up to today] + [any]  

Operating System: Windows XP, 5.1, SP3

**REPRODUCTION CASE**  

Using file\_util::AbsolutePath("C:/myapp/ext/mydir/.../.../.../passwords.txt") gives this results:

- Windows 7/8: "C:\myapp\ext\mydir.........\passwords.txt" (invalid path, can't open file so it's OK)
- Windows XP: "C:\myapp\ext\mydir......\passwords.txt" (valid path from root directory!)  
  
  (Example that uses \_wfullpath/\_fullpath in attached test1.cpp - run it under WinXP)

My "first thought workaround" for file\_util::AbsolutePath (src\base\file\_util\_win.cc)  

is to make an additional check/scan for ".." after calling \_wfullpath and failing this function in this case.  

This would also make paths with "..." invalid.

I do not know chrome source enough to make an exploit (if it's possible at all),  

but searching src for "file\_util::AbsolutePath" gives several results.  

Some of them I've described in attached src-file\_util\_AbsolutePath.txt

I've found only that after opening this url in Chrome (under XP):  

chrome-extension://aohghmighlieiainnegkcijnfilokake/.../.../.../.../.../.../.../.../.../.../.../.../.../.../.../index.html  

then Process Monitor shows that chrome.exe accesses file C:\index.html with SUCCESS,  

but Chrome at the end gives Error 9 (net::ERR\_UNEXPECTED): Unknown error. (Clipboard01.jpg)  

So it's possible that it's secured other way.

## Attachments

- [test1.cpp](attachments/test1.cpp) (text/x-c; charset=us-ascii, 407 B)
- [Clipboard01.jpg](attachments/Clipboard01.jpg) (image/jpeg; charset=binary, 83.1 KB)
- [src-file_util_AbsolutePath.txt](attachments/src-file_util_AbsolutePath.txt) (text/x-c++; charset=us-ascii, 1.4 KB)
- [Chrome-on-WXP-r175641.jpg](attachments/Chrome-on-WXP-r175641.jpg) (image/jpeg; charset=binary, 294.4 KB)

## Timeline

### ts...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-03-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-03-12)

Bumping to high-severity since this is being used as a primary security check in some paces.

### js...@chromium.org (2013-03-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-19)

[Empty comment from Monorail migration]

### kr...@gmail.com (2013-03-20)

I've setup chrome build and debugged a little "C:\index.html" file access.
You can get to this directly by chrome-extensions://... or by extension it-self (like loading script from html, or opening file from js/script via XHR).

This file is accessed by:
GetFileAttributes("C:\profile\Default\Extensions\bmagokdooijbeehmkpknfglimnifench\1.4.0.11967_0\..\..\..\..\..\index-security.html")

from this stack:

ChildEBP RetAddr  
1e31fb94 03ecbc9e base!file_util::PathExists+0x9 [c:\chromiumtrunk\src\base\file_util_win.cc @ 290]
1e31fc7c 03ecb89e chrome_1070000!ExtensionResource::GetFilePath+0x2ee [c:\chromiumtrunk\src\chrome\common\extensions\extension_resource.cc @ 89]
1e31fd9c 03514bac chrome_1070000!ExtensionResource::GetFilePath+0x1ae [c:\chromiumtrunk\src\chrome\common\extensions\extension_resource.cc @ 42]
1e31fda8 03519b84 chrome_1070000!`anonymous namespace'::ReadResourceFilePath+0xc [c:\chromiumtrunk\src\chrome\browser\extensions\extension_protocols.cc @ 196]
1e31fdc0 03519885 chrome_1070000!base::internal::RunnableAdapter<void (__cdecl*)(ExtensionResource const &,base::FilePath *)>::Run+0x34 [c:\chromiumtrunk\src\base\bind_internal.h @ 228]
1e31fdd0 0351955f chrome_1070000!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__cdecl*)(ExtensionResource const &,base::FilePath *)>,void __cdecl(ExtensionResource const &,base::FilePath *)>::MakeItSo+0x25 [c:\chromiumtrunk\src\base\bind_internal.h @ 900]
1e31fdf8 1005e91f chrome_1070000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl*)(ExtensionResource const &,base::FilePath *)>,void __cdecl(ExtensionResource const &,base::FilePath *),void __cdecl(ExtensionResource,base::internal::UnretainedWrapper<base::FilePath>)>,void __cdecl(ExtensionResource const &,base::FilePath *)>::Run+0x6f [c:\chromiumtrunk\src\base\bind_internal.h @ 1257]
1e31fe10 101b6eba base!base::Callback<void __cdecl(void)>::Run+0x2f [c:\chromiumtrunk\src\base\callback.h @ 396]
1e31fe40 101b789b base!base::`anonymous namespace'::PostTaskAndReplyRelay::Run+0x4a [c:\chromiumtrunk\src\base\threading\post_task_and_reply_impl.cc @ 45]
1e31fe50 101b784a base!base::internal::RunnableAdapter<void (__thiscall base::`anonymous namespace'::PostTaskAndReplyRelay::*)(void)>::Run+0x1b [c:\chromiumtrunk\src\base\bind_internal.h @ 134]
1e31fe5c 101b77aa base!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall base::`anonymous namespace'::PostTaskAndReplyRelay::*)(void)>,void __cdecl(base::`anonymous namespace'::PostTaskAndReplyRelay *)>::MakeItSo+0x1a [c:\chromiumtrunk\src\base\bind_internal.h @ 872]
1e31fe7c 1005e91f base!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall base::`anonymous namespace'::PostTaskAndReplyRelay::*)(void)>,void __cdecl(base::`anonymous namespace'::PostTaskAndReplyRelay *),void __cdecl(base::internal::UnretainedWrapper<base::`anonymous namespace'::PostTaskAndReplyRelay>)>,void __cdecl(base::`anonymous namespace'::PostTaskAndReplyRelay *)>::Run+0x4a [c:\chromiumtrunk\src\base\bind_internal.h @ 1173]
1e31fe94 101e58b3 base!base::Callback<void __cdecl(void)>::Run+0x2f [c:\chromiumtrunk\src\base\callback.h @ 396]
1e31fef8 7c92796d base!base::`anonymous namespace'::WorkItemCallback+0x113 [c:\chromiumtrunk\src\base\threading\worker_pool_win.cc @ 33]
1e31ff40 7c9279ab ntdll!RtlpWorkerCallout+0x70
1e31ff60 7c927a6d ntdll!RtlpExecuteWorkerRequest+0x1a
1e31ff74 7c927a44 ntdll!RtlpApcCallout+0x11
1e31ffb4 7c80b729 ntdll!RtlpWorkerThread+0x87
1e31ffec 00000000 kernel32!BaseThreadStart+0x37

In extension_resource.cc(ExtensionResource::GetFilePath) you can read that:
  // The relative path must not resolve to a location outside of
  // |extension_root|. Iff |file_can_symlink_outside_root| is true, then the
  // file can be a symlink that links outside of |extension_root|.

However as you see below, it can go outside of |extension_root|

...
  // We must resolve the absolute path of the combined path when
  // the relative path contains references to a parent folder (i.e., '..').
  // We also check if the path exists because the posix version of AbsolutePath
  // will fail if the path doesn't exist, and we want the same behavior on
  // Windows... So until the posix and Windows version of AbsolutePath are
  // unified, we need an extra call to PathExists, unfortunately.
  // TODO(mad): Fix this once AbsolutePath is unified.
  if (file_util::AbsolutePath(&full_path) &&            <- full_path == "C:\profile\Default\Extensions\bmagokdooijbeehmkpknfglimnifench\1.4.0.11967_0\...\...\...\...\...\index-security.html"
      file_util::PathExists(full_path) &&               <- GetFileAttributes("C:\profile\Default\Extensions\bmagokdooijbeehmkpknfglimnifench\1.4.0.11967_0\..\..\..\..\..\index-security.html") Success (because AbsolutePath/_wfullpath converted "..." into "..")
      (symlink_policy == FOLLOW_SYMLINKS_ANYWHERE ||
       clean_extension_root.IsParent(full_path))) {     <- IsParent -> true!!!
    return full_path;                                   <- full_path == "C:\profile\Default\Extensions\bmagokdooijbeehmkpknfglimnifench\1.4.0.11967_0\..\..\..\..\..\index-security.html"
  }
...

But because of recently added security check https://codereview.chromium.org/11782005
  if (name.ReferencesParent()) { <---
    if (error)
      *error = PLATFORM_FILE_ERROR_ACCESS_DENIED;
    return kInvalidPlatformFileValue;  <---
  }

this file cannot be opened. I can guess that before r175642, extensions could read user files by XHR.open(...) outside extensions directory.

0:005> k
ChildEBP RetAddr  
193ffc90 0c0e874b base!base::CreatePlatformFile+0x21 [c:\chromiumtrunk\src\base\platform_file.cc @ 24]
193ffcd8 0c0ed740 net!net::FileStream::Context::OpenFileImpl+0x3b [c:\chromiumtrunk\src\net\base\file_stream_context.cc @ 192]
193ffd0c 0c0ed3f8 net!base::internal::RunnableAdapter<net::FileStream::Context::OpenResult (__thiscall net::FileStream::Context::*)(base::FilePath const &,int)>::Run+0x50 [c:\chromiumtrunk\src\base\bind_internal.h @ 248]
...

But I'm not sure about other places that calls file_util::AbsolutePath with user/extension/etc. input.

### [Deleted User] (2013-03-21)

Bulk Edit

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### kr...@gmail.com (2013-03-22)

I've build Chrome r175641, and can confirm that extension could read any file from drive where profile/extensions directory was located (so in most cases on drive C).

### in...@chromium.org (2013-04-03)

M26 has sailed. Moving all m25 bugs to m26.

### js...@chromium.org (2013-04-12)

I plan on knocking this out today or tomorrow. The fix is trivial, but I have a bunch of tests to update.

### js...@chromium.org (2013-04-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-18)

------------------------------------------------------------------------
r148507 | jschuh@chromium.org | 2013-04-16T23:33:42.947224Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/op-get-entry-expected.txt?r1=148507&r2=148506&pathrev=148507
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/resources/op-get-entry.js?r1=148507&r2=148506&pathrev=148507

Updating HTML Filesystem tests for Windows quirks

Windows may handle path components in odd ways
(e.g. truncating or ignoring certain leading or
trailing characters). I have a patch for this
in Chromium, but first I need to fix the WebKit
tests.

R=kinuko@chromium.org
BUG=181617

Review URL: https://codereview.chromium.org/13932031
------------------------------------------------------------------------

### jo...@chromium.org (2013-05-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### bu...@chromium.org (2013-05-13)

------------------------------------------------------------------------
r150169 | jschuh@chromium.org | 2013-05-11T17:54:04.950016Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/resources/op-get-entry.js?r1=150169&r2=150168&pathrev=150169
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/op-get-entry-expected.txt?r1=150169&r2=150168&pathrev=150169

Disable ... filepath tests as part of multipart fix

These tests will be re-enabled with different error codes
after the third chunk lands.

BUG=181617

Review URL: https://chromiumcodereview.appspot.com/14705011
------------------------------------------------------------------------

### bu...@chromium.org (2013-05-16)

------------------------------------------------------------------------
r200603 | jschuh@chromium.org | 2013-05-16T19:29:39.831409Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/fileapi/sandbox_mount_point_provider_unittest.cc?r1=200603&r2=200602&pathrev=200603
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path_unittest.cc?r1=200603&r2=200602&pathrev=200603
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path.cc?r1=200603&r2=200602&pathrev=200603

Make Windows traversal checking handle pathological cases 

Different versions of Windows have undocumented quirks in handling path components 
(e.g. truncating or ignoring certain leading or trailing characters). In order to avoid potential 
security bugs we're going to treat components more loosely and risk a few unlikely false 
positives from FilePath::ReferencesParent(). 

BUG=181617
R=brettw@chromium.org, ericu@chromium.org

Review URL: https://codereview.chromium.org/12771015
------------------------------------------------------------------------

### bu...@chromium.org (2013-05-16)

------------------------------------------------------------------------
r200610 | rouslan@chromium.org | 2013-05-16T19:46:56.717083Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/fileapi/sandbox_mount_point_provider_unittest.cc?r1=200610&r2=200609&pathrev=200610
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path_unittest.cc?r1=200610&r2=200609&pathrev=200610
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path.cc?r1=200610&r2=200609&pathrev=200610

Revert 200603 "Make Windows traversal checking handle pathologic..."

Seems to have broken base_unittests on Linux ASAN.

> Make Windows traversal checking handle pathological cases 
> 
> Different versions of Windows have undocumented quirks in handling path components 
> (e.g. truncating or ignoring certain leading or trailing characters). In order to avoid potential 
> security bugs we're going to treat components more loosely and risk a few unlikely false 
> positives from FilePath::ReferencesParent(). 
> 
> BUG=181617
> R=brettw@chromium.org, ericu@chromium.org
> 
> Review URL: https://codereview.chromium.org/12771015

TBR=jschuh@chromium.org

Review URL: https://codereview.chromium.org/15095015
------------------------------------------------------------------------

### bu...@chromium.org (2013-05-17)

------------------------------------------------------------------------
r200707 | jschuh@chromium.org | 2013-05-17T02:27:46.184530Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path_unittest.cc?r1=200707&r2=200706&pathrev=200707
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/files/file_path.cc?r1=200707&r2=200706&pathrev=200707
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/fileapi/sandbox_mount_point_provider_unittest.cc?r1=200707&r2=200706&pathrev=200707

Make Windows traversal checking handle pathological cases 

Different versions of Windows have undocumented quirks in handling path components 
(e.g. truncating or ignoring certain leading or trailing characters). In order to avoid potential 
security bugs we're going to treat components more loosely and risk a few unlikely false 
positives from FilePath::ReferencesParent(). 

BUG=181617
R=brettw@chromium.org, ericu@chromium.org

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=200603

Review URL: https://codereview.chromium.org/12771015
------------------------------------------------------------------------

### js...@chromium.org (2013-05-17)

Oddly enough, this trivial fix took a long time to land due to various test issues. Also, on further reflection I think the bug is more accurately a medium severity now that I've confirmed it affects only Windows XP, which is already a grossly deficient platform on the security front. However, it's a very clever bug and a good report, so I'm flagging it with a reward nomination.

### sc...@gmail.com (2013-05-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-26)

@krystian.bigaj: thanks reporting this clever bug to us!

Although it only affects XP, it's kind of an interesting issue, so we're happy to reward your discovery with a $1337 Chromium Security Reward :D

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### kr...@gmail.com (2013-07-02)

Thanks :) If there will be any credits please use: Krystian Bigaj

One more about that issue with GetFullPathName/_fullpath (on XP/2k3), I haven't found any 'warnings' about "..."/".. " problem with this function, however there are many threads/posts that people suggest to use this function for canonicalize/normalize paths (even for security purposes), also many cases suggest it as a Unix 'realpath' replacement on Windows. It's possible that some libraries/programs ported from Unix/Linux might be affected by this issue.
I think that it might be not very well know problem (if at all?), so have you forwarded any notice to other Google Security teams (like security@google.com)? :)

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171330

------------------------------------------------------------------
r171330 | ltilve@igalia.com | 2014-04-11T10:16:19.806038Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/op-get-entry-expected.txt?r1=171330&r2=171329&pathrev=171330
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/filesystem/resources/op-get-entry.js?r1=171330&r2=171329&pathrev=171330

Fix filepath tests for EncodingError

As the issue on the management of dot-dot-dot path sequences has been
solved, this change re-enables and fixes the filepath  tests and removes
the corresponding FIXMEs.

BUG=181617

Review URL: https://codereview.chromium.org/227093003
-----------------------------------------------------------------

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/181617?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077105)*
