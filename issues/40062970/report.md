# Security: Heap-buffer-overflow in FrameSinkManagerImpl::UnregisterFrameSinkHierarchy

| Field | Value |
|-------|-------|
| **Issue ID** | [40062970](https://issues.chromium.org/issues/40062970) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ky...@chromium.org |
| **Created** | 2023-02-08 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

commit d0cd00a40cccd8061390f0c2cd8a7294d02d1adb

1. compile Chromium with ASAN
2. `python copy_mojo_js_bindings.py path/to/ASAN/gen/` and copy poc.html and a.pdf to the same folder
3. run `./chrome --user-data-dir=/tmp/noexist --enable-blink-features=MojoJS http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html`

**Problem Description:**  

This crash occurs in VIZ service which is releated to GPU process.

1. Analysis

In function `FrameSinkManagerImpl::UnregisterFrameSinkHierarchy`[1], it didn't check whether the result of find is `std::end` (only a DCHECK),so overflow occusr when using the `end()->second.children.erase`(1).

To trigger this overflow, we need to exit the GPU Process. According to the poc and asan log, I have debugged the code and find that when GPU process exited, the map `frame_sink_source_map_`[1] will become empty. But this map will be filled with new element soon, so it's quite hard to trigger. We need to call `UnregisterFrameSinkHierarchy` before the map is filled again as soon as possible.

Because it's really hard to reproduce, you may need to try my poc.html serveral times to trigger this overflow. Please see the ASAN log for more information.

```
void FrameSinkManagerImpl::UnregisterFrameSinkHierarchy(  
    const FrameSinkId& parent_frame_sink_id,  
    const FrameSinkId& child_frame_sink_id) {  
  // Deliberately do not check validity of either parent or child FrameSinkId  
  // here. They were valid during the registration, so were valid at some point  
  // in time. This makes it possible to invalidate parent and child FrameSinkIds  
  // independently of each other and not have an ordering dependency of  
  // unregistering the hierarchy first before either of them.  
  
  for (auto& observer : observer_list_) {  
    observer.OnUnregisteredFrameSinkHierarchy(parent_frame_sink_id,  
                                              child_frame_sink_id);  
  }  
  
  auto iter = frame_sink_source_map_.find(parent_frame_sink_id);  
  DCHECK(iter != frame_sink_source_map_.end());  
  
  // Remove |child_frame_sink_id| from parents list of children.  
  auto& mapping = iter->second;  
  DCHECK(base::Contains(mapping.children, child_frame_sink_id));  
  mapping.children.erase(child_frame_sink_id);   // (1)=> overflow occurs here  
  
  // Now the hierarchy has been updated, update throttling.  
  UpdateThrottling();  
  
  // Delete the FrameSinkSourceMapping for |parent_frame_sink_id| if empty.  
  if (mapping.children.empty() && !mapping.source) {  
    frame_sink_source_map_.erase(iter);  
    return;  
  }  
  
  // If the parent does not have a begin frame source, then disconnecting it  
  // will not change any of its children.  
  BeginFrameSource\* parent_source = iter->second.source;  
  if (!parent_source)  
    return;  
  
  // TODO(enne): these walks could be done in one step.  
  RecursivelyDetachBeginFrameSource(child_frame_sink_id, parent_source);  
  for (auto& source_iter : registered_sources_)  
    RecursivelyAttachBeginFrameSource(source_iter.second, source_iter.first);  
}  

```

Note that I crash the GPU process by Mojo, I believe that this overflow can be triggered without Mojo, but it's hard to trigger so I don't explore more.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/frame_sink_manager_impl.cc;l=288;bpv=1;bpt=0;drc=6b91fb85688d6e62f8eb8588f7b34647d7380ce3>

2. Bisect  
   
   <https://chromium-review.googlesource.com/c/chromium/src/+/576397>
3. Patch  
   
   I think you should check the result of find in `frame_sink_source_map_`

auto iter = frame\_sink\_source\_map\_.find(parent\_frame\_sink\_id);

- CHECK(iter != frame\_sink\_source\_map\_.end());

- DCHECK(iter != frame\_sink\_source\_map\_.end());

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 3.8 KB)
- [a.pdf](attachments/a.pdf) (application/pdf, 4.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 19.5 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 8.8 MB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)

