# Security: Possible to partially break sandbox restrictions imposed upon popup windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40094752](https://issues.chromium.org/issues/40094752) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-04-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Popup windows opened from sandboxed windows tend to have the same sandbox restrictions applied (except in the case where the "allow-popups-to-escape-sandbox" keyword has been specified).

There's usually no way of escaping this. Any embedded frames included in the popup will also be sandboxed and any further popups opened by the popup will be sandboxed as well.

However, by opening a popup window in a specific way, the sandbox restrictions can be partially bypassed within the popup.

**VERSION**  

Chrome Version: Tested on 74.0.3729.108 (stable) and 76.0.3777.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page includes a sandboxed iframe with the following attributes set:

<iframe src="iframe.html" sandbox="allow-scripts allow-popups"></iframe>

5. iframe.html contains a single link. Once you click that link, a new window will be opened using the following call:

window.open("javascript:", "\_blank");

6. This window will have the sandbox restrictions partially removed. To demonstrate this, an alert box will be shown. This works, even though the "allow-modals" keyword wasn't set on the original iframe.

The new window also has several other interesting properties:

1. It's same-origin with the original iframe. My understanding is that this shouldn't be possible. As the "allow-same-origin" flag hasn't been set, the original iframe shouldn't be able to create windows that share its origin. In practical terms, I don't think this is very useful, as you can't do anything within the popup that you can't do within the original iframe. But they still share an origin.

To allow you to verify this, the original iframe prints the following message to the console for the new window once it's been opened:

Test message from original iframe

2. iframes embedded within the new window will continue to be sandboxed as normal. An embedded iframe won't be able to call alert(), for example, even though the parent page can.
3. The exception to this are frames that are on the same origin as the original sandboxed iframe. These frames seemingly have most of the sandbox restrictions removed. For example, these frames can show alerts and fetch content from the same origin.

To allow you to verify the second point, the original sandboxed iframe creates an iframe embedded within the new window, with the iframe pointing to new\_window\_iframe.html. Note that this iframe (along with any other content on the page) won't actually be visible because of this issue:

<https://bugs.chromium.org/p/chromium/issues/detail?id=930179>

The iframe page first logs its origin to the console (which should be null, given that it's embedded within a page that's still technically sandboxed, but isn't), resulting in an output like the following:

Origin of embedded frame: <http://localhost:8080>

It then runs the following fetch command and logs the status of the result to the console:

fetch(window.location.href);

There are still some restrictions on what frames like these can do. For example, they can't access window.localStorage or window.sessionStorage. If one of these frames can create another popup window, though, that window will be able to access the storage areas. That would require another user activation, however.

4. I mentioned above that the window opened by the sandboxed iframe is partially sandboxed. Partially because although the page can show modals and do other things not allowed in the original sandboxed iframe, the page is still technically sandboxed and windows it opens or embeds will also be sandboxed.

Finally, note that the window doesn't need to be opened with the specific scheme used in step 5 above. The following examples will also have the same sort of effect:

window.open("file:///C:/");  

window.open("feed://");  

window.open("non-existent-scheme://");

These ultimately all get rewritten to about:blank, but that about:blank page is same-origin with the sandboxed iframe and allows the same effects as described above.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 204 B)
- [iframe.js](attachments/iframe.js) (text/plain, 609 B)
- [index.html](attachments/index.html) (text/plain, 152 B)
- [new_window_iframe.html](attachments/new_window_iframe.html) (text/plain, 149 B)
- [new_window_iframe.js](attachments/new_window_iframe.js) (text/plain, 200 B)
- [out-8.ogv](attachments/out-8.ogv) (video/ogg, 2.5 MB)

## Timeline

### mm...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### sh...@chromium.org (2019-04-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-11)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-26)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2019-05-31)

dcheng@: Would you mind taking a look at this?

### mm...@chromium.org (2019-07-01)

dcheng@, ping from the security marshal :) This issue has been reported more than 2 months ago.

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. dcheng, any updates?

### dc...@chromium.org (2019-08-07)

Oops sorry, I missed this in my owned bugs... I'll take a look today.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 342 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 356 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ar...@google.com (2020-12-07)

Daniel, may I steal this bug from you?
This week is a security fix-it week.
I have worked around sandbox recently. I just looked at the code. I understand the bug and I can trivially fix it for today.

### ar...@google.com (2020-12-07)

[Empty comment from Monorail migration]

### ar...@google.com (2020-12-07)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-12-08)

Sorry, I suspected a real bug, I found it, but it is very different from the one reported here.

