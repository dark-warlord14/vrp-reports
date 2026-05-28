# Security: UAF in HidService::GetDevices

| Field | Value |
|-------|-------|
| **Issue ID** | [40060395](https://issues.chromium.org/issues/40060395) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HID |
| **Platforms** | Android, Fuchsia, Linux, Mac, iOS, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2022-07-25 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=1284916>

There is a raw pointer `browser_context_` stored as member variable in class HidService. And the lifetime of HidService binds to a self-owned receiver [1], which means it will stay alive as long as the underlying message pipe stays connected.

`browser_context_` comes from BrowserContext and will be a dangling pointer after the Profile is gone.

Because HidService can continue receiving mojo calls after the Profile is freed, a UAF would occur when function like HidService::GetDevices being invoked and accessing the raw pointer again [2].

```
// static  
void HidService::Create(  
    BrowserContext\* browser_context,  
    const url::Origin& origin,  
    mojo::PendingReceiver<blink::mojom::HidService> receiver) {  
  DCHECK(browser_context);  
  
  // Avoid creating the HidService if there is no HID delegate to provide  
  // the implementation.  
  if (!GetContentClient()->browser()->GetHidDelegate())  
    return;  
  
  // This makes HidService a self-owned receiver so it will self-destruct when a  
  // mojo interface error occurs.  
  mojo::MakeSelfOwnedReceiver<blink::mojom::HidService, HidService>( //--->[1]  
      std::make_unique<HidService>(browser_context, origin,  
                                   /\*render_frame_host=\*/nullptr),  
      std::move(receiver));  
}  
  
void HidService::GetDevices(GetDevicesCallback callback) {  
  GetContentClient()  
      ->browser()  
      ->GetHidDelegate()  
      ->GetHidManager(browser_context_) //--->[2]  
      ->GetDevices(base::BindOnce(&HidService::FinishGetDevices,  
                                  weak_factory_.GetWeakPtr(),  
                                  std::move(callback)));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/hid/hid_service.cc;l=200;drc=8adc9cb73b65f12d089dabbad06a9fb7446e478f;bpv=1;bpt=1>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/hid/hid_service.cc;l=215;drc=8adc9cb73b65f12d089dabbad06a9fb7446e478f;bpv=1;bpt=1>

**VERSION**  

Chrome Version: dev  

OS: except android

**REPRODUCTION CASE**

1. apply repro.diff to patch origin check, reach the trigger point. (and provide some logs to help analysis)
   
   ```
   key patch  
   ->  
   
   diff --git a/content/browser/service_worker/embedded_worker_instance.cc b/content/browser/service_worker/embedded_worker_instance.cc  
   index bc7cada2615a9..adc4ee6036a39 100644  
   --- a/content/browser/service_worker/embedded_worker_instance.cc  
   +++ b/content/browser/service_worker/embedded_worker_instance.cc  
   @@ -779,9 +779,11 @@ void EmbeddedWorkerInstance::BindHidService(  
      if (!hid_delegate) {  
        return;  
      }  
   -  if (hid_delegate->IsServiceWorkerAllowedForOrigin(origin)) {  
   +  // if (hid_delegate->IsServiceWorkerAllowedForOrigin(origin)) {  
   +      LOG(ERROR) << "sakura in EmbeddedWorkerInstance::BindHidService4";  
   +  
        rph->BindHidService(origin, std::move(receiver));  
   -  }  
   +  // }  
    }  
    #endif  // !BUILDFLAG(IS_ANDROID)  
   
   ```
2. copy js mojo binding files to working dir  
   
   python3 ./copy\_mojo\_bindings.py /path/to/chrome/.../out/Asan/gen
3. setup a HTTP server  
   
   python3 -m http.server 8000
4. run `out/asan/chrome --incognito --user-data-dir=/tmp/xxx/ --enable-blink-features=MojoJS http://localhost:8000/poc.html`
5. close the tab immediately and the browser should crash in a few seconds

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan log

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 20.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 185 B)
- [sw.js](attachments/sw.js) (text/plain, 469 B)
- [HidExtensionServiceWorker.zip](attachments/HidExtensionServiceWorker.zip) (application/octet-stream, 66.6 KB)
- [ServiceWorkerHost_destructor_stack.txt](attachments/ServiceWorkerHost_destructor_stack.txt) (text/plain, 5.5 KB)
- [HidService_destructor_stack.txt](attachments/HidService_destructor_stack.txt) (text/plain, 6.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 273 B)
- [sw.js](attachments/sw.js) (text/plain, 442 B)

