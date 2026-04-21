# Security: container-overflow in chrome_pdf::PDFiumEngine::SelectFindResult

| Field | Value |
|-------|-------|
| **Issue ID** | [40060084](https://issues.chromium.org/issues/40060084) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sk...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-06-27 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

pdf/pdfium/pdfium\_engine.cc

```
gfx::Size PDFiumEngine::ApplyDocumentLayout(  
    const DocumentLayout::Options& options) {  
      
  // ...  
    
  UpdateDocumentLayout(&layout_);  
  if (!layout_.dirty())  
    return layout_.size();  
  
  // Store the current find index so that we can resume finding at that  
  // particular index after we have recomputed the find results.  
  std::string current_find_text = current_find_text_;  
  resume_find_index_ = current_find_index_; // [1]  
  
  // Save the current page.  
  int most_visible_page = most_visible_page_;  
  
  InvalidateAllPages(); // [2]  
  
  // Restore find results.  
  if (!current_find_text.empty()) {  
    // Clear the UI.  
    client_->NotifyNumberOfFindResultsChanged(0, false);  
    StartFind(current_find_text, false); // [3]  
  }  
    
  // ...  
    
}  

```
```
void PDFiumEngine::SearchUsingICU(const std::u16string& term,  
                                  bool case_sensitive,  
                                  bool first_search,  
                                  int character_to_start_searching_from,  
                                  int current_page) {  
  // ...  
    
  std::vector<PDFEngine::Client::SearchStringResult> results =  
      client_->SearchString(adjusted_page_text.c_str(), adjusted_term.c_str(),  
                            case_sensitive);  
  for (const auto& result : results) {  
    
    // ...  
      
    AddFindResult(PDFiumRange(pages_[current_page].get(), start, end - start)); // [4]  
  }  
}  

```
```
void PDFiumEngine::AddFindResult(const PDFiumRange& result) {  
  bool first_result = find_results_.empty();  
    
  // ...  
    
  find_results_.insert(find_results_.begin() + result_index, result);  
    
  // ...  
    
  if (first_result) {  
    DCHECK(!resume_find_index_);  
    DCHECK(!current_find_index_);  
    SelectFindResult(/\*forward=\*/true); // [5]  
  }  
}  

```
```
bool PDFiumEngine::SelectFindResult(bool forward) {  
  
  // ...  
    
  // Move back/forward through the search locations we previously found.  
  size_t new_index;  
  const size_t last_index = find_results_.size() - 1;  
  
  if (resume_find_index_) {  
    new_index = resume_find_index_.value(); // [6]  
    resume_find_index_.reset();  
  } else if (current_find_index_) {  
  
    // ...  
  
  } else {  
      
    // ...  
      
  }  
  current_find_index_ = new_index; [7]  
  
  // Update the selection before telling the client to scroll, since it could  
  // paint then.  
  selection_.clear();  
  selection_.push_back(find_results_[current_find_index_.value()]); // [8]  
  
  // ...  
  
}  

```

`PDFiumEngine:ApplyDocumentLayout()` stores `current_find_index_` to `resume_find_index_` [1], then clears `find_results_` vector via `PDFiumEngine::InvalidateAllPages()` [2], and it finally calls `PDFiumEngine::StartFind()`[3] to restore `find_results_` vector.

`PDFiumEngine::StartFind()` uses `PDFiumEngine::SearchUsingICU()` to search text. In `PDFiumEngine::SearchUsingICU()`, the search result is added to `find_results_` [4] vector via `AddFindResult()` one by one.

While the first result is added to `find_results_`, `PDFiumEngine::AddFindResult()` uses `PDFiumEngine::SelectFindResult()` [5] to select result. However, since `resume_find_index_` has been set, `current_find_index_` will be assigned to `resume_find_index_` [6][7], and `find_results_[current_find_index_.value()]` will be pushed into `selection_` vector [8]. `find_results_` has only one item at the moment. if `current_find_index_` >= 1, an out-of-bounds read will occur.

**VERSION**  

Chrome Version: Version 105.0.5131.1 (Developer Build) (64-bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

This bug can be triggered manually

1. Open provided a.pdf in Chrome PDF Viewer
2. Find 'a' in PDF page, select index other than 1
3. Rotate PDF (or use two page view)

AFAIK, step 1. and 2. can be achieved with `chrome.webviewTag.find`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State: see asan.log

**CREDIT INFORMATION**  

Reporter credit:  

YU-CHANG CHEN and CHIH-YEN CHANG, working with DEVCORE Internship Program

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 17.2 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.2 MB)
- [a.pdf](attachments/a.pdf) (application/pdf, 8.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 14.2 KB)

## Timeline

### [Deleted User] (2022-06-27)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-27)

In my recentish asan build I'm hitting a breakpoint:

==29708==ERROR: AddressSanitizer: breakpoint on unknown address 0x7ffdbfaa6a44 (pc 0x7ffdbfaa6a44 bp 0x0099ccdfc680 sp 0x0099ccdfc600 T0)
==29708==*** WARNING: Failed to initialize DbgHelp!              ***
==29708==*** Most likely this means that the app is already      ***
==29708==*** using DbgHelp, possibly with incompatible flags.    ***
==29708==*** Due to technical reasons, symbolization might crash ***
==29708==*** or produce wrong results.                           ***
[38672:49424:0627/094357.020:FATAL:pdfium_engine.cc(1990)] Check failed: !resume_find_index_.
Backtrace:
        base::debug::CollectStackTrace [0x00007FFDBFCDC8B2+18] (D:\chromium\src\base\debug\stack_trace_win.cc:305)
        base::debug::StackTrace::StackTrace [0x00007FFDBFA4B44A+26] (D:\chromium\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFDBFAA5846+774] (D:\chromium\src\base\logging.cc:648)
        logging::LogMessage::~LogMessage [0x00007FFDBFAA9020+16] (D:\chromium\src\base\logging.cc:641)
        chrome_pdf::PDFiumEngine::AddFindResult [0x00007FFDBE80348A+1904] (D:\chromium\src\pdf\pdfium\pdfium_engine.cc:1990)
        chrome_pdf::PDFiumEngine::SearchUsingICU [0x00007FFDBE8022F5+7527] (D:\chromium\src\pdf\pdfium\pdfium_engine.cc:1968)
        chrome_pdf::PDFiumEngine::StartFind [0x00007FFDBE7FF7E2+2874] (D:\chromium\src\pdf\pdfium\pdfium_engine.cc:1774)
        chrome_pdf::PDFiumEngine::ApplyDocumentLayout [0x00007FFDBE82068B+941] (D:\chromium\src\pdf\pdfium\pdfium_engine.cc:3762)
        chrome_pdf::PdfViewWebPlugin::HandleViewportMessage [0x00007FFDCB682EC4+708] (D:\chromium\src\pdf\pdf_view_web_plugin.cc:1129)
        chrome_pdf::PdfViewWebPlugin::OnMessage [0x00007FFDCB680800+310] (D:\chromium\src\pdf\pdf_view_web_plugin.cc:1017)
        base::TaskAnnotator::RunTaskImpl [0x00007FFDBFC08713+1011] (D:\chromium\src\base\task\common\task_annotator.cc:135)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFDC330574F+3935] (D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:409)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFDC3303B33+483] (D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:287)
        base::MessagePumpDefault::Run [0x00007FFDC32D14BA+490] (D:\chromium\src\base\message_loop\message_pump_default.cc:39)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFDC33081DB+1947] (D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:554)
        base::RunLoop::Run [0x00007FFDBFB67CC2+1826] (D:\chromium\src\base\run_loop.cc:143)
        content::RendererMain [0x00007FFDC2C9FB79+2761] (D:\chromium\src\content\renderer\renderer_main.cc:290)
        content::RunOtherNamedProcessTypeMain [0x00007FFDBF6466FF+1828] (D:\chromium\src\content\app\content_main_runner_impl.cc:720)
        content::ContentMainRunnerImpl::Run [0x00007FFDBF648C14+2094] (D:\chromium\src\content\app\content_main_runner_impl.cc:1061)
        content::RunContentProcess [0x00007FFDBF64497A+3677] (D:\chromium\src\content\app\content_main.cc:407)
        content::ContentMain [0x00007FFDBF645113+407] (D:\chromium\src\content\app\content_main.cc:435)
        ChromeMain [0x00007FFDB14914BE+954] (D:\chromium\src\chrome\app\chrome_main.cc:182)
        MainDllLoader::Launch [0x00007FF687087704+2324] (D:\chromium\src\chrome\app\main_dll_loader_win.cc:162)
        main [0x00007FF68708320D+8607] (D:\chromium\src\chrome\app\chrome_exe_main_win.cc:395)
        __scrt_common_main_seh [0x00007FF68759EBC4+268] (d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FFE5BAB7034+20]
        RtlUserThreadStart [0x00007FFE5BC62651+33]
