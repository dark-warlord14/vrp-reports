# Security: XSS in contenteditable elements via svg>use xlink:href 

| Field | Value |
|-------|-------|
| **Issue ID** | [40074376](https://issues.chromium.org/issues/40074376) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>DataTransfer, Blink>Editing>Paste, Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | da...@microsoft.com |
| **Created** | 2023-10-07 |
| **Bounty** | $500.00 |

## Description

Heyy there,

Taking an example from MDN for contenteditable elements:

```html
<blockquote contenteditable="true">
  <p>Edit this content to add your own quote</p>
</blockquote>

<cite contenteditable="true">-- Write your own name here</cite>
```

Elements with contenteditable attribute allows users to not only input normal plain text but also html (in cases where it comes directly from clipboard) this is already known. If the user types the html code inside contenteditable  element , it will get html encode but in case when it comes from the clipboard the formatting is preserved.

This blog really explains this behaviour well and also the problem with allowing html injection : https://davidyat.es/2016/02/16/contenteditable/


I used this website to easily store some xss payload in my clipboard and test out the contenteditable element : https://cdn.sekurak.pl/copy-paste/playground.html

```html
test<img src=x onerror=alert()>
```

The above payload was used but when I pasted it in the conteneditable element using ctrl+v , I noticed that the onerror attribute was removed which means that some sanitization is going on here to avoid xss.

After testing it for a while, I found that this payload gets pass through the sanitization as it is:

```html
<svg><use xlink:href="external.svg#xss" /></svg>
```

So basically by using the above payload it's possible for an attacker to bypass the sanitizer used for sanitizing user inputted values in contenteditable elements.I have tested the same in firefox too and there they are properly sanitizing this payload

Checked the attached screenshot for the differences in chrome and firefox sanitization:

In chrome it's this:

```html
<svg style="color: rgb(0, 0, 0); font-size: medium; font-style: normal; font-weight: 400;"><use xlink:href="external.svg#xss"></use></svg>
```

And in firefox:

```html
<svg><use></use></svg>
```

There is only one small caveat for this payload that the origin of the external svg file should be same origin then only it will load otherwise you will get the below error:

```
Unsafe attempt to load URL https://sudistark.github.io/external.svg from frame with URL https://target.com Domains, protocols and ports must match.
```

In real world scenario the attacker would need to upload a svg file also on the targetted site (such image upload features are pretty common everywhere so the chances are very high that this could indeed by exploited) where he wants to exploit xss in contenteditable element.


**Steps to reproduce:**

1.I have hosted the mdn example code for contenteditable here: https://sudistark.github.io/contenteditable.html , so open this url in one tab
2.In another tab open this url: https://cdn.sekurak.pl/copy-paste/playground.html
 (we will using it to store the xss payload to our clipboard)
3.In the *HTML Input* field add this payload:

```html
<svg><use xlink:href="https://sudistark.github.io/external.svg#xss" /></svg>

```

The external.svg file has this payload in it:

```html
<?xml version="1.0" encoding="UTF-8" standalone="no"?> <svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" width="100" height="100" id="xss"> <a xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="javascript:alert(1)"> <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /> </a> </svg>

```


I have already uploaded the `external.svg` file on the same host where the contenteditable element exists (in real world the same could be achieve via image file upload or something)

4.Click on *Copy as HTML* to store it in our clipboard
5.Now paste this by using ctrl+v in the https://sudistark.github.io/contenteditable.html which we opened in step 1
6.A red circle should be visible if you click on it the xss popup will appear


I have also attached a video poc

**Impact**
This will allow an attacker to have copy paste xss in sites using contenteditable elements.


Tested on :
Version 117.0.5938.150 (Official Build) (64-bit)
Windows 11


## Attachments

- [chrome_DCUwkDs5ih.png](attachments/chrome_DCUwkDs5ih.png) (image/png, 183.0 KB)
- [firefox_jrT28YDg6P.png](attachments/firefox_jrT28YDg6P.png) (image/png, 124.8 KB)
- [chrome_Z8E8AswCZw.mp4](attachments/chrome_Z8E8AswCZw.mp4) (video/mp4, 4.8 MB)
- [chrome_X4ixxcPPMo.png](attachments/chrome_X4ixxcPPMo.png) (image/png, 30.6 KB)
- [firefox_Buvk3qW2QH.png](attachments/firefox_Buvk3qW2QH.png) (image/png, 52.5 KB)
- [index.html](attachments/index.html) (text/plain, 457 B)
- [chrome_WYTatcv8sG.png](attachments/chrome_WYTatcv8sG.png) (image/png, 94.0 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-10-07)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-10-07)

