# Security: stack-buffer-overflow in crashpad 

| Field | Value |
|-------|-------|
| **Issue ID** | [40062893](https://issues.chromium.org/issues/40062893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>CrashReporting |
| **Platforms** | Windows |
| **Reporter** | su...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2023-02-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

In Windows, the renderer process automatically collects process context information after a crash and sends it to the crashpad process for processing. If an attacker takes control of the renderer process, he can simulate a crash and send faked context information.

At [third\_party/crashpad/crashpad/snapshot/win/exception\_snapshot\_win.cc;l=265](https://source.chromium.org/chromium/chromium/src/+/main:third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc;l=265;drc=b8524150039182faf7988e9478a9eff89728ac03)

```
template <class ExceptionRecordType,  
          class ExceptionPointersType,  
          class ContextType>  
bool ExceptionSnapshotWin::InitializeFromExceptionPointers(  
    ProcessReaderWin\* process_reader,  
    WinVMAddress exception_pointers_address,  
    DWORD exception_thread_id,  
    void (\*native_to_cpu_context)(const ContextType\* context_record,  
                                  CPUContext\* context,  
                                  CPUContextUnion\* context_union)) {  
  ExceptionPointersType exception_pointers;  
  if (!process_reader->Memory()->Read(exception_pointers_address,  
                                      sizeof(exception_pointers),  
                                      &exception_pointers)) {  
    LOG(ERROR) << "EXCEPTION_POINTERS read failed";  
    return false;  
  }  
  if (!exception_pointers.ExceptionRecord) {  
    LOG(ERROR) << "null ExceptionRecord";  
    return false;  
  }  
  
  ExceptionRecordType first_record;  
  if (!process_reader->Memory()->Read(  
          static_cast<WinVMAddress>(exception_pointers.ExceptionRecord),  
          sizeof(first_record),  
          &first_record)) {  
    LOG(ERROR) << "ExceptionRecord";  
    return false;  
  }  
  
  const bool triggered_by_client =  
      first_record.ExceptionCode == ExceptionCodes::kTriggeredExceptionCode &&  
      first_record.NumberParameters == 2;  
  if (triggered_by_client)  
    process_reader->DecrementThreadSuspendCounts(exception_thread_id);  
  
  if (triggered_by_client && first_record.ExceptionInformation[0] != 0) {  
    ...  
  } else {  
    // Normal case.  
    exception_code_ = first_record.ExceptionCode;  
    exception_flags_ = first_record.ExceptionFlags;  
    exception_address_ = first_record.ExceptionAddress;  
    for (DWORD i = 0; i < first_record.NumberParameters; ++i)   // [1]  
      codes_.push_back(first_record.ExceptionInformation[i]);    
    ...  
  }  
  
  return true;  
}  

```

[1] There is no check of `first_record.NumberParameters` here, and since it can be controlled by an attacker, there is an overflow vulnerability here.

**VERSION**  

Chrome Version: 109.0.5414.120 stable  

Operating System: Windows

**REPRODUCTION CASE**

1. apply the patch

```
diff --git a/third_party/blink/renderer/core/frame/local_dom_window.cc b/third_party/blink/renderer/core/frame/local_dom_window.cc  
index 35a36f2181316..df9335d6da3ca 100644  
--- a/third_party/blink/renderer/core/frame/local_dom_window.cc  
+++ b/third_party/blink/renderer/core/frame/local_dom_window.cc  
@@ -24,6 +24,7 @@  
  \* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
  \*/  
  
+#include "base/debug/dump_without_crashing.h"  
 #include "third_party/blink/renderer/core/frame/local_dom_window.h"  
  
 #include <memory>  
@@ -1325,6 +1326,7 @@ void LocalDOMWindow::stop() {  
 }  
  
 void LocalDOMWindow::alert(ScriptState\* script_state, const String& message) {  
+  base::debug::DumpWithoutCrashing();  
   if (!GetFrame())  
     return;  
  
diff --git a/third_party/crashpad/crashpad/client/crashpad_client_win.cc b/third_party/crashpad/crashpad/client/crashpad_client_win.cc  
index c6c170396f7de..16e5954f71e36 100644  
--- a/third_party/crashpad/crashpad/client/crashpad_client_win.cc  
+++ b/third_party/crashpad/crashpad/client/crashpad_client_win.cc  
@@ -821,6 +821,7 @@ void CrashpadClient::DumpWithoutCrash(const CONTEXT& context) {  
   EXCEPTION_RECORD record = {};  
   record.ExceptionCode = kSimulatedExceptionCode;  
   record.ExceptionAddress = ProgramCounterFromCONTEXT(&context);  
+  record.NumberParameters = 0xffff;  
  
   exception_pointers.ExceptionRecord = &record;  

```

2. compile chromium with asan
3. launch chrome.exe and execute `window.alert()`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: crashpad  

Crash State:

=================================================================  

==11204==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x009d6cdfd438 at pc 0x7ff73aecd795 bp 0x009d6cdfcf80 sp 0x009d6cdfcfc8  

READ of size 8 at 0x009d6cdfd438 thread T-1  

#0 0x7ff73aecd794 in std::Cr::construct\_at ....\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:36  

#1 0x7ff73aecd794 in std::Cr::allocator\_traits<std::Cr::allocator<unsigned long long> >::construct ....\buildtools\third\_party\libc++\trunk\include\_\_memory\allocator\_traits.h:297  

#2 0x7ff73aecd794 in std::Cr::vector<unsigned \_\_int64, class std::Cr::allocator<unsigned \_\_int64>>::\_\_construct\_one\_at\_end<unsigned \_\_int64>(unsigned \_\_int64 &&) ....\buildtools\third\_party\libc++\trunk\include\vector:794:3  

#3 0x7ff73b26fc3f in std::Cr::vector<unsigned long long,std::Cr::allocator<unsigned long long> >::push\_back ....\buildtools\third\_party\libc++\trunk\include\vector:1509  

#4 0x7ff73b26fc3f in crashpad::internal::ExceptionSnapshotWin::InitializeFromExceptionPointers<struct \_EXCEPTION\_RECORD64, struct crashpad::process\_types::EXCEPTION\_POINTERS<struct crashpad::process\_types::internal::Traits64>, struct \_CONTEXT>(class crashpad::ProcessReaderWin \*, unsigned \_\_int64, unsigned long, void (\_\_cdecl \*)(struct \_CONTEXT const \*, struct crashpad::CPUContext \*, union crashpad::internal::CPUContextUnion \*)) ....\third\_party\crashpad\crashpad\snapshot\win\exception\_snapshot\_win.cc:265:14  

#5 0x7ff73b26f28c in crashpad::internal::ExceptionSnapshotWin::Initialize(class crashpad::ProcessReaderWin \*, unsigned long, unsigned \_\_int64, unsigned int \*) ....\third\_party\crashpad\crashpad\snapshot\win\exception\_snapshot\_win.cc:123:10  

#6 0x7ff73b22019a in crashpad::ProcessSnapshotWin::Initialize(void \*, enum crashpad::ProcessSuspensionState, unsigned \_\_int64, unsigned \_\_int64) ....\third\_party\crashpad\crashpad\snapshot\win\process\_snapshot\_win.cc:95:22  

#7 0x7ff73b1bfbcd in crashpad::CrashReportExceptionHandler::ExceptionHandlerServerException(void \*, unsigned \_\_int64, unsigned \_\_int64) ....\third\_party\crashpad\crashpad\handler\win\crash\_report\_exception\_handler.cc:61:25  

#8 0x7ff73b1c7913 in crashpad::ExceptionHandlerServer::OnNonCrashDumpEvent(void \*, unsigned char) ....\third\_party\crashpad\crashpad\util\win\exception\_handler\_server.cc:559:23  

#9 0x7ff85f30857a (C:\Windows\SYSTEM32\ntdll.dll+0x18007857a)  

#10 0x7ff85f2a0ebb (C:\Windows\SYSTEM32\ntdll.dll+0x180010ebb)  

#11 0x7ff85f2e2f25 (C:\Windows\SYSTEM32\ntdll.dll+0x180052f25)  

#12 0x7ff85de07033 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#13 0x7ff85f2e2650 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)  

Address 0x009d6cdfd438 is a wild pointer inside of access range of size 0x000000000008.  

SUMMARY: AddressSanitizer: stack-buffer-overflow ....\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:36 in std::Cr::construct\_at  

Shadow bytes around the buggy address:  

0x009d6cdfd180: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f2 f2 f2 f2 f2  

0x009d6cdfd200: f2 f2 f2 f2 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x009d6cdfd280: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x009d6cdfd300: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f2 f2 f2 f2 f2  

0x009d6cdfd380: f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x009d6cdfd400: 00 00 00 00 00 00 00[f2]f2 f2 f2 f2 f2 f2 f2 f2  

0x009d6cdfd480: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x009d6cdfd500: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x009d6cdfd580: f8 f8 f8 f8 f8 f8 f8 f2 f2 f2 f2 f2 f2 f2 f2 f2  

0x009d6cdfd600: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x009d6cdfd680: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==11204==ABORTING

**CREDIT INFORMATION**

sunburst of Ant Group Tianqiong Security Lab

## Timeline

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-07)

Hi & thanks for the detailed bug report!

My Windows machine is misbehaving at the moment, so I can't reproduce this.  However, based on that ASAN stacktrace + the steps in the writeup, I do think I see the vuln here and we can go ahead and triage this.

jdh@, I'm assigning this to you somewhat arbitrarily, as I actually don't know who works on crash reporting, and you had the most recently-merged relevant-ish-looking commit I could find :)  Please reassign if you're not the right person for this.

