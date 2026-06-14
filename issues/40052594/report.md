# Security: heap-buffer-overflow on media_history::MediaHistoryKeyedService::OnURLsDeleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40052594](https://issues.chromium.org/issues/40052594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>History |
| **Platforms** | Linux, Windows |
| **Reporter** | he...@gmail.com |
| **Assignee** | be...@chromium.org |
| **Created** | 2020-06-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

It looks like the heap-buffer-overflow happened in [1].  

src\chrome\browser\media\history\media\_history\_keyed\_service.cc:160

for (const url::Origin& origin : origins) {  

const auto& origin\_count =  

deletion\_info.deleted\_urls\_origin\_map().find(origin.GetURL());

```
if (origin_count->second.first > 0) // \*\*\*\*\* [1]  
  continue;  

```

the origin\_count is `end` of the map.

**VERSION**  

Chrome Version: 00e0c31c9aa943f8b3c7a4c8ac9baa5144c98348  

Operating System: Windows 10

**REPRODUCTION CASE**

Download the latest version(778703) of chromium with asan in <https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/>  

.\chrome.exe --user-data-dir=/path/to/123

Then you will get the crash infomation as bellow.

==9956==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11f270bf7980 at pc 0x7ffd0c91781d bp 0x0057635fe860 sp 0x0057635fe8a8  

READ of size 4 at 0x11f270bf7980 thread T0  

#0 0x7ffd0c91781c in media\_history::MediaHistoryKeyedService::OnURLsDeleted C:\b\s\w\ir\cache\builder\src\chrome\browser\media\history\media\_history\_keyed\_service.cc:160  

#1 0x7ffd08b51223 in history::HistoryService::NotifyURLsDeleted C:\b\s\w\ir\cache\builder\src\components\history\core\browser\history\_service.cc:1215  

#2 0x7ffd072dce22 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:142  

#3 0x7ffd09b2b2c7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:332  

#4 0x7ffd09b2a9f4 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:252  

#5 0x7ffd0737e0f0 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:230  

#6 0x7ffd0737ba2f in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:86  

#7 0x7ffd09b2cabb in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:451  

#8 0x7ffd07291441 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:124  

#9 0x7ffd0c788a83 in ChromeBrowserMainParts::MainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1688  

#10 0x7ffd012d055f in content::BrowserMainLoop::RunMainMessageLoopParts C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:998  

#11 0x7ffd012d6775 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:150  

#12 0x7ffd012c8754 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47  

#13 0x7ffd06f8a729 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:518  

#14 0x7ffd06f8d21c in content::ContentMainRunnerImpl::RunServiceManager C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:975  

#15 0x7ffd06f8c392 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:861  

#16 0x7ffd0704b594 in service\_manager::Main C:\b\s\w\ir\cache\builder\src\services\service\_manager\embedder\main.cc:454  

#17 0x7ffd06f8a4f0 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:19  

#18 0x7ffcfdf313f0 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:118  

#19 0x7ff7577d5b51 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:164  

#20 0x7ff7577d2a64 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:271  

#21 0x7ff757ba1cdf in \_\_scrt\_common\_main\_seh d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ffda29a4033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180014033)  

#23 0x7ffda2c43690 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180073690)

Address 0x11f270bf7980 is a wild pointer.  

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\chrome\browser\media\history\media\_history\_keyed\_service.cc:160 in media\_history::MediaHistoryKeyedService::OnURLsDeleted  

Shadow bytes around the buggy address:  

0x0410bebfeee0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0410bebfeef0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0410bebfef00: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0410bebfef10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0410bebfef20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0410bebfef30:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0410bebfef40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0410bebfef50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0410bebfef60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0410bebfef70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0410bebfef80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

Shadow gap: cc  

==9956==ABORTING

## Attachments

- [123.rar](attachments/123.rar) (application/octet-stream, 3.2 MB)
- [crash.txt](attachments/crash.txt) (text/plain, 5.0 KB)
- [crash.mp4](attachments/crash.mp4) (video/mp4, 2.4 MB)
- [chromium_version.png](attachments/chromium_version.png) (image/png, 60.6 KB)
- [crash.png](attachments/crash.png) (image/png, 248.1 KB)
- [123.rar](attachments/123_53144213.rar) (application/octet-stream, 671.1 KB)
- [History](attachments/History) (text/plain, 3.2 MB)
- [crash_linux.png](attachments/crash_linux.png) (image/png, 604.2 KB)
- [blob.html](attachments/blob.html) (text/plain, 84 B)
- [History](attachments/History_53144261) (text/plain, 116.0 KB)
- [new_crash.mp4](attachments/new_crash.mp4) (video/mp4, 4.0 MB)
- [ttt.rar](attachments/ttt.rar) (application/octet-stream, 3.0 KB)
- [new_new_crash.mp4](attachments/new_new_crash.mp4) (video/mp4, 9.4 MB)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 11.5 KB)
- [crash-extension.mp4](attachments/crash-extension.mp4) (video/mp4, 2.1 MB)
- [extension.zip](attachments/extension_53144609.zip) (application/octet-stream, 2.7 KB)
- [crash_extension.mp4](attachments/crash_extension.mp4) (video/mp4, 4.0 MB)

