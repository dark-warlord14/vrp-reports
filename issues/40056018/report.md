# Security: Full screen notification overlap on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40056018](https://issues.chromium.org/issues/40056018) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | li...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2021-05-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36

Steps to reproduce the problem:
Similar to https://crbug.com/chromium/1037730

I create https://crbug.com/chromium/1212909 you made it public

- Please allow pop-ups from index.html

1. Lunch below html
2. Click on the button 
3. Click on the button 

<html onmousedown=onmousedown() onmouseup=onmouseup()>

<script>  
var w;
onmousedown=function(){
document.documentElement.webkitRequestFullScreen();
}

onmouseup=function(){
w=window.open("tel:https://google.com", "test", "width=1500 height=10");

 x = w.document.write("<h1>Hello World!</h1><p>Have a nice day!</p>");
document.body.style.backgroundImage = "url('https://lijoatppr.000webhostapp.com/back.png')";

}

</script>
</html>

What is the expected behavior?

What went wrong?
A popup can show up over fullscreen mode and block fullscreen function.

Did this work before? N/A 

Chrome version: 91.0.4472.77  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [spf.webm](attachments/spf.webm) (video/webm, 3.3 MB)
- [screen-capture (7).webm](attachments/screen-capture (7).webm) (video/webm, 1.5 MB)
- [screen-capture (3).webm](attachments/screen-capture (3).webm) (video/webm, 1.1 MB)
- [screen-capture (4).webm](attachments/screen-capture (4).webm) (video/webm, 351.8 KB)
- [screen-capture (24).webm](attachments/screen-capture (24).webm) (video/webm, 1.0 MB)

## Timeline

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-27)

ajgo@, please could you have a crack at reproducing this one? It's extremely similar to https://crbug.com/chromium/1212909 which you looked at yesterday. You may wish to strip out the reference to back.png. I still can't reproduce any z-order problem on Mac hence sending your way.

My interpretation of this report is that the reporter claims that the pop-up covers up the 'Esc to exit full screen' warning. We have previously considered that to be a valid security bug in 1037730. I can't reproduce that effect on Mac; I get similar results to your description in https://bugs.chromium.org/p/chromium/issues/detail?id=1212909#c10.

### aj...@chromium.org (2021-05-27)

This is super-unreliable, I perhaps got this to trigger around 1:23 in the video but only after a sequence of the main window not being in full screen, and me pressing esc and the right time.

https://drive.google.com/file/d/1-lKel2Tx1K70aReGqZd1nlWbZ-AJAr2H/view?usp=sharing (chromium.org)



### aj...@chromium.org (2021-05-27)

(either way it's the same issue)

### aj...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-28)

OK. Thanks Alex.

So to summarize:
* We think there is a case where the. "press esc to get out of fullscreen" may be hidden and we think that's a valid security bug
* We think it's really hard to reproduce
* It seems to involve the telephone call pop-up being visible

The call pop-up should make this a much less exploitable spoof than https://crbug.com/chromium/1037730 so I'm setting this to Low severity.

[Monorail components: Blink>Fullscreen UI>Browser>FullScreen]

### ad...@google.com (2021-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### li...@gmail.com (2021-08-10)

[Comment Deleted]

### li...@gmail.com (2021-10-12)

[Comment Deleted]

### li...@gmail.com (2022-05-09)

[Comment Deleted]

### li...@gmail.com (2022-09-02)

Hi,
I checked issue using Chrome
Version 105.0.5195.54 (Official Build) (64-bit)
And now it's fixed.

Lijo

### av...@chromium.org (2023-01-04)

Closing as per https://crbug.com/chromium/1213778#c12.

### li...@gmail.com (2023-01-05)

Hi,

When I reported it. It was bug so why don't make it as fixed could you please clarify. It's my second case. I report a bug after one year when I retest it it's fixed. So I report it. Your code change make it fixed after my repoting.

### li...@gmail.com (2023-01-05)

Also I reported more than 10 bugs now it's all in assigned stage. And if I report it as fixed you make it won't fix and my bug is not valid it's disgusting.

### li...@gmail.com (2023-01-11)

Sir,

Please replay robliao@chromium.org, cthomp@chromium.org, 	a...@chromium.org, I deleted my comment. When I reported it. It was bug so why don't make it as fixed could you please clarify. It's my second case. I report a bug, after one year when I retest it it's fixed. So I report it. Your code change make it fixed after my reporting. Also I reported more than 10 bugs now it's all in assigned stage. And if I report it as fixed you make it won't fix and my bug is not valid it's disgusting. the purpose of all hunting is your bounty. so please consider it

### li...@gmail.com (2023-02-22)

Sir,

It's my request please replay. 

### li...@gmail.com (2023-03-09)

Sir,

It's my request please replay.

### li...@gmail.com (2023-03-10)

Issue is not resolved. Showing new screen cast. press escape is not working and window continue to fullscreen and we can make fake omnibar as https://crbug.com/chromium/1393732 which is reported in Nov 26, 2022

### li...@gmail.com (2023-03-10)

Did i need to create another issue because here nothing is shared

### [Deleted User] (2023-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-10-23)

Per #19, sounds like this is not fixed?

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-07)