Thanks to you both for helping to keep Chrome secure!

[Monorail components: Internals>CrashReporting]

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2023-02-17)

I provide a patch here, it works fine:

diff --git a/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc b/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
index 2a70c5c0cea23..dcfeb5ad4d7ba 100644
--- a/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
+++ b/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
@@ -261,7 +261,8 @@ bool ExceptionSnapshotWin::InitializeFromExceptionPointers(
     exception_code_ = first_record.ExceptionCode;
     exception_flags_ = first_record.ExceptionFlags;
     exception_address_ = first_record.ExceptionAddress;
-    for (DWORD i = 0; i < first_record.NumberParameters; ++i)
+    DWORD number_parameters = std::min<DWORD>(first_record.NumberParameters, EXCEPTION_MAXIMUM_PARAMETERS);
+    for (DWORD i = 0; i < number_parameters; ++i)
       codes_.push_back(first_record.ExceptionInformation[i]);
     if (first_record.ExceptionRecord) {
       // https://crashpad.chromium.org/bug/43

### [Deleted User] (2023-02-17)

jdh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2023-02-21)

Reassigning to rsesek@ since they are one of the //third_party/crashpad owners and I don't work on crash-reporting.

### rs...@chromium.org (2023-02-22)

Thanks for the report. Bumping to Sev-High because this is a buffer overflow in a privileged process.

### gi...@appspot.gserviceaccount.com (2023-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/crashpad/crashpad/+/3e8727238bae3c069bd71cfb3b2bbaa98b55f05b

commit 3e8727238bae3c069bd71cfb3b2bbaa98b55f05b
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Feb 22 23:37:10 2023

win: Only process up to EXCEPTION_MAXIMUM_PARAMETERS in an EXCEPTION_RECORD

The EXCEPTION_RECORD contains a NumberParameters field, which could
store a value that exceeds the amount of space allocated for the
ExceptionInformation array.

Bug: chromium:1412658
Change-Id: Ibfed8eb6317e28d3addf9215cda7fffc32e1030d
Reviewed-on: https://chromium-review.googlesource.com/c/crashpad/crashpad/+/4284559
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>

[modify] https://crrev.com/3e8727238bae3c069bd71cfb3b2bbaa98b55f05b/snapshot/win/exception_snapshot_win_test.cc
[modify] https://crrev.com/3e8727238bae3c069bd71cfb3b2bbaa98b55f05b/snapshot/win/exception_snapshot_win.cc


### gi...@appspot.gserviceaccount.com (2023-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d05bea76b7ce72d66507ebbe00caf5e45afd587a

commit d05bea76b7ce72d66507ebbe00caf5e45afd587a
Author: Robert Sesek <rsesek@chromium.org>
Date: Thu Feb 23 01:48:48 2023

Update Crashpad to 3e8727238bae3c069bd71cfb3b2bbaa98b55f05b

3e8727238bae win: Only process up to EXCEPTION_MAXIMUM_PARAMETERS in an
             EXCEPTION_RECORD

Fixed: 1412658
Change-Id: I7461602d1a18d44ea1a11ac19f1487fbdb92acf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4285061
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Alex Gough <ajgo@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1108722}

