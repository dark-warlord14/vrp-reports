# Security: use-after-free vulnerability in flash player

| Field | Value |
|-------|-------|
| **Issue ID** | [40084462](https://issues.chromium.org/issues/40084462) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use-after-free vulnerability in flash player. Which hold a dangling pointer point to the memory had been freed.

In flash player the crash as follow:  

001dc9f0 8b442408 mov eax,dword ptr [esp+8]  

001dc9f4 56 push esi  

001dc9f5 57 push edi  

001dc9f6 8bf1 mov esi,ecx  

001dc9f8 85c0 test eax,eax  

001dc9fa 7405 je flashplayer\_21\_sa!WinMainSandboxed+0x1dfd7 (001dca01)  

001dc9fc 8b4034 mov eax,dword ptr [eax+34h] ds:0023:02b29074=????????  

eax=02b29040 ebx=012e1a90 ecx=02d06000 edx=00000001 esi=02d06000 edi=021d7710  

eip=001dc9fc esp=012e17cc ebp=012e1868 iopl=0 nv up ei pl nz na po nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202  

flashplayer\_21\_sa!WinMainSandboxed+0x1dfd2:  

001dc9fc 8b4034 mov eax,dword ptr [eax+34h] ds:0023:02b29074=????????

**VERSION**  

Flash player 21.0.0.242 in Chrome 51.0.2704.63 m windows 7 x86(other platform should be trigger)

Please drag the uaf.swf into chrome will crash.The source code file is uaf.as.

Credit is to "JieZeng of Tencent Zhanlu Lab"

And I do not want this issues to be public.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### fe...@chromium.org (2016-06-03)

Thank you for the report.



### fe...@chromium.org (2016-06-03)

natashenka@, could you take a look please?

[Monorail components: Internals>Plugins>Flash]

### cl...@chromium.org (2016-06-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-06)

adobe-flash@ friends, can any of you help triage this? I am not sure how to pass along bugs to Adobe.

### ih...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2016-06-06)

These go to Adobe, but I think natashenka@ has been helping here.

### na...@google.com (2016-06-06)

Yeah, looking at this one, but it's taking awhile because the PoC is so complex. I'll send a bug report to Adobe and update this bug once I figure out why it is crashing :)

### fe...@chromium.org (2016-06-06)

Great, thanks natashanka@! Someone had told me I shouldn't have assigned it to you, that's why I moved it. :)

### na...@google.com (2016-06-07)

Just reported it!

JieZeng, you say "And I do not want this issues to be public", but provide a credit, so I'm not sure what you want here. Can you let me know whether or not you want Adobe to name you in the bulletin when they issue an update?

### ji...@gmail.com (2016-06-07)

thanks natashanka@!

natashanka@!,please forgive my poor English! I want to say please do not public the vulnerability detail to others, for example MAPP and chrome issuess list. but I want my name in the Security Bulletins of Adobe when they update.

natashanka@,I am your fan! :)

### na...@google.com (2016-06-07)

Thanks, that makes sense. I'll let Adobe know about your preferences about MAPP, but I can't make any promises, it's their decision.

I'm not sure what we can do about the Chrome issues list, adding timwillis@ for more info. 

### wf...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-07)

Hey JieZeng,

If you want to keep this report private, we can do that but the credit goes to "anonymous". The reasoning is that we only lock down reports for anonymity reasons.

So, there are two options for you to choose from:

1) You can keep this report and PoC private, but credit goes to "anonymous" in the release notes.
2) This report will eventually become public (approximately 14 weeks after being marked as Fixed), and you can be credited as "JieZeng of Tencent Zhanlu Lab".

Please let me know if you would like Option 1 or Option 2. 

Thanks for the report!

### cl...@chromium.org (2016-06-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5622975151996928

### ji...@gmail.com (2016-06-08)

natashanka@,got it，thanks again！Wish you all the best！:)

### ji...@gmail.com (2016-06-08)

timwillis@

Hi timwillis,

I got it,I prefer option 2!

Thanks, Best regards!

### wf...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

@Jie - thanks for the quick reply. We'll make sure to credit you by name.

Tim

### ji...@gmail.com (2016-06-08)

@Tim

Thanks! 

### sh...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-14)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### ti...@google.com (2016-06-14)

@natashenka - can you please pass on Jie's preferred credit string to Adobe for the release notes?

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-06-14)

Sorry for the incorrect ClusterFuzz update, please ignore it. Reopening bug.

