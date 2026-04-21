# UAF in mojo::WaitSet::State::Context::OnNotification

| Field | Value |
|-------|-------|
| **Issue ID** | [41481374](https://issues.chromium.org/issues/41481374) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage, Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2023-12-06 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os: Ubuntu 22.04  

tested chromium version:  

Chromium 121.0.6129.0  

Chromium 121.0.6163.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1232441.zip)

Repro Steps:  

Due to the instability of the reproduction, I used a Puppeteer script to simultaneously open multiple browsers. The script requires modifications based on the actual environment, such as changing the Chrome path and the URL of the PoC (Proof of Concept).

- Install Node.js and Puppeteer.
- Execute the script with: node ./test.js 2>&1 | grep -E 'AddressSanitizer'  
  
  On my local machine, the issue can be reproduced in over 10 minutes. If you're unable to reproduce it after several attempts, consider adjusting the number of browsers the script opens, as well as the number of iframes in the main.html file, to suit your specific environment.

**Problem Description:**  

Normally, when mojo::Remote[mojom::blink::Blob](javascript:void(0);)[0] is created, it also creates a mojo::WaitSet::State::Context[2]. When blob.Unbind()[1] is called, it is supposed to release the corresponding Context. However,in the ASAN log, you can see the call to blob Unbind() actually released the Context created by mojo::Remote[blink::mojom::blink::StorageArea](javascript:void(0);)::Bind()[c], ultimately resulting in UAF. I haven't identified the root cause yet. If there is any progress, I will update again.

```
void BlobDataHandle::CloneBlobRemote(  
    mojo::PendingReceiver<mojom::blink::Blob> receiver) {  
  base::AutoLock locker(blob_remote_lock_);  
  if (!blob_remote_.is_valid())  
    return;  
  mojo::Remote<mojom::blink::Blob> blob(std::move(blob_remote_));  --->[0]  
  blob->Clone(std::move(receiver));  
  blob_remote_ = blob.Unbind();                                    --->[1]  
}  

```

[a]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/blob/blob_data.cc;l=390?q=third_party%2Fblink%2Frenderer%2Fplatform%2Fblob%2Fblob_data.cc:390:23>

```
MojoResult AddHandle(Handle handle, MojoHandleSignals signals) {  
    DCHECK(trap_handle_.is_valid());  
    ```  
    scoped_refptr<Context> context = new Context(this, handle);      --->[2]  
  
    {  
      base::AutoLock lock(lock_);  
  
      if (handle_to_context_.count(handle))  
        return MOJO_RESULT_ALREADY_EXISTS;  
      DCHECK(!contexts_.count(context->context_value()));  
  
      handle_to_context_[handle] = context;  
      contexts_[context->context_value()] = context;  
    }  
    ```  
    return rv;  
  }  

```

[b]<https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/system/wait_set.cc;l=60?q=mojo%2Fpublic%2Fcpp%2Fsystem%2Fwait_set.cc:60:38>  

[c]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/storage/cached_storage_area.cc;l=244?q=third_party%2Fblink%2Frenderer%2Fmodules%2Fstorage%2Fcached_storage_area.cc:244:18>

**Additional Comments:**

\*\*Chrome version: \*\* 121.0.6129.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [test.js](attachments/test.js) (text/plain, 1.3 KB)
- [main.html](attachments/main.html) (text/plain, 6.0 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 40.8 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 39.0 KB)
- [crash.html](attachments/crash.html) (text/plain, 429 B)

## Timeline

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-12-06)

I just tested it in version Chromium 119.0.6041.0 and it can be reproduced. It should affect the stable version.

### bo...@chromium.org (2023-12-08)

Thanks for the report! 

I'm running the test harness now and will provide an update here after letting it run for a while. At the time of posting the harness has been running for about 15 minutes with no ASan reports. 

However, I'm setting triage flags based on an assumption that the report is valid, but holding off routing to an owner until the test has time to run longer.

The UAF looks to be occurring in a renderer process and triggerable from web content, making this High severity. I don't see anything that looks platform-specific, so I'm setting platform flags on the assumption that this is not platform specific. I'm testing on an ASan release close to tip-of-tree. Per https://crbug.com/chromium/1508753#c3 the bug goes back to at least M119. Since M120 just shipped that means both Stable and Extended are presumably impacted.

[Monorail components: Internals>Mojo]

### [Deleted User] (2023-12-08)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-12-08)