## Timeline

### et...@gmail.com (2022-07-25)

Supplementary explanation
1. The commit that introduced the vulnerability is from 2022.5.24
https://source.chromium.org/chromium/chromium/src/+/1af73f3c0c3a7d8fdb52b6035e8188a1590430f7

2. There is an incorrect assumption here.
```cpp
// The BrowserContext pointed by |browser_context_| always outlives HidService itself.
const raw_ptr<BrowserContext> browser_context_;
```

**By calling mojocall frequently( >0x2000) and blocking the mojo pipe, we can see such a log**
```
...
...
[104442:104442:0725/180122.030195:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030281:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030376:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030461:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180125.648951:ERROR:browser_context.cc(91)] sakura in BrowserContextImpl::~BrowserContextImpl: 0x61100056ef40
[104442:104442:0725/180125.651628:ERROR:hid_service.cc(141)] sakura in HidService::~HidService
```

browser_context_ **not always** outlives HidService.

### et...@gmail.com (2022-07-25)

Patch suggestion:
Convert browser_context_ from raw_ptr to weak_ptr,  and check it before use

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-25)

The patch is equivalent to having --enable-features=EnableWebHidOnExtensionServiceWorker and triggering this from an extension. That features is not enabled, so this is Impact-None.

[Monorail components: Blink>HID]

### ch...@chromium.org (2022-07-25)

[Empty comment from Monorail migration]

### ch...@chromium.org (2022-07-25)

[Empty comment from Monorail migration]

### ch...@chromium.org (2022-07-30)

Some updates:
- After BrowserContext is destroyed, ServiceWorkerHost and content::HidService will be destroyed trigger by mojo pipe disconnection handler (OnPipeConnectionError()).
```
(GetDevices is set to trigger from renderer side every 5ms)
[1955265:1955265:0730/060415.897594:INFO:hid_service.cc(215)] GetDevices[DEBUG]
[1955265:1955265:0730/060415.898033:INFO:hid_service.cc(215)] GetDevices[DEBUG]
[1955265:1955265:0730/060415.898410:INFO:hid_service.cc(215)] GetDevices[DEBUG]

// Browser context destroyed
[1955265:1955265:0730/060415.953202:INFO:browser_context.cc(90)] ~BrowserContext[DEBUG]
[1955265:1955265:0730/060415.953298:INFO:browser_context_impl.cc(76)] ~BrowserContextImpl[DEBUG]
[1955265:1955265:0730/060415.953379:INFO:browser_context_impl.cc(120)] ~BrowserContextImpl[DEBUG] done
[1955265:1955265:0730/060415.953608:INFO:browser_context.cc(99)] ~BrowserContext[DEBUG] done

[1955265:1955265:0730/060415.955286:INFO:hid_service.cc(215)] GetDevices[DEBUG]
...
[1955265:1955265:0730/060415.963505:INFO:hid_service.cc(215)] GetDevices[DEBUG]

// ServiceWorkerHost destroyed (see ServiceWorkerHost_destructor_stack.txt for call stack to ~ServiceWorkerHost)
[1955265:1955265:0730/060415.975082:INFO:service_worker_host.cc(53)] ~ServiceWorkerHost[DEBUG]
[1955265:1955265:0730/060415.975380:INFO:service_worker_host.cc(65)] ~ServiceWorkerHost[DEBUG] done
[1955265:1955265:0730/060415.984445:INFO:hid_service.cc(215)] GetDevices[DEBUG]
[1955265:1955265:0730/060415.984804:INFO:hid_service.cc(215)] GetDevices[DEBUG]

// HidService destroyed (see HidService_destructor_stack.txt for call stack to ~HidService)
[1955265:1955265:0730/060416.041334:INFO:hid_service.cc(140)] ~HidService[DEBUG]
[1955265:1955265:0730/060416.041444:INFO:hid_service.cc(149)] ~HidService[DEBUG] done

```

