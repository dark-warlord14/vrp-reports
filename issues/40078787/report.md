# Security: Windows Sandbox Anonymous Kernel Object Unrestricted DACL

| Field | Value |
|-------|-------|
| **Issue ID** | [40078787](https://issues.chromium.org/issues/40078787) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox |
| **Platforms** | Windows |
| **Reporter** | ty...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2014-01-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

The Windows sandbox relies heavily on duplicating various handles into the sandboxed processes from the broker to provide for things like IPC. Probably the most used is the SharedMemory class which wraps sharing of section objects up in a relatively platform independent manner.

On Windows the SharedMemory class uses anonymous section objects (i.e. backed by swap and not named in the object namespace). This has the effect of assigning a default NULL DACL to the kernel object associated with this section. You can confirm this by looking up the section handle in something like Process Explorer or Process Hacker and checking its DACL.

This has an interesting consequence when used to duplicate sections between processes, namely that the NULL DACL means there are effectively no permissions associated with the object (this includes bypassing integrity level checks). So a sandboxed process can use DuplicateHandle to increase the access mask of a section handle in their process. This might be most important if the broker code calls SharedMemory::ShareReadOnlyToProcess or similar assuming that it means the sandbox process cannot tamper with it, and only read it.

The only place I've seen this being used, and not sure its for security necessarily is the sharing of user/Greasemonkey scripts. You might be able to cause issues with other renderer processes this way by changing the section to R/W and corrupting the data. You might also be able to resize the section to cause issues such as reducing it and then placing memory at that address.

Note that this affects any sandboxed process including renderers. It probably will only work if the object was opened with write permissions first then mapped read only in the sandbox. Also note that it should affect any anonymous kernel object such as events and semaphores but they are probably uninteresting.

**VERSION**  

Chrome Version: 34.0.1806.0 (247121)  

Operating System: Windows 7 SP1 x64

**REPRODUCTION CASE**

Just call DuplicateHandle in process on an anonymous section handle of your choosing. You should be able to increase permissions to include SECTION\_ALL\_ACCESS.

## Attachments

- [nulldacl.cpp](attachments/nulldacl.cpp) (application/octet-stream, 2.3 KB)

## Timeline

### js...@chromium.org (2014-01-27)

This one is pretty cool. Carlos, Rick, thoughts?

### wf...@chromium.org (2014-01-27)

[Empty comment from Monorail migration]

### cp...@chromium.org (2014-01-28)

Win7 only?


### ty...@gmail.com (2014-01-28)

I've done a basic test on Win8.1 x86, seems to work the same.

### rv...@chromium.org (2014-01-28)

Yeah, a default security descriptor is not applied for unnamed sections... in fact, unnamed sections seem to be non-securable from what I see :(

Looks like either we remove the option to share "read-only" sections, or move to only use named sections, at least in that case.

BTW, too bad the unit test that was supposed to verify this behavior is broken :(


### wf...@chromium.org (2014-01-28)

how about just adding a non-NULL token to the renderer duplicated object?  Sounds like this only affects NULL token.

### rv...@chromium.org (2014-01-28)

[Comment Deleted]

### rv...@chromium.org (2014-01-28)

as far as I can see, unnamed sections are just not securable objects (I don't know if there is a complete, official list of unnamed object types that can be secured). And by "see" I mean I already tried that.

### ty...@gmail.com (2014-01-28)

You can find object types which can set a security descriptor based on calling NtQueryObject with the ObjectTypeInformation class. It returns a boolean SecurityRequired. If that isn't set only named objects get a security descriptor. 

From what I can tell that pretty much amounts to: Thread, Process, File, Key, WindowStation, Desktop, Token. Anything else if unnamed will not assign an SD.

### cp...@chromium.org (2014-01-28)

Yeah, events are also broken this way. I wrote a test program (see attached).

This behavior was unknown to me, could it be that Windows is broken?
http://msdn.microsoft.com/en-us/library/windows/desktop/aa446598(v=vs.85).aspx


### ty...@gmail.com (2014-01-28)

I believe it's by "design" in the sense that an anonymous kernel object is not shareable except through the duplication of handles as you can't open it in the via the NT object manager. I'm surprised there is _no_ way to set an SD though, that seems to be against the design principles of NT and its barely documented if at all. Might go and dig out my copy of Windows Internals :)

### rv...@chromium.org (2014-01-28)

That not all unnamed objects are securable is documented:

http://msdn.microsoft.com/en-us/library/windows/desktop/aa379557(v=vs.85).aspx

### cl...@chromium.org (2014-01-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-01)

jln: Can you please take a look or find someone else to own it.

You are auto-assigned this issue since you are the top fixer for area label 'Cr-Internals-Sandbox'.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-03)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-05)

This is somewhat similar to Linux with https://crbug.com/chromium/302724. Also see the somewhat related https://crbug.com/chromium/321818 (i.e., what is vulnerable if RO shared memory can be turned to RW?).

Will, can you own this?

### cl...@chromium.org (2014-02-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-07)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-16)

wfh@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-02-16)

This really isn't medium. We need to fix it because in the future we will rely on enforcing things like read-only memory, but today we shouldn't be. So, bumping down to low-severity (just in case I missed something).

### cl...@chromium.org (2014-02-16)

jln: Can you please take a look or find someone else to own it.

You are auto-assigned this issue since you are the top fixer for area label 'Cr-Internals-Sandbox'.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-02-16)

