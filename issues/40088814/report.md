# Security: Use after free vulnerability about psdk in the latest version of Flash player

| Field | Value |
|-------|-------|
| **Issue ID** | [40088814](https://issues.chromium.org/issues/40088814) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2017-11215, CVE-2017-11225 |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2017-08-25 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
This is a UAF vulnerability about psdk.

VERSION
Flash Version: pepflashplayer32_26_0_0_151
Operating System: windows 7 x86 （other operating systems may also crash,but not test）

REPRODUCTION CASE
There are 2 poc file here.
The first one will crash when open the file which name is uaf_poc_open.swf
The second one will crash when quit Chrome which name is uaf_poc_quit.swf

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: 
636b9425 83c108          add     ecx,8
636b9428 6a00            push    0
636b942a 8b01            mov     eax,dword ptr [ecx]
636b942c ff5004          call    dword ptr [eax+4]    ds:0023:feeefef2=????????

Crash State: 
4:049> dd ecx
003cd418  feeefeee feeefeee feeefeee feeefeee
003cd428  feeefeee feeefeee feeefeee feeefeee
003cd438  feeefeee feeefeee feeefeee feeefeee
003cd448  feeefeee feeefeee feeefeee feeefeee
003cd458  feeefeee feeefeee feeefeee feeefeee
003cd468  feeefeee feeefeee feeefeee feeefeee
003cd478  feeefeee feeefeee feeefeee feeefeee



## Attachments

- [uaf_poc_open.swf](attachments/uaf_poc_open.swf) (application/octet-stream, 3.7 KB)
- [uaf_poc_quit.swf](attachments/uaf_poc_quit.swf) (application/octet-stream, 2.2 KB)

## Timeline

### ji...@gmail.com (2017-08-25)

Please tell Adobe I do not want to put this poc file in MAPP when report to Adobe.
Thank you!

### el...@chromium.org (2017-08-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### ta...@google.com (2017-08-28)

natashenka@, would you be the right person to look at this?

### ta...@google.com (2017-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-08-31)

I'm sorry I forgot something shown below.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-08)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2017-09-08)

Thanks, I've reported this to Adobe.

### ra...@chromium.org (2017-09-19)

ihf: do we typically mark these as externaldependency once they have been reported? 

### ih...@chromium.org (2017-09-19)

Yes, ExternalDependency is correct here. Normally I would also CC/assign Adobe the bug, but it sounds like in this case this is different?

### na...@google.com (2017-09-19)

Yeah, for security bugs, we send them to the Adobe Security Team. So just cc me on these bugs and I can send them in.

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-11-15)

[Comment Deleted]

### ji...@gmail.com (2017-11-15)

@natashenka hi!
This bug has been fixed, but I have questions.
Why the acknowledgments is "Jie Zeng of Tencent Zhanlu Lab" instead of "JieZeng of Tencent Zhanlu Lab working with the Chromium Vulnerability Rewards Program" on this page: https://helpx.adobe.com/security/products/flash-player/apsb17-33.html?

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-12-08)

[Comment Deleted]

### ji...@gmail.com (2017-12-08)

@natashenka hi!
Can anyone answer my question here?

I reported 3 bugs,they are https://crbug.com/chromium/758848,  768762 ,758863. And there are only 2 CVEs credit to me on the November's Adobe Security Bulletins and Advisories page: https://helpx.adobe.com/security/products/flash-player/apsb17-33.html . And all of 3 bugs are fixed.

Thanks!

### na...@google.com (2017-12-08)

https://crbug.com/chromium/758848 is still open with Adobe, I'll check what's going on with it. 

### na...@google.com (2017-12-08)

According to Adobe: We found that PSIRT-7347 was a dupe of PSIRT-7239 (CVE-2017-11215). So one issue was a duplicate. 

### ji...@gmail.com (2017-12-09)

Hi!
I do not know how Adobe definition repeated submission,but I know they may be wrong.

If there are duplicate pocs, they should be https://crbug.com/chromium/768762 and https://crbug.com/chromium/758863.But their trigger path is different.