- So even moving HidService into ServiceWorkHost, the issue might still persist as it is destroyed after browserContext destruction. Hence I will try to use BrowserContextKeyedServiceShutdownNotifierFactory[1] to have HidService be notified when BrowserContext is destroyed and clear the raw_ptr<BrowserContext>.

- HidExtensionServiceWorker.zip is the extension package that could be used to reproduce the issue, steps as below:
  1. Unzip HidExtensionServiceWorker.zip and load it for unpacked extension.
  2. More Tools -> Extensions -> Inspect Service Worker of the extension. It will then trigger "service-worker-utils.js" which calls "navigator.hid.getDevices();" every 5ms.
  3. In my experiment, I made below change to content::HidService::GetDevices() to make it return immediately to help catch right destrcutor stack.
  ```
    void HidService::GetDevices(GetDevicesCallback callback) {
        LOG(INFO) << __func__ << "[DEBUG]";
        std::vector<device::mojom::HidDeviceInfoPtr> result;
        std::move(callback).Run(std::move(result));
      // GetContentClient()
      //     ->browser()
      //     ->GetHidDelegate()
      //     ->GetHidManager(browser_context_)
      //     ->GetDevices(base::BindOnce(&HidService::FinishGetDevices,
      //                                 weak_factory_.GetWeakPtr(),
      //                                 std::move(callback)));
    }
  ```

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/content/browser_context_keyed_service_shutdown_notifier_factory.h;l=20;bpv=1;bpt=1

### ch...@chromium.org (2022-07-30)

for https://crbug.com/chromium/1347015#c7 using HidExtensionServiceWorker.zip, need to enable the feature by:
1. chrome://flags/#enable-web-hid-on-extension-service-worker 
2. Enable and relaunch chrome.

### re...@chromium.org (2022-08-01)

I agree, it looks like the service worker code rarely uses the BrowserContext and handles lifetimes a bit differently from RenderProcessHost and RenderFrameHost objects. The other option is that if you could get access to the ServiceWorkerContextWrapper that can provide you with a BrowserContext* which may be null if the BrowserContext has been shut down.

### ch...@chromium.org (2022-08-02)

Thank Reilly. I tried the suggestion in https://crbug.com/chromium/1347015#c9 and the HidService could leverage that to check if BrowserContext still valid, and it aligns very well with BrowserContext destruction.

Below are trace just for information. We can see ServiceWorkerContextCore is destroyed when BrowserContext is about to be destroyed. And ServiceWorkerContextCore can be access through a few steps from ServiceWorkerHost.