## Timeline

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-02-09)

attach the video.

### me...@gmail.com (2023-02-10)

Hello, any update?

### ma...@google.com (2023-02-10)

vmpstr@, could you please help triage and/or route this issue?

Could you also confirm what releases would be affected by this and set the appropriate FoundIn-* label?

[Monorail components: Internals>Services>Viz]

### [Deleted User] (2023-02-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### vm...@chromium.org (2023-02-13)

kylechar@, can you please triage

### am...@chromium.org (2023-02-16)

Current Stable/Extended Stable == M110, so FoundIn-110 though this issue has been around for seemingly much longer 

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### ky...@chromium.org (2023-02-16)

Where dose copy_mojo_js_bindings.py come from? I am trying to reproduce but I don't see any file with that name.

### me...@gmail.com (2023-02-17)

Upload the copy_mojo_js_bindings.py 

If you can't find the third_party/blink/public/mojom/frame_sinks/embedded_frame_sink.mojom.js, Please use `ninja -C out/ui/ third_party/blink/public/mojom:embedded_frame_sink_mojo_bindings_js` to generate it.


### [Deleted User] (2023-02-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2023-02-20)

Hello any update?

### ky...@chromium.org (2023-02-21)

So I can't actually reproduce the asan error. I did manage to get poc.html to not throw any JS errors with the following:

# Modify //components/performance_manager/public/mojom:mojom to not be cpp only
$ autoninja -C out/asan chrome third_party/blink/public/mojom:embedded_frame_sink_mojo_bindings_js components/performance_manager/public/mojom:mojom_js
$ cp out/asan/gen/mojo/public/js/mojo_bindings.js ~/repro/
$ find out/asan -name "*.mojom.js" -exec cp --parents '{}' ~/repro/ \;
# start local webserver in ~/repro/
$ out/asan/chrome  --enable-blink-features=MojoJS http://localhost:8000/poc.html http://localhost:8000/poc.html http://localhost:8000/poc.html

I don't know if there is more to it but I ran it a bunch of times with different numbers of poc.html without triggering asan. 

I did see bad message triggered from browser to GPU that triggers ReportBadMessage [1].  That is followed by GPU process intentionally crash at this CHECK [2] shortly afterwards. There are also numerous bad IPCs from renderer to browser that cause renderer to be killed. That seems to be working fine.

One thing I didn't see is all of the poc.html running in the same renderer process which since they're all from localhost I was kinda expecting. I'm not sure if having all the poc.html running in the renderer with process_id=5 is key to reproducing or not.

However, if I run with DCHECKs I can see the same FrameSinkId is registered more than once [3]. Once for a top level renderer from DelegatedFrameHost and then again from EmbeddedFrameSinkImpl [4]. If both places call HostFrameSinkManager::RegisterFrameSinkHierarchy() with the same parent and child FrameSinkIds it would only insert one entry into FrameSinkSourceMapping::children. Calling HostFrameSinkManager::UnregisterFrameSinkHierarchy() twice would then probably end up in  FrameSinkManagerImpl::UnregisterFrameSinkHierarchy() twice. The first call would potentially delete the entry from the map at [4] so the second call into FrameSinkManagerImpl::UnregisterFrameSinkHierarchy() would find frame_sink_source_map_.end().

EmbeddedFrameSinkImpl::has_registered_compositor_frame_sink_ tries to guard against duplicated hierarchy registration/unregistration but that doesn't work if some other piece of code,  namely DelegatedFrameHost, also thinks it's controlling the same FrameSinkId.

