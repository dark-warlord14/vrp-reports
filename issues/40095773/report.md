# Security: Malicious Extension can ignore SOP, with only `downloads` permission.

| Field | Value |
|-------|-------|
| **Issue ID** | [40095773](https://issues.chromium.org/issues/40095773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | co...@kjsman.me |
| **Assignee** | rd...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Same-Origin Policy wasn't applied at `chrome.downloads.download` API. So, malicious extension can ignore SOP, with only `downloads` permission.  

If victim clicks somewhere on the extension's malicious page, it triggered.

**VERSION**  

Chrome Version: 75.0.3770.90 Stable  

Operating System: Ubuntu 18.04.1 LTS x86\_64 - But it seems to work everywhere.

**REPRODUCTION CASE**  

Attached files are PoC.crx file, and poc.js file.  

poc.js is included in PoC.crx.  

You can install .crx file or watch .js file to see how exploit works.

Below is explaination.

```
// This works without permission of https://www.google.com  
chrome.downloads.download({  
    url: "https://www.google.com"  
})  

```

If attacker wants to hide Download Shelf to spoof victim much better, you also need `download.shelf` permission, but it's optional.  

Anyway, then, extension can bring this data when user just click extension's page, like:

```
startDrag = (e) => {  
    chrome.downloads.drag(#ID of DownloadItem#)  
}  
window.addEventListener('mousedown', startDrag)  
document.addEventListener('dragover', (e) => e.preventDefault())  
document.addEventListener('drop', processData);  

```

It's included as comment in .js file, but you can also request with POST method:

```
chrome.downloads.download({  
    url: "https://httpbin.org/post",  
    method: "POST",  
    headers: [{name: "X-Header", value: "Hi"}],  
    body: "it=works&with=POST"  
})  

```

So, malicious extension can bypass SOP and bring data, with only `downloads` permission.

**CREDIT INFORMATION**  

Reporter credit: Jinseo Kim

## Attachments

- [PoC.crx](attachments/PoC.crx) (application/octet-stream, 4.4 KB)
- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)

## Timeline

### co...@kjsman.me (2019-07-20)

Addition:
I tried to bring "file://*" URL, but failed. It throws: "NETWORK_INVALID_REQUEST"
Downloading online file without any permission seems to be vulnerable, but is stealing 'past download' vulnerable too? It can also work with chrome.downloads.drag().

### in...@chromium.org (2019-07-20)

Devlin, can you please help to triage.

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2019-07-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@kjsman.me (2019-07-21)

** https://crbug.com/chromium/986127 talks about chrome.downloads.drag. This issue talks about chrome.downloads.download.

### rd...@chromium.org (2019-07-22)

Great find!  I was able to reproduce this.  It's definitely scary.

For others, basically what's happening here is:
- The extension initiates a download of the target page (in the PoC, this is google.com).
- The extension has some sort of UI that the user clicks
- On click, the extension initiates chrome.downloads.drag(), which starts the drag-and-drop operation for the downloaded file (google.com)
- The mouse up from the user clicking is treated as a drop operation, which essentially shares the HTML file with the extension (and is then read through a basic FileReader()).

dtrainor@, as OWNER of the downloads API, could you take a look (or help triage further)?  +meacer@ as well from a security perspective.

[Monorail components: UI>Browser>Downloads]

### co...@kjsman.me (2019-07-22)

I thought about this bug - and I found that most of problem come from drag(), not download().
But we also should fix download() (It can send arbitary header).
Anyway, Before I thought, I created https://crbug.com/chromium/986127.
So, how will we track these bug?

### rd...@chromium.org (2019-07-22)

I think these two are basically the same bug - in each case, the (main) issue is that the drag() API allows the extension to read a local file from disk.  In this version, the extension uses the download() API to put that file on disk; in the other, it uses the chrome.tabs API to trigger the download.  That step seems to be WAI.  But then the extension uses the drag() API to read the contents.

I don't think there's a different in the exploit here - fixing drag() to not allow this will fix both bugs, and I don't think either the download() or tabs.create() methods are doing anything terribly wrong here.

