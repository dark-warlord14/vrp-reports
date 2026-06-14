# Security: extensions with downloads.open permission can execute code on the device using .fileloc files

| Field | Value |
|-------|-------|
| **Issue ID** | [40050836](https://issues.chromium.org/issues/40050836) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>Downloads |
| **Platforms** | Mac |
| **Reporter** | vl...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2019-11-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

1. .fileloc files behave on macOS similarly to .url files on Windows - as shortcuts that can execute local apps.
2. A malicious extension with downloads/downloads.open permissions can download a .fileloc file + execute it to launch arbitrary local apps.
3. It looks like a non-secure feature of macOS(that I'm going to report), so it's not clear what'd be your opinion. I guess you'd like to add this file to your file handling mechanism as well.

**VERSION**  

Google Chrome 78.0.3904.108 (Official Build) (64-bit)  

Revision 4b26898a39ee037623a72fcfb77279fce0e7d648-refs/branch-heads/3904@{#889}  

OS macOS Version 10.15.1 (Build 19B88)

**REPRODUCTION CASE**

1. Install the attached extension
2. Click "Download" and "Run" in the popup
3. Notice Terminal.app popups with sudo command being executed

**CREDIT INFORMATION**  

Reporter credit: Vladimir Metnew (twitter.com/vladimir\_metnew)

## Attachments

- [chrome-extension-open-fileloc.zip](attachments/chrome-extension-open-fileloc.zip) (application/octet-stream, 4.1 KB)

## Timeline

### aj...@google.com (2019-12-02)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API UI>Browser>Downloads]

### pa...@chromium.org (2019-12-02)

Hmm, I've got my doubts about `downloads.open` being a good idea. Is it deprecatable? `downloads.show` is less risky but still not risk-free. We could deprecate `open` by just making it a synonym for `show`, perhaps?

Could we do a sweep of the Chrome Web Store and get a feeling for how many extensions are using `downloads.open`, and of those how many seem legit?

Safe Browsing: It seems like we should add .fileloc to ./chrome/browser/resources/safe_browsing/download_file_types.asciipb, too? And any other related formats (on any platform)? (We already have .url for Windows.)

[Monorail components: Services>Safebrowsing]

### pa...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### ac...@chromium.org (2019-12-03)

I can pull up a list of the extensions currently using that permission and evaluate their legitimacy. 

### dr...@chromium.org (2019-12-03)

Agreed - the solution on the Safe Browsing side is to add some platform_settings for fileloc. I'll get started on that.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c2b7b1feda96cb26c638275cf2fb262750a810f3

commit c2b7b1feda96cb26c638275cf2fb262750a810f3
Author: Daniel Rubery <drubery@chromium.org>
Date: Thu Dec 05 20:52:28 2019

Add fileloc and webloc to download_file_types.asciipb

These file types are used on MacOS to open files or websites automatically.
They should be treated similar to .url files on Windows.

Bug: 1029375
Change-Id: I2d7c0c7e722a41b7f4eb62fcc569aaca4cb19700
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1953547
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/master@{#722186}

[modify] https://crrev.com/c2b7b1feda96cb26c638275cf2fb262750a810f3/chrome/browser/resources/safe_browsing/download_file_types.asciipb
[modify] https://crrev.com/c2b7b1feda96cb26c638275cf2fb262750a810f3/components/download/internal/common/download_stats.cc
[modify] https://crrev.com/c2b7b1feda96cb26c638275cf2fb262750a810f3/tools/metrics/histograms/enums.xml


### rd...@chromium.org (2019-12-05)

There are a good number of legit extensions using downloads.open (and some non-legit ones).  The non-legit ones are likely in violation of some of our policies, and we can take them down.

We can do some more analysis of the legit extensions, and see how important it is to them.  Unfortunately, being able to open a download from a download manager *is* pretty useful (just opening it in the file manager isn't as good a UX, especially if most downloads go into a black hole of C:\Users\Alice\Downloads or similar).  My suspicion is that this would be a bit hard to deprecate, though not impossible.

FWIW, we do prevent downloads that are marked as "Dangerous" from being opened automatically by the extension, and it requires user confirmation.  I'm not sure whether adding the fileloc file extension to SB is sufficient to flag them as dangerous - drubery@ or vakh@, do either of you know?

I'm not sure if there's a single best course of action yet here, so unassigning myself for now.

### dr...@chromium.org (2019-12-05)

It should fix the immediate problem. I've made the platform setting DANGEROUS on MacOS, which causes us to show a warning on all fileloc downloads (this is not ideal, but it's the standard solution at the moment). This causes DownloadItem::GetState() not to progress past IN_PROGRESS, and this check to keep the file from being opened:
https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/downloads/downloads_api.cc?rcl=0ffa945796765841debff7e18567ee8cc3bf5146&l=1454

### mm...@chromium.org (2019-12-10)

Assigning to Daniel as per c#6 and c#8.

### dr...@chromium.org (2019-12-10)

There's no further action planned on the Safe Browsing side - is this bug tracking any future action from the extensions team? Otherwise I'll just mark it fixed.

### dr...@chromium.org (2019-12-11)

Marking Fixed. Feel free to take the bug if work is needed.

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $500 for this report

### vl...@gmail.com (2019-12-17)

Honestly, I expected to see a bigger reward for a P1 Severity-Medium issue.

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-20)

Not requesting merge to beta (M80) because latest trunk commit (722186) appears to be prior to beta branch point (722274). If this is incorrect, please replace the Merge-na label with Merge-Request-80. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-01-28)

vladimirmetnew@ thanks for the report.. If it's OK with you I am going to slightly adjust your requested credit information to "Vladimir Metnew (@vladimir_metnew)" to avoid URIs in the release notes.

### vl...@gmail.com (2020-01-28)

Yeah, "Vladimir Metnew (@vladimir_metnew)" seems fine

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-19)

This issue was migrated from crbug.com/chromium/1029375?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, Services>Safebrowsing, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050836)*