The PoC can be further simplified, and I have re-uploaded it. I noticed that the alloc part of the ASAN log is slightly different than before. In the previous asan.log, the mojo::WaitSet::State::Context was created when binding the blink.mojom.Storage interface, but in asan2.log, the mojo::WaitSet::State::Context was created when binding the blink.mojom.RestrictedCookieManager.

This description[0] and the UAF stack I reported are almost identical. I think it is possible that this method can still be bypassed under edge conditions, which may cause UAF.
```
   // NOTE: We retain a context ref in |cancelled_contexts_| to ensure that
      // this Context's heap address is not reused too soon. For example, it
      // would otherwise be possible for the user to call AddHandle() from the
      // WaitSet's sequence immediately after this notification has fired on
      // another sequence, potentially reusing the same heap address for the
      // newly added Context; and then they may call RemoveHandle() for this
      // handle (not knowing its context has just been implicitly cancelled) and
      // cause the new Context to be incorrectly removed from |contexts_|.
      //
      // This vector is cleared on the WaitSet's own sequence every time
      // RemoveHandle is called.
      cancelled_contexts_.emplace_back(base::WrapRefCounted(context));
[0]https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/system/wait_set.cc;l=287-298
```


### em...@gmail.com (2023-12-08)

Due to the issues caused by a race condition, it might be difficult to reproduce the issue on different machine environments.
If you're unable to reproduce the issue, you might try increasing the number of iframes in main.html. I just realized that the '--disable-popup-blocking' flag is not needed, and I have re-uploaded the new PoC.

### bo...@chromium.org (2023-12-08)

@emilykim8708, I'm not seeing a successful repro after more than 3 hours. The default text.js script parameters (20 instances with ~150 iframes each) might've been too much for my workstation, so I'm dropping it down to 10 instances and that seems to be comfortably within capacity. 

### bo...@chromium.org (2023-12-09)

Confirming the POC as described in https://crbug.com/chromium/1508753#c0 does reproduce. I haven't tried the updated POC in #6. My workstation ran overnight and in that time ASan got 2 UAFs. 

@emilykim8708, as you know the --no-sandbox flag is unsupported. If the flag is required then this report would be labeled ImpactNone. Do you have reason to suspect the POC should work without that flag? I updated test.js to remove both --no-sandbox and --disable-popup-blocking, and started another run to see if it gets lucky. I'm routing to the Mojo team on the assumption that the --no-sandbox flag is not required.

This looks interesting. I would route this one to @rockot, but I believe he's OOO through next week. @oksamyt (and anyone on the CC line), would you take a look at the observation in https://crbug.com/chromium/1508753#c5 please? 

### em...@gmail.com (2023-12-09)

Actually, no extra flags are required; I just habitually use --no-sandbox in the script (not using --no-sandbox might make it easier to lose crash information).

### [Deleted User] (2023-12-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2023-12-11)

@emilykim8708, sorry for the confusion re. the --no-sandbox flag. That's fine here, no worries about ImpactNone in this case.

### ok...@chromium.org (2023-12-11)

From looking at the code/logs, it looks like a MOJO_RESULT_CANCELLED notification is received before blob.Unbind() is called, and a context is added to cancelled_contexts_ (and then removed by RemoveHandle()):

https://crsrc.org/c/mojo/public/cpp/system/wait_set.cc;drc=8e78783dc1f7007bad46d657c9f332614e240fd8;l=283

It's not clear why exactly the cancelled notification is received, but I found this CL that added unconditional clearing of all cancelled contexts in RemoveHandle() to fix a memory leak a while ago:

https://codereview.chromium.org/2907823002

### em...@gmail.com (2023-12-12)

You are correct. After receiving a cancelled notification, all cancelled contexts are deleted. However, after adding debugging code, I found that OnNotification is called twice. The first call has event->result as 1 (MOJO_RESULT_CANCELLED) [0], at which point all cancelled contexts are deleted（in RemoveHandle() ）. Then, OnNotification is called a second time, this time with event->result being 9 (MOJO_RESULT_FAILED_PRECONDITION) [1].
The debug log format is roughly as follows:
LOG(ERROR) << "[USE]["<<getpid()<<"][" << std::this_thread::get_id() << "]"
                  <<"OnNotification()"
                  <<"context=" << context
                  <<",event->result=" << event->result;
                  
