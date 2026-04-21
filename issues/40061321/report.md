# Security: heap-use-after-free in ProfileDestroyer::DestroyProfileNow

| Field | Value |
|-------|-------|
| **Issue ID** | [40061321](https://issues.chromium.org/issues/40061321) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-10-12 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 108.0.5356.0 (Developer Build) (64-bit)  

Operating System: Linux

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser process Crash State:

==1147118==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100018cbc0 at pc 0x556767b1418c bp 0x7ffc25782e50 sp 0x7ffc25782e48  

READ of size 8 at 0x61100018cbc0 thread T0 (chrome)  

#0 0x556767b1418b in DestroyProfileNow chrome/browser/profiles/profile\_destroyer.cc:159:16  

#1 0x556767b1418b in Timeout chrome/browser/profiles/profile\_destroyer.cc:323:3  

#2 0x556767b1418b in ProfileDestroyer::DestroyPendingProfilesForShutdown() chrome/browser/profiles/profile\_destroyer.cc:127:16  

#3 0x556767b80391 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:563:3  

#4 0x556767b635cd in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:534:35  

#5 0x5567675fb345 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#6 0x5567675fb345 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#7 0x5567675fb345 in BrowserProcessImpl::StartTearDown() chrome/browser/browser\_process\_impl.cc:453:22  

#8 0x5567675f6682 in ChromeBrowserMainParts::PostMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1931:21  

#9 0x55676095ecda in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() content/browser/browser\_main\_loop.cc:1092:13  

#10 0x5567609645b4 in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser\_main\_runner\_impl.cc:189:17  

#11 0x5567609586ad in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:32:16  

#12 0x5567673f3da4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:710:10  

#13 0x5567673f6f19 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1243:10  

#14 0x5567673f683c in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1103:12  

#15 0x5567673ef07c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:342:36  

#16 0x5567673ef689 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:370:10  

#17 0x556758489a37 in ChromeMain chrome/app/chrome\_main.cc:175:12  

#18 0x7fb801bfa082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61100018cbc0 is located 0 bytes inside of 248-byte region [0x61100018cbc0,0x61100018ccb8)  

freed by thread T0 (chrome) here:  

#0 0x556758487abd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x556767b0fdc3 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x556767b0fdc3 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x556767b0fdc3 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x556767b0fdc3 in ~pair buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:46:29  

#5 0x556767b0fdc3 in \_\_destroy\_at<std::Cr::pair<const Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile> > >, 0> buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:64:13  

#6 0x556767b0fdc3 in destroy\_at<std::Cr::pair<const Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile> > >, 0> buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:89:5  

#7 0x556767b0fdc3 in destroy<std::Cr::pair<const Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile> > >, void, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:315:9  

#8 0x556767b0fdc3 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::\_\_map\_value\_compare<Profile::OTRProfileID, std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::less[Profile::OTRProfileID](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>>>::erase(std::Cr::\_\_tree\_const\_iterator<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, void\*>\*, long>) buildtools/third\_party/libc++/trunk/include/\_\_tree:2423:5  

#9 0x556767b0c321 in \_\_erase\_unique[Profile::OTRProfileID](javascript:void(0);) buildtools/third\_party/libc++/trunk/include/\_\_tree:2446:5  

#10 0x556767b0c321 in erase buildtools/third\_party/libc++/trunk/include/map:1375:25  

#11 0x556767b0c321 in ProfileImpl::DestroyOffTheRecordProfile(Profile\*) chrome/browser/profiles/profile\_impl.cc:1004:17  

#12 0x556767b14452 in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:145:34  

#13 0x556767b0a223 in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile\_impl.cc:879:5  

#14 0x556767b0aa7d in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile\_impl.cc:849:29  

#15 0x556767b15268 in ProfileDestroyer::DestroyOriginalProfileNow(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:196:3  

#16 0x556767b11dd2 in DestroyProfileNow chrome/browser/profiles/profile\_destroyer.cc:162:5  

#17 0x556767b11dd2 in ProfileDestroyer::DestroyProfileWhenAppropriateWithTimeout(Profile\*, base::TimeDelta) chrome/browser/profiles/profile\_destroyer.cc:119:3  

#18 0x556767b7a37b in ProfileManager::ProfileInfo::~ProfileInfo() chrome/browser/profiles/profile\_manager.cc:1783:3  

#19 0x556767b81dfc in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#20 0x556767b81dfc in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#21 0x556767b81dfc in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#22 0x556767b81dfc in ~pair buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:46:29  

#23 0x556767b81dfc in \_\_destroy\_at<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, 0> buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:64:13  

#24 0x556767b81dfc in destroy\_at<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, 0> buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:89:5  

#25 0x556767b81dfc in destroy<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:315:9  

#26 0x556767b81dfc in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<base::FilePath, std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::less[base::FilePath](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1802:9  

#27 0x556767b80331 in clear buildtools/third\_party/libc++/trunk/include/\_\_tree:1839:5  

#28 0x556767b80331 in clear buildtools/third\_party/libc++/trunk/include/map:1380:37  

#29 0x556767b80331 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:562:18  

#30 0x556767b635cd in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:534:35  

#31 0x5567675fb345 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#32 0x5567675fb345 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#33 0x5567675fb345 in BrowserProcessImpl::StartTearDown() chrome/browser/browser\_process\_impl.cc:453:22  

#34 0x5567675f6682 in ChromeBrowserMainParts::PostMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1931:21  

#35 0x55676095ecda in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() content/browser/browser\_main\_loop.cc:1092:13  

#36 0x5567609645b4 in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser\_main\_runner\_impl.cc:189:17  

#37 0x5567609586ad in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:32:16  

#38 0x5567673f3da4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:710:10  

#39 0x5567673f6f19 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1243:10  

#40 0x5567673f683c in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1103:12  

#41 0x5567673ef07c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:342:36  

#42 0x5567673ef689 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:370:10  

#43 0x556758489a37 in ChromeMain chrome/app/chrome\_main.cc:175:12  

#44 0x7fb801bfa082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x55675848725d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x556767b1c3c9 in make\_unique<OffTheRecordProfileImpl, Profile \*&, const Profile::OTRProfileID &> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:26  

#2 0x556767b1c3c9 in Profile::CreateOffTheRecordProfile(Profile\*, Profile::OTRProfileID const&) chrome/browser/profiles/off\_the\_record\_profile\_impl.cc:654:15  

#3 0x556767b0ba6a in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&, bool) chrome/browser/profiles/profile\_impl.cc:983:7  

#4 0x55675896a6d0 in Profile::GetPrimaryOTRProfile(bool) chrome/browser/profiles/profile.cc:515:10  

#5 0x5567788cada5 in (anonymous namespace)::GetPrivateProfileIfRequested(base::CommandLine const&, StartupProfileInfo) chrome/browser/ui/startup/startup\_browser\_creator.cc:406:21  

#6 0x5567788c8c77 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::Cr::vector<Profile\*, std::Cr::allocator<Profile\*>> const&) chrome/browser/ui/startup/startup\_browser\_creator.cc:939:7  

#7 0x5567788c875f in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::Cr::vector<Profile\*, std::Cr::allocator<Profile\*>> const&) chrome/browser/ui/startup/startup\_browser\_creator.cc:635:10  

#8 0x5567675f3e5b in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome\_browser\_main.cc:1778:25  

#9 0x5567675f2335 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1181:18  

#10 0x55676095c6cd in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser\_main\_loop.cc:952:28  

#11 0x55676096189f in Invoke<int (content::BrowserMainLoop::\*)(), content::BrowserMainLoop \*> base/functional/bind\_internal.h:647:12  

#12 0x55676096189f in MakeItSo<int (content::BrowserMainLoop::\*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::RawPtrBanDanglingIfSupported> > > base/functional/bind\_internal.h:826:12  

#13 0x55676096189f in RunImpl<int (content::BrowserMainLoop::\*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::RawPtrBanDanglingIfSupported> >, 0UL> base/functional/bind\_internal.h:920:12  

#14 0x55676096189f in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::RawPtrBanDanglingIfSupported>>, int ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:871:12  

#15 0x556761d5fb38 in Run base/functional/callback.h:145:12  

#16 0x556761d5fb38 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup\_task\_runner.cc:43:29  

#17 0x55676095bc32 in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser\_main\_loop.cc:863:25  

#18 0x556760963b63 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) content/browser/browser\_main\_runner\_impl.cc:141:15  

#19 0x556760958632 in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:26:32  

#20 0x5567673f3da4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:710:10  

#21 0x5567673f6f19 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1243:10  

#22 0x5567673f683c in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1103:12  

#23 0x5567673ef07c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:342:36  

#24 0x5567673ef689 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:370:10  

#25 0x556758489a37 in ChromeMain chrome/app/chrome\_main.cc:175:12  

#26 0x7fb801bfa082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/profiles/profile\_destroyer.cc:159:16 in DestroyProfileNow  

Shadow bytes around the buggy address:  

0x61100018c900: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00  

0x61100018c980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x61100018ca00: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

0x61100018ca80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x61100018cb00: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

=>0x61100018cb80: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd  

0x61100018cc00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61100018cc80: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa  

0x61100018cd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61100018cd80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x61100018ce00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

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

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to the crash.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==1147118==ABORTING

**Client ID (if relevant): [see link above]**

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 15.4 KB)