## Timeline

### rs...@chromium.org (2020-06-16)

Do you have a more reduced reproduction rather than a whole profile directory? I cannot repro the crash when running with the directory. But the ASan report does look valid.

[Monorail components: Internals>Media>History]

### he...@gmail.com (2020-06-17)

I attach a crash video here.

### [Deleted User] (2020-06-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2020-06-17)

I compile the chromium (59f1802018c55bdd13387630aa7439eeffdedb0c) without asan to debug it. I attache the crash infomation in windbg here. It looks like that the ` find ` return a address (@rax). Then threating the object as  `std::pair<int, base::Time>` rather than `OriginCountAndLastVisitMap.end()`. As the http://www.cplusplus.com/reference/map/map/end/ says, `It does not point to any element, and thus shall not be dereferenced`.
```
OriginCountAndLastVisitMap deleted_urls_origin_map_;
typedef std::map<GURL, std::pair<int, base::Time>> OriginCountAndLastVisitMap;
```

### he...@gmail.com (2020-06-17)

Attache the new POC. the `History`  is in the 123.rar. The `History`  needs to be placed under the directory like ` 123/Defalut/History`. 

### he...@gmail.com (2020-06-17)

It also crashed on linux.

### rs...@chromium.org (2020-06-17)

I was able to repro on Linux but not Mac. Appears this code is the same as on Stable, so adjusting Impact.

### rs...@chromium.org (2020-06-17)

[Empty comment from Monorail migration]

### he...@gmail.com (2020-06-18)

It looks like that the `deleted_urls_origin_map_`  use  url in  `deleted_rows()` as index to store and find. So it does not consider the `find`  will return an `end()` here. But it is different when using `row.url().GetOrigin()` as an index to store in [1] and `url::Origin::Create(row.url())` as an index to find in [2].

```
  for (const history::URLRow& row : deletion_info.deleted_rows())
    origins.insert(row.url().GetOrigin());                        [1]

  deletion_info.set_deleted_urls_origin_map(
      GetCountsAndLastVisitForOrigins(origins));
  
  ...
 
  for (const history::URLRow& row : deletion_info.deleted_rows()) {
    origins.insert(url::Origin::Create(row.url()));               [2]
  }

  // Find any origins that do not have any more data in the history database.
  std::set<url::Origin> deleted_origins;
  for (const url::Origin& origin : origins) {
    const auto& origin_count =
        deletion_info.deleted_urls_origin_map().find(origin.GetURL());

    std::cout << deletion_info.deleted_urls_origin_map().begin()->first << std::endl;

    if (origin_count->second.first > 0)
      continue;
```

when the url like `"blob:http://127.0.0.1:8605/58ca2454-090d-4dd8-8723-80abc48dfefa"`  be processed, the `IsStandard()` will return false to make `GURL::GetOrigin()` return an empty `GURL()` as index of `deleted_urls_origin_map_`. Then `url::Origin::Create(row.url())` will make `find` use a not empty `GURL()` to find the value, so it will return an `end()`.

