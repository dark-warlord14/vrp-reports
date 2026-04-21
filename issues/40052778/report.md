# Security: Keystone for macOS should use auditToken to validate incoming XPC message

| Field | Value |
|-------|-------|
| **Issue ID** | [40052778](https://issues.chromium.org/issues/40052778) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Updater |
| **Platforms** | Mac |
| **Reporter** | co...@gmail.com |
| **Assignee** | no...@google.com |
| **Created** | 2020-07-05 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

The update system of Google Chrome on macOS is based on KeyStone:

/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle

There is a root daemon:

/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle/Contents/MacOS/GoogleSoftwareUpdateDaemon

It provides two XPC endpoints as follow:

\* com.google.Keystone.Daemon.AdministrationXPC  

\* com.google.Keystone.Daemon.UpdateEngineXPC

In their corresponding authentication callbacks, they both rely on `+[KSSecurityValidation isTrustworthyProcess:]` to validate the code signature of the incoming XPC connections

\* -[KSDaemonAdministrationXPCAdapter listener:shouldAcceptNewConnection:]  

\* -[KSUpdateEngineXPCListener listener:shouldAcceptNewConnection:]

The problem is that it's based on processIdentifier which has known race condition issue that leads to authentication bypass, then the privileged interfaces provided by the root daemon will be reachable to untrusted local programs.

[https://crbug.com/chromium/1223: MacOS/iOS userspace entitlement checking is racy](https://bugs.chromium.org/p/project-zero/issues/detail?id=1223)

For example, a local program without valid code signature (i.e. same TeamId as Google Chrome) that try to communicate with the privileged daemon:

```
  NSXPCConnection \*connection = [[NSXPCConnection alloc] initWithMachServiceName:@"com.google.Keystone.Daemon.AdministrationXPC"  
                                                                         options:NSXPCConnectionPrivileged];  
  connection.remoteObjectInterface = [NSXPCInterface interfaceWithProtocol:@protocol(KSDaemonAdministrationXPCProtocol)];  
  [connection resume];  
  id remote = connection.remoteObjectProxy;    
  [remote uninstallSystemKeystoneWithReply:^(BOOL arg1, KSError \*arg2) {}];  

```

It will not pass the signature check, leaving this in the syslog of GoogleSoftwareUpdateDaemon process.

> 2020-07-06 00:47:54.289 GoogleSoftwareUpdateDaemon[19854/0x70000e6ef000] [lvl=3] +[KSSecurityValidation isTrustworthyProcess:] Cannot fetch security information for connecting process 19865. Code: 100003

To trigger the race condition and bypass the check:

1. Create many child processes simultaneously to fill the message queue.
2. In each child process, use the same NSXPC invocation code as normal. Then use `POSIX_SPAWN_SETEXEC | POSIX_SPAWN_START_SUSPENDED` flag in `posix_spawn` to replace itself to a trusted binary, while keeping the same pid untouched.
3. Some of the XPC request will bypass codesign check and trigger the desired NSXPC methods.

**VERSION**

Chrome Version: 83.0.4103.116 (Official Build) (64-bit) Stable  

Operating System: macOS Big Sur 11.0 Beta (build 20A4299v) (it doesn't matter)

**REPRODUCTION CASE**

Compile the provided poc: `cc poc.m -fmodules -o poc`

This won't pass the check and you can see the error message in syslog:

`./poc normal`

Now start the service and quickly set a breakpoint as follow. Note that GoogleSoftwareUpdateDaemon will quit after being idle for few seconds.

```
➜  /tmp sudo launchctl kickstart -k -p system/com.google.keystone.daemon ; sudo lldb -n GoogleSoftwareUpdateDaemon  
service spawned with pid: 21148  
(lldb) process attach --name "GoogleSoftwareUpdateDaemon"  
Process 21148 stopped  
\* thread #3, stop reason = signal SIGSTOP  
    frame #0: 0x00007fff710a3a02 libsystem_kernel.dylib` __sigsuspend_nocancel  + 10  
libsystem_kernel.dylib`__sigsuspend_nocancel:  
->  0x7fff710a3a02 <+10>: jae    0x7fff710a3a0c            ; <+20>  
    0x7fff710a3a04 <+12>: mov    rdi, rax  
    0x7fff710a3a07 <+15>: jmp    0x7fff7109ea81            ; cerror_nocancel  
    0x7fff710a3a0c <+20>: ret  
    0x7fff710a3a0d <+21>: nop  
    0x7fff710a3a0e <+22>: nop  
    0x7fff710a3a0f <+23>: nop  
libsystem_kernel.dylib'__exit:    0x7fff710a3a10 <+0>: mov    eax, 0x2000001  
Target 0: (GoogleSoftwareUpdateDaemon) stopped.  
  
Executable module set to "/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle/Contents/MacOS/GoogleSoftwareUpdateDaemon".  
Architecture set to: x86_64h-apple-macosx-.  
(lldb) po @import Foundation  
(lldb) print (void\*)class_getMethodImplementation((id)NSClassFromString(@"KSDaemonAdministrationXPCAdapter"), NSSelectorFromString(@"uninstallSystemKeystoneWithReply:"))  
(void \*) $0 = 0x0000000105798e91  
(lldb) b 0x0000000105798e91  
Breakpoint 1: where = GoogleSoftwareUpdateDaemon`___lldb_unnamed_symbol43$$GoogleSoftwareUpdateDaemon, address = 0x0000000105798e91  
(lldb) c  
Process 21148 resuming  

```

Now run `./poc` without parameter. You'll see the breakpoint `- [KSDaemonAdministrationXPCAdapter uninstallSystemKeystoneWithReply:]` is hit, which means the security check is bypassed.

```
Process 21148 stopped  
\* thread #7, queue = 'com.apple.NSXPCConnection.user.com.google.Keystone.Daemon.AdministrationXPC.21176', stop reason = breakpoint 1.1  
    frame #0: 0x0000000105798e91 GoogleSoftwareUpdateDaemon` ___lldb_unnamed_symbol43$$GoogleSoftwareUpdateDaemon  
GoogleSoftwareUpdateDaemon`___lldb_unnamed_symbol43$$GoogleSoftwareUpdateDaemon:  
->  0x105798e91 <+0>:  push   rbp  
    0x105798e92 <+1>:  mov    rbp, rsp  
    0x105798e95 <+4>:  push   r15  
    0x105798e97 <+6>:  push   r14  
    0x105798e99 <+8>:  push   r12  
    0x105798e9b <+10>: push   rbx  
    0x105798e9c <+11>: sub    rsp, 0x90  
    0x105798ea3 <+18>: mov    r14, rdx  
Target 0: (GoogleSoftwareUpdateDaemon) stopped.  
(lldb) bt  
\* thread #7, queue = 'com.apple.NSXPCConnection.user.com.google.Keystone.Daemon.AdministrationXPC.21176', stop reason = breakpoint 1.1  
  \* frame #0: 0x0000000105798e91 GoogleSoftwareUpdateDaemon` ___lldb_unnamed_symbol43$$GoogleSoftwareUpdateDaemon  
    frame #1: 0x00007fff33c75632 Foundation` __NSXPCCONNECTION_IS_CALLING_OUT_TO_EXPORTED_OBJECT_S1__  + 10  
    frame #2: 0x00007fff33c20a18 Foundation` -[NSXPCConnection _decodeAndInvokeMessageWithEvent:flags:]  + 2271  
    frame #3: 0x00007fff33bd8a61 Foundation` message_handler  + 206  
    frame #4: 0x00007fff711b28c4 libxpc.dylib` _xpc_connection_call_event_handler  + 56  

```

To patch this bug, use `auditToken` instead of `processIdentifier`.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: CodeColorist of Ant-Financial LightYear Labs

## Attachments

- [poc.m](attachments/poc.m) (text/plain, 3.2 KB)

## Timeline

### ca...@chromium.org (2020-07-06)

Thanks for the report, I'm triaging this as low severity since it doesn't quite fit in with Chrome's threat model, but it's similar to crbug.com/1100280, which was treated as a security bug. 

avi: Do you know who would be a good owner for this (or, alternatively, are you a good owner for this?), can you reassign as appropriate? Thanks. 

[Monorail components: Internals>Updater]

### av...@chromium.org (2020-07-07)

Assigning to one Adam email and ccing another; I’m not sure which is preferred. +cc rsesek who also knows a lot in this area.

### av...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-07-07)

Thanks for the report. I agree with the conclusion that we should use the audit token to evaluate the peer, even if it relies on the undocumented API to obtain the audit token from the XPC connection.

### [Deleted User] (2020-07-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2020-07-07)

Marking as Sev-High after discussion within the security team. Our current severity guidelines for Chrome don't quite fit for the updater component, so we'll be working on some adjustments to better cover this kind of LPE.

### co...@gmail.com (2020-07-08)

[Comment Deleted]

### co...@gmail.com (2020-07-08)

`+[KSSecurityValidation isTrustworthyProcess:]` only checks for the same Team ID, which is too loose. 

There are two possible ways to inject malicious code to trusted binaries and perform LPE attack:

1. Use an outdated Chrome that has public n-day exploit. Gain code execution and abuse its code signature;
2. Find an macOS executable signed by Google, but no Library Validation or Hardende Runtime flag. (https://github.com/chromium/chromium/commit/1390f8a0dd43f192a3b322e7230ae5ff4de96491) Use `DYLD_INSERT_LIBRARIES` or [Pepper Plugin](https://www.chromium.org/developers/design-documents/pepper-plugin-implementation) to inject malicious code

If this XPC service is for GoogleSoftwareUpdateAgent.app only, consider adding a custom flag in GoogleSoftwareUpdateAgent.app's Info.plist and check both team id and this flag. For example:

Info.plist:

```
{
   ...
    com.google.keystone.updater = true
}
```

Then add this to [Code Requirement](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/RequirementLang/RequirementLang.html) string:

```
... and info [com.google.keystone.updater]
```

### [Deleted User] (2020-07-08)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2020-07-08)

Looking at the code, I don't think +[KSSecurityValidation isTrustworthyProcess:] is validating by team ID; it's comparing the hash of its own (Keystone's) code signature to the hash of the peer's certificate.

The PID race is definitely an issue though.

### no...@google.com (2020-07-09)

Investigating. We are indeed validating by cert hash, but using an old Chrome with some kind of code execution vulnerability, signed with the same certificate, could indeed be an escalation path. Thank you for the suggestion on adding a custom field to info.plist, I think I can generalize that to protect against possible unknown flaws existing in various versions of Keystone Agent, too.

Thank you for the report!

### no...@google.com (2020-07-10)

Current plan:

On macOS 10.12+: use .auditToken to identify remote process, as suggested, closing the PID race hole.

On macOS 10.11-: no change. I have not found any way to go from an audit_token_t to a SecCodeRef on these platforms. I spent most of yesterday looking for anything. Everywhere I got close, I found that Apple's implementation was to use only the PID, reinstating the same security defect in the same way. I don't think there's any sense in complicating the code only to retain the flaw. I believe the issue is fundamentally unpatchable on these very old versions of macOS, which Apple no longer supports with security patches. Since the issue exists in OS components on these platforms, Keystone isn't realistically extending the attack surface - the OS itself is just as vulnerable, and far more users of the OS are using the OS than are using Keystone, for tautological reasons.

On all platforms: Tighten up the check to also verify bundle ID and version info of the remote process, using existing info.plist information. and a to-be-determined allow-list of clients. I expect us to need to version this "access to the Keystone Daemon" flag if new vulnerabilities are discovered and we wish to block off access from previously-permitted clients to avoid the attack described where an old, unpatched version is exploited to communicate with the Daemon; if we're going to have to use a versioning scheme anyway, we might as well use the version information we already have.

I plan to start implementation early next week.

### rs...@chromium.org (2020-07-14)

Plan in c#12 SGTM. I agree this is not fixable on OSes prior to macOS 10.12 because the underlying OS is broken. I’m not too concerned about that though because there are several other un-patched vulnerabilities on those older systems.

I do not think the Info.plist key adds much value if it is not versioned, because the hash of the certificate is currently checked. But the suggestion in c#12 to have it be a versioned value could be useful for preventing downgrade attacks.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### no...@google.com (2020-07-23)

Status update: I have written a candidate fix and it passes unit tests, but it's going to be more work to get the proof of concept running against it (mostly because I have to get my dev build adequately signed). I'm working on that now.

### no...@google.com (2020-07-23)

Additionally, https://bugs.chromium.org/p/project-zero/issues/detail?id=1757 describes a different exploit that defeats audit_token_t's improvements over raw PID on all versions of macOS before 10.14.4. On the flip side, that exploit requires thousands and thousands of fork/exec operations, making it less feasible than the attack against only the PID, which can realistically hit the timing window in just a few tries, and in any case at least the issue is closed on 10.14.4+ with this patch.

It would be nice if Apple would backport their security fixes further, but they don't. Oh well.

### no...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### no...@google.com (2020-07-24)

So, after self-signing my dev build, the proof-of-concept code no longer successfully sends any messages to Keystone Daemon. Keystone Daemon decides to segfault instead, which is arguably an improvement but not the behavior I expected or desired. Investigating.

### no...@google.com (2020-07-27)

Fixed, simple bug in my implementation of the patch led to a double free. Fix verified against proof-of-concept code in my dev build; we'll start another Keystone release so we can package it with Chrome, deploy the fix, and let the original reporter take another swing at it.

### [Deleted User] (2020-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-27)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M84. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M85. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-27)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### no...@google.com (2020-07-27)

Brief reply to sheriffbot's https://crbug.com/chromium/1102196#c22 - this isn't in Chrome yet, it's in closed-source Keystone code that has not yet been packaged. We're working on it.

### sr...@google.com (2020-07-28)

Merge approved for M85 branch:4183 please merge your changes once this is verified as working .

### [Deleted User] (2020-08-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### sr...@google.com (2020-08-03)

Please complete your merges to M85 branch before 2pm PST tuesday Aug 4th 2020, so they can be included in this week's beta release.

### ad...@google.com (2020-08-03)

Per https://crbug.com/chromium/1102196#c23 this is not in code which we can merge.

There was an e-mail discussion about this and we plan to let this release organically in M85 or M85 depending on when it's ready.

norberg@, even if this doesn't land in Chrome code it's still important that we know which release it's fixed in, so we can credit the reporter appropriately. Please could you ensure you comment here? (Adding a label for the first release of 86 so that, worst case, I credit it there.)

### no...@google.com (2020-08-04)

Update: My patch was not correct for older versions of macOS and we caught it in our automated tests. I fixed it, but got slowed down by an unrelated issue. My fixed fix is in, and assuming I don't need to fix my fixed fix, we'll start the Keystone release process and will release it to Chrome once it's passed tests and passed canarying.

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel has decided to award you $10,000 for this report. Someone from our finance team will be in touch to arrange payment.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### no...@google.com (2020-08-21)

The fixed version of Keystone is currently being distributed to 5% of Keystone self-updates, and we'll roll it out fully and inside Chrome soon if stats continue to look good. (We didn't start at 5%, we've been ramping this up for a few days.) CodeColorist, if you'd like to check out the new version of Keystone, you can pick it up at https://dl.google.com/release2/mac/eQ6vm-JZJeybZv0u4tptUA_1.3.14.145/GoogleSoftwareUpdate-1.3.14.145.dmg .

Thanks again for spotting this issue!

### no...@google.com (2020-08-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-26)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/deps/googlemac/+/5bfa1f14bda304dd9342af774c58a2b71402455d

commit 5bfa1f14bda304dd9342af774c58a2b71402455d
Author: Joshua Pawlicki <waffles@google.com>
Date: Wed Aug 26 19:23:12 2020


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-26)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/src-internal.git/+/1384526b46d078a0a7002439fcbad9f307a3a054

commit 1384526b46d078a0a7002439fcbad9f307a3a054
Author: Joshua Pawlicki <waffles@google.com>
Date: Wed Aug 26 19:37:56 2020


### wa...@chromium.org (2020-08-26)

I apologize for any confusion here, in fact we do need to merge the CL in https://crbug.com/chromium/1102196#c36 to stable and beta. Adding the request labels.

If I understand correctly, this should also address the question in https://crbug.com/chromium/1102196#c28 about where to credit the reporter.

### [Deleted User] (2020-08-26)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2020-08-26)

1 - Yes, as a Security_Severity-High, this qualifies by the guidelines.
2 - https://crbug.com/chromium/1102196#c36
3 - landed yes, verification will be in tonight's canary (sorry, jumped the gun a bit there)
4 - open vulnerability
5 - no
6 - n/a

IIUC from chatting with Srinivas, we'll take this CL for the first M85 stable respin.

Prudhvi, any concerns about merging to M86 prior to the next beta roll?

### ad...@google.com (2020-08-26)

pbommana@ will approve this for merge to M85 after some canary coverage.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ddc995cc88327ec2d078c59bfa2251bd231dc53

commit 2ddc995cc88327ec2d078c59bfa2251bd231dc53
Author: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Date: Wed Aug 26 22:45:49 2020

Roll src-internal from ee3d26b3cdc2 to 53daab94768a (7 revisions)

https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/ee3d26b3cdc2..53daab94768a

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://skia-autoroll.corp.goog/r/src-internal-chromium-autoroll
Please CC estade@google.com,sahel@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chrome.try:linux-chromeos-chrome
Bug: chromium:1004848,chromium:1102196,chromium:1121776,chromium:912681
Tbr: estade@google.com,sahel@google.com
Change-Id: Ia8114a5c2e268314aa55afe961a2325d5a8cc687
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2377622
Reviewed-by: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#801995}

[modify] https://crrev.com/2ddc995cc88327ec2d078c59bfa2251bd231dc53/DEPS


### [Deleted User] (2020-08-27)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2020-08-28)

Thanks all, we've completed qualification of the change in https://crbug.com/chromium/1102196#c36 on canary, and will proceed with merging as soon as approvals are granted.

### pb...@google.com (2020-08-28)

Thank you Joshua, Approving the Cl for M86 Branch : 4240 pleae goahead and get the Cl merged asap.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/src-internal.git/+/cce6827ff835455501a3f4c858c50335910222fa

commit cce6827ff835455501a3f4c858c50335910222fa
Author: Joshua Pawlicki <waffles@google.com>
Date: Fri Aug 28 18:01:59 2020


### pb...@google.com (2020-08-31)

Approving the Cl for M85 branch : 4183, Please goahead and get the Cl merged asap.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-01)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/src-internal.git/+/d44753e0e39eea475629a39bd99b873ebd658a8f

commit d44753e0e39eea475629a39bd99b873ebd658a8f
Author: Joshua Pawlicki <waffles@google.com>
Date: Tue Sep 01 16:25:28 2020


### wa...@chromium.org (2020-09-01)

This is now merged to stable and my understanding is that the work here is complete.

We are updating existing installations of the affected versions of Keystone and new installations of Chrome will have the updated version of Keystone starting with the next stable respin.

If you would like to verify the fix, please see the instructions in https://crbug.com/chromium/1102196#c33.

Thanks again, everyone.

Thanks all.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa5392f02d628f3144acb24ab75a7e94cf310cf4

commit fa5392f02d628f3144acb24ab75a7e94cf310cf4
Author: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Date: Tue Sep 01 17:53:06 2020

Roll src-internal from b497ca9c0cae to d44753e0e39e (1 revision)

https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/b497ca9c0cae..d44753e0e39e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://skia-autoroll.corp.goog/r/src-internal-chromium-stable-autoroll
Please CC nsatragno@google.com,tguilbert@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1102196
Tbr: nsatragno@google.com,tguilbert@google.com
Change-Id: I20bc26212634038b7ff59a0e331ec6e00fe974dc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2387959
Reviewed-by: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4183@{#1728}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/fa5392f02d628f3144acb24ab75a7e94cf310cf4/DEPS


### ad...@google.com (2020-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1102196?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052778)*