## Timeline

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2022-10-12)

[Comment Deleted]

### jd...@chromium.org (2022-10-12)

arthursonzogni@: would you mind taking a look at this one, too, since you fixed https://crbug.com/chromium/1337388?

I haven't tried to reproduce this, but it seems plausible, so forwarding it along.

[Monorail components: Services>SignIn]

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### ar...@chromium.org (2022-10-13)

Thanks!

I don't really follow the explanation in https://crbug.com/chromium/1373941#c2. See below: 

> When profiles_info_ is cleared in [1], owned_profile_ is released in the destructor of ProfileInfo ([3])

Note: here, it is not freed. The ownership is just moved toward the ProfileDestroyer.

> As a result, the DestroyProfileNow method will still reference the freed object.

Where was it freed?

---

Would you have a way for someone to reproduce the bug?

### ar...@chromium.org (2022-10-13)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2022-10-13)


Please see the ASan log for detailed release process.

```
ProfileManager::ProfileInfo::~ProfileInfo() {
  // Regardless of sync or async creation, we always take ownership right after
  // Profile::CreateProfile(). So we should always own the Profile by this
  // point.
  DCHECK(owned_profile_);
  DCHECK_EQ(owned_profile_.get(), unowned_profile_);
  unowned_profile_ = nullptr;
  ProfileDestroyer::DestroyProfileWhenAppropriate(owned_profile_.release());            // [1]
}
```