```
[2624319:2624319:0802/220533.881197:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:0x5560da7d3070
[2624319:2624319:0802/220533.881252:INFO:hid_service.cc(229)] GetDevices[DEBUG] browser_context:0x5560d8355d20
[2624319:2624319:0802/220533.881721:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.881779:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:0x5560da7d3070
[2624319:2624319:0802/220533.881828:INFO:hid_service.cc(229)] GetDevices[DEBUG] browser_context:0x5560d8355d20
[2624319:2624319:0802/220533.882206:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.882268:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:0x5560da7d3070
[2624319:2624319:0802/220533.882317:INFO:hid_service.cc(229)] GetDevices[DEBUG] browser_context:0x5560d8355d20

// Before BrowserContext destruction, ServiceWorkerContextCore is still valid, so can access browser_context ptr
[2624319:2624319:0802/220533.882709:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.882772:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:0x5560da7d3070
[2624319:2624319:0802/220533.882823:INFO:hid_service.cc(229)] GetDevices[DEBUG] browser_context:0x5560d8355d20

// ServiceWorkerContextCore is destroyed alinged with BrowserContext destruction
[2624319:2624319:0802/220533.930766:INFO:service_worker_context_core.cc(343)] ~ServiceWorkerContextCore[DEBUG]
[2624319:2624319:0802/220533.930889:INFO:service_worker_context_core.cc(349)] ~ServiceWorkerContextCore[DEBUG] done
[2624319:2624319:0802/220533.940956:INFO:browser_context.cc(90)] ~BrowserContext[DEBUG]
[2624319:2624319:0802/220533.941055:INFO:browser_context_impl.cc(76)] ~BrowserContextImpl[DEBUG]
[2624319:2624319:0802/220533.941143:INFO:browser_context_impl.cc(120)] ~BrowserContextImpl[DEBUG] done
[2624319:2624319:0802/220533.941421:INFO:browser_context.cc(99)] ~BrowserContext[DEBUG] done

// After that even service worker isn't destroyed, ServiceWorkerContextCore is already null so we are aware browserContext destruction.
[2624319:2624319:0802/220533.943471:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.943544:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:0x5560da7d3070
[2624319:2624319:0802/220533.943602:INFO:hid_service.cc(231)] GetDevices[DEBUG] ServiceWorkerContextCore is null

...
// A while later, serviceWorkerHost is destroyed.
[2624319:2624319:0802/220533.969050:INFO:service_worker_host.cc(53)] ~ServiceWorkerHost[DEBUG]
[2624319:2624319:0802/220533.969399:INFO:service_worker_host.cc(65)] ~ServiceWorkerHost[DEBUG] done
[2624319:2624319:0802/220533.978719:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.978795:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:(nil)
[2624319:2624319:0802/220533.979064:INFO:hid_service.cc(221)] GetDevices[DEBUG]
[2624319:2624319:0802/220533.979124:INFO:hid_service.cc(222)] GetDevices[DEBUG] service_worker_host_:(nil)
[2624319:2624319:0802/220534.040129:INFO:hid_service.cc(144)] ~HidService[DEBUG]

```

### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88f88727a268b42a09193d098da6600b35c277ec

commit 88f88727a268b42a09193d098da6600b35c277ec
Author: Jack Hsieh <chengweih@chromium.org>
Date: Tue Aug 16 05:03:00 2022

Webhid: Fix UAF issue when BrowserContext is destroyed

There is a smaller window between BrowserContext and HidService
destruction timing in service worker condition, which creates an UAF
issue as the stored BrowserContext pointer can still be accessed by the
HidService. This is fixed by using weak pointer of
ServiceWorkerContextCore to access BrowserContext when it is valid.

This change also refactor HidService and its related unit tests to have
its constructors be used explicitly for RenderFrameHost or
ServiceWorkerContextCore.

Bug: 1347015
Change-Id: Id0c35da5a24ad4c742a0e58d17775b8db5180bf9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809913
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1035367}