``` 
[1212/142035.612998:ERROR:wait_set.cc(66)] [ALLOC][1327140][140594804921472]AddHandle(),State(this)=0x511000005b80,context=0x503000061900,handle=89129161723136
```
[1212/142246.323801:ERROR:wait_set.cc(295)] [USE][1327140][140594804921472]OnNotification()context=0x503000061900,event->result=1      --->[0]
```
[1212/142246.323906:ERROR:wait_set.cc(319)] [UAF][1327140][140594804921472][before]Notify(),Context(this): 0x503000061900,result=1
```
[1212/142246.324024:ERROR:wait_set.cc(323)] [UAF][1327140][140594804921472][after]Notify(),Context(this): 0x503000061900,state_=0x511000005b80,handle=89129161723136,result=1
```
[1212/142246.324703:ERROR:wait_set.cc(309)] [FREE][1327140][140594804921472]~Context: 0x503000061900
```
[1212/142246.324279:ERROR:wait_set.cc(295)] [USE][1327140][140594665928256]OnNotification()context=0x503000061900,event->result=9  --->[1]
```
[1212/142246.327791:ERROR:wait_set.cc(319)] [UAF][1327140][140594665928256][before]Notify(),Context(this): 0x503000061900,result=9
=================================================================
==1327140==ERROR: AddressSanitizer: heap-use-after-free on address 0x503000061908 at pc 0x55f61461d4ec bp 0x7fdebf1e8f30 sp 0x7fdebf1e8f28
READ of size 8 at 0x503000061908 thread T3 (Chrome_ChildIOT)
0x503000061908 is located 8 bytes inside of 24-byte region [0x503000061900,0x503000061918)
ntext(this): 0x5030006294d0,state_=0x51100008aec0,handle=89129179473216,result=1
Shadow bytes around the buggy address:
  0x503000061680: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd
  0x503000061700: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x503000061780: fd fd fd fa fa fa fd fd fd fd fa fa fd fd fd fd
  0x503000061800: fa fa fd fd fd fa fa fa 00 00 00 00 fa fa fd fd
  0x503000061880: fd fa fa fa fd fd fd fa fa fa fd fd fd fd fa fa
=>0x503000061900: fd[fd]fd fa fa fa fd fd fd fd fa fa fd fd fd fa
  0x503000061980: fa fa fd fd fd fa fa fa fd fd fd fa fa fa 00 00
  0x503000061a00: 00 fa fa fa 00 00 00 fa fa fa 00 00 00 00 fa fa
  0x503000061a80: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x503000061b00: fa fa 00 00 00 fa fa fa fd fd fd fd fa fa fd fd
  0x503000061b80: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
```

### aj...@chromium.org (2023-12-12)

I agree that a cycle of Add() Notify(CANCELLED) Remove() (which is fine) followed by a second Notify(FAILED_PRECONDITION) that doesn't manipulate state_ but state_ is already free from the previous cycle will result in the UAF - I'm not sure yet why there are two notifications

### aj...@chromium.org (2023-12-12)

I think the contexts are ok - I think the trouble is that the MOJO_RESULT_FAILED_PRECONDITION can happen after the MOJO_RESULT_CANCELLED but cancelled should be last according to https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/c/system/trap.h;l=52?q=mojo%20trap%20cancelled%20mojo_result_failed_precondition&ss=chromium%2Fchromium%2Fsrc

I see that the precondition notification comes from a different thread than the cancelled notification

### aj...@chromium.org (2023-12-12)

Unbind:  https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/bindings/remote.h;l=292;drc=8e78783dc1f7007bad46d657c9f332614e240fd8

```
Unbinds this Remote, rendering it unable to issue further Interface method
   calls. Returns a PendingRemote which may be passed across threads or
   processes and consumed by another Remote elsewhere.

   Note that it is an error (the bad, crashy kind of error) to attempt to
   |Unbind()| a Remote which is awaiting one or more responses to previously
   issued Interface method calls. Calling this method should only be
   considered in cases where satisfaction of that constraint can be proven.

   Must only be called on a bound Remote.
```

Suggests that: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/blob/blob_data.cc;l=390?q=third_party%2Fblink%2Frenderer%2Fplatform%2Fblob%2Fblob_data.cc:390&ss=chromium%2Fchromium%2Fsrc

void BlobDataHandle::CloneBlobRemote(
    mojo::PendingReceiver<mojom::blink::Blob> receiver) {
  base::AutoLock locker(blob_remote_lock_);
  if (!blob_remote_.is_valid())
    return;
  mojo::Remote<mojom::blink::Blob> blob(std::move(blob_remote_));
  blob->Clone(std::move(receiver));
  blob_remote_ = blob.Unbind();
}

Is not behaving.

### ok...@chromium.org (2023-12-13)

