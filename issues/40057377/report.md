# Security: heap-use-after-free in PrefChangeRegistrar::~PrefChangeRegistrar

| Field | Value |
|-------|-------|
| **Issue ID** | [40057377](https://issues.chromium.org/issues/40057377) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments, Internals |
| **Platforms** | Linux, Windows |
| **Reporter** | me...@gmail.com |
| **Assignee** | du...@chromium.org |
| **Created** | 2021-09-24 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1. apply the patch and compile chrome
2. start a server: `python -m SimpleHTTPServer 8605`
3. ./chrome --incognito http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
Chrome will use OffTheRecordProfileImpl in incognito mode. When ~OffTheRecordProfileImpl() [1]is called, it will call DestroyFactoriesInOrder()[2] to destroy the KeyedService, including ClientSideDetectionService.
However, if we could close the browser before ClientSideDetectionService was added to the  `dependency_manager_`[3], there will still be a ClientSideDetectionService instance but  DestroyFactoriesInOrder() will not destroy it, because it was not in the  `destruction_order1`[4]. After ~OffTheRecordProfileImpl(), ClientSideDetectionServiceFactory will destruct ClientSideDetectionService, which will call ~PrefChangeRegistrar()[5] and use `PrefServiceSyncable` in function RemoveAll(). But `PrefServiceSyncable` has been deleted in ~OffTheRecordProfileImpl() => UAF occurs.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/off_the_record_profile_impl.cc;l=218;drc=858dba0e633d254450dec76ffb53e7433f6fb477;bpv=0;bpt=0
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/core/dependency_manager.cc;l=148;drc=fc723c22d630f206c338b04881ab69e3287de071;bpv=0;bpt=0
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/core/keyed_service_base_factory.cc;l=28;drc=131fe11afea739154e72f430a80aa5db6fc18b6d;bpv=0;bpt=0
[4] https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/core/dependency_manager.cc;l=127;drc=fc723c22d630f206c338b04881ab69e3287de071;bpv=0;bpt=0
[5] https://source.chromium.org/chromium/chromium/src/+/main:components/prefs/pref_change_registrar.cc;l=23;drc=805a9df0b462c26bbd0b05dc69c6779483758176;bpv=0;bpt=0

It's difficult to reproduce this UAF because you cannot precisely control when the browser is closed. So I patch the code in `PerformInterlockedTwoPhaseShutdown` to simulate that ClientSideDetectionService is not in the `destruction_order1`. BTW, other keyedservices could also trigger this problem, I happen to reproduce it with HostContentSettingsMap without any patches. You can see the asan log for more information.

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: n/a
OS Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 171 B)
- [asan.HostContentSettingsMap](attachments/asan.HostContentSettingsMap) (application/octet-stream, 20.7 KB)
- [patch](attachments/patch) (text/plain, 1.1 KB)
- [logs.asan](attachments/logs.asan) (text/plain, 23.3 KB)
- [video.webm](attachments/video.webm) (video/webm, 8.0 MB)
- [poc.html](attachments/poc.html) (text/plain, 8.1 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [uesrdata.zip](attachments/uesrdata.zip) (application/octet-stream, 8.2 MB)
- [poc.html](attachments/poc.html) (text/plain, 8.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [backtrace.txt](attachments/backtrace.txt) (text/plain, 17.7 KB)

## Timeline

### [Deleted User] (2021-09-24)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-09-24)

I will upload the ASAN log of `ClientSideDetectionService` ASAP.

### aj...@google.com (2021-09-24)

1st few frames of the asan.HostContentSettingsMap (monorail does not "open" the file):

==2270600==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160000c7b80 at pc 0x55f6b98e282d bp 0x7ffe417ad080 sp 0x7ffe417ad078
READ of size 8 at 0x6160000c7b80 thread T0 (chrome)
    #0 0x55f6b98e282c in RemoveAll components/prefs/pref_change_registrar.cc:60:15
    #1 0x55f6b98e282c in PrefChangeRegistrar::~PrefChangeRegistrar() components/prefs/pref_change_registrar.cc:23:3
    #2 0x55f6bde601a7 in ~PolicyProvider components/content_settings/core/browser/content_settings_policy_provider.cc:235:1
    #3 0x55f6bde601a7 in content_settings::PolicyProvider::~PolicyProvider() components/content_settings/core/browser/content_settings_policy_provider.cc:233:35
    #4 0x55f6bde5c10d in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #5 0x55f6bde5c10d in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #6 0x55f6bde5c10d in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #7 0x55f6bde5c10d in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #8 0x55f6bde5c10d in destroy<std::__1::pair<const HostContentSettingsMap::ProviderType, std::__1::unique_ptr<content_settings::ProviderInterface, std::__1::default_delete<content_settings::ProviderInterface> > >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15


### aj...@google.com (2021-09-24)

In a dcheck build I hit this:-

KeyedServiceFactory::KeyedServiceFactory(const char* name,
                                         DependencyManager* manager,
                                         Type type)
    : KeyedServiceBaseFactory(name, manager, type) {}

KeyedServiceFactory::~KeyedServiceFactory() {
  DCHECK(mapping_.empty());
}

=================================================================
==32052==ERROR: AddressSanitizer: breakpoint on unknown address 0x7ff941fb1a5b (pc 0x7ff941fb1a5b bp 0x002875dff400 sp 0x002875dff330 T0)
==32052==*** WARNING: Failed to initialize DbgHelp!              ***
==32052==*** Most likely this means that the app is already      ***
==32052==*** using DbgHelp, possibly with incompatible flags.    ***
==32052==*** Due to technical reasons, symbolization might crash ***
==32052==*** or produce wrong results.                           ***
    #0 0x7ff941fb1a5a in base::debug::BreakDebuggerAsyncSafe C:\src\chromium\src\base\debug\debugger_win.cc:27
    #1 0x7ff941fb1a5a in base::debug::BreakDebugger(void) C:\src\chromium\src\base\debug\debugger_win.cc:35:3
    #2 0x7ff941d0d308 in logging::LogMessage::~LogMessage(void) C:\src\chromium\src\base\logging.cc:881:7
    #3 0x7ff941d10886 in logging::LogMessage::`scalar deleting dtor'(unsigned int) C:\src\chromium\src\base\logging.cc:576:27
    #4 0x7ff943615d7a in KeyedServiceFactory::~KeyedServiceFactory(void) C:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:22:3
    #5 0x7ff950b26b37 in safe_browsing::ClientSideDetectionServiceFactory::`scalar deleting dtor'(unsigned int) C:\src\chromium\src\chrome\browser\safe_browsing\client_side_detection_service_factory.h:35:57
    #6 0x7ff950b26ed2 in base::DefaultSingletonTraits<safe_browsing::ClientSideDetectionServiceFactory>::Delete C:\src\chromium\src\base\memory\singleton.h:54
    #7 0x7ff950b26ed2 in base::Singleton<class safe_browsing::ClientSideDetectionServiceFactory, struct base::DefaultSingletonTraits<class safe_browsing::ClientSideDetectionServiceFactory>, class safe_browsing::ClientSideDetectionServiceFactory>::OnExit(void *) C:\src\chromium\src\base\memory\singleton.h:268:5
    #8 0x7ff941c500e3 in base::OnceCallback<void ()>::Run C:\src\chromium\src\base\callback.h:100
    #9 0x7ff941c500e3 in base::AtExitManager::ProcessCallbacksNow(void) C:\src\chromium\src\base\at_exit.cc:93:28
    #10 0x7ff941c4faff in base::AtExitManager::~AtExitManager(void) C:\src\chromium\src\base\at_exit.cc:45:5
    #11 0x7ff93b3a7c01 in std::__1::default_delete<base::AtExitManager>::operator() C:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:54
    #12 0x7ff93b3a7c01 in std::__1::unique_ptr<class base::AtExitManager, struct std::__1::default_delete<class base::AtExitManager>>::reset(class base::AtExitManager *) C:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315:7
    #13 0x7ff93b3a7a18 in content::ContentMainRunnerImpl::Shutdown(void) C:\src\chromium\src\content\app\content_main_runner_impl.cc:1132:17
    #14 0x7ff93b3a18be in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\src\chromium\src\content\app\content_main.cc:408:24
    #15 0x7ff93b3a2bce in content::ContentMain(struct content::ContentMainParams const &) C:\src\chromium\src\content\app\content_main.cc:418:10
    #16 0x7ff93115159a in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:172:12
    #17 0x7ff6d0e58dfa in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:169:12
    #18 0x7ff6d0e53c7a in main C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382:20
    #19 0x7ff6d13fe60f in invoke_main d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #20 0x7ff6d13fe60f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #21 0x7ff9f5557033  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #22 0x7ff9f7202650  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

AddressSanitizer can not provide additional info.

----------------
Setting as severity=medium as this is mitigated by needing to happen at shutdown. Let us know if you can create a more reliable poc.

Assigning to blundell based on KeyedService OWNERS as this seems systemic. Feel free to CC in others who may be able to help resolve this issue. 

[Monorail components: Internals]

### [Deleted User] (2021-09-24)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-25)

I can repro the ClientSideDetectionService stack (attached) but perhaps this is really incognito profile related. CC'd some profile folks for any ideas.

### [Deleted User] (2021-09-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2021-09-27)

It looks like some keyed services may still be alive after the incognito profile shutdown.

I don't think the patch is super useful, because it merely shows that leaking services causes a crash, which is not surprising.
What would be interesting is to know how it happened.

Do you have repro steps without that patch? Even if they are unreliable it may help understand what is causing this.

My guess (but it's only a guess at this point) is that maybe the HostContentSettingsMap has been created after the profile shutdown?


### me...@gmail.com (2021-09-27)

Just open browser in incognito and close, repeatedly. But it is really unreliable.

### dr...@chromium.org (2021-09-27)

Taking the bug, I started looking into the code.

Another possible cause is that HostContentSettingsMap seems to delete its state in its destructor, whereas maybe it should do that in Shutdown(). This is especially important because HostContentSettingsMap is refcounted, so there's no guarantee that the profile is still alive at destruction.

### dr...@chromium.org (2021-09-27)

Noting my current observations here:
- the crash happens because a PolicyProvider in  HostContentSettingsMap::content_settings_providers_ is still holding a reference to profile when destroyed
- PolicyProvider has the same lifetime as HostContentSettingsMap (constructed and destroyed at the same time, and also has a  ShutdownOnUIThread() method)

This would point to either ShutdownOnUIThread() 1) not being called or 2) not releasing the reference to the profile. However, so far I'm not seeing anything wrong in the code that would cause either of those.

### dr...@chromium.org (2021-09-27)

merc.ouc@gmail.com, I have a few more questions:
1)  I could not repro the crash.  Are you launching chrome with --incognito parameter? What are the exact steps to repro?
2) I assume your build did not have DCHECKs enabled. If you could repro the bug (without the patch) with DCHECKs enabled, I think it's likely we would hit a DCHECK and  it would be easier to pinpoint the cause.