[modify] https://crrev.com/d05bea76b7ce72d66507ebbe00caf5e45afd587a/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
[modify] https://crrev.com/d05bea76b7ce72d66507ebbe00caf5e45afd587a/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win_test.cc
[modify] https://crrev.com/d05bea76b7ce72d66507ebbe00caf5e45afd587a/third_party/crashpad/README.chromium


### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-02-23)

Note to VRP: this lets an an attacker-controlled amount of the crashpad_handler’s stack memory, and the contents of the first 120 bytes are also attacker-controlled, to be copied to a properly managed heap buffer. I think this would require a compromised renderer in order to craft an exception with this format, and crashpad_handler is equivalent to the browser process in terms of privilege.

### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-23)

Requesting merge to stable M110 because latest trunk commit (1108722) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1108722) appears to be after beta branch point (1097615).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-24)

Merge review required: M111 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-24)

Merge review required: M110 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2023-02-27)

1. Security bug fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/4285061
3. Yes
4. No
5. N/A
6. No

### am...@chromium.org (2023-02-27)

M111 and M110 merges approved, please merge to branches 5563 and 5481 respectively before 9am Pacific tomorrow (Tuesday, 28 February) so this fix can be included in M111 Stable RC and M110 Extended - ty! 

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac45a9a428621f8c891987a6f7cc24b0ddfa537f

