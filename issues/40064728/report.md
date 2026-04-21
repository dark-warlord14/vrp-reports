# Security: TALOS-2023-1751 - Google Chrome VideoEncoder av1_svc_check_reset_layer_rc_flag use-after-free vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40064728](https://issues.chromium.org/issues/40064728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@thelead82.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2023-05-22 |
| **Bounty** | $10,000.00 |

## Description

None (published patch date) 
TALOS-2023-1751   


Google Chrome VideoEncoder av1_svc_check_reset_layer_rc_flag use-after-free vulnerability


### Summary

A use-after-free vulnerability exists in the VideoEncoder av1_svc_check_reset_layer_rc_flag functionality of Google Chrome 113.0.5672.127 (64-bit) and Chromium 115.0.5779.0 (Build) (64-bit). A specially-crafted web page can lead to a use-after-free. An attacker can serve a malicious HTML page to trigger this vulnerability.


### Confirmed Vulnerable Versions

The versions below were either tested or verified to be vulnerable by Talos or confirmed to be vulnerable by the vendor.

Google Chrome 113.0.5672.127 (64-bit)   
Google Chrome Chromium 115.0.5779.0 (Build) (64-bit)   


### Product URLs

Chrome - [https://www.google.com/chrome/](https://www.google.com/chrome/)


### CVSSv3 Score

8.3 - CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L

### CWE

CWE-416 - Use After Free


### Details

Google Chrome is a cross-platform web browser, developed by Google.




By continuously switching the encoder configuration (reconfiguring the encoder) through javascript code it is possible to force Chrome to call media::Av1VideoEncoder::ChangeOptions function (multiple times). This function executes the SetUpAomConfig function which prepares the configuration for the video encoder. 

    // src\media\video\av1_video_encoder.cc
    EncoderStatus SetUpAomConfig(const VideoEncoder::Options& opts,
                                 aom_codec_enc_cfg_t& config,
                                 aom_svc_params_t& svc_params) {
                                 
    ...
      // Setting up SVC parameters
      svc_params = {};
      svc_params.framerate_factor[0] = 1;
      svc_params.number_spatial_layers = 1;
      if (opts.scalability_mode.has_value()) { // here
        switch (opts.scalability_mode.value()) {
          case SVCScalabilityMode::kL1T1:
            // Nothing to do
            break;
          case SVCScalabilityMode::kL1T2:
            svc_params.framerate_factor[0] = 2;
            svc_params.framerate_factor[1] = 1;
            svc_params.number_temporal_layers = 2;
            // Bitrate allocation L0: 60% L1: 40%
            svc_params.layer_target_bitrate[0] =
                60 * config.rc_target_bitrate / 100;
            svc_params.layer_target_bitrate[1] = config.rc_target_bitrate;
            break;
          case SVCScalabilityMode::kL1T3:
            svc_params.framerate_factor[0] = 4;
            svc_params.framerate_factor[1] = 2;
            svc_params.framerate_factor[2] = 1;
            svc_params.number_temporal_layers = 3;

            // Bitrate allocation L0: 50% L1: 20% L2: 30%
            svc_params.layer_target_bitrate[0] =
                50 * config.rc_target_bitrate / 100;
            svc_params.layer_target_bitrate[1] =
                70 * config.rc_target_bitrate / 100;
            svc_params.layer_target_bitrate[2] = config.rc_target_bitrate;

            break;
          default:
            return EncoderStatus(
                EncoderStatus::Codes::kEncoderUnsupportedConfig,
                "Unsupported configuration of scalability layers.");
        }
      }
    ...
    
    
Through the javascript code, we have created first a video encoder with the scalabilityMode set. However during the loop we are also reconfiguring the encoder again, this time without the scalabilityMode option set. In this case SetUpAomConfig will "skip" the `svc_params.number_temporal_layers` initialization, which will be set to zero. This parameter will be not validated properly afterwards.

At this point, the future call list will be `vpx_codec_enc_config_set` -> `encoder_set_config` -> `av1_change_config` -> `check_reset_rc_flag`. The `check_reset_rc_flag` function is interesting to us because it will lead to the `av1_svc_check_reset_layer_rc` (explained below).

        // src\third_party\libaom\source\libaom\av1\encoder\rc_utils.h
        static AOM_INLINE void check_reset_rc_flag(AV1_COMP *cpi) {
          RATE_CONTROL *rc = &cpi->rc;
          PRIMARY_RATE_CONTROL *const p_rc = &cpi->ppi->p_rc;
          if (cpi->common.current_frame.frame_number >
              (unsigned int)cpi->svc.number_spatial_layers) {
            if (cpi->ppi->use_svc) {
              av1_svc_check_reset_layer_rc_flag(cpi);   --> we need to reach this one 
            } else {
              if (rc->avg_frame_bandwidth > (3 * rc->prev_avg_frame_bandwidth >> 1) ||
                  rc->avg_frame_bandwidth < (rc->prev_avg_frame_bandwidth >> 1)) {
                rc->rc_1_frame = 0;
                rc->rc_2_frame = 0;
                p_rc->bits_off_target = p_rc->optimal_buffer_level;
                p_rc->buffer_level = p_rc->optimal_buffer_level;
              }
            }
          }
        }


In order to reach the `av1_svc_check_reset_layer_rc_flag` function, `cpi->common.current_frame.frame_number > (unsigned int)cpi->svc.number_spatial_layers` condition and the `cpi->ppi->use_svc` condition need to be passed. Those conditions can be easily be passed by specific javascript code (ie. multiple videoframe with encode/configure calls), like the POC code shows. 

Now the `av1_svc_check_reset_layer_rc` function will be reached with the `svc->number_temporal_layers` set to zero:

        // src\third_party\libaom\source\libaom\av1\encoder\svc_layercontext.c
        void av1_svc_check_reset_layer_rc_flag(AV1_COMP *const cpi) {
          SVC *const svc = &cpi->svc;
          for (int sl = 0; sl < svc->number_spatial_layers; ++sl) {
            // Check for reset based on avg_frame_bandwidth for spatial layer sl.
            int layer = LAYER_IDS_TO_IDX(sl, svc->number_temporal_layers - 1,
                                         svc->number_temporal_layers);          // layer = -1
            LAYER_CONTEXT *lc = &svc->layer_context[layer];                     // ups, negative index!!!
            RATE_CONTROL *lrc = &lc->rc;
            if (lrc->avg_frame_bandwidth > (3 * lrc->prev_avg_frame_bandwidth >> 1) ||
                lrc->avg_frame_bandwidth < (lrc->prev_avg_frame_bandwidth >> 1)) {
              // Reset for all temporal layers with spatial layer sl.
              for (int tl = 0; tl < svc->number_temporal_layers; ++tl) {
                int layer2 = LAYER_IDS_TO_IDX(sl, tl, svc->number_temporal_layers);
                LAYER_CONTEXT *lc2 = &svc->layer_context[layer2];
                RATE_CONTROL *lrc2 = &lc2->rc;
                PRIMARY_RATE_CONTROL *lp_rc2 = &lc2->p_rc;
                PRIMARY_RATE_CONTROL *const lp_rc = &lc2->p_rc;
                lrc2->rc_1_frame = 0;
                lrc2->rc_2_frame = 0;
                lp_rc2->bits_off_target = lp_rc->optimal_buffer_level;
                lp_rc2->buffer_level = lp_rc->optimal_buffer_level;
              }
            }
          }
        }
        
        
The important part here is that the `svc->number_temporal_layers param` ( see `LAYER_IDS_TO_IDX` macro ) which will be used to calculate the layer index (int layer). Due to the fact we were able to force `svc->number_temporal_layers` to zero (through SetUpAomConfig function) this will give the negative (-1) index. Now this negative index will be used to getting the `svc->layer_context` pointer (lc). So in this particular case:

        LAYER_CONTEXT *lc = &svc->layer_context[layer]; -> LAYER_CONTEXT *lc = &svc->layer_context[-1];
        // layer_context is a memory pointer, due to negative index we can reference to heap memory 0x3340 (size of LAYER_CONTEXT) bytes before "base" region 

        // src\third_party\libaom\source\libaom\av1\encoder\svc_layercontext.h
          /*!
           * Layer context used for rate control in CBR mode.
           * An array. The index for spatial layer `sl` and temporal layer `tl` is
           * sl * number_temporal_layers + tl.
           */
          LAYER_CONTEXT *layer_context;


This leads to out of bounds heap memory access (see the negative array index) which can turn both to heap use-after-free or heap overflow afterwards. 



### Crash Information


		POC command line: chrome.exe --no-sandbox C:\poc\poc.html
    ( TESTED ON WINDOWS X64 )

		=================================================================
		==13184==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1221d7f5bf30 at pc 0x7ff833b6bb98 bp 0x008e8a5ff000 sp 0x008e8a5ff048
		READ of size 4 at 0x1221d7f5bf30 thread T4
		==13184==WARNING: Failed to use and restart external symbolizer!
		==13184==*** WARNING: Failed to initialize DbgHelp!              ***
		==13184==*** Most likely this means that the app is already      ***
		==13184==*** using DbgHelp, possibly with incompatible flags.    ***
		==13184==*** Due to technical reasons, symbolization might crash ***
		==13184==*** or produce wrong results.                           ***
			#0 0x7ff833b6bb97 in av1_svc_check_reset_layer_rc_flag C:\b\s\w\ir\cache\builder\src\third_party\libaom\source\libaom\av1\encoder\svc_layercontext.c:567
			#1 0x7ff833b3b5ed in av1_change_config C:\b\s\w\ir\cache\builder\src\third_party\libaom\source\libaom\av1\encoder\encoder.c:932
			#2 0x7ff830955655 in encoder_set_config C:\b\s\w\ir\cache\builder\src\third_party\libaom\source\libaom\av1\av1_cx_iface.c:1536
			#3 0x7ff8308c5b87 in vpx_codec_enc_config_set C:\b\s\w\ir\cache\builder\src\third_party\libvpx\source\libvpx\vpx\src\vpx_encoder.c:347
			#4 0x7ff8250b83c5 in media::Av1VideoEncoder::ChangeOptions C:\b\s\w\ir\cache\builder\src\media\video\av1_video_encoder.cc:454
			#5 0x7ff825084901 in base::internal::Invoker<base::internal::BindState<void (media::VideoEncoder::*)(const media::VideoEncoder::Options &, base::RepeatingCallback<void (media::VideoEncoderOutput, absl::optional<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> > >)>, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>),base::internal::UnretainedWrapper<media::VideoEncoder,base::unretained_traits::MayNotDangle,0>,media::VideoEncoder::Options,base::RepeatingCallback<void (media::VideoEncoderOutput, absl::optional<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> > >)>,base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:976
			#6 0x7ff82f90dd96 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:186
			#7 0x7ff8371463bf in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:643
			#8 0x7ff8371475c9 in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:628
			#9 0x7ff83714577a in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:485
			#10 0x7ff83714481f in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:400
			#11 0x7ff83c61f01e in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:480
			#12 0x7ff83c61e1bf in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:356
			#13 0x7ff82f82ba51 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133
			#14 0x7ff7c21e58b3 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
			#15 0x7ff914027613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
			#16 0x7ff9145426a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

		Address 0x1221d7f5bf30 is a wild pointer inside of access range of size 0x000000000004.
		SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\libaom\source\libaom\av1\encoder\svc_layercontext.c:567 in av1_svc_check_reset_layer_rc_flag
		Shadow bytes around the buggy address:
		  0x1221d7f5bc80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5bd00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5bd80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5be00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5be80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		=>0x1221d7f5bf00: fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa
		  0x1221d7f5bf80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5c000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5c080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5c100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		  0x1221d7f5c180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
		Shadow byte legend (one shadow byte represents 8 application bytes):
		  Addressable:           00
		  Partially addressable: 01 02 03 04 05 06 07
		  Heap left redzone:       fa
		  Freed heap region:       fd
		  Stack left redzone:      f1
		  Stack mid redzone:       f2
		  Stack right redzone:     f3
		  Stack after return:      f5
		  Stack use after scope:   f8
		  Global redzone:          f9
		  Global init order:       f6
		  Poisoned by user:        f7
		  Container overflow:      fc
		  Array cookie:            ac
		  Intra object redzone:    bb
		  ASan internal:           fe
		  Left alloca redzone:     ca
		  Right alloca redzone:    cb
		Thread T4 created by T0 here:
			#0 0x7ff7c21e4392 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
			#1 0x7ff82f82a87f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198
			#2 0x7ff83c61ca09 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:193
			#3 0x7ff837164c95 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl::<lambda_2>::operator() C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:179
			#4 0x7ff8371647b7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ../../base/task/thread_pool/thread_group_impl.cc:178:37'> C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:146
			#5 0x7ff837164246 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:178
			#6 0x7ff83715ad8e in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:102
			#7 0x7ff83715aa3b in base::internal::ThreadGroupImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:408
			#8 0x7ff832e81f79 in base::internal::ThreadPoolImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:213
			#9 0x7ff832358cbf in content::ChildProcess::ChildProcess C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:115
			#10 0x7ff83b20df19 in content::RenderProcess::RenderProcess C:\b\s\w\ir\cache\builder\src\content\renderer\render_process.cc:18
			#11 0x7ff83603a650 in content::RenderProcessImpl::RenderProcessImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:106
			#12 0x7ff83603ac97 in content::RenderProcessImpl::Create C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:281
			#13 0x7ff8326a1fb0 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:273
			#14 0x7ff82e0a5a5e in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:767
			#15 0x7ff82e0a8ac1 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1140
			#16 0x7ff82e0a33e7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:326
			#17 0x7ff82e0a40f1 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:343
			#18 0x7ff8220b171d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:187
			#19 0x7ff7c21363e4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
			#20 0x7ff7c2132bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:390
			#21 0x7ff7c2561aab in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
			#22 0x7ff914027613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
			#23 0x7ff9145426a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)


		==13184==ADDITIONAL INFO

		==13184==Note: Please include this section with the ASan report.
		Task trace:
			#0 0x7ff82507fe4f in media::OffloadingVideoEncoder::ChangeOptions C:\b\s\w\ir\cache\builder\src\media\video\offloading_video_encoder.cc:74
			#1 0x7ff82507ed0b in media::OffloadingVideoEncoder::WrapCallback<base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)> > C:\b\s\w\ir\cache\builder\src\media\video\offloading_video_encoder.cc:96
			#2 0x7ff825080329 in media::OffloadingVideoEncoder::Flush C:\b\s\w\ir\cache\builder\src\media\video\offloading_video_encoder.cc:83
			#3 0x7ff8306645a8 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1011


    ==13184==END OF ADDITIONAL INFO
    ==13184==ABORTING




### Credit

Discovered by Piotr Bania of Cisco Talos.
https://talosintelligence.com/vulnerability_reports/




## Attachments

- [TALOS-2023-1751 - Google_Chrome_VideoEncoder_av1_svc_check_reset_layer_rc_flag_use-after-free_vulnerability.txt](attachments/TALOS-2023-1751 - Google_Chrome_VideoEncoder_av1_svc_check_reset_layer_rc_flag_use-after-free_vulnerability.txt) (text/plain, 17.5 KB)
- [e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.htm](attachments/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.htm) (text/plain, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 32.6 KB)

## Timeline

### vu...@sourcefire.com (2023-05-22)

reward_to-piotr_at_thelead82.com


### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### aj...@google.com (2023-05-23)

Thanks for the report - this UAF repros in the renderer on ~ HEAD.

-> eugene as they appear in a lot of the history

[Monorail components: Internals>Media]

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### eu...@chromium.org (2023-05-23)

Got this on my Linux box

chrome: ../../third_party/libaom/source/libaom/av1/encoder/svc_layercontext.c:434: void av1_set_svc_fixed_mode(AV1_COMP *const): Assertion `svc->number_spatial_layers >= 1 && svc->number_spatial_layers <= 3 && svc->number_temporal_layers >= 1 && svc->number_temporal_layers <= 3' failed.


### eu...@chromium.org (2023-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-05-23)

@eugene: Did you check to see why our own fuzzer didn't find this? Are we seeding av1 svc content?

### [Deleted User] (2023-05-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f312efac1b90117729e8961b58c643fc0eae1fbd

commit f312efac1b90117729e8961b58c643fc0eae1fbd
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Tue May 23 18:12:36 2023

webcodecs: Fix crash when changing temporal layer count in AV1 encoder

Bug: 1447568
Change-Id: I4ecb02ed956707571573a65ade17fdffe676b502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4554300
Auto-Submit: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1148041}

[modify] https://crrev.com/f312efac1b90117729e8961b58c643fc0eae1fbd/media/video/software_video_encoder_test.cc
[modify] https://crrev.com/f312efac1b90117729e8961b58c643fc0eae1fbd/media/video/av1_video_encoder.cc


### eu...@chromium.org (2023-05-24)

It turned out that SVC settings aren't even in the fuzzer proto inputs for VideoEncoder 
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webcodecs/fuzzer_inputs.proto;l=82

### da...@chromium.org (2023-05-24)

Ah, that's too bad, lets make sure we add that before closing this as fixed. Thanks!

### gi...@appspot.gserviceaccount.com (2023-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1

commit 38607f3b15a2e8a0ac1af747b3588a7ee8013fc1
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Wed May 24 22:36:53 2023

webcodecs: Fuzz all config params of VideoEncoder

Bug: 1447568
Change-Id: I485be69140065fd32520c749cd36882621fcffe4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4561206
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1148797}

[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_seed_corpus/video_encoder/encode_vp8.textproto
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_seed_corpus/video_encoder/encode_av1.textproto
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_seed_corpus/video_encoder/encode_vp9.textproto
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/video_encoder.cc
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_utils.h
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_inputs.proto
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_utils.cc
[modify] https://crrev.com/38607f3b15a2e8a0ac1af747b3588a7ee8013fc1/third_party/blink/renderer/modules/webcodecs/fuzzer_seed_corpus/video_encoder/encode_h264.textproto


### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-06-01)

[Empty comment from Monorail migration]

### eu...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

Requesting merge to stable M114 because latest trunk commit (1148797) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1148797) appears to be after beta branch point (1148114).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-10)

Requesting merge to stable M114 because latest trunk commit (1148797) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1148797) appears to be after beta branch point (1148114).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-11)

Requesting merge to stable M114 because latest trunk commit (1148797) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1148797) appears to be after beta branch point (1148114).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-12)

Requesting merge to stable M114 because latest trunk commit (1148797) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1148797) appears to be after beta branch point (1148114).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-12)

Updating with OS as it wasn't visible in the merge review queue due to lack of OS.
In the future, please close security bugs as fixed when the resolving CL is landed. There is a ~2 week diff between CL landing and being updated for merge review due to not being closed. 

### am...@chromium.org (2023-06-12)

updating reward to as per OP report acknowledgement to Piotr Bania; OP please correct me if this is not correct 

### eu...@chromium.org (2023-06-12)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4554300

> 2. Has this fix been tested on Canary?
yes

> 3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
yes

> 4. Does this fix pose any known compatibility risks?
no

> 5. Does it require manual verification by the test team? If so, please describe required testing.
yes, open e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.htm from the report
and wait couple of minutes for the tab to crash.

### [Deleted User] (2023-06-13)

Requesting merge to stable M114 because latest trunk commit (1148797) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1148797) appears to be after beta branch point (1148114).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-13)

https://chromium-review.googlesource.com/c/chromium/src/+/4554300 was landed on 115 so no 115 merge needed 

Please merge this fix to M114 / branch 5735 at your earliest convenience (but before Monday, 26 June) so this fix can be included in the next M114/Stable security refresh and M114/Extended Stable RC 

Also, thank you for the additional work here to ensure future SVC issues can be potentially discovered by fuzzing 

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations, Piotr! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eu...@chromium.org (2023-06-20)

amyressler@
mac-rel bot is broken for M114 branch. Currently I can't submit a cherry-pick CL.

### gi...@appspot.gserviceaccount.com (2023-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/60b93798c9914b1320a53aef6bfa275302d93924

commit 60b93798c9914b1320a53aef6bfa275302d93924
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Wed Jun 21 17:57:52 2023

[M114] webcodecs: Fix crash when changing temporal layer count in AV1 encoder

(cherry picked from commit f312efac1b90117729e8961b58c643fc0eae1fbd)

Bug: 1447568
Change-Id: I4ecb02ed956707571573a65ade17fdffe676b502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4554300
Auto-Submit: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1148041}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4610718
Cr-Commit-Position: refs/branch-heads/5735@{#1360}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/60b93798c9914b1320a53aef6bfa275302d93924/media/video/software_video_encoder_test.cc
[modify] https://crrev.com/60b93798c9914b1320a53aef6bfa275302d93924/media/video/av1_video_encoder.cc


### am...@chromium.org (2023-06-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### pg...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2023-07-20)

[Empty comment from Monorail migration]

### rz...@google.com (2023-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-07-25)

1. Just https://crrev.com/c/4705203
2. Low, only conflicts in the added test
3. 114
4. Yes

### gm...@google.com (2023-07-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ce6b6f5fca649be67e4a038e32342c2aa692341

commit 1ce6b6f5fca649be67e4a038e32342c2aa692341
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Thu Jul 27 14:34:25 2023

[M108-LTS] webcodecs: Fix crash when changing temporal layer count in AV1 encoder

M108 Merge issues:
  media/video/software_video_encoder_test.cc:
    ChangeLayers():
      - Changed scalability_mode to SVCScalabilityMode::kL1T2 as
      kL1T1 isn't present in M108.
      - RunUntilQuit() isn't available, changed to RunUntilIdle()

(cherry picked from commit f312efac1b90117729e8961b58c643fc0eae1fbd)

Bug: 1447568
Change-Id: I4ecb02ed956707571573a65ade17fdffe676b502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4554300
Auto-Submit: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1148041}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4705203
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1497}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/1ce6b6f5fca649be67e4a038e32342c2aa692341/media/video/software_video_encoder_test.cc
[modify] https://crrev.com/1ce6b6f5fca649be67e4a038e32342c2aa692341/media/video/av1_video_encoder.cc


### rz...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1447568?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1450161]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064728)*