I could repro a similar UAF by calling HostContentSettingsMapFactory::GetForProfile() after profile shutdown, so this is still my best guess.
If this is what is happening, it will be hard to find without a repro.
Luckily, I think this would fire multiple DCHECKs if it happens.

### [Deleted User] (2021-09-27)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-09-28)

Hi droger@, 
1) Actually I find this by fuzzing occasionally, and I run chrome with "--incognito". My fuzzer just open chrome with some samples and then close it, over and over again.  But the ASAN log shows that there are nothing wrong with the samples, just an incognito browser can trigger this.
2) Yes I run it without DCHECKs enabled.  However this bug cannot be reproduced easily without patch, I don't know which DCHECKs it will hit.
Hope these are useful to you.

### dr...@chromium.org (2021-09-28)

Ok, thank you. I don't think this bug is actionable without repro steps.
The patch does not really count here, as the patch directly introduces a crash (i.e. the correct way to fix the crash in that state is just to remove the patch), and it's not the same cause as the real crash in HostContentSettingsMap.

Lowering the priority and assigning the bug to an owner of HostContentSettingsMap, as I suspect it's caused by some code calling HostContentSettingsMapFactory::GetForProfile() in the middle or after profile shutdown.

### du...@chromium.org (2021-10-06)

It is expected that HostContentSettingsMap can live longer than the Profile as it is still needed after shutdown of some other services. E.g. for cookie deletion on exit.
This means that HostContentSettingsMap and all of its providers drop all profile-related references in ShutdownOnUIThread(). The PolicyProvider does this as well and it also calls RemoveAll() on pref_change_registrar. So it is really weird that pref_change_registrar crashes when PolicyProvider is destroyed.