### ji...@gmail.com (2016-06-15)

Thanks for you reply. I was just about to ask the update from ClusterFuzz  since I can still reproduce it locally.

### sh...@chromium.org (2016-06-22)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2016-06-22)

Here's our current status on this:

I tested this a little more and found out this has been fixed in Townsend by CL 47709, where we added "GCRef<ScriptObjectHandle> soh = GetHandle();" to ScriptObject::GetLength() in splay.cpp.

22_0_d0_136=First Townsend build with Townsend CL 47709
23_0_d0_7=First Underwood build with Main CL 47708
22_0_r0_185=Townsend GM build
23_0_d0_56=Latest Underwood build

[After-fix]
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 in Firefox 46.0.1.5966 (32-bit) on Windows 7 x64 SP1
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 in IE 11.0.9600.18315 (32-bit) on Windows 7 x64 SP1
  PASS: FP 22_0_d0_136, 23_0_d0_7, 22_0_r0_185, 23_0_d0_56 (PPAPI) in Chrome 51.0.2704.84 (32-bit) on Windows 7 x64 SP1  
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Windows 7 x64 SP1  
  
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 in Firefox 46.0.1.5966 (32-bit) on Windows 8.1 x64
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 in Firefox 46.0.1.5966 (64-bit) on Windows 8.1 x64  
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 in Classic IE 11.0.9600.18124 (32-bit) on Windows 8.1 x64
  PASS: FP 22_0_d0_135, 22_0_r0_185, 23_0_d0_56 in Metro IE 11.0.9600.18124 (64-bit) on Windows 8.1 x64  
  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Windows 8.1 x64  

  PASS: FP 22_0_d0_135, 22_0_r0_185, 23_0_d0_56 in Firefox 46.0.1 on Mac OS 10.10.5 x64 x86_64
  PASS: FP 22_0_d0_135, 22_0_r0_185, 23_0_d0_56 in Safari 9.1.1 (10601.6.17) on Mac OS 10.10.5 x64 x86_64
  PASS: FP 22_0_d0_135, 22_0_r0_185, 23_0_d0_56 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Mac OS 10.10.5 x64 x86_64

  PASS: FP 22_0_d0_136, 22_0_r0_185, 23_0_d0_56 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Ubuntu 14.04 x64 trusty
  
[Before-fix]
* FAIL: FP 22_0_d0_135 in Firefox 46.0.1.5966 (32-bit) on Windows 7 x64 SP1
* FAIL: FP 22_0_d0_135 in IE 11.0.9600.18315 (32-bit) on Windows 7 x64 SP1
* FAIL: FP 22_0_d0_135, 23_0_d0_6 (PPAPI) in Chrome 51.0.2704.84 (32-bit) on Windows 7 x64 SP1
  PASS: FP 22_0_d0_135 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Windows 7 x64 SP1

* FAIL: FP 22_0_d0_135 in Firefox 46.0.1.5966 (32-bit) on Windows 8.1 x64
  PASS: FP 22_0_d0_135 in Firefox 46.0.1.5966 (64-bit) on Windows 8.1 x64
* FAIL: FP 22_0_d0_135 in Classic IE 11.0.9600.18124 (32-bit) on Windows 8.1 x64
  PASS: FP 22_0_d0_135 in Metro IE 11.0.9600.18124 (64-bit) on Windows 8.1 x64
  PASS: FP 22_0_d0_135 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Windows 8.1 x64

  PASS: FP 22_0_d0_136 in Firefox 46.0.1 on Mac OS 10.10.5 x64 x86_64
  PASS: FP 22_0_d0_136 in Safari 9.1.1 (10601.6.17) on Mac OS 10.10.5 x64 x86_64
  PASS: FP 22_0_d0_136 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Mac OS 10.10.5 x64 x86_64
  
  PASS: FP 22_0_d0_135 (PPAPI) in Chrome 51.0.2704.84 (64-bit) on Ubuntu 14.04 x64 trusty

### na...@google.com (2016-06-22)

I agree with the assessment. JieZeng, does this look fixed in the latest Flash update to you?

### ji...@gmail.com (2016-06-23)

natashenka,
Yes,it be fixed in 22.0.0.192. sad!
And I have reported another vulnerability which is better. ;) 
Please help me report it as soon as possible.

### sh...@chromium.org (2016-07-07)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2016-07-07)

Marking as fixed, based on comments #29 and #30.

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-14)

This issue was migrated from crbug.com/chromium/617105?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084462)*