Hello OP, thanks for reaching out, but your comments here are a bit confusing. 
In https://crbug.com/chromium/1213778#c12 you relay that this issue was fixed. Because no action was taken on this bug, it was closed as WontFix. 
While externally reported security bugs should not be closed as WontFix if they are resolved, it seems likely this report is a duplicate of another reported issue and some work will need to be done to sort out which work was performed that resulted in resolving this issue. 

However, you have followed up to say this issue is not fixed. It was, therefore, reopened. However, the omnibar spoof you mention in https://crbug.com/chromium/1213778#c19 was indeed reported in November 2022 but resolved in December 2022. 
In your reproduction video in https://crbug.com/chromium/1213778#c20, it appears you are using Chrome version 112.0.5615.20. This appears to be an old video, since 112 has not been an actively supported release channel since May of 2023. 
Can you please clarify if this issue is still reproducible on a current version of Chrome (e.g. 118 Extended Stable or newer version)? 

I would also like to add that we understand your frustration here. Unfortunately low severity security bugs do not have an SLO, so in cases like this they are open for some time. I also understand that having an issue closed as WontFix doesn't seem fair without a greater explanation. It appears it was done in the most recent cases as a mistake based on your requests and conveying that these issues were resolved. While this can be cause for frustration, I need to request that you please keep your communications respectful and constructive, adhering to the Chromium Code of Conduct. [1]
Comments like those in c#14-16 are not respectful or conducive to finding a solution. Please be mindful of how you are communicating. 

As mentioned in previous issues, reaching out to security-vrp@ is a good thing to do in terms of getting responses to your questions since we can't monitor all active low severity issues or functional bugs. 

Again, we need you to please clearly follow-up here and let us know if this issue is still reproducible on an active production version of Chrome. 
Once we have that confirmation or information, we can move forward from there.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/CODE_OF_CONDUCT.md#be-respectful-and-constructive



### li...@gmail.com (2023-11-08)

Mam,

This is the screen cast of my issue in Version 121.0.6114.0 (Official Build) canary (64-bit) attaching here

### li...@gmail.com (2023-11-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-29)

Thank you for the video. I'll leave this open for the Openscreen team who is handling Fullscreen issues at this time to address. 
As this is a low severity bug and is less exploitable type of spoof, there is no SLO for this issue to be addressed.
The team is working on holistic changes to full screen so it may be some time before individual issues like this are resolved. Thank you for your patience in the meantime. 
Since this was opened in 2021, I'm going to set the Foundin as 118 even though it has existed long before this time, but that is current Extended Stable. The foundin- isn't super relevant here anyway, as a backmerge for a fix of this sort would not be needed. 

Additionally I see that this issue is opened to the public since it was previously closed as Fixed. Given the low impact and potential to exploit, I considered leaving it open, but since it is still considered a low severity issue, I'm going to follow our standard processes and add RV-ST. Please let me know if there are any issues with that. 

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-29)

This issue was migrated from crbug.com/chromium/1213778?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

### li...@gmail.com (2024-03-23)

Mam,
I checked issue using Chrome
Version 124.0.6367.8 (Official Build) beta (64-bit)
And now it's fixed.

Lijo

### li...@gmail.com (2024-04-11)

Mam,
I checked issue using Chrome
Version 124.0.6367.8 (Official Build) beta (64-bit)
And now it's fixed.

Lijo

### am...@chromium.org (2024-04-11)

Hello, the fullscreen team is working through issues. I'm going to let them confirm if this issue is resolved and verifying which CLs resulted in the fix. takumif@ can you verify if this issue has been resolved?

### li...@gmail.com (2024-07-10)

Dear Team,

It's Fixed 
I checked issue using Chrome
Version 128.0.6559.0 (Official Build) dev (64-bit)
Attaching Screen cast.

Lijo


### ms...@chromium.org (2024-08-02)

This does not seem to repro on Win + 126 Stable nor 129.0.6632.0 Canary.
The intended behavior's code has been pretty stable since 2020:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=c1b9831c8c232ab9470645977a18527cfa7bb993;l=4972
I can't think of a specific recent CL that would have had an impact here, but the original defect may have been flaky and made harder to trigger by orthogonal changes.
This seems safe to mark Fixed for now, but please do reopen if there's new repro information, thanks!

### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
$500 thank you reward for report of lower impact security UI bug


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Thank you for the effort and reporting this issue to us, Lijo.

### pe...@google.com (2024-11-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $500 thank you reward for report of lower impact security UI bug

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056018)*