Not sure if that's exactly the same problem but it seems related. This would only be accessible from a compromised renderer that can make arbitrary calls via the blink::mojom::EmbeddedFrameSinkProvider. 

merc.ouc: Anything else to add or other repro instructions?

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/frame_sink_manager_impl.cc;l=210;drc=6b91fb85688d6e62f8eb8588f7b34647d7380ce3
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/main/viz_main_impl.cc;l=271;drc=12be03159fe22cd4ef291e9561762531c2589539
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/host/host_frame_sink_manager.cc;l=68;drc=e1591f7e48004bf610e6e53a4f213d032e221f23
[4] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/frame_sink_manager_impl.cc;l=301;drc=6b91fb85688d6e62f8eb8588f7b34647d7380ce3


### me...@gmail.com (2023-02-22)

Thank you for your analysis. It seems that your steps is right, but this overflow is hard to trigger.

>Not sure if that's exactly the same problem but it seems related. This would only be accessible from a compromised renderer that can make arbitrary calls via the blink::mojom::EmbeddedFrameSinkProvider. 
According to my analysis, there are two main factors to trigger this overflow:
1. crash the GPU process,  I think a normal renderer could do this
2. crash the renderer, there are also other ways to crash the renderer from a normal renderer
Considering the difficult to trigger the overflow, I don't find a stable poc which can trigger this overflow with a normal renderer.

The `CHECK` has ensured that there will no duplicate keys in the map, I think the poc.html use this call to crash the renderer (I also try to use anther way to crash the renderer like %Abort(0), it can also trigger the overflow. But this need `--js-flags="--allow-natives-syntax"` flag). Actually there are no dup keys in map. Here are some debug info when the overflow occurs.
After the GPU process crash, we can see that the size of map is reset to zero. If the renderer is crash then, it will run into function ` FrameSinkManagerImpl::UnregisterFrameSinkHierarchy` and find the FrameSinkId(5,3).  FrameSinkId(5,3) is the id of the embed PDF.


```
[3286615:3286615:0202/122153.498630:ERROR:gpu_process_host.cc(952)] GPU process exited unexpectedly: exit_code=133
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[3287162:3287180:0202/122153.891977:ERROR:frame_sink_manager_impl.cc(665)] [child contains]  find?? 0
[3287162:3287180:0202/122153.892675:ERROR:frame_sink_manager_impl.cc(666)] [child contains]  size?? 0

[3287162:3287180:0202/122156.089837:ERROR:frame_sink_manager_impl.cc(310)] [unregister] unregister start: have 5,3? 0
[3287162:3287180:0202/122156.090027:ERROR:frame_sink_manager_impl.cc(319)]  [!!] end here size is 2
[3287162:3287180:0202/122156.090242:ERROR:frame_sink_manager_impl.cc(320)]  [!!] end here  FrameSinkId(5, 3)
[3287162:3287180:0202/122156.090437:ERROR:frame_sink_manager_impl.cc(326)] [unregister] unregister : have 5,3? 0
=================================================================\
```

### ky...@chromium.org (2023-02-22)

Since I can't reproduce can you try patching in https://crrev.com/c/4283141 and verifying it's no longer reproducible? The browser process should crash before HostFrameSinkManager (browser) / FrameSinkManagerImpl (gpu) can get into a bad state.

### me...@gmail.com (2023-02-23)

Hi kylechar@,  I use a simple python script to start chrome with poc and then close it. 
Before this patch https://crrev.com/c/4283141 , overflow occurs after less than ten times
After this patch, it is no longer reproducible within hundreds of times.
So I think this patch works fine.


### ky...@chromium.org (2023-02-23)

 merc.ouc: Thanks for confirming.

+jonross FYI

### gi...@appspot.gserviceaccount.com (2023-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a707ac2d95e4726f4cf0267c9b0c038926c2a691