Task trace:
Backtrace:
        chrome_pdf::PostMessageReceiver::PostMessageW [0x00007FFDCF6B990B+939] (D:\chromium\src\pdf\post_message_receiver.cc:131)
        mojo::SimpleWatcher::Context::Notify [0x00007FFDBFFE4172+856] (D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102)

Do you have a particular commit you've tested with?

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2022-06-27)

re: https://crbug.com/chromium/1339745#c2 - Maybe turn off DCHECKs and see what happens next?

### sk...@gmail.com (2022-06-27)

I tested it on commit 5652d6587f1637b3ca8d13459bb299b589b52f31with following build arguments

args.gn:
```
dcheck_always_on = false
is_asan = true
is_component_build = true
is_debug = false
symbol_level = 2
v8_enable_object_print = true
```

### [Deleted User] (2022-06-27)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-06-27)

Good thought

with dcheck_always_off on get a renderer crash.

Steps:

run chrome asan --no-sandbox (for stack trace)
open a.pdf
ctrl-f find 'a'
click to next 'a'
click on dots
select two page view
boom!

Medium - as this needs some interaction.

thestig - could you take a look or assign to someone.

### [Deleted User] (2022-06-27)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-27)

This may be the same issue as https://crbug.com/chromium/1108574 and https://crbug.com/chromium/1279497. We've seen on the crash report, but not the repro steps.