If it is possible to create a HostContentSettingsMap after Profile shutdown, maybe we could detect this by adding some DCHECK into the HCSM constructor to ensure that it is not created for a dead Profile?

### du...@chromium.org (2021-10-06)

What I don't understand is how this is related to ClientSideDetectionServiceFactory, which is mentioned in many comments?

### dr...@chromium.org (2021-10-07)

I don't think this is related to ClientSideDetectionServiceFactory.

The OP had a crash in ClientSideDetectionServiceFactory, but this was caused by a local change they had in their build, so there's nothing to do about that.
However they mention:

> I happen to reproduce it with HostContentSettingsMap without any patches

As far as I understand they trigger the bug using fuzzing, and by launching Chrome with the --incognito command line parameter, but I don't have more details than this.

### me...@gmail.com (2021-10-12)

Hi, I find a way to trigger this UAF without any patches. But it seems need a old `user-data-dir`, if I change another new user-data-dir, it will noe be triggered. If you need the user-data-dir I will upload it AND it's about 400M.

setp:
1. download asan-linux-release-930377.zip  and unzip
2. start a http server :  `python -m SimpleHTTPServer 8605`
3. ./chrome --enable-blink-features=MojoJS    --user-data-dir=/tmp/noexit123     http://127.0.0.1:8605/poc.html  http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html  http://127.0.0.1:8605/poc.html
4. After you see the "second" picture in picture is shown, close the browser.