Ok after taking a second look at securityMB's blog, the bug which I have reported should be classic Copy Paste XSS (not limited to contenteditable elements) same as what securityMB reported.



### wf...@chromium.org (2023-10-09)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>SanitizerAPI]

### ad...@google.com (2023-10-09)

(I am a bot: this is an auto-cc on a security bug)

### ts...@chromium.org (2023-10-09)

The one small caveat that the origin of the external svg file must be same origin as the page isn't so small -- it is, in fact, the underlying basis of the security model for SVG images. While sites may allow user image uploads, they are generally restrictive in the types of formats supported, since sites that allow uploads pretty much publish links to view the uploaded images themselves.  In other words, the problem is in the site, and this sort of trickery isn't usually required if the site will re-display an SVG image on a credentialled domain directly. 

See also https://crbug.com/1110511 was the implementation bug for svg support. mek, per c32 on that bug, might you have some context about who should be looking at this?


[Monorail components: Blink>DataTransfer]

### me...@chromium.org (2023-10-09)

I don't think that bug is related to this; that was specifically about adding svg support to the async clipboard API, not about any ctrl-v behavior, and also never shipped (https://chromestatus.com/feature/5125790490427392).

This case seems much more related to for example https://crbug.com/chromium/1315040? Although not sure if it is similar enough that the same people would be the ones to look at this.

[Monorail components: Blink>Editing>Paste]

### ts...@chromium.org (2023-10-09)

Agreed, assigning to author of the fix to 1315040.

### su...@gmail.com (2023-10-10)

Hey, the researcher ( Michał Bentkowski ) which reported the drag and drop xss in https://crbug.com/1315040 now works for Google itself :p , would it be possible to add him to this report as he knows this stuff better than anyone else? 

### su...@gmail.com (2023-10-10)

>While sites may allow user image uploads, they are generally restrictive in the types of formats supported, since sites that allow uploads pretty much publish links to view the uploaded images themselves.  In other words, the problem is in the site, and this sort of trickery isn't usually required if the site will re-display an SVG image on a credentialled domain directly

I kinda agree if the site is allowing users to upload svg files then it's a problem in the site as xss could be executed directly by visiting the uploaded public url only when it's served as inline. But consider this scenario, it would be the fault of site if they are serving the upload svg files as inline. What if they are serving the files with this header instead of inline:

```
<?php

header('Content-Disposition: attachement; filename="image.svg"');
.....
?>

```

Now if anyone would try to visit the uploaded svg url it will be downloaded instead of executing directly in browser, we would consider this good measure to avoid xss via svg files.


The svg>xlink:href would still reference the uploaded svg file and the xss would still work

You can try by using this script

```php
<?php

// svg attachement

header('Content-Type: image/svg+xml');
header('Content-Disposition: attachement; filename="image.svg"');

// svg content
echo "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> <svg xmlns:svg=\"http://www.w3.org/2000/svg\" xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\" id=\"xss\"> <image href=\"1\" onerror=\"alert(1)\" /> </a> </svg>";

?>


```

```bash
php -S 127.0.0.1:1337
```

index.html:

```html
<svg><use xlink:href="index.php#xss" /></svg>

```

Now try to access http://127.0.0.1:1337/index.html, the xss popup should appear.

In this case we can't blame the site for not having enough protection to avoid xss via svg they did everything correct, but the xss still worked.

### [Deleted User] (2023-10-10)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2023-10-10)

We've been blocking data hrefs, and that seems not enough.

I think we have to block all non-local hrefs.