### [Deleted User] (2022-06-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb259a8225ee562a656a40ba62a00a37fdc24300

commit cb259a8225ee562a656a40ba62a00a37fdc24300
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Jul 06 21:48:33 2022

Better define "first result" in PDFiumEngine::AddFindResult().

Currently, changing the PDF layout confuses AddFindResult() and causes
it to fail a DCHECK(). Add a unit test to trigger this scenario, and
adjust AddFindResult() to avoid the failing DCHECK().

Bug: 1339745
Change-Id: Ia75d7844a4ba05a848962c31979ae0ce215f0a08
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736501
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021389}

[modify] https://crrev.com/cb259a8225ee562a656a40ba62a00a37fdc24300/pdf/pdfium/findtext_unittest.cc
[modify] https://crrev.com/cb259a8225ee562a656a40ba62a00a37fdc24300/pdf/pdfium/pdfium_engine.cc


### th...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

Requesting merge to beta M104 because latest trunk commit (1021389) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-07)

Merge review required: M104 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-07-07)

If we merge, we can merge the pdf/pdfium/pdfium_engine.cc portion, but not the pdf/pdfium/findtext_unittest.cc portion, as the tests is built on top of other CLs.

### am...@chromium.org (2022-07-08)

Thanks thestig@ - merge approved to M104, please go ahead and merge the DCHECK fix portion to M104 (branch 5112) at your earliest convenience. Not only can this fix be included in next beta, but can also ship in M104 Stable when that promotion occurs. Thank you! 

### th...@chromium.org (2022-07-09)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-09)

BTW, it looks like we've known about the DCHECK() failure for a while, as seen in https://crbug.com/chromium/1014203.

### [Deleted User] (2022-07-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-07-12)

Thanks sheriffbot. Will merge today.

### sr...@google.com (2022-07-12)

This CL is approved for Merge to M104, Please help complete all merges before 3pm PST today ( July 12) so that these can be included in this week's beta release going out tomorrow,. I will be cutting RC build today at 3pm PST

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/60d8559e150a6bc99704967c06c68c2d0926cd5a

commit 60d8559e150a6bc99704967c06c68c2d0926cd5a
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jul 12 18:52:14 2022