### [Deleted User] (2021-10-20)

dullweber: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2021-11-03)

hi, any updates?

### [Deleted User] (2021-11-04)

dullweber: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@google.com (2021-11-04)

I tried the PoC in Chrome Dev (97.0.4688.2) and sadly couldn't reproduce any crashes. I'm also not sure what it is trying to trigger by opening this file a bunch of times? Further above, you mentioned that it only triggers in incognito mode and there is no --incognito parameter?

### me...@gmail.com (2021-11-05)

Sorry there is a mistake, it can be triggered in non incognito mode...

### du...@google.com (2021-11-05)

Not triggering on my side. I'm also not sure where these windows that are popping up in your video are coming from? 

### me...@gmail.com (2021-11-06)

That’s the window of Picture in Picture.

### me...@gmail.com (2021-11-09)

Hi, if you still can't repro that, maybe you can download the userdata.zip and use it as the `--user-data-dir`

Step:
1. download asan-linux-release-939207.zip  and unzip
2. `mkdir out` and copy `poc.html` and `copy_mojo_js_bindings.py` to `out`.
3.  cd to `out` and `python copy_mojo_js_bindings.py /path/to/asan-linux-release-939207/gen/`
4. start a http server at `out` :  `python -m SimpleHTTPServer 8605`
5. unzip userdata.zip to get `noexist` directory.
6. ./chrome --enable-blink-features=MojoJS    --user-data-dir=/PATH/TO/noexist  http://127.0.0.1:8605/poc.html  http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html  http://127.0.0.1:8605/poc.html
7. After you see the "second" pictureInpicture window is shown, close the browser.

### rh...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-11-24)

[Comment Deleted]

### me...@gmail.com (2022-01-05)

Hi, after debugging this problem, I finally find a simple poc that can easily trigger this UAF. 
Repo:
1. download asan-linux-release-955038.zip and unzip
2. at the folder of poc.html create a file:  `touch no.js`  and start a server: 1python -m SimpleHTTPServer 86051
3. ./chrome --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html

And I also find a root cause:
~ProfileImpl() will call ShutdownStoragePartitions()[1], and it will finally create another `HostContentSettingsMapFactory`[2]. `HostContentSettingsMapFactory` is a keyed_service, so it was created at the beginning of chrome firstly. Now we have two  `HostContentSettingsMapFactory` . ~ProfileImpl() will delete one and when another one is destructed, UAF occurs.