The owned_profile_ is not freed by release(), but by the ProfileDestroyer::DestroyProfileWhenAppropriate method.

```
void ProfileImpl::DestroyOffTheRecordProfile(Profile* otr_profile) {
  CHECK(otr_profile);
  OTRProfileID profile_id = otr_profile->GetOTRProfileID();
  DCHECK(HasOffTheRecordProfile(profile_id));
  otr_profiles_.erase(profile_id);                                                      // [4]
#if BUILDFLAG(ENABLE_EXTENSIONS)
```

The pointer that actually causes the bug is otr_profiles_, which is a member variable of the ProfileImpl object.

[1] https://chromium.googlesource.com/chromium/src/+/fa21164ee80884660b5441bd7d0f8191a5f60978/chrome/browser/profiles/profile_manager.cc#1783
[2] https://chromium.googlesource.com/chromium/src/+/fa21164ee80884660b5441bd7d0f8191a5f60978/chrome/browser/profiles/profile_destroyer.cc#119
[3] https://chromium.googlesource.com/chromium/src/+/fa21164ee80884660b5441bd7d0f8191a5f60978/chrome/browser/profiles/profile_destroyer.cc#196
[4] https://chromium.googlesource.com/chromium/src/+/fa21164ee80884660b5441bd7d0f8191a5f60978/chrome/browser/profiles/profile_destroyer.cc#196

0x61100018cbc0 is located 0 bytes inside of 248-byte region [0x61100018cbc0,0x61100018ccb8)
freed by thread T0 (chrome) here:
    #0 0x556758487abd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x556767b0fdc3 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #2 0x556767b0fdc3 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
...
    #9 0x556767b0c321 in __erase_unique<Profile::OTRProfileID> buildtools/third_party/libc++/trunk/include/__tree:2446:5
    #10 0x556767b0c321 in erase buildtools/third_party/libc++/trunk/include/map:1375:25
    #11 0x556767b0c321 in ProfileImpl::DestroyOffTheRecordProfile(Profile*) chrome/browser/profiles/profile_impl.cc:1004:17                                             // [4]
    #12 0x556767b14452 in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile*) chrome/browser/profiles/profile_destroyer.cc:145:34
    #13 0x556767b0a223 in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:879:5
    #14 0x556767b0aa7d in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:849:29
    #15 0x556767b15268 in ProfileDestroyer::DestroyOriginalProfileNow(Profile*) chrome/browser/profiles/profile_destroyer.cc:196:3                                      // [3]
    #16 0x556767b11dd2 in DestroyProfileNow chrome/browser/profiles/profile_destroyer.cc:162:5
    #17 0x556767b11dd2 in ProfileDestroyer::DestroyProfileWhenAppropriateWithTimeout(Profile*, base::TimeDelta) chrome/browser/profiles/profile_destroyer.cc:119:3      // [2]
    #18 0x556767b7a37b in ProfileManager::ProfileInfo::~ProfileInfo() chrome/browser/profiles/profile_manager.cc:1783:3                                                 // [1]
    #19 0x556767b81dfc in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #20 0x556767b81dfc in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