M104: Better define "first result" in PDFiumEngine::AddFindResult().

Currently, changing the PDF layout confuses AddFindResult() and causes
it to fail a DCHECK(). Adjust AddFindResult() to avoid the failing
DCHECK().

This is a cherry-pick of https://crrev.com/1021389 without the test
changes.

Bug: 1339745
Change-Id: I25c2b6b436700f9aeca4924fef662ad2909f0a8c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758626
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#820}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/60d8559e150a6bc99704967c06c68c2d0926cd5a/pdf/pdfium/pdfium_engine.cc


### [Deleted User] (2022-07-12)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-15)

rzanoni@: Straight-froward cherrypicking to M96 and M102 won't work.

### th...@chromium.org (2022-07-18)

To clarify https://crbug.com/chromium/1339745#c28, r1021389 builds on to of a CL chain involving r1021371, r1021347, and r1020156.

### rz...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-26)

1. https://crrev.com/c/3762672
2. Medium, I had issues with the added test, and cherry-picking the CL chain mentioned by thestig@ causes build issues. Ended up removing the test added on the original CL and keeping only the fix.
3. Merged to main in Jul 06
4. Yes

### gm...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations, Yu-Chang Chen and Chih-Yen Chang! The VRP Panel has decided to award you $2,000 for this report. The reward amount was decided upon based on this issue resulting in memory corruption in the renderer process and being mitigated by not being remote exploitable and requiring user interaction. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us -- nice work! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. https://crrev.com/c/3765224
2. Medium, I had issues with the added test, and cherry-picking the CL chain mentioned by thestig@ causes build issues. Ended up removing the test added on the original CL and keeping only the fix.
3. Merged to main in Jul 06
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a2b63640282757dbcc57e65708f38ffea0455b8c

commit a2b63640282757dbcc57e65708f38ffea0455b8c
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Aug 12 14:36:43 2022

[M102-LTS] Better define "first result" in PDFiumEngine::AddFindResult().

M102 merge issues:
  The added test has expectations that doesn't correspond to the current
  state, other CLs would be needed (https://crbug.com/1339745#c29) but
  they cause build issues. Kept the fix and a few test changes, but
  skipped the new test.

Currently, changing the PDF layout confuses AddFindResult() and causes
it to fail a DCHECK(). Add a unit test to trigger this scenario, and
adjust AddFindResult() to avoid the failing DCHECK().

(cherry picked from commit cb259a8225ee562a656a40ba62a00a37fdc24300)

Bug: 1339745
Change-Id: Ia75d7844a4ba05a848962c31979ae0ce215f0a08
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736501
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1021389}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3765224
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1298}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/a2b63640282757dbcc57e65708f38ffea0455b8c/pdf/pdfium/findtext_unittest.cc
[modify] https://crrev.com/a2b63640282757dbcc57e65708f38ffea0455b8c/pdf/pdfium/pdfium_engine.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b9ea6536a4206157793a0f4e62b77ff3fdd0d18

commit 6b9ea6536a4206157793a0f4e62b77ff3fdd0d18
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Aug 12 16:06:03 2022

[M96-LTS] Better define "first result" in PDFiumEngine::AddFindResult().

M96 merge issues:
  The added test has expectations that doesn't correspond to the current
  state, other CLs would be needed (https://crbug.com/1339745#c29) but
  they cause build issues. Kept the fix and a few test changes, but
  skipped the new test.

Currently, changing the PDF layout confuses AddFindResult() and causes
it to fail a DCHECK(). Add a unit test to trigger this scenario, and
adjust AddFindResult() to avoid the failing DCHECK().

(cherry picked from commit cb259a8225ee562a656a40ba62a00a37fdc24300)

Bug: 1339745
Change-Id: Ia75d7844a4ba05a848962c31979ae0ce215f0a08
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736501
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1021389}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3762672
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1681}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6b9ea6536a4206157793a0f4e62b77ff3fdd0d18/pdf/pdfium/findtext_unittest.cc
[modify] https://crrev.com/6b9ea6536a4206157793a0f4e62b77ff3fdd0d18/pdf/pdfium/pdfium_engine.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1339745?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1108574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060084)*