### gi...@appspot.gserviceaccount.com (2023-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/32da120404652a48fbd1f02ed70ca78acd7cf819

commit 32da120404652a48fbd1f02ed70ca78acd7cf819
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Oct 10 23:48:02 2023

Disallow pasting any svg use element with non-local hrefs

We've been blocking data hrefs but other non-local hrefs can still be
exploited, so this patch disallows all non-local hrefs.

Fixed: 1490811
Change-Id: If7cef9bf71ce8628fb7b4897b228fd6e2045ce06
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4928769
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1207985}

[modify] https://crrev.com/32da120404652a48fbd1f02ed70ca78acd7cf819/third_party/blink/renderer/platform/runtime_enabled_features.json5
[modify] https://crrev.com/32da120404652a48fbd1f02ed70ca78acd7cf819/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/32da120404652a48fbd1f02ed70ca78acd7cf819/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html


### [Deleted User] (2023-10-10)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2023-10-11)

The fix came out pretty quick really, wanted to ask is the severity going to changed to Medium? As in past similar bugs the severity has been medium only not low eg: https://bugs.chromium.org/p/chromium/issues/detail?id=1315040

### xi...@chromium.org (2023-10-11)

Reason for Security_Severity-Low is already given in https://crbug.com/chromium/1490811#c5.

Because the external svg must be from the same site, which means the site must have already been compromised somehow. Your example in https://crbug.com/chromium/1490811#c9 is also similar -- if the site allows uploaded php to be run (and return an svg), that's already a successful XSS.



### su...@gmail.com (2023-10-11)