commit a707ac2d95e4726f4cf0267c9b0c038926c2a691
Author: kylechar <kylechar@chromium.org>
Date: Fri Feb 24 13:05:33 2023

Add CHECKs in HostFrameSinkManager

It looks like it's possible for a compromised renderer to get multiple
things to register the same FrameSinkId with HostFrameSinkManager. This
violates assumptions around ownership so turn DCHECKs here into CHECKs.
Also convert DCHECKs into CHECKs for registering/unregistering frame
sink hierarchy just in case.

Bug: 1414018
Change-Id: If948e758a8484024666f4066360620bc3a9cb493
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4283141
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1109533}

[modify] https://crrev.com/a707ac2d95e4726f4cf0267c9b0c038926c2a691/components/viz/service/frame_sinks/frame_sink_manager_impl.cc
[modify] https://crrev.com/a707ac2d95e4726f4cf0267c9b0c038926c2a691/components/viz/host/host_frame_sink_manager.cc


### me...@gmail.com (2023-02-27)

Hi kylechar@, can we mark this as fixed？ Thanks.

### ky...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### ky...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-27)

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d9081493c4b2d7dece6312335c868a33f7c4958e

commit d9081493c4b2d7dece6312335c868a33f7c4958e
Author: kylechar <kylechar@chromium.org>
Date: Tue Feb 28 21:02:51 2023

Add CHECKs in HostFrameSinkManager

It looks like it's possible for a compromised renderer to get multiple
things to register the same FrameSinkId with HostFrameSinkManager. This
violates assumptions around ownership so turn DCHECKs here into CHECKs.
Also convert DCHECKs into CHECKs for registering/unregistering frame
sink hierarchy just in case.

(cherry picked from commit a707ac2d95e4726f4cf0267c9b0c038926c2a691)

Bug: 1414018
Change-Id: If948e758a8484024666f4066360620bc3a9cb493
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4283141
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1109533}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4298330
Cr-Commit-Position: refs/branch-heads/5615@{#69}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/d9081493c4b2d7dece6312335c868a33f7c4958e/components/viz/service/frame_sinks/frame_sink_manager_impl.cc
[modify] https://crrev.com/d9081493c4b2d7dece6312335c868a33f7c4958e/components/viz/host/host_frame_sink_manager.cc


### am...@chromium.org (2023-03-08)

hi kylechar@, thank you for fixing this issue and merging it to M112 based on the bot's autoapproval. 
This is a fix to a high-severity bug impacting Stable and Extended Stable and should be backmerged to M111/Stable and M110/Extended. 
I checked the perf/stability info in crash data and see no issues from this fix since it landed, so I've gone ahead and approved/reviewed it for backmerge. 

If there is issue with backmerging this or a complexity/compatibility that I am missing, please let me know. 
Otherwise, please merge this fix to branches 5563 and 5481 respectively so this fix can be included in the next security updates for M111/Stable and M110/Extended. 

In the future, when landing fixes for security bug, please simply update the issue as Fixed. This will allow the bot to apply the appropriate merge review labels based on severity and impact and put them in the security merge review queue. Thank you. 

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations, Weipeng! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### me...@gmail.com (2023-03-10)

Hi Amy, thank you for your reward!
And I want to change my credit to 'Weipeng Jiang (@Krace) of VRI'
Thank you!

### ky...@chromium.org (2023-03-10)

One of the CHECKs is being triggered on Android, see https://crbug.com/1421566. I am not particularly confident that is the only thing that will trip over the CHECK either so merging too far back is risky.

### am...@chromium.org (2023-03-10)

Ah good catch on that bit. Thanks for pointing that out. Let's just leave this as merged to 112 for now. 

### am...@chromium.org (2023-03-10)

re: https://crbug.com/chromium/1414018#c30 - acknowledged; this change will be reflected in future updates!

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello Krace, we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), so I have undeleted them. Please refrain from deleting attachments and comments with pertinent information. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414018?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062970)*
