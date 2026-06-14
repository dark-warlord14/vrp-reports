# [LangFuzz] Invalid write in v8::internal::ElementsAccessorBase<...>::CopyElements

| Field | Value |
|-------|-------|
| **Issue ID** | [40056023](https://issues.chromium.org/issues/40056023) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-04-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 19.0.1077.3 dev and d8 shell (trunk version, tested rev 11193) in function v8::internal::ElementsAccessorBase<...>::CopyElements with an invalid write to a scary address (0x3506bf000000 in shell, browser looks different).

**VERSION**  

Chrome Version: 19.0.1084.1 dev  

Operating System: Ubuntu 11.10 64 bit

**REPRODUCTION CASE**  

var a = [0,1,2,3];  

a[2000000] = 2000000;  

a.length=2000;  

for (var i = 0; i <= 256; i++) {  

a[i] = new Object();  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00005555565a1e7e in ?? ()  

(gdb) bt 4  

#0 0x00005555565a1e7e in ?? ()  

#1 0x0000555556691df7 in ?? ()  

#2 0x000055555669238d in ?? ()  

#3 0x0000555556694945 in ?? ()  

(More stack frames follow...)  

(gdb) x /i $pc  

=> 0x5555565a1e7e: mov %rdx,0xf(%rbx,%rax,1)  

(gdb) info reg rdx rbx rax  

rdx 0xc1704804141 13292999295297  

rbx 0x1ee268f7fcc1 33957772524737  

rax 0x80330 525104  

(gdb)

Trace from D8 with Valgrind:

==28596== Warning: set address range perms: large range [0x3b9a91403000, 0x3b9ab1403000) (noaccess)  

==28596== Invalid write of size 8  

==28596== at 0x46A10A: v8::internal::ElementsAccessorBase<v8::internal::DictionaryElementsAccessor, v8::internal::ElementsKindTraits<(v8::internal::ElementsKind)3> >::CopyElements(v8::internal::JSObject\*, unsigned int, v8::internal::FixedArrayBase\*, v8::internal::ElementsKind, unsigned int, int, v8::internal::FixedArrayBase\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x566B8D: v8::internal::JSObject::SetFastElementsCapacityAndLength(int, int, v8::internal::JSObject::SetFastElementsCapacityMode) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x575A06: v8::internal::JSObject::SetDictionaryElement(unsigned int, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag, bool, v8::internal::SetPropertyMode) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x5769C4: v8::internal::JSObject::SetElement(unsigned int, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag, bool, v8::internal::SetPropertyMode) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x57715A: v8::internal::JSObject::SetElement(v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), unsigned int, v8::internal::Handle[v8::internal::Object](javascript:void(0);), PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::SetPropertyMode) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x5CEB25: v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), PropertyAttributes, v8::internal::StrictModeFlag) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x4EFB7A: v8::internal::KeyedStoreIC\_Slow(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== by 0x3B9A91506361: ???  

==28596== by 0x3B9A9153D4C3: ???  

==28596== by 0x3B9A9150C926: ???  

==28596== by 0x3B9A91506115: ???  

==28596== by 0x46EDCF: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28596== Address 0x3506bf000000 is not stack'd, malloc'd or (recently) free'd

## Timeline

### in...@chromium.org (2012-04-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-02)

I'll take a look.

### da...@chromium.org (2012-04-02)

The crash is due to a missing bounds check that allowed values to be copied beyond the end of an array when it's length gets shrunk and it converts from Dictionary to FastElements mode. With a little bit of cleverness, this would allow writing arbitrary values into arbitrary locations. Patch is in review.

### in...@chromium.org (2012-04-02)

Is this a regression or does this bug affects stable ?

### in...@chromium.org (2012-04-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=33011091

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f5e19000000
Crash State:
  - crash stack -
  v8::internal::DictionaryElementsAccessor::CopyElementsImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=127453:127460

Minimized Testcase (0.13 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95lZKNay7_78r84RQULko-O6rTTKTIu4VeY_4nTUFEu2aAmwUuBXt7m8-jAPmPrAmuGRD7ZhwIBQZAaVnqXN581dqt3bre3k1UWpZV6XoVE6PiatdFtlBNjZkVjWslRb8Cv_xC7ZEEe5CqsXC5RU-j5PASy9w
<script>
var a = [0,1,2,3];
a[2000000] = 2000000;
a.length=2000;
for (var i = 0; i <= 256; i++) {
  a[i] = new Object();
}
</script>

### in...@chromium.org (2012-04-03)

Seems to have regressed in v8: r11039:r11082 as per ClusterFuzz. Danno, do you think it regressed recently, just wanted to double check.

### bu...@chromium.org (2012-04-03)

Commit: 8c0a43f09f145d9fc6f969d559873018176eeb6a
 Email: danno@chromium.org@ce2b1a6d-e550-0410-aec6-3dcde31c8c00

Merged r11194, r11198, r11201, r11214 into trunk branch.

Ensure that arguments object is materialized when deoptimizing from inlined function.

Fix performance regressions due to lazy initialization.

Fix broken build on Windows due to r11198.

Properly support shrinking arrays in CopyDictionaryToObjectElements.

BUG=v8:2045,chromium:118686,chromium:121407

R=ulan@chromium.org

Review URL: https://chromiumcodereview.appspot.com/9959093

git-svn-id: http://v8.googlecode.com/svn/trunk@11215 ce2b1a6d-e550-0410-aec6-3dcde31c8c00

M	src/api.cc
M	src/arm/lithium-arm.cc
M	src/elements.cc
M	src/hydrogen-instructions.h
M	src/hydrogen.cc
M	src/ia32/lithium-ia32.cc
M	src/isolate.cc
M	src/isolate.h
M	src/lazy-instance.h
M	src/mips/lithium-mips.cc
M	src/platform-cygwin.cc
M	src/platform-freebsd.cc
M	src/platform-linux.cc
M	src/platform-macos.cc
M	src/platform-nullos.cc
M	src/platform-openbsd.cc
M	src/platform-posix.cc
A	src/platform-posix.h
M	src/platform-solaris.cc
M	src/platform-win32.cc
M	src/platform.h
M	src/v8.cc
M	src/version.cc
M	src/x64/lithium-x64.cc
A	test/mjsunit/regress/regress-121407.js
A	test/mjsunit/regress/regress-2045.js
M	tools/check-static-initializers.sh
M	tools/gyp/v8.gyp

### da...@chromium.org (2012-04-03)

This is a regression that only affects canary and M19. The patch has landed in V8 trunk, and we will roll into Chrome and merge back to M19 ASAP. 

### in...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-04-04)

ClusterFuzz has detected this issue as fixed in range 130617:130650.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=33011091

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f5e19000000
Crash State:
  - crash stack -
  v8::internal::DictionaryElementsAccessor::CopyElementsImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=127453:127460
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130617:130650

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95lZKNay7_78r84RQULko-O6rTTKTIu4VeY_4nTUFEu2aAmwUuBXt7m8-jAPmPrAmuGRD7ZhwIBQZAaVnqXN581dqt3bre3k1UWpZV6XoVE6PiatdFtlBNjZkVjWslRb8Cv_xC7ZEEe5CqsXC5RU-j5PASy9w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### da...@chromium.org (2012-04-05)

We've had trouble getting a trunk V8 roll to stick in Chromium the last several days. The merge of this patch to M19 is still pending until trunk sticks and the fix gets minimum real coverage.

### cl...@chromium.org (2012-04-06)

ClusterFuzz has detected this issue as fixed in range 130896:130956.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=33011091

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f5e19000000
Crash State:
  - crash stack -
  v8::internal::DictionaryElementsAccessor::CopyElementsImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=127453:127460
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130896:130956

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95lZKNay7_78r84RQULko-O6rTTKTIu4VeY_4nTUFEu2aAmwUuBXt7m8-jAPmPrAmuGRD7ZhwIBQZAaVnqXN581dqt3bre3k1UWpZV6XoVE6PiatdFtlBNjZkVjWslRb8Cv_xC7ZEEe5CqsXC5RU-j5PASy9w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-04-22)

@danno: I'm assuming this was merged long ago; please correct me if not :)

### da...@chromium.org (2012-04-23)

The problem only affected 3.9, and the fix was merged into 3.9 on April 11, and it automatically went out with the in the next Chrome 19 Beta after that.

### sc...@gmail.com (2012-05-04)

I seem to be tagging a lot of rewards for you today, decoder :P Thanks for your ongoing help, it's particularly awesome that you catch regressions.
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/121407?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056023)*