```
GURL GURL::GetOrigin() const {
  // This doesn't make sense for invalid or nonstandard URLs, so return
  // the empty URL.
  if (!is_valid_ || !IsStandard())
    return GURL(); 
...
Origin Origin::Create(const GURL& url) {
  if (!url.is_valid())
    return Origin();

  SchemeHostPort tuple;

  if (url.SchemeIsFileSystem()) {
    tuple = SchemeHostPort(*url.inner_url());
  } else if (url.SchemeIsBlob()) {
```

### he...@gmail.com (2020-06-18)

I found that it can be triggered through a web page.

```
<script>
b = new Blob();
o = URL.createObjectURL(b);
location.href = o
</script>

```

This html file will create a piece of data in the `urls` and `visits` table of the History database. I changed the `visit_time` field in the `visits` table and the `last_visit_time` field in the `urls` table to make it expire (since the expiration time is about two months). It also crashed.

### he...@gmail.com (2020-06-18)

Note: It should be triggered on a web server.

### he...@gmail.com (2020-06-19)

Sorry, the expiration time is about three months. And attached the smaller 'History' file.

### he...@gmail.com (2020-06-19)

I found a new way to trigger the crash.

1. Open the chromium with any `--user-data-dir`
2. Access the blob.html twice from a web server.
3. Delete the history.

Then it will crash as the video shows.

### he...@gmail.com (2020-06-19)

[Comment Deleted]

### he...@gmail.com (2020-06-19)

[Empty comment from Monorail migration]

### he...@gmail.com (2020-06-19)

I can change the system time to trigger the crash.

1. Open the chromium with any `--user-data-dir`
2. Access the index.html in the ttt.rar from a web server.
3. Close the chromium
4. Change the system time.
5. Open the chromium and wait 30s.
6. Close the chromium.
7. Open the chromium.

Then it will crash as the video shows.

### he...@gmail.com (2020-06-19)

[Empty comment from Monorail migration]

### he...@gmail.com (2020-06-21)

I think that the Security Severity should be Critical, because it can make the browser process crash remotely.

### rs...@chromium.org (2020-06-22)

I am still unable to reproduce this crash, but the iterator analysis in c#9 looks accurate.

This is not Critical because manually editing a database or changing the system time are significant preconditions for remote exploitability. Per severity guidelines though, c#13 indicates an in-Chrome user gesture to trigger this, which suggests High.

### he...@gmail.com (2020-06-22)

I didn't initially trigger the crash by changing the system time or editing the database. The crash was caused by a three-month old browsing history. So I think this crash can be triggered without any interaction, but it takes three months.

### he...@gmail.com (2020-06-23)

I suggest replacing `if (origin_count->second.first > 0)` with `if (origin_count != deletion_info.deleted_urls_origin_map().end() && origin_count->second.first > 0)` to avoid this crash

### he...@gmail.com (2020-06-23)

I can reproduce this crash very steadily on windows. Maybe you need a clean user-data-dir. Then acess the blob.html on a web server TWICE. And delete the History like the video in c#15 shows.

### rs...@chromium.org (2020-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-30)

beccahughes: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1755fa3ec13735194ebc95b9c06052244040fdae

commit 1755fa3ec13735194ebc95b9c06052244040fdae
Author: Becca Hughes <beccahughes@chromium.org>
Date: Tue Jun 30 20:33:14 2020

Add end() check to fix security bug

Fix the bug by checking we have not reached the
end before accessing.

BUG=1095560

Change-Id: I309237562ddd5058c3b3b99d58a03c526cf49b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276511
Commit-Queue: Becca Hughes <beccahughes@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#784113}

[modify] https://crrev.com/1755fa3ec13735194ebc95b9c06052244040fdae/chrome/browser/media/history/media_history_keyed_service.cc
[modify] https://crrev.com/1755fa3ec13735194ebc95b9c06052244040fdae/chrome/browser/media/history/media_history_keyed_service_unittest.cc


### be...@google.com (2020-06-30)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

beccahughes@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### he...@gmail.com (2020-07-01)

CREDIT INFORMATION
Reporter credit: ZeKai Wu (@hellowuzekai) of Tencent Security Xuanwu Lab.


