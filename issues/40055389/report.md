# UNKNOWN in v8::Message::GetScriptResourceName

| Field | Value |
|-------|-------|
| **Issue ID** | [40055389](https://issues.chromium.org/issues/40055389) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-03-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached page causes a crash at address 0x00050000000f at v8::Message::GetScriptResourceName. The page tries to open JS debugger at a certain point in a recursive function.

Not sure if there is control over this one, but reporting as a security bug to be on the safe side since the address is unusual and this seems to affect all versions.

**VERSION**  

Chrome Version: 18.0.1025.113, 17.0.963.79, 19.0.1068.1  

Operating System: Linux (Debian 6.0.4, x84\_64)

**REPRODUCTION CASE**  

$ chrome-san rec.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==21610== ERROR: AddressSanitizer crashed on unknown address 0x00050000000f (pc 0x7fda8a21bf7d sp 0x7fff3523d180 bp 0x7fff3523d270 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7fda8a21bf7d in v8::Message::GetScriptResourceName() const ???:0  

#1 0x7fda8bf1b6e8 in WebCore::v8UncaughtExceptionHandler(v8::Handle[v8::Message](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);)) third\_party/WebKit/Source/WebCore/bindings/v8/V8DOMWindowShell.cpp:0  

#2 0x7fda8a595d26 in v8::internal::MessageHandler::ReportMessage(v8::internal::Isolate\*, v8::internal::MessageLocation\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ???:0  

#3 0x7fda8a2ad3e9 in v8::internal::Debug::CompileDebuggerScript(int) ???:0  

#4 0x7fda8a2ae0c1 in v8::internal::Debug::Load() ???:0  

#5 0x7fda8a2c6a99 in v8::internal::EnterDebugger::EnterDebugger() ???:0  

#6 0x7b68c10800007fda  

Stats: 126M malloced (44M for red zones) by 177398 calls  

Stats: 0M realloced by 42 calls  

Stats: 125M freed by 169653 calls  

Stats: 0M really freed by 0 calls  

Stats: 204M (52233 full pages) mmaped in 51 calls  

mmaps by size class: 8:32766; 9:8191; 10:155610; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8; 20:4;  

mallocs by size class: 8:18828; 9:2569; 10:154682; 11:636; 12:462; 13:99; 14:73; 15:10; 16:11; 17:11; 18:8; 19:7; 20:2;  

frees by size class: 8:11637; 9:2253; 10:154599; 11:536; 12:441; 13:88; 14:60; 15:8; 16:4; 17:10; 18:8; 19:7; 20:2;  

rfrees by size class:  

Stats: malloc large: 28 small slow: 1318

## Attachments

- [rec.html](attachments/rec.html) (text/plain; charset=us-ascii, 150 B)

## Timeline

### ao...@gmail.com (2012-03-22)

I'm also seeing a similar crash at other places near GC, such as "crashed on unknown address 0x000200000068 (v8::internal::MarkCompactCollector::PrepareThreadForCodeFlushing(v8::internal::Isolate*,)".

### ke...@chromium.org (2012-03-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29344154

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x00050000000f
Crash State:
  - crash stack -
  v8::Message::GetScriptResourceName
  WebCore::v8UncaughtExceptionHandler
  v8::internal::MessageHandler::ReportMessage
  

Minimized Testcase (0.12 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97D5SYNl9BILy548vOl9F-RghzXaL9zNpHs55AwNdwe0MFp61kao77FW9ZUSx_kohXiSmyqHJZgMJNsAKPt1xzsFXrYjJmWZYSfEwIMu4B6XFRBV7fbIY2qVagjHycdkXIKb307skPweC62ZOHGnT8-t_9oNQ
<script>
var d = 0;
function recurse() {
  if (d++ == 62) {
    debugger;
    d = 0;
  }
  recurse();
}
recurse();
</script>

### ke...@chromium.org (2012-03-22)

I don't know if this is a security bug or not, cluster-fuzz reports the same as Aki. It appears to be an issue with v8 debugging.

Can anyone on cc help us figure out what is happening here?

Running in a debugger I see a failed assert in pending_exception() in isolate.h.


 	v8.dll!v8::internal::OS::Abort()  Line 950	C++
 	v8.dll!V8_Fatal(const char * file, int line, const char * format, ...)  Line 59	C++
 	v8.dll!v8::internal::Isolate::pending_exception()  Line 533 + 0x28 bytes	C++
 	v8.dll!v8::internal::Isolate::ExceptionScope::ExceptionScope(v8::internal::Isolate * isolate)  Line 650 + 0x20 bytes	C++
 	v8.dll!v8::internal::MessageHandler::ReportMessage(v8::internal::Isolate * isolate, v8::internal::MessageLocation * loc, v8::internal::Handle<v8::internal::Object> message)  Line 109 + 0xc bytes	C++
 	v8.dll!v8::internal::Debug::CompileDebuggerScript(int index)  Line 778 + 0x14 bytes	C++
 	v8.dll!v8::internal::Debug::Load()  Line 833 + 0x13 bytes	C++
 	v8.dll!v8::internal::EnterDebugger::EnterDebugger()  Line 3208 + 0x8 bytes	C++
 	v8.dll!v8::internal::Execution::ProcessDebugMessages(bool debug_command_only)  Line 861 + 0xb bytes	C++
 	v8.dll!v8::internal::Execution::DebugBreakHelper()  Line 848 + 0xd bytes	C++
>	v8.dll!v8::internal::Runtime_DebugBreak(v8::internal::Arguments args, v8::internal::Isolate * isolate)  Line 10303	C++


### ke...@chromium.org (2012-03-22)

[Empty comment from Monorail migration]

### ao...@gmail.com (2012-03-26)

These kinds of addresses also seem to pop up usually in GC context. Could this be the same issue as 119926 and 119960? The situation in this is fairly similar to 119960, but I can't see 119926.

### da...@chromium.org (2012-03-26)

I doubt this is related to 119926 or 119960, since it doesn't involve large arrays. We'll take a look.

### da...@chromium.org (2012-03-26)

I doubt this is related to 119926 or 119960, since it doesn't involve large arrays. We'll take a look.

### sc...@gmail.com (2012-03-30)

Did you turn up anything, Danno?

### sc...@gmail.com (2012-03-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-03-30)

Sorry, this slipped through the cracks, I'll make sure it gets attention from somebody ASAP.

### da...@chromium.org (2012-04-02)

This crash is caused by missing stack overflow checks. There seem to be read accesses of initialized variables that are used for address calculations, which doesn't seem good. I'm working on a patch.

### in...@chromium.org (2012-04-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-03)

Patch has landed in v8 trunk and will be in our next roll into Chromium. I'll merge back to 3.9 and 3.8.

### in...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-05)

We've had trouble landing this on trunk, so merge is still pending on 3.9 and 3.8 until there's a little bit coverage on the patch.

### da...@chromium.org (2012-04-11)

The fix for this and related stack overflow issues was merged into V8 3.9 for version 3.9.24.9 (V8 r11260) and 3.8 version 3.8.9.17 (V8 r11262).

### sc...@gmail.com (2012-04-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-04-11)

ClusterFuzz has detected this issue as fixed in range 131559:131571.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29344154

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x00050000000f
Crash State:
  - crash stack -
  v8::Message::GetScriptResourceName
  WebCore::v8UncaughtExceptionHandler
  v8::internal::MessageHandler::ReportMessage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108839:108881
Fixed: https://cluster-fuzz.appspot.com/revisions?range=131559:131571

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97D5SYNl9BILy548vOl9F-RghzXaL9zNpHs55AwNdwe0MFp61kao77FW9ZUSx_kohXiSmyqHJZgMJNsAKPt1xzsFXrYjJmWZYSfEwIMu4B6XFRBV7fbIY2qVagjHycdkXIKb307skPweC62ZOHGnT8-t_9oNQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-04)

Hard to state that this OOB read could not be recovered. Therefore:
$500

### sc...@gmail.com (2012-05-06)

Reward to be upped to $1337 and donated to http://www.betterplace.org/en/projects/2001-school-project-welkite-i-in-ethiopia-east-africa

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-06-28)

Donated this reward and the other pending one to the betterplace.org project indicated.

### sc...@gmail.com (2012-06-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/119429?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055389)*