[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/hid/hid_service.cc
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/hid/hid_service_unittest.cc
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/chrome/browser/hid/chrome_hid_delegate_unittest.cc
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/chrome/browser/hid/chrome_hid_delegate.cc
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/hid/hid_service.h
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/renderer_host/render_process_host_impl.h
[modify] https://crrev.com/88f88727a268b42a09193d098da6600b35c277ec/content/browser/service_worker/embedded_worker_instance.cc


### ch...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-23)

Congratulations! The VRP Panel has decided to award you $5,000 for your report of this mildly mitigated (https://g.co/chrome/vrp) security bug + $1,000 bisect bonus. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-06)

Hello reporter, I got the following setback when trying to verify another problem about BrowserContext:

An assertion is occured when using the destroyed BrowserContext which will cause a crash. I was wondering how did you bypass it to trigger the Use-After-Free? Thanks a lot!

void* RefcountedBrowserContextKeyedServiceFactory::GetContextToUse(
    void* context) const {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  AssertContextWasntDestroyed(context);   ----- will CHECK(false) if use a dead context
  return GetBrowserContextToUse(static_cast<content::BrowserContext*>(context));
}

### [Deleted User] (2022-12-06)

I also encountered the same assert exception when trying to reproduce this issue:

FATAL:dependency_manager.cc(173)] Check failed: false. Attempted to access a context that was ShutDown(). This is most likely a heap smasher in progress. After KeyedService::Shutdown() completes, your service MUST NOT refer to depended services again.
=================================================================
==190920==ERROR: AddressSanitizer: breakpoint on unknown address
==190920==*** WARNING: Failed to initialize DbgHelp!              ***
==190920==*** Most likely this means that the app is already      ***
==190920==*** using DbgHelp, possibly with incompatible flags.    ***
==190920==*** Due to technical reasons, symbolization might crash ***
==190920==*** or produce wrong results.                           ***
#0 std::Cr::__cxx_atomic_load F:\odd\chromium\src\buildtools\third_party\libc++\trunk\include\atomic:954
#1 std::Cr::__atomic_base<base::debug::GlobalActivityTracker *,0>::load F:\odd\chromium\src\buildtools\third_party\libc++\trunk\include\atomic:1541
#2 base::debug::GlobalActivityTracker::Get F:\odd\chromium\src\base\debug\activity_tracker.h:953
#3 logging::LogMessage::~LogMessage(void) F:\odd\chromium\src\base\logging.cc:925:9
#4 logging::LogMessage::`scalar deleting dtor'(unsigned int) F:\odd\chromium\src\base\logging.cc:712:27
#5 DependencyManager::AssertContextWasntDestroyed(void *) const F:\odd\chromium\src\components\keyed_service\core\dependency_manager.cc:173:5
#6 SimpleKeyedServiceFactory::GetContextToUse(void *) const F:\odd\chromium\src\components\keyed_service\core\simple_keyed_service_factory.cc:86:3
#7 KeyedServiceFactory::GetServiceForContext(void *, bool) F:\odd\chromium\src\components\keyed_service\core\keyed_service_factory.cc:69:13

The attachments are the poc I used, there seems to be something wrong with the original poc.
I'm a bit confused if I'm doing something wrong. Can you provide the version and the GN args of the chromium you were using? Thanks a lot!

### ch...@google.com (2022-12-06)

Hi minnabaddeley@gmail.com,

I think the way the previous reporter reported this issue is to point out the dangling pointer in content::HidService but didn't really access it, though the is enough evidence to show a potential UAF issue.

From https://crbug.com/chromium/1347015#c1
```
[104442:104442:0725/180122.030195:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030281:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030376:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180122.030461:ERROR:hid_service.cc(216)] sakura in HidService::GetDevices : 0x61100056ef40
[104442:104442:0725/180125.648951:ERROR:browser_context.cc(91)] sakura in BrowserContextImpl::~BrowserContextImpl: 0x61100056ef40
[104442:104442:0725/180125.651628:ERROR:hid_service.cc(141)] sakura in HidService::~HidService  < - - content::HidService holds the dangling BrowserContext pointer while BrowserContext  has been destroyed. [1]
```

[1] https://source.chromium.org/chromium/chromium/src/+/1af73f3c0c3a7d8fdb52b6035e8188a1590430f7:content/browser/hid/hid_service.h;l=88 (content::HidService store the pointer of BrowserContext here)

### ch...@google.com (2022-12-06)

Hi minnabaddeley@gmail.com,

I would also like to clarify with you that do you  mean you can cause this BrowserContext CHECK(false) by using the attached file in https://crbug.com/chromium/1347015#c20? Because the WebHID API are guarded in Extension origin, if you are using Chrome even with the feature chrome://flags#enable-web-hid-on-extension-service-worker enabled, we don't expect WebHID API can be accessed by sw.js.



### [Deleted User] (2022-12-07)

Hi chengweih@google.com, thanks for the explanation, but the assertion I'm encountering is not about the WebHID. I used the patch from the original report to turn off the origin check.

What really confuses me is:
The function call GetServiceForContext in the line #1 in the asan attached to the original report:
=================================================================
==82604==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000587040 at pc 0x5564e06d274f bp 0x7ffdb80b1dd0 sp 0x7ffdb80b1dc8
READ of size 8 at 0x611000587040 thread T0 (chrome)
    #0 0x5564e06d274e in HostContentSettingsMapFactory::BuildServiceInstanceFor(content::BrowserContext*) const chrome/browser/content_settings/host_content_settings_map_factory.cc:90:40
    #1 0x7f9b37e6873b in RefcountedKeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/refcounted_keyed_service_factory.cc:90:15
    #2 0x5564e06d210d in HostContentSettingsMapFactory::GetForProfile(content::BrowserContext*) chrome/browser/content_settings/host_content_settings_map_factory.cc:75:22
    #3 0x5564e0e87768 in HidChooserContext::HidChooserContext(Profile*) chrome/browser/hid/hid_chooser_context.cc:137:11

GetServiceForContext(void*, bool) components/keyed_service/core/refcounted_keyed_service_factory.cc:
	RefcountedKeyedServiceFactory::GetServiceForContext(void* context,
	                                                    bool create) {
	  context = GetContextToUse(context);
	  if (!context)
	    return nullptr;

GetContextToUse:
	void* RefcountedBrowserContextKeyedServiceFactory::GetContextToUse(
	    void* context) const {
	  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
	  AssertContextWasntDestroyed(context);
	  return GetBrowserContextToUse(static_cast<content::BrowserContext*>(context));
	}

AssertContextWasntDestroyed:
	void KeyedServiceBaseFactory::AssertContextWasntDestroyed(void* context) const {
	  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
	  dependency_manager_->AssertContextWasntDestroyed(context);
	}

dependency_manager_->AssertContextWasntDestroyed:
	void DependencyManager::AssertContextWasntDestroyed(void* context) const {
	  if (dead_context_pointers_.find(context) != dead_context_pointers_.end()) {
	    // We want to see all possible use-after-destroy in production environment.
	    CHECK(false) << "Attempted to access a context that was ShutDown(). "
	                 << "This is most likely a heap smasher in progress. After "
	                 << "KeyedService::Shutdown() completes, your service MUST "
	                 << "NOT refer to depended services again.";
	  }
	}

If the BrowserContext has been destroyed, CHECK(false) will take effect and cause the crash described in https://crbug.com/chromium/1347015#c20. It will not output the asan result in the original report. I kind of don't understand how the reporter bypassed it. Have you ever encountered this assertion when you reproduced?

### et...@gmail.com (2022-12-07)

Hi, minnabaddeley@gmail.com.
this issue is a bit early for me, I don't remember much.
I located this problem mainly through static analysis, and made some patches to trigger it. 
Since I have been using chromium compiled by myself, there may be some debugging patches（such as log or bypass） that have not been removed, which may cause me and your reproduction environment to be different.
The root cause of this vulnerability is clear enough in https://crbug.com/chromium/1347015#c1 that it is a potential uaf problem. 
I have not recorded your other questions including the version and gn args I reproduced at that time.  
Hope this answers your questions:)

### et...@gmail.com (2022-12-07)

Since this question is based on some kind of vulnerability pattern, in order to avoid duplication, my report is a bit dirty and may be missing some necessary conditions.  
But thanks to the perfect reproduction and repair process provided by the developer, so I don't make any further additions, good job!

### et...@gmail.com (2022-12-07)

Remove the original attachment that might be confusing, the correct steps are https://crbug.com/chromium/1347015#c1 and https://crbug.com/chromium/1347015#c7
Thank you for your correction :)