Thank you for the analysis emilykim8708@ and ajgo@!

ayui@, could you please route this issue to the appropriate owner? Thanks!

(from https://crsrc.org/c/storage/OWNERS)

[Monorail components: -Internals>Mojo Blink>Storage]

### aj...@chromium.org (2023-12-13)

CC'ing some folks - ptal

### ay...@chromium.org (2023-12-14)

Haven't repro'd this locally yet, still running the test. In the meantime, so far I'm unable to identify where might the second notification might be coming from... 

+mek@ - wondering if you can help take a look? looks like you added the cloning behavior that might be the suspected area.

### me...@chromium.org (2023-12-16)

My understanding of the Remote::Unbind comment was that that specifically is about interface method calls that have responses. None of the Blob methods that are called this way have any response callbacks, so my assumption was (and still is) that this is supposed to work right.

Are we sure this isn't "just" a mojo bug?

[Monorail components: Internals>Mojo]

### [Deleted User] (2023-12-20)

rockot: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2024-01-17)

[secondary security shepherd]

Hi rockot@, can you take a look at https://crbug.com/chromium/1508753#c20 and reply? Thanks!

### th...@chromium.org (2024-01-30)

[secondary shepherd] Hi rockot@, could you please respond to https://crbug.com/chromium/1508753#c20? (will ping over chat as well)

### ro...@google.com (2024-01-30)

Yes it's possible that this is just a bug in WaitSet. I have already looked and not found anything obvious, but I'll keep looking.

### ro...@google.com (2024-01-31)

Still no repro but I have a solid hypothesis now. Working on a regression test to validate it.

### em...@gmail.com (2024-01-31)

Thank you for your update.While I understand that different machine configurations might influence the repro, I'd like to share a small suggestion for reproducing the issue (though it might not be helpful due to different machine environments).
In my local tests, increasing the number of iframes in main.html to 250 and then running test.js(browser instance 25) with puppeteer quickly repro this issue.
tested version:
Chromium 123.0.6273.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1254377.zip)

### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3557a2fcbdd8167f97ca81171be2e0da9c4f0647

commit 3557a2fcbdd8167f97ca81171be2e0da9c4f0647
Author: Ken Rockot <rockot@google.com>
Date: Thu Feb 01 00:28:55 2024

Prevent MojoTrap event re-ordering

Fixed: 1508753
Change-Id: I9ec14a12e7d1d147bda63703e1d6619fa30c8a51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5253039
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1254840}

[modify] https://crrev.com/3557a2fcbdd8167f97ca81171be2e0da9c4f0647/mojo/core/ipcz_driver/mojo_trap.cc
[modify] https://crrev.com/3557a2fcbdd8167f97ca81171be2e0da9c4f0647/mojo/core/trap_unittest.cc


### ro...@google.com (2024-02-01)

Could someone who reliably reproed this give it a shot with the patch above to verify the fix?

### em...@gmail.com (2024-02-01)

I ran for over 2 hours and have not been able to reproduce the issue again. However, since the issue was somewhat difficult to reproduce, I cannot be 100% certain that it has been fixed. 
So I'll run it overnight to check for any issues and will update here.

### [Deleted User] (2024-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-01)

Requesting merge to extended stable M120 because latest trunk commit (1254840) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1254840) appears to be after stable branch point (1233107).

Requesting merge to beta M122 because latest trunk commit (1254840) appears to be after beta branch point (1250580).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-02-02)

Merge review required: M122 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-02-02)

Merge review required: M121 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-02-02)

Merge review required: M120 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2024-02-02)

Ran all night, did not reproduce again.

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1508753?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage, Internals>Mojo]
[Monorail components added to Component Tags custom field.]

### ro...@google.com (2024-02-05)

1. fixes a critical security bug affecting all processes including browser
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5253039>
3. yes
4. no
5. n/a
6. n/a

### am...@chromium.org (2024-02-07)

merges approved for https://crrev.com/c/5253039
please merge this fix to M122 / branch 6261 by EOD Monday 12 February so this fix can be included in M122 Stable cut 
please merge this fix to M121 Stable/ branch 6167 by EOD tomorrow, 8 February so this fix can be included in next week's M121 Stable security update

There are no further planned releases of M120 Extended Stable, so M120 merges are not needed 

### am...@google.com (2024-02-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-08)

