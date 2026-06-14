# Security: Windows Sandbox Named Pipe Policy Doesn't Block Relative Paths

| Field | Value |
|-------|-------|
| **Issue ID** | [40078693](https://issues.chromium.org/issues/40078693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox |
| **Platforms** | Windows |
| **Reporter** | ty...@gmail.com |
| **Assignee** | wf...@chromium.org |
| **Created** | 2014-01-16 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Every sandboxed process on Windows has a default policy to create named pipes with a chrome.nacl or chrome.sync prefixes. This is done through the broker. For example the code in AddGenericPolicy is:

result = policy->AddRule(sandbox::TargetPolicy::SUBSYS\_NAMED\_PIPES,  

sandbox::TargetPolicy::NAMEDPIPES\_ALLOW\_ANY,  

L"\\.\pipe\chrome.nacl.\*");  

if (result != sandbox::SBOX\_ALL\_OK)  

return false;

This should only allow named pipes with a chrome.nacl prefix, however it doesn't as CreateNamedPipe will canonicalize the pipe path (it seems counter intuitive) if it starts with the \.\ prefix.  

So for example call the broker passing it "\.\pipe\chrome.nacl...\abc" and you will create a named pipe called "abc" outside of the chrome namespace.

This could be fixed in a number of ways, the least impact would be to pre-canonicalize the path before evaluating the policy in NamedPipeDispatcher::CreateNamedPipe. Alternatively you could require the path be the form: \?\pipe... which will not get canonicalized. The "correct" way is probably to hook NtCreateNamedPipeFile instead.

This is an exploitable condition for various different reasons. While this only opens the server side of a pipe you should be able to impersonate chrome named pipes (although wouldn't be trivial to guess the random values). You could also create a server instance of any multi-use pipe in the user's session and use that reference to change the DACL of the pipe by requesting WRITE\_DAC permissions. Once the DACL has been modified you should be able to open it directly from the sandboxed process and potentially escape the sandbox.

**VERSION**  

Chromium Version: 34.0.1784.0 - dev from SVN/GIT  

Operating System: Windows 7 SP1 x64

**REPRODUCTION CASE**

Apply the following patch:

--- src/content/renderer/renderer\_main.cc.orig 2014-01-16 00:50:07.609924900 +0000  

+++ src/content/renderer/renderer\_main.cc 2014-01-16 00:49:35.423083900 +0000  

@@ -233,6 +233,26 @@  

new RenderThreadImpl();  

#endif

- {
- ```
    HANDLE hPipe = CreateNamedPipeW(  
  
  ```
- ```
       L"\\\\.\\pipe\\chrome.nacl.a\\..\\this_shouldn't_work",  
  
  ```
- ```
       PIPE_ACCESS_DUPLEX | WRITE_DAC,       // read/write access  
  
  ```
- ```
       PIPE_TYPE_MESSAGE |       // message type pipe  
  
  ```
- ```
       PIPE_READMODE_MESSAGE |   // message-read mode  
  
  ```
- ```
       PIPE_WAIT,                // blocking mode  
  
  ```
- ```
       PIPE_UNLIMITED_INSTANCES, // max. instances  
  
  ```
- ```
       512,                  // output buffer size  
  
  ```
- ```
       512,                  // input buffer size  
  
  ```
- ```
       0,                        // client time-out  
  
  ```
- ```
       NULL);                    // default security attribute  
  
  ```
- if(hPipe != INVALID\_HANDLE\_VALUE) {
- ```
  LOG(ERROR) << "Created Pipe (BAD)";  
  
  ```
- } else {
- ```
  LOG(ERROR) << L"Failed to create pipe (GOOD)";  
  
  ```
- }
- }
- base::HighResolutionTimerManager hi\_res\_timer\_manager;
  
  platform.RunSandboxTests(no\_sandbox);

This will try and create a named pipe called 'this\_shouldn't\_work' for every new renderer. If it was successful in creating the pipe you should get an appropriate log message. You can also see the new pipe by looking at handle view in process explorer or process hacker.

## Timeline

### wf...@chromium.org (2014-01-16)

Interesting bug, I was not aware that object namespaces would be vulnerable to this type of path traversal bug.  I agree probably the best option here is to canonicalize before we run the policy validation engine.

### sc...@gmail.com (2014-01-16)

@wfh or @jschuh: you are our Windows experts. What's the severity here? Is it as readily exploitable as @tyranid documents?

### js...@chromium.org (2014-01-16)

Well, that's an obnoxious Windows quirk that I'd never even considered. Nice find.

I'm not sure about the exploitability. The Chrome IPC pipes shouldn't be vulnerable to squatting or hijacking. The pipe server includes a strong random value in the name and the client must validate itself with with a strong random nonce.

Odds should be better going after something Windows exposes. However, that's going to be very hard from a renderer or pepper process where you shouldn't be able to enumerate much of anything or trigger external activity. The GPU process may be a different story, since it can enumerate resources and trigger some activity directly.

I'll flag it high-severity out of an abundance of caution, but I'd be very curious to see a more concrete target for the bug.


### cl...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-01-20)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-01-20)

[Empty comment from Monorail migration]

### dh...@chromium.org (2014-01-28)

CL is under review - https://codereview.chromium.org/145553007/

### bu...@chromium.org (2014-01-28)

------------------------------------------------------------------------
r247511 | wfh@chromium.org | 2014-01-28T21:26:58.610728Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/win/src/named_pipe_policy_test.cc?r1=247511&r2=247510&pathrev=247511
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/win/src/named_pipe_dispatcher.cc?r1=247511&r2=247510&pathrev=247511

Correctly test for canonicalized path in the CreateNamedPipe policy engine.

BUG=334897
TEST=sbox_integration_tests.exe

Review URL: https://codereview.chromium.org/145553007
------------------------------------------------------------------------

### cl...@chromium.org (2014-01-29)

wfh@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### wf...@chromium.org (2014-01-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-29)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-01-29)

------------------------------------------------------------------------
r247725 | wfh@chromium.org | 2014-01-29T18:24:37.672236Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/win/src/named_pipe_dispatcher.cc?r1=247725&r2=247724&pathrev=247725

Fix nit introduced in r247511

BUG=334897
TBR=rvargas@chromium.org

Review URL: https://codereview.chromium.org/149513004
------------------------------------------------------------------------

### dh...@chromium.org (2014-02-03)

Merge requested for both M32 and M33.

### la...@google.com (2014-02-04)

Approved for M33 (1750 branch) only.

### bu...@chromium.org (2014-02-04)

------------------------------------------------------------------------
r248761 | wfh@chromium.org | 2014-02-04T18:57:35.579542Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/sandbox/win/src/named_pipe_dispatcher.cc?r1=248761&r2=248760&pathrev=248761
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/sandbox/win/src/named_pipe_policy_test.cc?r1=248761&r2=248760&pathrev=248761

Merge 247511 "Correctly test for canonicalized path in the Creat..."

> Correctly test for canonicalized path in the CreateNamedPipe policy engine.
> 
> BUG=334897
> TEST=sbox_integration_tests.exe
> 
> Review URL: https://codereview.chromium.org/145553007

TBR=wfh@chromium.org

Review URL: https://codereview.chromium.org/143683006
------------------------------------------------------------------------

### wf...@chromium.org (2014-02-04)

Merge requested for M32

### ka...@google.com (2014-02-05)

there will be no more 32s, please make sure to request merge to M33 instead

### wf...@chromium.org (2014-02-05)

Already merged to 33, so all done. Thanks!

### in...@chromium.org (2014-02-05)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $2000 reward. This was an interesting bug and the patch you provided was very helpful for reproducing the issue. 

### ti...@chromium.org (2014-04-14)

Hey - my apologies for the delay here. I'll start the process for this payment today. Feel free to reach out to me directly with any payment or reward questions.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-13)

Processing via our e-payment system can take up to a month, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-05-13)

Bulk update: removing view restriction from closed bugs.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/334897?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078693)*