Thanks.

### ji...@gmail.com (2018-01-02)

Anyone there? Why two months have passed without any new progress?

### na...@google.com (2018-01-02)

Sorry, can you provide a quick explanation of why you think they are different bugs, and I'll provide it to Adobe?

### ji...@gmail.com (2018-01-03)

[Comment Deleted]

### ji...@gmail.com (2018-01-03)

Hi natashenka!
I was wrong in https://crbug.com/chromium/758863#c19 and we start from here.

First: I want to know PSIRT-7347 is which one issue in https://crbug.com/chromium/758863#c22 ?
I assume PSIRT-7347 is  https://crbug.com/chromium/768762  ,because  https://crbug.com/chromium/758848  and https://crbug.com/chromium/758863 were fixed in the November patch(I saw pocs form November mapp). And I also know the PSIRT-7239 (CVE-2017-11215) is https://crbug.com/chromium/758848.

So I will explanation  https://crbug.com/chromium/768762 is different from https://crbug.com/chromium/758848 or https://crbug.com/chromium/758863.

Second: The reason is as follows:
The key point is to register the event handler in  https://crbug.com/chromium/768762 ,and free the problem object in the event handler.The source code is as follows:

public function main(){
    //some code
    try{ mediaPlayer = PSDK.pSDK.createMediaPlayer(eventDisp); } catch(e:Error){}
    //...
    try{ mediaPlayer.addEventListener(118,Listen); } catch(e:Error){}
}
public funciton Listen(e:PSDKEvent){
    //free internally
    try{ audSetting.getObject.call(contentResolver,ob_toStr); } catch(e:Error){}
    try{ tempVar3 = psdk.createMediaPlayer(eventDisp); } catch(e:Error){}
    try{ audSetting.setObject(ob_toStr,tempVar3); } catch(e:Error){}
    try{ tempVar3 = psdk.createDispatcher(); } catch(e:Error){}
    return;
}

However in https://crbug.com/chromium/758848 or https://crbug.com/chromium/758863 do not have the register the event handler code. So their trigger path are different.

Last: Please contact me if have any other questions!

### na...@google.com (2018-01-03)

PSIRT-7347 is 768762. I'll send this info to Adobe and see what they say.

### na...@google.com (2018-01-03)

PSIRT-7347 is 768762 and PSIRT-7239 is 758863. I'll give Adobe your explanation and let you know what I hear.

### ji...@gmail.com (2018-01-05)

Thanks!

### ji...@gmail.com (2018-01-15)

Adobe doesn't have any response?

### na...@google.com (2018-01-16)

From Adobe:

Apologies for the delayed reply.  While we agree that the two submissions are not exactly the same, they are nevertheless related, and were resolved with the same code change.  

This is the dev's comment:

I can see that this is a problem revolving around the MediaPlayer object being released similarly to how the QOSProvider object was mistakenly released in PSIRT-7239.

The fix for PSIRT-7239 was a very general fix and repairs issues with QOSProvider, MediaPlayer and MediaPlayerItemLoader.

### ji...@gmail.com (2018-01-17)

Ok, I understand.

I agree.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### na...@google.com (2018-01-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-29)

[Empty comment from Monorail migration]

### mb...@google.com (2018-01-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

Hi jiezengoftencentzhanlulab@! The VRP decided to award $5,000 for this report. Many thanks!

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### ji...@gmail.com (2018-02-06)

OK,I will do not publicly disclose details with others,but until when?

This bug has been fixed two months ago.

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

No merge needed.

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

Apologies, you're OK to disclose this and 758848 now. We push flash updates out of band of the main release cycle so this didn't get picked up for release notes until now.

### aw...@chromium.org (2018-03-06)

[Comment Deleted]

### ji...@gmail.com (2018-03-07)

The CVE number may not be correct, and the correct CVE should be CVE-2017-11215 or CVE-2017-11225?


### aw...@google.com (2018-03-07)

Thanks for flagging! Fixing here and on the release blog.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-04)

This issue was migrated from crbug.com/chromium/758863?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/768762]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088814)*
