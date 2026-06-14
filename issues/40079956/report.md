# Security: Extensions can spoof the list of host permissions in the permission dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40079956](https://issues.chromium.org/issues/40079956) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Platform>Apps, Platform>Extensions |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | yo...@chromium.org |
| **Created** | 2014-07-01 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**  

By inserting a NUL byte in a host permission, extension authors can hide all host permission requests, giving users a false sense of security when they install an extension. To solve this issue, I suggest to reject the URL pattern if it contains a NUL byte.

**VERSION**  

Chrome Version: 37.0.2019.0 (all versions, all channels)  

Operating System: ArchLinux x64

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

1. Create a directory and create contentscript.js and manifest.json (attached below).
2. Start Chrome and load the unpacked extension, e.g. using chromium --load-extension=/tmp/extensiondirectory
3. Visit chrome://extensions/ and click on "Permissions". Observe that the dialog shows "Access your data on:" instead of "Access your data on: example.com" (as seen in the attached screenshot)
4. Visit <http://example.com/>, and observe that the content script executes, even though the permission dialog said nothing about granting permissions to access this website.

manifest.json  

{  

"name": "Seemingly harmless",  

"version": "1",  

"manifest\_version": 2,  

"content\_scripts": [{  

"js": ["contentscript.js"],  

"matches": [  

"\*://\x00/\*",  

"\*://\*.example.com/\*"  

]  

}]  

}

contentscript.js  

alert('You did not expect this dialog, did you?');

## Attachments

- [access-your-data-on-blank.png](attachments/access-your-data-on-blank.png) (image/png, 40.4 KB)
- [contentscript.js](attachments/contentscript.js) (text/javascript, 51 B)
- [manifest.json](attachments/manifest.json) (application/json, 245 B)
- [Screen Shot 2014-07-02 at 11.57.29 AM.png](attachments/Screen Shot 2014-07-02 at 11.57.29 AM.png) (image/png, 21.6 KB)
- [Screen Shot 2014-07-02 at 11.59.25 AM.png](attachments/Screen Shot 2014-07-02 at 11.59.25 AM.png) (image/png, 44.4 KB)
- [contentscript.js](attachments/contentscript_53272170.js) (text/javascript, 51 B)
- [cws.zip](attachments/cws.zip) (application/zip, 531 B)
- [manifest.json](attachments/manifest_53272172.json) (application/json, 253 B)

## Timeline

### fe...@chromium.org (2014-07-02)

This only reproduces on linux.

### fe...@chromium.org (2014-07-02)

Thanks for the report.

I'm marking this as high severity since it lets an extension on Linux access websites without it showing up in the warning.

finnur@, would you be the right person to look at this?

### fe...@chromium.org (2014-07-02)

[Empty comment from Monorail migration]

### [Deleted User] (2014-07-02)

Yeah we should clearly be rejecting nonsensical characters in this host permissions, but that still begs the question where in the chain of manifest JSON --> permission warnings the \0 gets lost.

### [Deleted User] (2014-07-02)

This bug also exists on chromeos.

### fe...@chromium.org (2014-07-02)

[Empty comment from Monorail migration]

### fi...@chromium.org (2014-07-03)

I'm one of many people who might be appropriate to look at this, but I'm going on vacation pretty soon (tomorrow) so I'm not sure I am going to have enough time to follow through on this.

But this doesn't seem as scary as it first looked, because I can only get the extension to load via --load-extension, whereas a .crx fails on the empty permission. That makes me think you can't distribute this kind of extension via the webstore.

### fi...@chromium.org (2014-07-03)

... empty host*

### ro...@robwu.nl (2014-07-03)

The bug does not rely on an empty host. If you change "\x00" to "\x00whatever", then the issue still shows up.

I've uploaded the extension (unlisted) to the CWS, and I was able to install the extension without any problems: 
https://chrome.google.com/webstore/detail/seemingly-harmless/jjdmabeidkgbkibjbifallgokbkhlpgf