Unless there's something I'm missing, I'll go ahead and de-dupe these and update the summary.

> But we also should fix download() (It can send arbitary header).
I think that's largely WAI, and falls into the scope of an API that allows the extension to initiate and manage downloads.  It also seems like changing that could break legitimate use cases.  I'll also wait for dtrainor@ or meacer@ to chime in with their thoughts, though.

### co...@kjsman.me (2019-07-25)

dtrainor@, meacer@, do you have any updates?


### rd...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-07-27)

dtrainor@ Is it in WIP? If then, can you add 'WIP' tag?

### co...@kjsman.me (2019-07-30)

[Comment Deleted]

### co...@kjsman.me (2019-07-31)

[Comment Deleted]

### sh...@chromium.org (2019-08-04)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2019-08-06)

Reassigning to qinmin@.  Sorry about that!  Please CC and don't directly assign so it goes through our triage queue.  My bad I missed the direct email.

### qi...@chromium.org (2019-08-07)

The easiest solution is probably only allow extensions with file:// permission to use the chrome.downloads.drag API.  WDYT, rdevlin@?

### co...@kjsman.me (2019-08-07)

1. Please ignore https://crbug.com/chromium/986043#c12, 13. I tested with wrong environment.
2. This behavior also exploitable at Opera browser; Maybe we have to discuss the release date with them.

### qi...@chromium.org (2019-08-07)

Oh,  rdevlin@ already asked about whether we are going to remove download.drag() API. So probably this will be the solution. This API has very low usage so qualifies for removal 

### co...@kjsman.me (2019-08-07)

qinmin@ Looks good to me

### qi...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-08-08)

I realize I forgot to circle back here after an internal email thread discussion.  After analyzing the utility and usage of downloads.drag(), in conjunction with the bugs that have cropped up around it, we've decided it best to simply remove the API.  I'm working on doing that now.

Because this is an API change, it isn't something we'll merge to M76 (M77, which branched very recently, is debatable).  I confirmed with meacer@ that this should be okay.

### co...@kjsman.me (2019-08-08)

As I said, we have to release this issue with Opera Browser. Is there any way to contact internally?
Anyway, https://crbug.com/chromium/986127 needs to be de-duped with this issue.

### rd...@chromium.org (2019-08-08)

> As I said, we have to release this issue with Opera Browser. Is there any way to contact internally?

You mean contact someone internally at Opera?  awhalley@, what's our normal procedure here?

> Anyway, https://crbug.com/chromium/986127 needs to be de-duped with this issue.

Just to confirm, you mean duped into this issue, right?

### co...@kjsman.me (2019-08-08)

rdevlin@ Yup.

### rd...@chromium.org (2019-08-08)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-09)

+some opera folk

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf

commit 8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue Aug 13 19:17:42 2019

[Extensions] Remove downloads.drag

The downloads.drag API has exceedingly low usage, and has other issues.
Remove it.

Bug: 986043

Change-Id: I3f0f41fba02a8d729feee9af036a1f383a0e1b0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1742547
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#686508}

[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/browser/extensions/api/downloads/downloads_api.cc
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/browser/extensions/api/downloads/downloads_api.h
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/common/extensions/api/downloads.idl
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/common/extensions/docs/examples/api/downloads/download_manager/popup.js
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/chrome/test/data/extensions/api_test/downloads/test.js
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/extensions/browser/extension_function_histogram_value.h
[modify] https://crrev.com/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf/tools/metrics/histograms/enums.xml


### rd...@chromium.org (2019-08-13)

Should be fixed.  I'll request a merge to M77 after letting it bake for a day.

### sh...@chromium.org (2019-08-14)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-08-14)

Could someone correct the description of this issue to the following?

-----

VULNERABILITY DETAILS
chrome.downloads.drag() API initiates drag for a downloaded file, which allows any droppable program can get the data of the file.
But, an attacker can simply abuse this API with malicious extension. If extension's install page is droppable and induces a victim to click the page, the following data can be leaked:
- Already Downloaded file
- Local binary file (chrome.tabs.create() automatically downloads the file if the URL is of the binary file.)
- Any websites' data (chrome.downloads.download() allows to download them all)

VERSION
Chrome Version: 75.0.3770.90 Stable
Operating System: Ubuntu 18.04.1 LTS x86_64 - But it seems to work on every environment.

REPRODUCTION CASE
Attached files are PoC.crx file, and poc.js file; poc.js is included in PoC.crx.


A malicious extension can execute this code when it's installed.
> chrome.downloads.download({
>   url: "https://www.example.com"
> })
> // or
> chrome.tabs.create({
>   url: "file:///bin/cat"
> })

Then, when the victim clicks the install page, which induces the victim to click itself, the extension can initiate dragging of the file.
> chrome.downloads.drag(<Download_File_ID>)

Finally, the extension can obtain the data of the file with the drop event.
> window.addEventListener('drop', callback);

CREDIT INFORMATION
Reporter credit: Jinseo Kim

### co...@kjsman.me (2019-08-14)

I uploaded https://crbug.com/chromium/986043#c30 to the wrong place: https://bugs.chromium.org/p/chromium/issues/detail?id=695474#c50
I removed it immediately.

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-20)