Specifically, `HostContentSettingsMapFactory` will create a `HostContentSettingsMap`, `HostContentSettingsMap` has member `std::map<ProviderType,std::unique_ptr<content_settings::ProviderInterface>>   content_settings_providers_;`. The value of this map is `ProviderInterface`, the actual class used there is `PolicyProvider`. `PolicyProvider` has a member `PrefChangeRegistrar pref_change_registrar_;`, `PrefChangeRegistrar ` has a member `service_`, this `service_` is a raw pointer created by `CreateSyncable`[3], `CreateSyncable` will create a unique_ptr owned by `ProfileImpl`, and `service_` is assigned with unique_ptr.get(). So after ~ProfileImpl(), this unique_ptr is reset and `service_` is also deleted. When we destruct seond `HostContentSettingsMap`, this `service_` is used again => UAF. This explains why ASAN report like this.


I provide the call stack when `HostContentSettingsMapFactory` is called the second time, we could infer that `payment` and `service worker` could create another `HostContentSettingsMapFactory`. So my poc uses a service worker and payment API.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=926;drc=45dc15e901ba2d7ca5549c9551ccb1cb3f6f9ec5;bpv=1;bpt=0
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/content_settings/host_content_settings_map_factory.cc;l=84;drc=e09bfa3d5c3078e3ae189fe9ce5bef6a4d70831c;bpv=0;bpt=0
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/sync_preferences/pref_service_syncable_factory.cc;l=58;drc=2ff27e52ab7c6bc47b275da47ed62a2616d79553;bpv=0;bpt=0

### me...@gmail.com (2022-01-10)

[Comment Deleted]

### du...@chromium.org (2022-01-10)

Thanks for the improved test case. I can reproduce the issue! 

In debug builds, there is actually a NOTREACHED() that gets triggered when we attempt to create a service after profile shutdown: https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/core/dependency_manager.cc;l=169;drc=bd1b0b6a99ed26149b2a9ec1e2c75f9e499b31f9

In release builds, this only triggers a silent crash report. Maybe we should just put a hard CHECK() here to avoid any potential use-after-free?
This only seems to happen very rarely in real usage: http://crash/browse?q=product_name%3D%27Chrome%27+AND+product.Version%3E%3D%2796.%27+AND+EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+FunctionName%3D%27DependencyManager%3A%3AAssertContextWasntDestroyed%28void+*%29%27%29#+samplereports,productname:1000,productversion:50,magicsignature:50,magicsignature2:50,stablesignature:50,clientid:20,url:30,simplifiedurl:30,experiments:1000,country:30

For the cases that access a HostContentSettingsMap after shutdown, we should ensure that they obtain a scoped_refptr before shutdown is started. This will ensure that HostContentSettingsMap is not created again.

### du...@chromium.org (2022-01-10)

I can't find any case where HostContentSettingsMap is the service that is causing the issue. I assume the poc only works if Chrome is started directly with the html as argument. Otherwise, a website can't trigger a whole browser shutdown?

### du...@chromium.org (2022-01-10)

I created https://crrev.com/c/3376968 to turn a potential use-after-free into a clean crash: https://crrev.com/c/3376968

PaymentAppDatabase::DidReadAllPaymentInstruments seems to be triggered by a WrapCallbackWithDefaultInvokeIfNotRun. This triggers the callback on shutdown.
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_registry.cc;l=687;drc=bd1b0b6a99ed26149b2a9ec1e2c75f9e499b31f9

The callback passes an error but PaymentAppDatabase::DidReadAllPaymentInstruments still calls its callback.
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/payments/payment_app_database.cc;l=702;drc=bd1b0b6a99ed26149b2a9ec1e2c75f9e499b31f9

I'll land the CL mentioned above and reassing to a payments owner for this specific crash. Please see comments from #32. I can easily reproduce the crash using the poc.html file and a build with DCHECKs enabled.

[Monorail components: Blink>Payments]

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91dd0b4e79848d9fc1c23324981efe20d9fd4a91

commit 91dd0b4e79848d9fc1c23324981efe20d9fd4a91
Author: Christian Dullweber <dullweber@chromium.org>
Date: Mon Jan 10 14:56:57 2022

Prevent use-after-free if a KeyedService is accessed after shutdown