Nope that's not what I meant I think you misunderstood, sorry if the explanation wasn;t correct. Let me explain it again, the website owner  can decide whether to serve uploaded files as inline or attachement.
In case of inline , if the user is able to upload svg files then it's a straight forward xss. 
But in case they use `attachement` to serve the uploaded files then no xss will be there, as the file will be downloaded instead (the browser won't execute the svg code in this case)

The php script which I shared was just an example of a website where they made sure to avoid xss via svg by serving uploaded files with this header:

```
header('Content-Disposition: attachement; filename="image.svg"');
```

As Content-Disposition isn't set inline, the website owner made sure that even if users are able to upload any file whether it be svg or something no xss would occur.

I was only trying to prove that the xlink:href still allows xss with svg files served with `Content-Disposition: attachement;` header also  (where there is no xss),using that php script.

Let me know if it still doesn't makes sense, I will try to explain it better next time.


### su...@gmail.com (2023-10-11)

>which means the site must have already been compromised somehow. Your example in https://crbug.com/chromium/1490811#c9 is also similar -- if the site allows uploaded php to be run (and return an svg), that's already a successful XSS.

The site is not compromised in any way, it's serving all uploaded files with `Content-Disposition: attachement;` header which makes the browser download those files instead of executing the code inside them. 
The reported bug makes a website vulnerable even when they did everything correct to avoid xss. No successful xss was possible before but with the copy paste thing and use of contenteditable elements the site is now vulnerable to xss.


### su...@gmail.com (2023-10-11)

Btw I tried using the same drag and drop poc which was used in (crbug.com/1315040 )  with my payload (xlink:href) and noticed that the xss popup appears there too. 

>Essentially, when you drag&drop an HTML data into an element that is content-editable, the HTML is automatically sanitized. I used to assume it is the same sanitization process that also works for copy&paste. It turns out that's not the case. I've found a way to execute arbitrary JavaScript on drag&drop by using SVG <use> tag.

From Michał Bentkowski comment in report crbug.com/1315040 , if I am understanding it correctly the fix made for this issue which I reported here ( in 1490811) is for COPY&PASTE behaviour only? 
So that means DRAG and DROP would be require another fix or one fix should take care of both XSSes whether it be from copy&paste or drag&drop


Here's the updated poc for drag and drop which I used with my payload:

```html
<!DOCTYPE html>
<meta charset="UTF-8">
<title>Drag And Drop Proof of Concept</title>
<script>const payload = `
  <svg><use xlink:href="index.php#xss" /></svg>
`;</script>
<div
  style="background:lightblue; padding: 2em; width:100px" 
  draggable=true
  ondragstart="event.dataTransfer.setData('text/html', payload)"
>Drag me!</div>
<div contenteditable style="border: 1px solid black; padding:2em; margin-top: 2em; height:200px">Drop here!</div>
```

In the attached screenshot you could see there also it's not sanitized.


### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-10-12)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-10-12)

Re https://crbug.com/chromium/1490811#c17:

> The reported bug makes a website vulnerable even when they did everything correct to avoid xss

This seems incorrect. The attack requires the uploaded php script to be run on the server side when requested as an inline svg, which is already a site issue.

Re https://crbug.com/chromium/1490811#c18:

Pasting and drag&drag currently use the same sanitizer, so normally a fix to one should also apply to the other.

That being said, the test case you provided in https://crbug.com/chromium/1490811#c18 does reproduce after my last fix landed, so I consider this issue not fixed yet. So I suppose there are still some link values (and possibly in combination with how the pages are hosted) that still slip through.

I don't have enough time to look into this thoroughly, so if you can find more cases that should be sanitized but still not (in either pasting or drag&drop), that will help a lot!

### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-10-13)

I am trying to explain it one more time using another example with much detail, please forget about my previous comments related to php,etc.I want to make sure you read the below with a clear mind.

The severity is being set to low because in order for an attacker to get xss using svg>xlink:href payload they need to upload a file  on the same origin (victim site)  which has the malicious svg content.

This is only possible when the victim site allows their user to upload svg files on their site. Your point is that if the site allows users to upload svg files then the site is already compromised means it's already vulnerable to xss.
So in order to get xss in contenteditable elements the attacker would need to use  a xss (via svg file upload) to get another xss in contenteditable elements
This is what your current thinking is right regarding this report bug?

The xss via svg file upload could only happen if the victim site is serving the file as inline
In case , if the svg files are served as attachment.Upon visiting the uploaded svg link the file gets downloaded and no xss occurs
So if the victim site is serving all the uploaded files with this header 

Content-Disposition: attachment; filename="cool.svg"

The cool.svg file will be saved as a regular download rather than displayed in the browser.

By serving the files as attachment the developer of victim site made sure that no xss could occur even if users managed to upload any arbitrary file such as svg,html,etc



Now we can conclude that the victim site is not vulnerable to any xss bug.As files are served as attachement.

Here comes the attacker which tries to uploads a svg image to the victim site to get xss, developers were clever so he couldn't get xss even after uploading svg files as the files were served as attachement.

When the attacker opened http://victim.site/user/1/upload/xss.svg , the file was downloaded by browser due to this response header `Content-Disposition: attachment; filename="xss.svg"`


Then the attacker saw that the victim site has contenteditable elements:


http://victim.site/index.html

```
<blockquote contenteditable="true">
  <p>Edit this content to add your own quote</p>
</blockquote>
```


So he uses this payload there:

```
<svg>
  <use xlink:href="http://victim.site/user/1/upload/xss.svg#xss" />
</svg>
```

Because this payload isn't sanitized by the Chrome browser , the attacker was able to get xss on the victim site even when the developer of victim site did everything correct to avoid xss. 
In this case we can't blame the developer of victim site for the xss bug which occured, as without the sanitizer bypass there was no occurence of xss before.

Similarly the same attack won't work in Firefox as there they are sanitizing properly by I removing xlink:href attribute.

I hope this should clear the misunderstanding on this.






> I don't have enough time to look into this thoroughly, so if you can find more cases that should be sanitized but still not (in either pasting or drag&drop), that will help a lot!

I have tried to look but svg>xlink:href was the only case which came as it is from the sanitizer for the time being. If anything else comes up I will let you know. Thanks for your work on this.




### su...@gmail.com (2023-10-30)

Ping ! I know this isn't a serious issue but was just making sure it's not been forgotten.

### su...@gmail.com (2024-01-07)

Ping, did you got some time to look into this?

### is...@google.com (2024-01-07)

This issue was migrated from crbug.com/chromium/1490811?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DataTransfer, Blink>Editing>Paste, Blink>SecurityFeature>SanitizerAPI]
[Monorail mergedwith: crbug.com/chromium/1492031]
[Monorail components added to Component Tags custom field.]

