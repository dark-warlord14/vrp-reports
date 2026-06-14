# Security: UAF in ReaderMode

| Field | Value |
|-------|-------|
| **Issue ID** | [40053909](https://issues.chromium.org/issues/40053909) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | UI>Browser>ReaderMode |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2020-11-18 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

The ownership of |old\_web\_contents| will be passed to |source\_page\_handle|[1] after |SwapWebContents|. Then |source\_page\_handle| will move to |MaybeStartDistillation|[2] as a parameter. At this time, if the check fails, it will return immediately. |source\_page\_handle| will be destroyed at this time, and |old\_web\_contents| becomes a dangling raw pointer. And the UAF will be triggered when accessing it[3].

```
void MaybeStartDistillation(  
    std::unique_ptr<SourcePageHandleWebContents> source_page_handle) {  
  const GURL& last_committed_url =  
      source_page_handle->web_contents()->GetLastCommittedURL();  
  if (!dom_distiller::url_utils::IsUrlDistillable(last_committed_url))    <<<-----------  
    return;  
  
  // Start distillation using |source_page_handle|, and ensure ViewerHandle  
  // stays around until the viewer requests distillation.  
  SelfDeletingRequestDelegate\* view_request_delegate =  
  ...  
  

```

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/dom_distiller/tab_utils.cc;l=176;drc=780cdfb2a0a86b71fdb9c5fc058883432853a3b8>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/dom_distiller/tab_utils.cc;l=127;drc=780cdfb2a0a86b71fdb9c5fc058883432853a3b8>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/dom_distiller/tab_utils.cc;l=182;drc=780cdfb2a0a86b71fdb9c5fc058883432853a3b8>

**VERSION**  

Chrome Version: stable  

Operating System: All except android

**REPRODUCTION CASE**

1. Setup an https Server with a valid certificate. (\*)
2. $ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  
   
   $ out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/xxxx --enable-dom-distiller "<https://localhost:8000/poc.html>"
3. Click the "Enter reader mode" icon in the location bar.

\* Or you can apply https.patch to bypass the verification of the certificate, it has nothing to do with the vulnerability itself.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud

## Attachments

- [asan](attachments/asan) (text/plain, 19.6 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [poc.html](attachments/poc.html) (text/plain, 516 B)
- [https.patch](attachments/https.patch) (text/plain, 770 B)

## Timeline

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>ReaderMode]

### ka...@chromium.org (2020-11-19)

I'm on a rotation through the end of the year. Reassigning to Dominic for triage.

### dm...@chromium.org (2020-11-19)

Just noting that ReaderMode is still behind a flag. This is critical before launch but not critical to merge sooner.

### [Deleted User] (2020-11-21)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-04)

dmazzoni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-14)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2020-12-17)

Lowering the priority and removing the target because the Reader Mode experiment is on hold right now. Will definitely fix before enabling the experiment again.

Let me know if you have any concerns.


### ad...@google.com (2020-12-17)

Dominic has confirmed that the feature would only currently be enabled for users who have turned it on via chrome://flags or a command line option, so downgrading so Security_Impact-None for now. Thanks!

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-03-03)

Checking in on this bug: Is this now impacting released versions of Chrome with Reader Mode shipping on Android and Desktop in https://crbug.com/chromium/952894?

### le...@gmail.com (2021-03-04)

dmazzoni@: It seems that more than three months have passed, do you have any plans to fix it recently?

### le...@gmail.com (2021-03-09)

Hi dmazzoni@ adetaylor@, friendly ping, could you make a plan or assign someone to do a fix? Because I want to confirm if I can share a bug pattern about some bugs including this issue in an upcoming meeting.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-16)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-18)

Hi leecraso@, apologies for the delay in response to your queries about this. ReaderMode was being run as an experiment and is not currently being run until all blocking issues (including this one) are fixed. ReaderMode development is on pause to determine the best path forward for the feature. Because of this, experimentation is paused and fixes for it are unable to be prioritized at this time. Currently there is not set timeline on when ReaderMode experimentation will begin again, so I am unable to provide insight into when this bug would be addressed. 

Unfortunately, given all the above, the only certainty I can provide at this time is that this bug is not likely be addressed and fixed by the time your presentation/meeting occurs to be able to share this bug or bug pattern. Sorry to be the bearer of bad news, but wanted to make sure I could provide as much insight as possible about this. Thank you for your patience and understanding. 

### le...@gmail.com (2021-03-18)

Thanks for your reply! Sorry to hear that, I at first thought it could be easy to fix. I will change the content that I share. Thanks again, and hope this issue could be fixed soon.

### le...@gmail.com (2021-04-15)

Friendly ping. Five months have passed, any news about it?

### am...@chromium.org (2021-04-15)

Hi leecraso@, thanks for checking in. Though it's been five months since your report it has only been about a month since the last update. Work on core ReaderMode feature experimentation and fixes appear to still be on pause. There is still currently no set timeline on when core ReaderMode feature work will resume. 
The Reader-Mode flag was just unexpired through the 95 release and ReaderMode remains behind its flag and experimentation for ReaderMode is still on pause at this time. 





### le...@gmail.com (2021-05-17)

Hi, I'm here again. Another month has passed, is there any new update? Is it possible to fix this bug first, regardless of the ReaderMode development?

### am...@chromium.org (2021-05-18)

Hi leecraso@ thanks for checking it, but there's not significant update. I'll share what I know at present from the ReaderMode team which is that this issue will absolutely be addressed before any Reader Mode deployment, but as of right now Reader Mode is experimental, behind a flag, and not on a roadmap for launch. This means there is no predetermined launch date so I can't provide any estimates about when this will be fixed. The developers are working on other higher priority issues affecting non-experimental features for now. 
I know this is not the type of update you are hoping for, but we appreciate your patience and understanding. Thank you! 


### le...@gmail.com (2021-05-26)

Hi, it seems that this bug has been fixed: https://source.chromium.org/chromium/chromium/src/+/7f44e0a0658e4b75c59a87a750124a90381f4688

But the issue id that the commit pointed to is 1203674, I think there might be something wrong with the processing, it should be duplicated into this issue.

### am...@chromium.org (2021-06-01)

Merging into https://crbug.com/chromium/1203674, even though this is the earlier report for the same issue, because the fix was landed there. I have confirmed with katie@ of the ReaderMode team that 1203674 is a duplicate of this issue. According to the ReaderMode team, https://crbug.com/chromium/1203674 resulted in a crash, which is why the fix was prioritized. That issue being a duplicate was an accidental oversight when that issue was being fixed.  

Note for VRP and release notes/CVE purposes, as this is the issue that should be credited and receive a CVE, as well as will need to be manually ported over for consideration by the VRP panel. 



### am...@chromium.org (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-02)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $20,000 for this report. Nice work and we appreciate your patience on this one!

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-06-25)

Hi, sorry to bother. I prepare to share a bug pattern about some bugs including this issue in an upcoming meeting. So could the view restrictions on this bug be removed early? Thanks.

### am...@chromium.org (2021-06-29)

Hi leecraso, since this is behind a flag and security_impact-None, it won't be a part of a stable channel release, so it can indeed be made public. Thanks again for the excellent report! Best of luck on your talk/presentation! 

### am...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### is...@google.com (2021-06-29)

This issue was migrated from crbug.com/chromium/1150328?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1203674]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053909)*