### [Deleted User] (2020-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-01)

Requesting merge to beta M84 because latest trunk commit (784113) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-01)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-07-01)

+Adetaylor(Security TPM) for merge decision.

Note : The CL in https://crbug.com/chromium/1095560#c25 isn't landed on Trunk yet.

### go...@chromium.org (2020-07-01)

Just to update: CL listed at #25 landed in trunk and in canary #86.0.4189.0 (currently building).  

### ad...@google.com (2020-07-01)

Working around Sheriffbot bug...

### [Deleted User] (2020-07-02)

Your change meets the bar and is auto-approved for M85. Please go ahead and merge the CL to branch 4183 (refs/branch-heads/4183) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-07-06)

Please complete the merges to M85 branch asap,so the change can be part of the M85 dev release this week

### aw...@google.com (2020-07-06)

Looks good for M84

### aw...@google.com (2020-07-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa344447a129fd350abc72f849839963c78b2c66

commit fa344447a129fd350abc72f849839963c78b2c66
Author: Becca Hughes <beccahughes@chromium.org>
Date: Mon Jul 06 22:16:32 2020

Add end() check to fix security bug

Fix the bug by checking we have not reached the
end before accessing.

BUG=1095560

(cherry picked from commit 1755fa3ec13735194ebc95b9c06052244040fdae)