commit ac45a9a428621f8c891987a6f7cc24b0ddfa537f
Author: Robert Sesek <rsesek@chromium.org>
Date: Mon Feb 27 21:15:39 2023

[M111] Update Crashpad to 3e8727238bae3c069bd71cfb3b2bbaa98b55f05b

3e8727238bae win: Only process up to EXCEPTION_MAXIMUM_PARAMETERS in an
             EXCEPTION_RECORD

(cherry picked from commit d05bea76b7ce72d66507ebbe00caf5e45afd587a)

Fixed: 1412658
Change-Id: I7461602d1a18d44ea1a11ac19f1487fbdb92acf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4285061
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Alex Gough <ajgo@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1108722}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4294858
Cr-Commit-Position: refs/branch-heads/5563@{#871}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/ac45a9a428621f8c891987a6f7cc24b0ddfa537f/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
[modify] https://crrev.com/ac45a9a428621f8c891987a6f7cc24b0ddfa537f/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win_test.cc
[modify] https://crrev.com/ac45a9a428621f8c891987a6f7cc24b0ddfa537f/third_party/crashpad/README.chromium


### wf...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56bd20b295b4179c26443e655e6cefaa6efffa4f

commit 56bd20b295b4179c26443e655e6cefaa6efffa4f
Author: Robert Sesek <rsesek@chromium.org>
Date: Mon Feb 27 21:25:11 2023

[M110] Update Crashpad to 3e8727238bae3c069bd71cfb3b2bbaa98b55f05b

3e8727238bae win: Only process up to EXCEPTION_MAXIMUM_PARAMETERS in an
             EXCEPTION_RECORD

(cherry picked from commit d05bea76b7ce72d66507ebbe00caf5e45afd587a)

Fixed: 1412658
Change-Id: I7461602d1a18d44ea1a11ac19f1487fbdb92acf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4285061
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Alex Gough <ajgo@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1108722}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295200
Cr-Commit-Position: refs/branch-heads/5481@{#1298}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/56bd20b295b4179c26443e655e6cefaa6efffa4f/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win.cc
[modify] https://crrev.com/56bd20b295b4179c26443e655e6cefaa6efffa4f/third_party/crashpad/crashpad/snapshot/win/exception_snapshot_win_test.cc
[modify] https://crrev.com/56bd20b295b4179c26443e655e6cefaa6efffa4f/third_party/crashpad/README.chromium


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, sunburst! The VRP Panel has decided to award you $3,000 for this report based on the narrow impact of exploiting this issue and the resulting information disclosure. Thank you for your efforts in discovering and reporting this issue to us! 

### su...@gmail.com (2023-03-03)

Hi, this bug is in the CrashHandler process, which has the same privileges as the Browser process. Why is only 3000 rewarded?

### am...@chromium.org (2023-03-03)

Hi, thanks for reaching out about this. The award was based on the actual impact of this issue which ended up being on par with a data leak / information disclosure. The reward amount is commensurate with that bug class / impact. Even if the renderer is compromised, the data leak / attacker controlled data that is manipulated is sent back to that of our crash system and is not related to user data or any memory corruption impacting the user.  

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1412658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062893)*