KeyedServices should not get created during shutdown. This is prevented
in debug builds by a NOTREACHED() but only leads to a silent crash
report in release builds. Considering that this can lead to security
bugs, we should have a hard CHECK(false) to prevent services from being
created during shutdown.

Bug: 1252716
Change-Id: I079cb6d8da8bcebb0b0e369ad4f67e2764fbc986
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3376968
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Reviewed-by: Colin Blundell <blundell@chromium.org>
Commit-Queue: Christian Dullweber <dullweber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957059}

[modify] https://crrev.com/91dd0b4e79848d9fc1c23324981efe20d9fd4a91/components/keyed_service/core/dependency_manager.cc
[modify] https://crrev.com/91dd0b4e79848d9fc1c23324981efe20d9fd4a91/components/keyed_service/core/dependency_manager.h


### ma...@chromium.org (2022-01-10)

[Comment Deleted]

### ma...@chromium.org (2022-01-10)

[Comment Deleted]

### ma...@chromium.org (2022-01-10)

ah, was looking at the wrong lines. DidReadAllPaymentInstruments() and DidReadAllPaymentApps() are very similar in names and structure. 

@rouslan, do you think the solution is to call the callback[1] with an empty map in PaymentAppDatabase::DidReadAllPaymentInstruments()[1] when error?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/payments/payment_app_database.cc;l=734;drc=bd1b0b6a99ed26149b2a9ec1e2c75f9e499b31f9

### ma...@chromium.org (2022-01-10)

WIP: https://chromium-review.googlesource.com/c/chromium/src/+/3378182

### ro...@chromium.org (2022-01-10)

That sounds like a good change from the consistency perspective, because the rest of the error code uses the empty map. Does this change fix the crash, though?

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/abfb897cfe10707226bb41ec6ee5c0ae2d800a06

commit abfb897cfe10707226bb41ec6ee5c0ae2d800a06
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Mon Jan 10 21:24:28 2022

Not to send Payment apps for permission check when service worker errors

Before the change, when a payment app was being registered while the
window was shutting down, the payment apps would still be sent for
permission checks, causing a crash.

After the change, in the same situation, the payment apps would not be
sent for permission checks.

Bug: 1252716
Change-Id: I9f0f80eadfdc598ee5f1c6e41fd56975b32df2a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378182
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957248}

[modify] https://crrev.com/abfb897cfe10707226bb41ec6ee5c0ae2d800a06/content/browser/payments/payment_app_database.cc


### ma...@chromium.org (2022-01-10)

#42, yep it fixes the crash. I've verified.

### du...@chromium.org (2022-01-11)

Awesome, thanks :) 

### ro...@chromium.org (2022-01-11)

Does this need a merge into dev and beta branches?

### du...@chromium.org (2022-01-11)

We could merge #43 into M98? 

I'm less comfortable about the change in #37 as it could introduce crashes. Although the crash dashboard lists very cases that currently record a "dumpWithoutCrashing"

### ma...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-01-11)

I will wait until the commit to be released to Canary before requesting the merge.

### ma...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-01-12)

https://crbug.com/chromium/1252716#c43 hasn't been released to Canary yet.

### ma...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2022-01-13)

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
Yes. It's a UAF security bug.

What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3378182

Have the changes been released and tested on canary?
Yes

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
N/A

### ma...@chromium.org (2022-01-13)

For those who want to test on Canary and MacOs, please follow https://crbug.com/chromium/1252716#c32 and use the command:
/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary http://127.0.0.1:8605/poc.html

### sr...@google.com (2022-01-13)

Merge approved for m98 branch:4758 pls merge asap 

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/836ea11d0c5e81087183d91285d23048b88c3a67

commit 836ea11d0c5e81087183d91285d23048b88c3a67
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Fri Jan 14 01:34:10 2022

[M98] Not to send Payment apps for permission check when service worker errors

Before the change, when a payment app was being registered while the
window was shutting down, the payment apps would still be sent for
permission checks, causing a crash.

After the change, in the same situation, the payment apps would not be
sent for permission checks.

(cherry picked from commit abfb897cfe10707226bb41ec6ee5c0ae2d800a06)

