# Security: Mixed content state reset when navigating back

| Field | Value |
|-------|-------|
| **Issue ID** | [40094866](https://issues.chromium.org/issues/40094866) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>PageSecurityState |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2019-05-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When a https site includes a http asset (e.g. an image) or targets a http site with a form, the lock icon shown in the omnibox will change to indicate that the site is including mixed content.

However, if a site uses history.pushState(), adds mixed content and then calls history.back(), the site security icon will change back to a lock icon and will indicate that the connection is secure. This is true even though the page won't have reloaded and will still contain mixed content.

**VERSION**  

Chrome Version: Tested on 74.0.3729.131 (stable) and 76.0.3785.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The demo here requires a https page. Therefore, I've set up the following page:

<https://derceg.gitlab.io/mixed_content_state_reset/>

As a first step, you'll need to open this page. I've attached the source for the page to this issue, which will allow you to test it locally, if necessary.

2. When loaded, the page will make the following call to add a history entry for the current page:

history.pushState({}, "");

3. After this has been done, JavaScript will add a form to the page that targets a http site. This is done using the following sequence of calls:

var form = document.createElement("form");  

form.action = "<http://example.com/>";  

document.body.appendChild(form);

Note that once this form has been added to the page, the security lock icon will change to indicate that the site is including mixed content.

4. After 5 seconds the site will go back using:

history.back();

This will navigate the page back to its original location, though the page won't be reloaded. The form added in step 3 will still be present (which you can verify through the devtools), though the security icon will have changed back to a lock. Clicking that icon will indicate that the connection is secure.

Aside from adding forms that target http sites, you can also include http images and then navigate back in the same way as above.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 136 B)
- [main.js](attachments/main.js) (text/plain, 289 B)

## Timeline

### ad...@google.com (2019-05-05)

Thanks for the report! I can reproduce this as described. Setting the severity to low per precedent for other situations where we've shown this wrongly.

carlosil@, over to you!

[Monorail components: Internals>PageSecurityState]

### sh...@chromium.org (2019-05-05)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-12-19)

Taking this one as part of our security UI fix-it.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/acfe65341eeedf10c09f2e98d75c760c085cbd99

commit acfe65341eeedf10c09f2e98d75c760c085cbd99
Author: Emily Stark <estark@google.com>
Date: Fri Dec 20 01:35:29 2019

Carry over SSL content status flags for same-doc navigations

Same-document navigations shouldn't clear content status flags,
because if there was mixed content on the page, it's still there after
a same-document navigation.

In many same-document navigation cases, this fix doesn't matter
because content status flags are copied as part of cloning the
original NavigationEntry to create the new one (see the
NavigationEntry::CloneAndReplace call in
NavigationControllerImpl::RendererDidNavigateToNewPage). However, not
all same-document navigations involve cloning an existing entry, and
in these cases it is important to copy over the previous entry's
content status flags. (See linked bug for an example.)

Bug: 959571
Change-Id: I353995ea153b10736020e24f29eca6f7e7be9ed9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1977395
Commit-Queue: Emily Stark <estark@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#726633}

[modify] https://crrev.com/acfe65341eeedf10c09f2e98d75c760c085cbd99/chrome/browser/ssl/ssl_browsertest.cc
[modify] https://crrev.com/acfe65341eeedf10c09f2e98d75c760c085cbd99/content/browser/ssl/ssl_manager.cc


### es...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/959571?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094866)*