Change-Id: I309237562ddd5058c3b3b99d58a03c526cf49b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276511
Commit-Queue: Becca Hughes <beccahughes@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2283703
Reviewed-by: Becca Hughes <beccahughes@chromium.org>
Cr-Commit-Position: refs/branch-heads/4173@{#5}
Cr-Branched-From: 4c6ab74320b2f8188cdadb14148c242bcb29beac-refs/heads/master@{#778145}

[modify] https://crrev.com/fa344447a129fd350abc72f849839963c78b2c66/chrome/browser/media/history/media_history_keyed_service.cc
[modify] https://crrev.com/fa344447a129fd350abc72f849839963c78b2c66/chrome/browser/media/history/media_history_keyed_service_unittest.cc


### pb...@google.com (2020-07-07)

[Empty comment from Monorail migration]

### pb...@google.com (2020-07-07)

Based on offline chat with  awhalley@ this is approved for M84 Banch.

### sr...@google.com (2020-07-07)

Please complete your merges today before 2pm PST so they can be part of the dev release tomorrow

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/50621ae1a5e8cfb2a7675ff05171694cb901ad3b

commit 50621ae1a5e8cfb2a7675ff05171694cb901ad3b
Author: Becca Hughes <beccahughes@chromium.org>
Date: Tue Jul 07 17:42:27 2020

Add end() check to fix security bug

Fix the bug by checking we have not reached the
end before accessing.

BUG=1095560

(cherry picked from commit 1755fa3ec13735194ebc95b9c06052244040fdae)

Change-Id: I309237562ddd5058c3b3b99d58a03c526cf49b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276511
Commit-Queue: Becca Hughes <beccahughes@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2283932
Reviewed-by: Becca Hughes <beccahughes@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#839}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/50621ae1a5e8cfb2a7675ff05171694cb901ad3b/chrome/browser/media/history/media_history_keyed_service.cc
[modify] https://crrev.com/50621ae1a5e8cfb2a7675ff05171694cb901ad3b/chrome/browser/media/history/media_history_keyed_service_unittest.cc


### he...@gmail.com (2020-07-09)

Hi, can i get a cve and bounty for this issue? thanks :)

### ad...@chromium.org (2020-07-09)

Hi, I'm expecting this to be released in the initial M84 release at which point we'll credit it in the release notes and assign a CVE. It will also then go to the VRP panel who will consider it for reward. Thanks for the report!

### [Deleted User] (2020-07-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-07-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-07-16)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-07-16)

[Empty comment from Monorail migration]

### he...@gmail.com (2020-07-16)

[Comment Deleted]

### he...@gmail.com (2020-07-17)

Hello, i want to know the reason why the bounty of this issue is $500. Because I think this issue is a  `Memory corruption in a non-sandboxed process`. As the https://www.google.com/about/appsecurity/chrome-rewards/ says, the baseline is $5,000 - $15,000.

### he...@gmail.com (2020-07-17)

And c#20 says the in-Chrome user gesture is not necessary. Another way to trigger the crash is to wait for three months to expire the history. After that, the browser will crash when deleting history automatically.

### ad...@chromium.org (2020-07-17)

hellowuzekai@ our understanding is that this is heavily mitigated. It requires either (a) quite specific user interaction, or (b) local machine access to change the time or edit the database, or (c) waiting three months.

If you feel this is a practical attack please could you explain the steps involved?

Thanks again for the report.

### he...@gmail.com (2020-07-17)

Sorry, i don't think the specific user interaction will make it heavily mitigated. https://crbug.com/chromium/956597 also need specific user interaction,but the reward of this issue is more than 500 dollars.


### he...@gmail.com (2020-07-20)

And this issue is persistent. As long as you visit the malicious webpage, bad data will be stored in the History file. Next time you delete the history (I think this is a very normal behavior), even if you do not visit the malicious webpage this time, it will crash. If you don’t delete the history, the browser will crash every time you open it after three months.

### ad...@google.com (2020-07-20)

[Empty comment from Monorail migration]

### sr...@google.com (2020-07-20)

Please complete your merges to M85 branch today before 2pm PST so that this change can be included in the Dev Release tomorrow. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf2fda06837b2dfa8be6092ce31d8e5fd3337198

commit bf2fda06837b2dfa8be6092ce31d8e5fd3337198
Author: Becca Hughes <beccahughes@chromium.org>
Date: Mon Jul 20 18:54:59 2020

Add end() check to fix security bug

Fix the bug by checking we have not reached the
end before accessing.

BUG=1095560

(cherry picked from commit 1755fa3ec13735194ebc95b9c06052244040fdae)

Change-Id: I309237562ddd5058c3b3b99d58a03c526cf49b6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276511
Commit-Queue: Becca Hughes <beccahughes@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2307618
Reviewed-by: Becca Hughes <beccahughes@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#758}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/bf2fda06837b2dfa8be6092ce31d8e5fd3337198/chrome/browser/media/history/media_history_keyed_service.cc
[modify] https://crrev.com/bf2fda06837b2dfa8be6092ce31d8e5fd3337198/chrome/browser/media/history/media_history_keyed_service_unittest.cc


### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-23)

Re https://crbug.com/chromium/1095560#c59, https://crbug.com/chromium/1095560#c60, the VRP panel reconsidered the reward amount and have determined that it will remain unchanged.

### he...@gmail.com (2020-08-03)

Steps to reproduce the problem:
1. Load the attached extension.
2. Visit the popup.html page through clicking the extension.

### he...@gmail.com (2020-08-03)

The method for triggering this issue is similar to https://crbug.com/chromium/1019161, with a video attached. Therefore, please reconsider the award amount, thank you.

### ad...@chromium.org (2020-08-03)

Could you confirm that this bug requires either:

1) A local attacker modifying the system time, or
2) A local attacker modifying the history database, or
3) Waiting three months?

That's our understanding.

If there is some other way to exploit this then please provide detailed steps. Thanks.

### he...@gmail.com (2020-08-03)

I used the chrome.history function of the Chrome extension to trigger the vulnerability by adding and deleting history records.

### he...@gmail.com (2020-08-03)

https://crbug.com/chromium/1095560#c66 is the detailed steps.

### he...@gmail.com (2020-08-04)

It only requires the `history` permissions in the manifest.json. Therefore, malicious chrome extensions can use it to cause "memory corruption in a non-sandboxed process"

### he...@gmail.com (2020-08-04)

Upload a clearer video and a chrome extension file with less permissions.

### ad...@google.com (2020-08-05)

The VRP panel reconsidered based on the new information and has decided to award $4,500 more. It'd be great if you can provide all information in the initial bug report in future. Thanks again for the report!

### he...@gmail.com (2020-08-05)

This is my mistake. Anyway, thank you for your generous rewards.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-10-07)

This issue was migrated from crbug.com/chromium/1095560?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1100118]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052594)*