### xi...@chromium.org (2024-02-05)

I'm no longer on the Chrome team and will have limited (but still some) time working on Chromium. Hence I'm putting all of my bugs back to the triage queue for someone to pick up.

### ap...@google.com (2024-03-26)

Project: chromium/src
Branch: main

commit f64c54abd0cb8da311c629dcd1e9afdc47c34484
Author: Anupam Snigdha <snianu@microsoft.com>
Date:   Tue Mar 26 16:45:03 2024

    [Editing] Remove PastingBlocksSVGUseNonLocalHrefs flag.
    
    Feature has been enabled since 120.
    
    Bug: 1490811
    Change-Id: If4c27c66593f2ef76f503266de938bb06bdd2482
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5394256
    Reviewed-by: Sanket Joshi <sajos@microsoft.com>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Commit-Queue: Anupam Snigdha <snianu@microsoft.com>
    Cr-Commit-Position: refs/heads/main@{#1278386}

M       third_party/blink/renderer/core/editing/serializers/serialization.cc
M       third_party/blink/renderer/platform/runtime_enabled_features.json5

https://chromium-review.googlesource.com/5394256


### ti...@chromium.org (2025-01-14)

(primary shepherd)

Assigning to [snianu@microsoft.com](mailto:snianu@microsoft.com) as you appeared to have made movement on fixing this bug.

Reporter, [sudhanshur705@gmail.com](mailto:sudhanshur705@gmail.com), could you confirm that this bug still reproduces on the latest version of chrome?

### su...@gmail.com (2025-01-15)

redacted

### pe...@google.com (2025-01-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### ma...@chromium.org (2025-05-29)

Removing sajos@ ownership

### th...@chromium.org (2025-05-30)

Reporter:
1) Could you confirm this bug still reproduces on the latest version of chrome? (Same question as #comment31; it seems your response in #comment32 was deleted.)
2) If it does reproduce, could you please attach a POC that does not link to a real site (the playground), but instead, could you upload the POC files directly? (e.g. uploading the html files directly as attachments)

Adding the Needs-Feedback hotlist and setting the Next Action date to Monday.

### pe...@google.com (2025-06-02)

The NextAction date has arrived: 2025-06-02
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### su...@gmail.com (2025-06-02)

Hello, yeah I can confirm the fix. I am not able to reproduce the issue anymore

### pe...@google.com (2025-06-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### sn...@microsoft.com (2025-06-02)

Assigning this to daniec@ as I'm not on the Edge team anymore.

### ch...@google.com (2025-06-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### th...@chromium.org (2025-06-02)

[security shepherd]
Adding hotlist id 6265590 because it is unclear to me which CL fixed this bug.

### ch...@google.com (2025-06-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### th...@chromium.org (2025-06-02)

Setting the "Fixed By Code Changes" field to NA and keeping hotlist id 6265590 because it is unclear to me which CL fixed this bug.

### sp...@google.com (2025-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
thank you reward report of issue with low security impact and requiring specific preconditions of the website and providing limited attacker utility; since this did allow us to make a beneficial change to Chrome, we did want to extend a reward of appreciation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-04)

Thank you for your efforts and reporting this issue to us.

### su...@gmail.com (2025-06-05)

Hey, thanks for the bounty. I would like to donate the amount, I don't have any recommended charity so you can proceed with any charity of your choice.

### su...@gmail.com (2025-06-12)

Hey, any updates on the previous query?
I haven't claimed the bugcrowd link

### am...@chromium.org (2025-06-12)

Processing rewards for donation is a manual process, not one handled by automation like reward payments, so while this is in our queue it will take a bit more time before we can take action on this. And this can only take place after we receive a report for from the system confirming the rewards set aside (unclaimed) for donation.

### ch...@google.com (2025-09-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> thank you reward report of issue with low security impact and requiring specific preconditions of the website and providing limited attacker utility; since this did allow us to make a beneficial change to Chrome, we did want to extend a reward of appreciation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074376)*