manifest.json
{
    "name": "Seemingly harmless",
    "version": "1",
    "manifest_version": 2,
    "content_scripts": [{
        "js": ["contentscript.js"],
        "matches": [
            "*://\x00/*",
            "*://*.example.com/*"
        ]
    }]
}


### ro...@robwu.nl (2014-07-03)

Ehh, "\x00" in the previous manifest.json in the previous comment should of course be changed to "\x00whatever".

### fi...@chromium.org (2014-07-03)

Yup. That's a better example. This one doesn't fail when installed via crx.

### me...@chromium.org (2014-07-07)

Filed http://b/16127784 for Webstore (internal bug).

### yo...@chromium.org (2014-07-07)

Going to look into this one from the Chrome side.

### bu...@chromium.org (2014-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/80d5aa4a1de9107d1442480b8ea9ba06feff2be2

commit 80d5aa4a1de9107d1442480b8ea9ba06feff2be2
Author: yoz@chromium.org <yoz@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jul 25 05:45:40 2014

Don't allow null bytes in hosts of host permissions.

BUG=390624
TEST=Load the sample manifest from the bug, https://crbug.com/chromium/390624#c9. It should fail to load.

Review URL: https://codereview.chromium.org/416263002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285492 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-25)

------------------------------------------------------------------
r285492 | yoz@chromium.org | 2014-07-25T05:45:40.163672Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern_unittest.cc?r1=285492&r2=285491&pathrev=285492
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern.cc?r1=285492&r2=285491&pathrev=285492
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern.h?r1=285492&r2=285491&pathrev=285492

Don't allow null bytes in hosts of host permissions.

BUG=390624
TEST=Load the sample manifest from the bug, https://crbug.com/chromium/390624#c9. It should fail to load.

Review URL: https://codereview.chromium.org/416263002
-----------------------------------------------------------------

### yo...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-07-29)

Bulk update

### js...@chromium.org (2014-07-29)

Bulk update.

### jo...@chromium.org (2014-07-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-04)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/879ee705feb62c7392bb7e38323d76b15b15f6e2

commit 879ee705feb62c7392bb7e38323d76b15b15f6e2
Author: yoz@chromium.org <yoz@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 04 20:21:04 2014

Merge 285492 "Don't allow null bytes in hosts of host permissions."

> Don't allow null bytes in hosts of host permissions.
> 
> BUG=390624
> TEST=Load the sample manifest from the bug, https://crbug.com/chromium/390624#c9. It should fail to load.
> 
> Review URL: https://codereview.chromium.org/416263002

TBR=yoz@chromium.org

Review URL: https://codereview.chromium.org/441643009

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@287396 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-04)

------------------------------------------------------------------
r287396 | yoz@chromium.org | 2014-08-04T20:21:04.051008Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/url_pattern_unittest.cc?r1=287396&r2=287395&pathrev=287396
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/url_pattern.cc?r1=287396&r2=287395&pathrev=287396
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/url_pattern.h?r1=287396&r2=287395&pathrev=287396

Merge 285492 "Don't allow null bytes in hosts of host permissions."

> Don't allow null bytes in hosts of host permissions.
> 
> BUG=390624
> TEST=Load the sample manifest from the bug, https://crbug.com/chromium/390624#c9. It should fail to load.
> 
> Review URL: https://codereview.chromium.org/416263002

TBR=yoz@chromium.org

Review URL: https://codereview.chromium.org/441643009
-----------------------------------------------------------------

### yo...@chromium.org (2014-08-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-22)

Thanks for the report! This qualifies for a $1000 reward. Someone should be reaching out to you soon with additional details.

How would you like to be credited when we mention this bug in our release notes?

### mb...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2014-08-22)

@mbarbella (c26)
Thanks for the credit! Preferably just using my full name, and since it is very short, also with a link to my home page:
<a href="https://robwu.nl">Rob Wu</a>

### ti...@chromium.org (2014-09-18)

Rob,

I've passed your details over to the finance team. If you haven't heard from them by this time next week asking for your payment details, please contact me directly (or update this bug).

Congratulations on the reward!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2014-10-16)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-11-11)

Bulk update: removing view restriction from closed bugs.

### pa...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### ab...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/390624?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079956)*
