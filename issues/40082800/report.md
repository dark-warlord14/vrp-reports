# Security: Linking to chrome:// urls inside pdf

| Field | Value |
|-------|-------|
| **Issue ID** | [40082800](https://issues.chromium.org/issues/40082800) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation |
| **CVE IDs** | CVE-2015-6779 |
| **Reporter** | [Deleted User] |
| **Assignee** | pa...@chromium.org |
| **Created** | 2015-09-04 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

A hyperlink inside a pdf file shown by the chrome pdf-viewer can link to a chrome:// url and can be opened as a new tab. As this is prohibited in html (it will open about:blank), it also shouldn't be possible in a pdf-file.

**VERSION**  

Chrome Version: 44.0.2403.157 stable  

Operating System: Kubuntu 14.04

**REPRODUCTION CASE**  

Create a pdf file containing a hyperlink to a chrome:// url or download the attached file. Open the file inside chrome and open the link in a new tab or window.

## Attachments

- [chromeUrls.pdf](attachments/chromeUrls.pdf) (application/pdf, 7.9 KB)

## Timeline

### th...@chromium.org (2015-09-05)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-05)

[Empty comment from Monorail migration]

### ra...@chromium.org (2015-09-07)

I had a look. We can easily put a hack in to whitelist the URLs that we allow navigation to (e.g. https://codereview.chromium.org/1325413002) but it seems like there is a deeper problem.

It seems that BrowserPlugins should not allow navigations to chrome: URLs either as per the comment here: https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/renderer_host/render_process_host_impl.cc&rcl=1441524365&l=1885

However this does not seem to be kicking in, in our case rph->IsForGuestsOnly() seems to be returning false.

It seems like paulmeyer@ wrote this so may be able to comment more.

### ts...@chromium.org (2015-09-08)

[Empty comment from Monorail migration]

### ra...@chromium.org (2015-09-13)

Paul: do you have any thoughts?

### pa...@chromium.org (2015-09-14)

I haven't had a chance to look at this yet. I've been extremely busy with other things since last week. I should be able to look into this later this week.

### pa...@chromium.org (2015-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-09-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-16)

Please also check file:// URLs while you are at it. It looks as though the PDF viewer allows navigation to them, whereas it does not for webpages.

### pa...@chromium.org (2015-09-16)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-09-16)

@paulmeyer: Can you find some time to investigate this?  Linking to chrome:// URLs has been used as a step in sandbox escapes in the past, so this is high priority to fix.

@raymes/@thestig: Thanks for pointing out the potential implications for BrowserPlugin and file:// URLs.

### pa...@chromium.org (2015-09-16)

I am investigating now.

Also, rph->IsForGuestsOnly() is actually correct in returning false, because a mime handler guest shares a process with the mime handler extension. Thus, the process is not ONLY for guests.

### th...@chromium.org (2015-09-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-09-17)

This bug seems to be caused by this code: https://code.google.com/p/chromium/codesearch#chromium/src/extensions/browser/extension_web_contents_observer.cc&l=89

Note that it references a 2-year-old bug that explains that the potential security problems are known. Not sure why this was never followed up on.

### fs...@chromium.org (2015-09-17)

I've escalated the security severity to medium since this seems more broad than just the PDF Viewer. Any objections to that security severity level? This seems like something we should fix now and not keep holding off on?

### wj...@chromium.org (2015-09-17)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-09-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-09-18)

The ability for PDFs to link to "file://" URLs seems to have a differetn cause than what has allowed navigation to "chrome://" URLs, so I've created a new bug for it: https://crbug.com/chromium/533520.

### cr...@chromium.org (2015-09-22)

For reference, the current discussion on https://crbug.com/chromium/226927 is closely related, and paulmeyer@ has a CL started here: https://codereview.chromium.org/1362433002/.

### bu...@chromium.org (2015-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4

commit 1eefa26e1795192c5a347a1e1e7a99e88c47f9c4
Author: paulmeyer <paulmeyer@chromium.org>
Date: Thu Oct 01 02:11:13 2015

This patch implements a mechanism for more granular link URL permissions (filtering on scheme/host). This fixes the bug that allowed PDFs to have working links to any "chrome://" URLs.

BUG=528505,226927

Review URL: https://codereview.chromium.org/1362433002

Cr-Commit-Position: refs/heads/master@{#351705}

[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/chrome/browser/extensions/chrome_extension_web_contents_observer.cc
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/chrome/browser/pdf/pdf_extension_test.cc
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/browser/child_process_security_policy_impl.cc
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/browser/child_process_security_policy_impl.h
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/browser/child_process_security_policy_unittest.cc
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/public/browser/child_process_security_policy.h
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/public/common/url_constants.cc
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/content/public/common/url_constants.h
[modify] http://crrev.com/1eefa26e1795192c5a347a1e1e7a99e88c47f9c4/extensions/browser/extension_web_contents_observer.cc


### pa...@chromium.org (2015-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-10-12)

Fix is already in M-47, leaving merge-triage on this issue for consideration for M-46 patch.

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-11-05)

tinazh: Shall we try to merge? If not, let's remove the Merge-Triage label.

### pa...@chromium.org (2015-11-05)

Okay, I think merge into 46 would be a good idea.

### ti...@google.com (2015-11-05)

[Automated comment] Request affecting a post-stable build (M46), manual review required.

### ti...@google.com (2015-11-05)

Hey, M46 Stable and Stable refresh have both launched, the merge bar for M46 is very high as we only consider 0-day level of critical Security/ Stability/ Critical regressions.

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Congratulations ullrich.tiljasper - our reward panel awarded you $2,000 for this report! 

We'll credit you in our release notes as "Ullrich Tiljasper". If you would like to use another name, please update with your preferred credit name and I'll update the release notes. We'll also provide a CVE ID for your reference in a few hours.

A member from our finance team should be in touch within the next week to arrange payment. If you haven't heard from them within a week, please update this bug or email me directly at timwillis@.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-12-01)

CVE-2015-6779

### [Deleted User] (2015-12-01)

Thanks for the reward. Please credit me as "Til Jasper Ullrich".
Also, if possible, the money should be donated to http://www.ingenieure-ohne-grenzen.org/

### ti...@google.com (2015-12-14)

I can donate via their US website at http://www.ewb-usa.org/ in your honor. Does that suit? 

If so, we'll match the donation and donate $4,000 total.

### [Deleted User] (2015-12-14)

Hi, that sounds good to me.

### cl...@chromium.org (2016-01-07)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-03-08)

Updating as $4,000 was paid to #33 in Til Jasper Ullrich's honor. Thanks again for the report and the donation!

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/528505?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/517713]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082800)*