Requesting merge to beta M77 because latest trunk commit (686508) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-20)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-08-26)

Can anyone add lakpamarthy@ to CC? It seems that he doesn't see this issue(This issue is closed)

### la...@google.com (2019-08-27)

please respond to C#34 to consider M77 merge request. Thanks.

### rd...@chromium.org (2019-08-27)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes

2. Links to the CLs you are requesting to merge.
https://chromium.googlesource.com/chromium/src.git/+/8c3e2c3c1fd30b3fcc4dff17e33e4a00c09438bf

3. Has the change landed and been verified on master/ToT?
Yes

4. Why are these changes required in this milestone after branch?
Security fix

5. Is this a new feature?
No

6. If it is a new feature, is it behind a flag using finch?
N/A

### la...@google.com (2019-08-27)

merge approved for M77 branch 3865

### rd...@chromium.org (2019-08-30)

Not sure why, but it looks like bugdroid missed the commit here.  This was landed on M77 on Tuesday:

https://chromium.googlesource.com/chromium/src/+/c50370cd40d57ee67f257fa7e65bda402266af2f

### sh...@chromium.org (2019-09-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2019-09-02)

(Already merged, see #44)

### co...@kjsman.me (2019-09-07)

https://crbug.com/chromium/986127 was triaged as High severity, and merged into this issue, which is Medium severity. May anyone check it out?

### rd...@chromium.org (2019-09-09)

@47 I'll let one of the security folks (meacer@?  awhalley@?) chime in for sure, but I think that "Medium" is correct.  Accessing local files alone is considered "High", but we generally reduce by one level when it requires a malicious extension be installed (because that's a significant extra step on the part of the user, and we have extra protections in place on the webstore side).

### aw...@google.com (2019-09-09)

+inferno@ who triaged https://crbug.com/chromium/986127

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-09-10)

lakpamarthy@ Can you check https://crbug.com/chromium/986043#c30 and edit https://chromereleases.googleblog.com/2019/09/stable-channel-update-for-desktop.html?
This bug doesn't match with its title.

### ad...@google.com (2019-09-12)

contact@kjsman.me Thanks for getting in touch.

I'll be very happy to update the release notes.

We do like to keep the descriptions vague though, as we don't like to release full details of the bugs until the fixes are in wide use (bugs go out of Restrict-View-SecurityNotify state 14 weeks after the fix). So I wouldn't want to highlight the downloads.drag() API specifically.

The current description on the blog is: "Extension can bypass same origin policy." How's about "Extensions can read some local files"?

### co...@kjsman.me (2019-09-12)

adetaylor@ That seems to be good

### ad...@google.com (2019-09-12)

OK, I've updated - thanks for the feedback!

### sh...@chromium.org (2019-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-11-28)

adetaylor@ This CVE description isn't correct: same as https://crbug.com/chromium/986043#c52 .

May you change the title of this issue?


### ad...@google.com (2019-11-28)

Ah thanks. Will do!

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/986043?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Downloads]
[Monorail mergedwith: crbug.com/chromium/986127]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095773)*
