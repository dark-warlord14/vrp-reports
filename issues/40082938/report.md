# Security: PureCall on CPWL_Edit::OnKillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40082938](https://issues.chromium.org/issues/40082938) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-09-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I mentioned this issue on <https://crbug.com/chromium/537173#c18> of 512445. But I feel this may need a separate fix.  

Open test.pdf file in a pdf editor to see javascript code which triggers pureCall. Javascript is available in Document Will Close Action.

**VERSION**  

Chrome Version: [47.0.2521.0] + [ TOT Debug build]  

Operating System: [Windows 10]

**REPRODUCTION CASE**

1. Build chrome debug build.  
   
   ninja -C out\Debug chrome
2. Run chrome debug build
3. Open test.pdf in chrome
4. Attach visual studio debugger to chrome PDF process.
5. Press reload button in chrome.
6. Debugger will fail several times on these asserts.  
   
   FFL\_FormFiller.cpp  
   
   CFFL\_FormFiller::GetPDFWindow -> ASSERT(pPageView);  
   
   CFFL\_FormFiller::GetViewBBox -> ASSERT(pPageView != NULL);  
   
   Press ignore for all of them.
7. The debugger will fail with pureCall debugbreak.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [pdf plugin process]  

Crash State: [stack trace]  

content.dll!`anonymous namespace'::PureCall() Line 29 msvcr120d.dll!6af6a93c() Unknown [Frames below may be incorrect and/or missing, no symbols loaded for msvcr120d.dll] chrome.dll!CPWL_Edit::OnKillFocus() Line 703 chrome.dll!CPWL_MsgControl::KillFocus() Line 157 chrome.dll!CPWL_Wnd::KillFocus() Line 720 chrome.dll!CPWL_Wnd::Destroy() Line 248 chrome.dll!CFFL_FormFiller::~CFFL_FormFiller() Line 30 chrome.dll!CFFL_TextField::~CFFL_TextField() Line 23 chrome.dll!CFFL_TextField::`scalar deleting destructor'(unsigned int)  

chrome.dll!CFFL\_IFormFiller::UnRegisterFormFiller(CPDFSDK\_Annot \* pAnnot) Line 587  

chrome.dll!CFFL\_IFormFiller::OnDelete(CPDFSDK\_Annot \* pAnnot) Line 125  

chrome.dll!CPDFSDK\_AnnotHandler::ReleaseAnnot(CPDFSDK\_Annot \* pAnnot) Line 364  

chrome.dll!CPDFSDK\_AnnotHandlerMgr::ReleaseAnnot(CPDFSDK\_Annot \* pAnnot) Line 69  

chrome.dll!CPDFSDK\_PageView::~CPDFSDK\_PageView() Line 636  

chrome.dll!CPDFSDK\_PageView::`scalar deleting destructor'(unsigned int) chrome.dll!CPDFSDK_Document::~CPDFSDK_Document() Line 410 chrome.dll!CPDFSDK_Document::`scalar deleting destructor'(unsigned int)  

chrome.dll!FPDFDOC\_ExitFormFillEnvironment(void \* hHandle) Line 100  

chrome.dll!chrome\_pdf::PDFiumEngine::~PDFiumEngine() Line 701  

chrome.dll!chrome\_pdf::PDFiumEngine::`scalar deleting destructor'(unsigned int) chrome.dll!base::DefaultDeleter<chrome_pdf::PDFEngine>::operator()(chrome_pdf::PDFEngine \* ptr) Line 128 chrome.dll!base::internal::scoped_ptr_impl<chrome_pdf::PDFEngine,base::DefaultDeleter<chrome_pdf::PDFEngine> >::reset(chrome_pdf::PDFEngine \* p) Line 239 chrome.dll!scoped_ptr<chrome_pdf::PDFEngine,base::DefaultDeleter<chrome_pdf::PDFEngine> >::reset(chrome_pdf::PDFEngine \* p) Line 366 chrome.dll!chrome_pdf::OutOfProcessInstance::~OutOfProcessInstance() Line 299 chrome.dll!chrome_pdf::OutOfProcessInstance::`scalar deleting destructor'(unsigned int)  