Bug: 1252716
Change-Id: I9f0f80eadfdc598ee5f1c6e41fd56975b32df2a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378182
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957248}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3387429
Cr-Commit-Position: refs/branch-heads/4758@{#598}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/836ea11d0c5e81087183d91285d23048b88c3a67/content/browser/payments/payment_app_database.cc


### ma...@chromium.org (2022-01-14)

The payment side has been fixed.

Assigning back to @dullweber because payment is subsidiary to the original issue.

### ro...@chromium.org (2022-01-14)

[Empty comment from Monorail migration]

### du...@chromium.org (2022-01-14)

I think there is nothing further to do. Thanks for quickly resolving the payments issue :)

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-15)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M96, which branched on 2021-10-07 (Chromium branch: 4664, Chromium branch position: 929512)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@chromium.org (2022-01-17)

I don't think we need to merge this back to M96? It looks like the UaF can only be triggered if a website is able to initiate a shutdown of Chrome. This only seems possible if Chrome is started with the website as an argument. Otherwise window.close() doesn't work.

### me...@gmail.com (2022-01-28)

[Comment Deleted]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### me...@gmail.com (2022-02-04)

This bug is a browser UAF and don’t need any flag or user interaction. Could you please reconsider the bounty?

### am...@chromium.org (2022-02-04)

It appears that this triggering this UAF requires browser shutdown and can only be triggered if the website itself is able to initiate that browser shutdown, which is reliant on starting Chrome with the website as an argument. As this issue UAF is triggered upon browser shutdown it provides quite a bit less of attacker control to exploit, which is why the reward amount was decided at $7,000, which is consistent for browser UAF with this amount of mitigation. 
You responded to the reward automation comment before I had a chance to follow up with that information first. 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-02-12)

[Comment Deleted]

### me...@gmail.com (2022-02-22)

any reply to this one? An uaf with complex user interaction can get $15,000,  but this one don't need any interaction any just need to close browse only get half of that, is that sounds reasonable?  As I said in 76, many issues also need to close browser, but it also get a reasonable bounty, I know you update your bounty rules, but this one don't need any interaction. And I have submit this issue Sep 24,2021, but you don't fix it until I totally analyse it and provide a clear and simple poc. So I feel so unfair and upset.

### me...@gmail.com (2022-02-22)

[Comment Deleted]

### am...@chromium.org (2022-02-22)

We are happy to reassess as the next panel discussion, but just to provide some context in advance. This was not judged as memory corruption a highly privileged process but was judged as memory corruption in the browser process, but requiring browser shutdown (repeatedly, as expressed by you in https://crbug.com/chromium/1252716#c10) which is less exploitable and provides less attacker control, as even as you mention in your original report "It's difficult to reproduce this UAF because you cannot precisely control when the browser is closed." 

>> And I have submit this issue Sep 24,2021, but you don't fix it until I totally analyse it and provide a clear and simple poc
Unfortunately, the earlier versions of the report and POC were just not reproducible on our side, as mentioned in https://crbug.com/chromium/1252716#c9, the patch was not helpful for us in discovery and required repro steps without the patch. There was a lot of back and forth from the original reports and POCs that delayed the root cause discovery and fix until the analysis dullweber@ was able to perform in https://crbug.com/chromium/1252716#c34 from the latest POC. 

>>So I feel so unfair and upset.
I am sorry you feel this process has been unfair and you are upset by it. While we do see and appreciate your efforts throughout, in the end, this doesn't appear to be a very likely or controllable/exploitable real-world issue (from https://crbug.com/chromium/1252716#c34 "In release builds, this only triggers a silent crash report. Maybe we should just put a hard CHECK() here to avoid any potential use-after-free? This only seems to happen very rarely in real usage") 

Again, we are happy to reassess with the VRP Panel based on your request, but I thought it would be helpful to provide this context up front. 



### am...@chromium.org (2022-02-23)

Hello, we have reassessed this issue and the VRP Panel has decided to award you an additional $3,000 for a total of a $10,000 reward for this report, based on your final POC and analysis in https://crbug.com/chromium/1252716#c32 as well as your continued efforts following the initial report. 

### am...@chromium.org (2022-02-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-05)

removing stale Merge-TBD-96 label

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1252716?no_tracker_redirect=1

[Multiple monorail components: Blink>Payments, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057377)*