...
    #28 0x556767b80331 in clear buildtools/third_party/libc++/trunk/include/map:1380:37
    #29 0x556767b80331 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile_manager.cc:562:18
    #30 0x556767b635cd in ProfileManager::~ProfileManager() chrome/browser/profiles/profile_manager.cc:534:35

### ne...@nesk.kr (2022-10-13)

[4] https://chromium.googlesource.com/chromium/src/+/fa21164ee80884660b5441bd7d0f8191a5f60978/chrome/browser/profiles/profile_impl.cc#1004

### ar...@chromium.org (2022-10-13)

Thanks! I understand now.

### [Deleted User] (2022-10-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2022-10-14)

https://chromium-review.googlesource.com/c/chromium/src/+/3956736

### ar...@chromium.org (2022-10-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83036b69fe85eabfe352d3401d42514372564cf6

commit 83036b69fe85eabfe352d3401d42514372564cf6
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Wed Oct 19 10:18:38 2022

Profile: Fix UAF in DestroyProfileNow

The whole memory ownership tracking for Profile is fragile. It also
depends on:
- The type of the Profile (Original, Off-the-Record, System, ...)
- The platform (ChromeAsh, Android, etc...)

To fix a use after free. This patch:
- Add `Profile::GetWeakPtr()`
- Make ProfileDestroyer to use weak pointer instead. We now assume they can be
  destroyed at any time.

Bug: 1373941
Change-Id: Id896a697bf7c546669e5a34b5fb11c04e1aad14f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3956736
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Mihai Sardarescu <msarda@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1060935}

[modify] https://crrev.com/83036b69fe85eabfe352d3401d42514372564cf6/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/83036b69fe85eabfe352d3401d42514372564cf6/chrome/browser/profiles/profile.cc
[modify] https://crrev.com/83036b69fe85eabfe352d3401d42514372564cf6/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/83036b69fe85eabfe352d3401d42514372564cf6/chrome/browser/profiles/profile_destroyer_unittest.cc
[modify] https://crrev.com/83036b69fe85eabfe352d3401d42514372564cf6/chrome/browser/profiles/profile.h


### ar...@chromium.org (2022-10-19)

nesk@

The patch above should have fixed the issue. If you can, it would be helpful you could confirm the fuzzer can no longer detect any issue about it.

I will wait for the patch to be used by one canary version, and then ask for a beta merge.

### ne...@nesk.kr (2022-10-19)

Yes, so far the bug doesn't seem to be happening anymore.
I've tested with the following version.
asan-linux-release-1061011 (65292347a16bf29be360df201005b5096edacfd7)

### ar...@chromium.org (2022-10-19)

> asan-linux-release-1061011 (65292347a16bf29be360df201005b5096edacfd7)

Thanks! 1061011 > 1060935, so you tried the fixed version: https://chromiumdash.appspot.com/commit/83036b69fe85eabfe352d3401d42514372564cf6



### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-10-20)

Merge for your CL has been approved for M108, please help complete these merges asap before end of day Friday PST this week so these changes can be part of dev release next week

if your merge is already complete, please remove the merge-approved-108 label.

### gi...@appspot.gserviceaccount.com (2022-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53bd0edcd492389a2e445e11bdfb7195d162aaf5

commit 53bd0edcd492389a2e445e11bdfb7195d162aaf5
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Oct 20 19:19:24 2022

Profile: Fix UAF in DestroyProfileNow

The whole memory ownership tracking for Profile is fragile. It also
depends on:
- The type of the Profile (Original, Off-the-Record, System, ...)
- The platform (ChromeAsh, Android, etc...)

To fix a use after free. This patch:
- Add `Profile::GetWeakPtr()`
- Make ProfileDestroyer to use weak pointer instead. We now assume they can be
  destroyed at any time.

(cherry picked from commit 83036b69fe85eabfe352d3401d42514372564cf6)

Bug: 1373941
Change-Id: Id896a697bf7c546669e5a34b5fb11c04e1aad14f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3956736
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Mihai Sardarescu <msarda@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1060935}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3968069
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#155}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/53bd0edcd492389a2e445e11bdfb7195d162aaf5/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/53bd0edcd492389a2e445e11bdfb7195d162aaf5/chrome/browser/profiles/profile.cc
[modify] https://crrev.com/53bd0edcd492389a2e445e11bdfb7195d162aaf5/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/53bd0edcd492389a2e445e11bdfb7195d162aaf5/chrome/browser/profiles/profile_destroyer_unittest.cc
[modify] https://crrev.com/53bd0edcd492389a2e445e11bdfb7195d162aaf5/chrome/browser/profiles/profile.h


### [Deleted User] (2022-10-20)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-11-01)

LTS new guidelines, not taking Medium severity bugs.

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, n3sk! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1373941?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061321)*