chrome.dll!pp::Instance\_DidDestroy(int instance) Line 89

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 1.9 KB)

## Timeline

### es...@chromium.org (2015-09-29)

thestig, do you think you might be able to take a look at this?

### th...@chromium.org (2015-09-29)

Oh, CPDFSDK_AnnotHandler... If anyone wants to grab it from me, please do.

### th...@chromium.org (2015-09-29)

Repro'd. Assigning to myself for now.

### es...@chromium.org (2015-09-30)

Thank you! Does it repro in dev or beta, or just ToT?

### th...@chromium.org (2015-09-30)

I think we just need to check for a NULL pointer to avoid this whole mess.

CPDFSDK_PageView* pPageView = GetCurPageView();
if (!pPageView)
  return TRUE;

### th...@chromium.org (2015-09-30)

I think this bug likely has been there all along based on my reading of FFL_FormFiller.cpp. There used to be more ASSERT()s, but they would not have been helpful in release builds. I didn't actually build an older version to test this.

### th...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-09-30)

Gotcha, thanks thestig.

### cl...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b331e81dd0357eb0c483cfac3e3fe2a594fe54ef

commit b331e81dd0357eb0c483cfac3e3fe2a594fe54ef
Author: thestig <thestig@chromium.org>
Date: Sat Oct 03 12:09:55 2015

Roll PDFium revision to 3dedace and use the new init API.

Also pick up another bug fix in the DEPS roll.
https://pdfium.googlesource.com/pdfium.git/+log/b8a0747..3dedace

BUG=531339,537173

Review URL: https://codereview.chromium.org/1383783003

Cr-Commit-Position: refs/heads/master@{#352254}

[modify] http://crrev.com/b331e81dd0357eb0c483cfac3e3fe2a594fe54ef/DEPS
[modify] http://crrev.com/b331e81dd0357eb0c483cfac3e3fe2a594fe54ef/pdf/pdfium/pdfium_engine.cc


### th...@chromium.org (2015-10-03)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-03)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2015-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2015-10-05)

Merge approved for M46 branch (branch: 2490).

### bu...@chromium.org (2015-10-05)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79226

------------------------------------------------------------------
r79226 | thestig@google.com | 2015-10-05T19:23:53.882027Z

-----------------------------------------------------------------

### th...@chromium.org (2015-10-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-06)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ss...@google.com (2015-10-06)

Merge approved for M47 (branch 2526). 

### bu...@chromium.org (2015-10-07)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79288

------------------------------------------------------------------
r79288 | thestig@google.com | 2015-10-07T00:07:43.199573Z

-----------------------------------------------------------------

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

We took this to the panel today and the panel needs more info from you to determine whether to reward here. Notes below.

Panel Notes: If you can demonstrate/explain that this is more than a null dereference or can cause something to go wrong with a map later on, we'll take this back to the reward panel. 

I'm going to mark this as $0 reward for now, but feel free to update this issue with more details if you can demonstrate a significant security impact here. Thanks!

### cl...@chromium.org (2016-01-09)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-01-20)

Based on https://crbug.com/chromium/572871, let's take this back to the reward panel.


### ti...@google.com (2016-04-22)

Based on the https://crbug.com/chromium/572871, the panel decided to pay $3000 for this report. Congratulations! I'll add this in with your other payment.

### ch...@gmail.com (2016-04-22)

Tim, Thanks a lot for this reward.
I would like to donate this reward ($3000) to Sri Lanka Red Cross.
http://www.redcross.lk/online-donations/
Will you be able to make this donation online to them?


### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-05-13)

I received reward for this bug today. But in https://crbug.com/chromium/537173#c25 I wanted to donate this reward.

### ti...@google.com (2016-05-13)

Hey Chamal,

As mentioned via email, this was a traditional security vuln: Time of check, time of use!

I've presented two options on how to proceed via email (i.e. you donate then we'll match, or you can return the payment and we'll donate).

Feel free to respond via email and we can take it from there.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/537173?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082938)*