### [Deleted User] (2022-12-08)

Thanks for your reply, etern! But the root cause of this issue does not seem to be what I'm concerned about. Do you remember that you encountered somewhat assertions when you tried to trigger this vulnerability before? Thanks!

The reproduction in https://crbug.com/chromium/1347015#c1 and https://crbug.com/chromium/1347015#c7 comment out the code that uses the freed browser_context_. If you uncomment this part, the assertion will still be triggered. If you don't uncomment, it seems that you can't trigger the Use-After-Free problem, so I'm a bit confused about how the issue was triggered in the original report. And could you please restore the "asan.txt" file that was deleted in the original report? It seems to be very helpful to me.

### et...@gmail.com (2022-12-08)

Hi, minnabaddeley@gmail.com.
I re-reviewed your question and thought maybe my original environment patched some code that caused the **wrong asan** to be triggered here, so I removed it not wanting to confuse others as well.
So you don't need to reply to this issue anymore, thanks！ :)

### [Deleted User] (2022-12-09)

Hi etern, do you mean that you inadvertently commented out the CHECK(false) to trigger this Use-After-Free issue? That makes sense, I get the same asan output after commenting out this check. So it's a pity that the assertion doesn't seem to be bypassable, thanks a lot!

### is...@google.com (2022-12-09)

This issue was migrated from crbug.com/chromium/1347015?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1322258]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060395)*