Okay, time to remind Abhishek that the cf auto-assigning and nagging is still way too aggressive. It should not be doing that for low-severity bugs. I'll assign to myself just to shut it up for now, and keep it from making further erroneous assignments.

### js...@chromium.org (2014-02-16)

[Comment Deleted]

### wf...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### fo...@chromium.org (2014-07-23)

I've had the opportunity to look at this a little bit more, specifically around the handling of content/greasemonkey scripts. All renderers have a shared section passed in from the main process via UserScriptMaster. While this is marked as a read-only section as it's anonymous you can remap it to be writable inside a compromised renderer process. This section contains the pickled content scripts, if one is already registered you can modify it in the section and unless the list of scripts is changed by the master all new renderers will get the same copy. Depending on the content script modified it's possible to inject script into pages such as chrome://settings which in theory would allow a certain amount of privilege escalation. I don't know if this could be leveraged for a full sandbox escape but I guess it isn't impossible. 

For example on a fresh install of Canary on Windows (38.0.2102.0 64bit) the section contains a copy of saml_injected.js which is marked accessible for all urls. Changing this in memory to add 'alert(document.location);' and opening chrome://settings window demonstrates the injection was successful into chrome UI renderer content. 

I've not tested if this has an impact on other platforms. I believe Linux/OSX should correctly handle read-only permissions on sections. 

### js...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc84fcce71f37e6faeab9dce6ae2a65f1e12a5d2

commit dc84fcce71f37e6faeab9dce6ae2a65f1e12a5d2
Author: jschuh@chromium.org <jschuh@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Jul 24 11:42:59 2014

Add a random name to anonymous shared memory sections

This prevents Windows from ignoring the DACL on unnamed sections.

BUG=338538
R=cpu@chromium.org,brettw@chromium.org

Review URL: https://codereview.chromium.org/412043002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285195 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-24)

------------------------------------------------------------------
r285195 | jschuh@chromium.org | 2014-07-24T11:42:59.987687Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/memory/shared_memory_win.cc?r1=285195&r2=285194&pathrev=285195

Add a random name to anonymous shared memory sections

This prevents Windows from ignoring the DACL on unnamed sections.

BUG=338538
R=cpu@chromium.org,brettw@chromium.org

Review URL: https://codereview.chromium.org/412043002
-----------------------------------------------------------------

### js...@chromium.org (2014-07-24)

I'm going to assume the only shared unnamed objects we care about are sections, and count this one as fixed. The login renderer sideways escalation shouldn't be much additional risk, because a compromised renderer can already get at most of what's exposed. However, I'll bump it back up to medium and request a merge, since this should be a fairly risk-free merge.

### cl...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-02)

M-36 patch train, weird RM forgot to approve this :(:(, lets request merge for m37.

### rv...@chromium.org (2014-08-04)

Justin: I guess you missed the comment on the review. Do you mind fixing the unit test?

### am...@chromium.org (2014-08-06)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6d6797eb60a6626fd48bd9fe92a6598de3a0ea8b

commit 6d6797eb60a6626fd48bd9fe92a6598de3a0ea8b
Author: jschuh@chromium.org <jschuh@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Aug 07 22:07:43 2014

Add DACL and fix test for anonymous read-only memory

BUG=338538
R=rvargas@chromium.org,brettw@chromium.org
TBR=brettw@chromium.org

Review URL: https://codereview.chromium.org/444323005

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@288152 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-07)

------------------------------------------------------------------
r288152 | jschuh@chromium.org | 2014-08-07T22:07:43.192544Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/memory/shared_memory_win.cc?r1=288152&r2=288151&pathrev=288152
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/memory/shared_memory_unittest.cc?r1=288152&r2=288151&pathrev=288152

Add DACL and fix test for anonymous read-only memory

BUG=338538
R=rvargas@chromium.org,brettw@chromium.org
TBR=brettw@chromium.org

Review URL: https://codereview.chromium.org/444323005
-----------------------------------------------------------------

### ti...@chromium.org (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations tyranid - $3000 for this report.

### cl...@chromium.org (2014-10-30)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-09)

Contacted tyranid re: payment.

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### bo...@gmail.com (2015-07-29)

If I have not misunderstood, instead of using anonymous shared memory you use named shared memory where name is randomly generated.
Whether the name of shared memory is randomly generated or not, it is named shared memory and as such it is possible to open it, read/write to it, it is even possible to do some code injection.
To list all shared memory of a process (chrome.exe) I have used ProcessExplorer.exe.
https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx
In my test application, I've used GetNamedSecurityInfo and SetNamedSecurityInfo to create and set new security descriptor to an existing named shared memory. In this way it is possible to change the access rights to the shared memory. 
After that, I can use OpenFileMapping without any restrictions.

### js...@chromium.org (2015-07-29)

Re #47: Of course you can change the security descriptor or memory contents from outside the sandbox. The point of the sandbox is to protect the system from malicious code *inside* the sandbox. It's not possible to protect code inside the sandbox from malicious code running at privilege *outside* the sandbox, because by definition that code has full control over anything in the sandbox.

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

This issue was migrated from crbug.com/chromium/338538?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078787)*