Congratulations on another one Cassidy Kim! The Chrome VRP Panel has decided to award you $5,000 for this issue of a mildly mitigated mojo memory corruption bug, mitigated by it being significantly racy and difficult to reasonably trigger (c#9). Thank you for your efforts and reporting this issue to us! 

### sr...@google.com (2024-02-12)

Based on discussion with adetaylor@ and others offline, we see a crash on canary which we are not 100% sure related to this or not, so we will not merge to M121 this week , but will wait for more coverage before merging 

### pg...@google.com (2024-02-13)

assigning to ajgo@ to help with merges when the time comes (thank you!!) - removing merge approval label for now

### aj...@chromium.org (2024-02-15)

Looking at stability - counts for canary are stable for TrapEventHandler &  HandleEvent so I think this is ok to merge

https://crash.corp.google.com/browse?q=EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+Regexp_Contains%28FunctionName%2C%27mojo%3A%3Acore%3A%3Aipcz_driver%3A%3AMojoTrap%3A%3AHandleEvent%27%29%29+AND+expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27#samplereports:30,productname:1000,productversion:40,processtype:120,+channel,magicsignature:1000,magicsignature2:50,stablesignature:50,clientid:100,osversion:100,cpuinfo:100,url:30,runningfinchexperiments:5000

https://crash.corp.google.com/browse?q=EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+Regexp_Contains%28FunctionName%2C%27mojo%3A%3Acore%3A%3Aipcz_driver%3A%3AMojoTrap%3A%3ATrapEventHandler%27%29%29+AND+expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27#samplereports:30,productname:1000,productversion:40,processtype:120,+channel,magicsignature:1000,magicsignature2:50,stablesignature:50,clientid:100,osversion:100,cpuinfo:100,url:30,runningfinchexperiments:5000

### sr...@google.com (2024-02-15)

amyressler@ gracepark@ can you review this and approve if you are good with M122 merge? M121 is already last re-spin this week so not needed

### aj...@chromium.org (2024-02-15)

Merging to 122, not merging to 121 as that is no longer necessary.

### am...@chromium.org (2024-02-15)

Yep -- approved

### am...@chromium.org (2024-02-15)

ajgo@ I'm sure you already know that branch for 122 == 6261 but putting this here for your convenience in case not

### ap...@google.com (2024-02-15)

Project: chromium/src
Branch: refs/branch-heads/6261

commit 654837047abe4d3a0f22d17a22396eb77bb8235a
Author: Ken Rockot <rockot@google.com>
Date:   Thu Feb 15 20:30:22 2024

    Prevent MojoTrap event re-ordering
    
    (cherry picked from commit 3557a2fcbdd8167f97ca81171be2e0da9c4f0647)
    
    Fixed: 1508753
    Change-Id: I9ec14a12e7d1d147bda63703e1d6619fa30c8a51
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5253039
    Commit-Queue: Ken Rockot <rockot@google.com>
    Reviewed-by: Robert Sesek <rsesek@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1254840}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5299857
    Reviewed-by: Oksana Zhuravlova <oksamyt@chromium.org>
    Commit-Queue: Alex Gough <ajgo@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6261@{#794}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       mojo/core/ipcz_driver/mojo_trap.cc
M       mojo/core/trap_unittest.cc

https://chromium-review.googlesource.com/5299857


### pe...@google.com (2024-02-15)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### na...@google.com (2024-02-18)

ajgo@chromium.org,
Based on comment#35, my understanding is, this vulnerability fix does not impact LTS-114. If that is not the case, pls add LTS-Merge-request-114 and respond to the questionnaire that gets added. thanks

### aj...@chromium.org (2024-02-18)

the fix fixed code introduced in 276ea49 M110 so if LTS114 has enabled mojoipcz then the fix should be considered for a backport.

### na...@google.com (2024-02-18)

thanks ajgo@chromium.org,
Could you help add the engineer who can verify if LTS-114 has enabled mojoipcz? After verifying, if the fix is needed, the engineer needs to add LTS-Merge-request-114 and respond to the questionnaire that gets added. thanks

voit@google.com,
Could you verify if LTS-114 has enabled mojoipcz? thanks

### vo...@google.com (2024-02-19)

It seems like mojoipcz is not enabled on ChromeOS (both in M114 and M120). See <https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/embedder/embedder.cc;l=43;drc=46a1696aecca1d6086987c428b4a7cac6e87547b>

so marking this as not applicable to both LTS versions.

### na...@google.com (2024-02-21)

Based on comment#55 & 57, LTS-114/ 120 has not enabled mojoipcz in ChromeOS, so Not applicable to these releases.

### pe...@google.com (2024-05-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41481374)*