The one reported here doesn't reproduce. See video. I tried also with allow-same-origin. It fails later, because the sandbox flags are correctly applied.

I bisected to find the possible patch that fixed this issue:
./tools/bisect-builds.py -b 638880 -g 812852 --verify-range --use-local-cache --archive=linux64
Scanning from 812852 to 638880 (173972 revisions).
Downloading list of known revisions... 
Loaded revisions 41523-809305 from /home/arthursonzogni/chromium/src/tools/.bisect-builds-cache.json
Saved revisions 41523-834670 to /home/arthursonzogni/chromium/src/tools/.bisect-builds-cache.json
Downloading revision 638880...
Received 115354535 of 115354535 bytes, 100.00%
Trying revision 638880...
Revision 638880 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 812847...
Trying revision 812847...
Revision 812847 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 721432...
Bisecting range [638880 (bad), 812847 (good)], roughly 16 steps left.
Trying revision 721432...
Revision 721432 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 683161...
Bisecting range [638880 (bad), 721432 (good)], roughly 15 steps left.
Trying revision 683161...
Revision 683161 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 658555...
Bisecting range [638880 (bad), 683161 (good)], roughly 14 steps left.
Trying revision 658555...
Revision 658555 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 673563...
Bisecting range [658555 (bad), 683161 (good)], roughly 13 steps left.
Trying revision 673563...
Revision 673563 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 678044...
Bisecting range [673563 (bad), 683161 (good)], roughly 12 steps left.
Trying revision 678044...
Revision 678044 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 675402...
Bisecting range [673563 (bad), 678044 (good)], roughly 11 steps left.
Trying revision 675402...
Revision 675402 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 674562...
Bisecting range [673563 (bad), 675402 (good)], roughly 10 steps left.
Trying revision 674562...
Revision 674562 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 673947...
Received 117972539 of 117972539 bytes, 100.00%
Bisecting range [673563 (bad), 674562 (good)], roughly 9 steps left.
Trying revision 673947...
Revision 673947 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 674262...
Bisecting range [673947 (bad), 674562 (good)], roughly 8 steps left.
Trying revision 674262...
Revision 674262 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 674035...
Bisecting range [673947 (bad), 674262 (good)], roughly 7 steps left.
Trying revision 674035...
Revision 674035 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 674128...
Bisecting range [674035 (bad), 674262 (good)], roughly 6 steps left.
Trying revision 674128...
Revision 674128 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 674191...
Received 117980877 of 117980877 bytes, 100.00%
Bisecting range [674128 (bad), 674262 (good)], roughly 5 steps left.
Trying revision 674191...
Revision 674191 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 674218...
Bisecting range [674191 (bad), 674262 (good)], roughly 4 steps left.
Trying revision 674218...
Revision 674218 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 674240...
Bisecting range [674218 (bad), 674262 (good)], roughly 3 steps left.
Trying revision 674240...
Revision 674240 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 674224...
Bisecting range [674218 (bad), 674240 (good)], roughly 2 steps left.
Trying revision 674224...
Revision 674224 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
You are probably looking for a change made after 674218 (known bad), but no later than 674224 (first known good).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/e6a1578d94cd94a7ffe2ce8dbec230883f1a1489..f898f31efa9b13b56985d60b30eddeb068598891

From the changelog, I strongly suspect Dave to have fixed this issue.
https://chromium.googlesource.com/chromium/src/+/f898f31efa9b13b56985d60b30eddeb068598891

Thanks Dave!

About potential reward, I don't know. This bug has been fixed more than a year ago.
Dave, did you discover this bug by yourself? Or do you have any bug opened related to this?

+CC antoniosartori@ FYI (I was talking about this bug / bisect on the chat)


### dt...@chromium.org (2020-12-08)

No, had no opened bug on this. It was just general cleanup.

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-08)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-09)

pls answer https://crbug.com/chromium/957042#c31

### ar...@chromium.org (2020-12-09)

Please read https://crbug.com/chromium/957042#c29.
Bug was fixed 1 year and 6 month ago. No merge required.

### ad...@google.com (2020-12-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $1000 for this bug. I'll also eventually figure out which version the fix landed in, and update the appropriate release notes to credit you. This may take me a few weeks.

### ar...@google.com (2020-12-17)

> I'll also eventually figure out which version the fix landed in

Version:(77.0.3842.0)
By: https://chromium.googlesource.com/chromium/src/+/f898f31efa9b13b56985d60b30eddeb068598891

### ar...@google.com (2020-12-17)

From https://crbug.com/chromium/957042#c26.

### ad...@google.com (2020-12-17)

Thanks :)

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/957042?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094752)*
