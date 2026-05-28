# Security: Heap-use-after-free in AboutThisSiteSidePanelView::HandleKeyboardEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40064571](https://issues.chromium.org/issues/40064571) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Bubbles>PageInfo |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | fs...@google.com |
| **Created** | 2023-05-15 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at 8c0f80a0a4f2a20b64bee9eacb69583cfa1a5fc9

1. apply change.diff and compile Chromium with ASAN enabled
2. run `./chrome --user-data-dir=/tmp/noexist --enable-features=PageInfoAboutThisSiteNonEn,AboutThisSitePersistentSidePanelEntry`
3. Open two windows `www.google.com` and `about:blank`
4. In `www.google.com`, open SidePanel and choose `About this page`, then move `www.google.com` to the second window
5. In `About this page`, press any key to trigger UAF

**Problem Description:**

1. Analysis

`AboutThisSiteSidePanelView` holds a raw\_ptr to `browser_view_`, which will be freed when the browser window is merged into a new window, causing UAF.

```
AboutThisSiteSidePanelView::AboutThisSiteSidePanelView(  
    BrowserView\* browser_view) {  
  browser_view_ = browser_view;  
  auto\* browser_context = browser_view->GetProfile();  
  
  // Allow view to be focusable in order to receive focus when side panel is  
  // opened.  
  SetFocusBehavior(FocusBehavior::ALWAYS);  
  
  // Align views vertically top to bottom.  
  SetOrientation(views::LayoutOrientation::kVertical);  
  SetMainAxisAlignment(views::LayoutAlignment::kStart);  
  
  // Stretch views to fill horizontal bounds.  
  SetCrossAxisAlignment(views::LayoutAlignment::kStretch);  
  
  loading_indicator_web_view_ =  
      AddChildView(CreateWebView(this, browser_context));  
  loading_indicator_web_view_->GetWebContents()->GetController().LoadURL(  
      GURL(kStaticLoadingScreenURL), content::Referrer(),  
      ui::PAGE_TRANSITION_FROM_API, std::string());  
  web_view_ = AddChildView(CreateWebView(this, browser_context));  
  
  SetContentVisible(false);  
  auto\* web_contents = web_view_->GetWebContents();  
  web_contents->SetDelegate(this);  
  web_contents->SetUserData(  
      kAboutThisSiteWebContentsUserDataKey,  
      std::make_unique<AboutThisSiteWebContentsUserData>(AsWeakPtr()));  
  Observe(web_contents);  
}  

```
```
bool AboutThisSiteSidePanelView::HandleKeyboardEvent(  
    content::WebContents\* source,  
    const content::NativeWebKeyboardEvent& event) {  
  // Redirect keyboard events to the main browser.  
  return outer_delegate()->HandleKeyboardEvent(source, event); // use of freed browser_view_  
}  
  
content::WebContentsDelegate\* AboutThisSiteSidePanelView::outer_delegate() {  
  return browser_view_->browser();  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/page_info/about_this_site_side_panel_view.cc;l=52;drc=5b9af51fdd3d9eef10ac47bd11606bc16c7be570;bpv=1;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/page_info/about_this_site_side_panel_view.cc;l=142;drc=5b9af51fdd3d9eef10ac47bd11606bc16c7be570;bpv=1;bpt=0>

2. Bisect

I think this problem is introduced when raw\_ptr `browser_view_` was introduced.  

According to the commit history, this problem is introduced in this commit: 7fdeb619de173a03846da4e738ecc6ec1e156acd  

<https://chromium-review.googlesource.com/c/chromium/src/+/3791041>

3. Suggested Patch

Use a WeakPtr rather than a raw\_ptr to ensure the lifetime of `browser_view_`

**Additional Comments:**  

change.diff is used to show the `About this page`.

\*\*Chrome version: \*\* 108 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 34.4 KB)
- [video.webm](attachments/video.webm) (video/webm, 982.4 KB)
- [change.diff](attachments/change.diff) (text/plain, 1.4 KB)

## Timeline

### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-05-17)

ping


### ke...@chromium.org (2023-05-17)

Thanks for the report.

I'm not able to repro because I can't manage to get the About This Site to appear, even after applying change.diff.

dullweber@: Can you confirm this, so I can set severity?

It likely makes sense to use a WeakPtr instead of the raw_ptr, regardless.

[Monorail components: UI>Browser>Bubbles>PageInfo]

### me...@gmail.com (2023-05-25)

ping

### du...@google.com (2023-05-25)

+olesia and filipa. Could one of you look into this while I'm out?

### fs...@google.com (2023-05-26)

Hey everyone! 

ATP might not show up for you without the change.diff because you need to have MSBB enabled for ATP to be available.  
I am able to reproduce the issue. I also think it makes sense to use WeakPtr instead of the raw pointer in ATSPanelView[1]. 

Also lens might have the same problem[2].

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/page_info/about_this_site_side_panel_view.cc;l=52;drc=5b9af51fdd3d9eef10ac47bd11606bc16c7be570
[2] https://crsrc.org/c/chrome/browser/ui/views/side_panel/lens/lens_unified_side_panel_view.cc;l=265

### fs...@google.com (2023-05-26)

There is also the same problem if you click or right click and click open in new tab on any of the links in the ATP side panel.

Steps to reproduce 2 scenarios:

Scenario 1:
1. Turn on MSBB in settings/syncSetup
2. Open two windows one with `www.google.com` and another with `about:blank`
3. In `www.google.com`, open SidePanel and choose `About this page`, then move `www.google.com` to the second window
4. Click on the side panel, press any key to trigger UAF OR click on any link OR right click and then `Open in new Tab` on any link
5. Observe the browser crashing

Scenario 2:
1. Turn on MSBB in settings/syncSetup
2. Open two windows one with `www.google.com` and `gmail.com` and another with `about:blank`
3. In `www.google.com`, open SidePanel and choose `About this page`, then move `www.google.com` to the second window with `about:blank`
4. On the side panel, click on any link OR right click and then `Open in new Tab` on any link
5. Observe that the links are open in a new tab in the window with `gmail.com` and not in the same window as the side panel

### fs...@google.com (2023-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0998075d2d9d44904b493c034c050a7e75720c1a

commit 0998075d2d9d44904b493c034c050a7e75720c1a
Author: Filipa Senra <fsenra@google.com>
Date: Wed May 31 13:02:05 2023

[AboutThisSite] Fix heap use after free & links opening on wrong window

The ATS was using BrowserView to deal with the events of the
ATSSidePanel WebContents, i.e. it redirects to the browser clicks on
links and mouse events on the SidePanel's diner webpage. However, the
BrowserView associated with a tab can change if a tab is moved to
another window.

In this CL, we make ATSSidePanel depend directly on the tab's
WebContents instead of the BrowserView associated with the tab's
WebContents at the creation moment of the ATSSidePanel. The tab's web
contents will remain the same for the lifetime of the ATSSidePanelView
and we can fetch the correct BrowserView when an event related to the
side panel's WebContents occurs.

Fixed: 1445492
Change-Id: I46bb21d434a339436bb03e1da3974155192f900e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4568268
Reviewed-by: Christian Dullweber <dullweber@chromium.org>
Commit-Queue: Filipa Senra <fsenra@google.com>
Cr-Commit-Position: refs/heads/main@{#1151185}

[modify] https://crrev.com/0998075d2d9d44904b493c034c050a7e75720c1a/chrome/browser/ui/views/page_info/about_this_site_side_panel_view.cc
[modify] https://crrev.com/0998075d2d9d44904b493c034c050a7e75720c1a/chrome/browser/ui/views/page_info/about_this_site_side_panel_coordinator.cc
[modify] https://crrev.com/0998075d2d9d44904b493c034c050a7e75720c1a/chrome/browser/ui/views/page_info/about_this_site_side_panel_view.h


### [Deleted User] (2023-05-31)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-06-02)

Triageing as high since this is memory corruption in the browser process but requires significant user interaction to trigger.

### ca...@chromium.org (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, Krace! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hi Krace, another kind reminder we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1445492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064571)*
