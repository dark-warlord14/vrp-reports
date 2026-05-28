# UAF in chrome::CloseAllBrowsers() with popin

| Field | Value |
|-------|-------|
| **Issue ID** | [388400226](https://issues.chromium.org/issues/388400226) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | et...@chromium.org |
| **Created** | 2025-01-08 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

UaF in chrome::CloseAllBrowsers() while opening the target web page.

VERSION
Chrome Version: 134.0.6944.0 canary
Operating System: [Linux]

REPRODUCTION CASE

To make reproduction more easier, I use the puppeteer-core to reproduce this UAF:

1. Under the same directory of the `run_poc.js`, install `npm i puppeteer-core`
2. Setup poc.html and sub.html with a https server. For example `http-server -S -p 8000 -a 127.0.0.1`
3. Modity your asan chrome path in the run_poc.js and just `node run_poc.js`

You would immediately notice the ASAN trace stack which I attached.

The root cause is working in progress and is coming soon. Note that this issue is related with the kPartitionedPopins (i.e., Partitioned Popins) features.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [browser]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: ret2happy

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 15.5 KB)
- [poc.html](attachments/poc.html) (text/html, 202 B)
- [run_poc.js](attachments/run_poc.js) (text/javascript, 1.1 KB)
- [sub.html](attachments/sub.html) (text/html, 74 B)
- [asan_1403981.txt](attachments/asan_1403981.txt) (text/plain, 21.1 KB)

## Timeline

### jd...@chromium.org (2025-01-08)

Thanks for the report. I'm unable to reproduce this in 134.0.6945.0 using your exact process. Are you still able to reproduce this issue?

### ha...@gmail.com (2025-01-09)

Hi,

I'm able to reproduce at the ToT chrome as well. The PoC works well. You could try the following latest version at 

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1403981.zip\?generation\=1736396583544462\&alt\=media

Note that you should try the PoC on the Linux machine.

I also attached the asan stack trace of the asan-linux-release-1403981

### pe...@google.com (2025-01-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### jd...@chromium.org (2025-01-10)

I'm still unable to reproduce this, on 134.0.6947.0 asan under linux, which is past the branch position of the asan you're using (1404121 vs 1403981). Given that the poc is pretty trivial, I'm inclined to think that the issue may be on your side, so I'm closing this bug as unable to reproduce. If you're able to narrow down the issue and increase the odds that we can reproduce it, feel free to submit a new report. Thanks!

### ha...@gmail.com (2025-01-10)

> "The poc is pretty trivial" 

I don't think that the poc which leveraging the popin feature and IDP client shutdown is trivial. Additionally, the PoC involved with the IDP client which send the closeBrowser instruction to the chromium, while the popin window is still handling the message during shutdown. Hence I think it is worth and hard to be found by the testing suite of the chromium. Indeed, this is a issue which related with the browser shutdown and deserved less focus and the severity, but I don't think it is trivial/simple enough for us to ignore it.

> "unable to reproduce"

You didn't tell me what output you get, and which nodejs/puppeteer-core version you're using. To align our setup, my environment:

nodejs: v18.19.1
puppeteer-core@^22.10
Ubuntu 22.04.4 LTS

I think you should align with my puppetter-core version by `npm install puppeteer-core@^22.10` to try it again.



### ha...@gmail.com (2025-01-10)

Additionally, there's some notes to reproduce it correctly:

1. Must use https-server rather than the http. (Http doesn't work, setup the SSL keys with `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes`)
2. You might need headless mode, add `headless: true,` in `puppeteer.launch` arguments.
3. You could try to run the chrome under the Xvbf display. Firstly, `Xvfb :99 -screen 0 1024x768x24 &` and `export DISPLAY=:98 && node run_poc.js`

### jd...@chromium.org (2025-01-10)

Ah ha. I'm sorry to have doubted you. I was able to reproduce this this morning (my error) across all channels using your script. I can't get the race to occur outside of your script.

Unfortunately I'm about to be OOO so leaving for the next Chrome Security Shepherd to further route and triage (I'm sorry, arthursonzogni@!), but tentatively setting sev-high since it's a race requiring browser shutdown, but is still potentially a web-reachable browser UAF.

### pe...@google.com (2025-01-11)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-11)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ar...@chromium.org (2025-01-13)

**security shepherd**

This seems to rely on disabled by default flags.

```
            "--no-sandbox",
            "--ignore-certificate-errors",
            "--enable-experimental-web-platform-features",
            "--disable-popup-blocking",

```

So, this is `Security_Impact-None` a priori.

### ar...@chromium.org (2025-01-13)

Please ignore my previous message. I do now understand they are not key part of the bug. They are just needed because this reproducer is using pupetter.

### ar...@chromium.org (2025-01-13)

I wasn't able to reproduce, but the provided stack\_traces are very helpful to understand the issue.

My understanding is this is a race in between closing Chrome twice with pupetter from two different paths:

- [T=0s] `browser_.close()` => `ChromeDevToolsManagerDelegate::CloseBrowserSoon`
- [T=5s] `process.exit(0)` => `kill signal`.

The first is "holding" a non MiraclePtr-protected list of pointers on the `std::vector<Browser*>`  stack objct. It really shouldn't. Then it iterates on them.

```
  // Make a copy of the BrowserList to simplify the case where we need to
  // destroy a Browser during the loop.
  std::vector<Browser*> browser_list_copy;
  base::ranges::copy(*BrowserList::GetInstance(),
                     std::back_inserter(browser_list_copy));

  bool ignore_unload_handlers = browser_shutdown::ShouldIgnoreUnloadHandlers();

  for (auto* browser : browser_list_copy) {

```

The issue is that we are also killing chrome from elsewhere while this happen. So it will use a dangling pointer.

- OWNER of `chrome/browser/lifetime/`, could you please take a look? [etienneb@chromium.org](mailto:etienneb@chromium.org)

To debug, I would suggest using `raw_ptr` in `std::vector<Browser*>` with the dangling pointer detector. This will "record" the stacktrace of who deleted the browser.

---

From the [Severity guideline](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md), I think this would fall into:

```
Not web accessible, reliant solely on direct UI interaction to trigger.

```
```
Bugs that require implausible interaction, interactions a user would not realistically be convinced to perform, will generally be downgraded to a functional bug and not considered a security bug.

```

If you manage to trigger this without pupetter, but from a regular website, please let us know!

### ha...@gmail.com (2025-01-13)

I was shocked by the bug type changed due to the triggering method of the pupetter and even the UaF would be expose as publicly known. Historical bug invoved with the pupetter reproduction are also considered as the security issue, I'm not sure whether this assumption is changed.

### ha...@gmail.com (2025-01-13)

I was disappointed by the triage result. I think you could FIRSTLY read the following issue carefully before turing this issue into the functional bug:

issues.chromium.org/issues/40063589
issues.chromium.org/issues/40061099

### ha...@gmail.com (2025-01-13)

I'm happy to provide more cases in case of the my mis-understanding of the security guideline, and feel free to correct me if I'm wrong on the understanding of the historical issue which relies on the pupetter-core:
issues.chromium.org/issues/40061670
issues.chromium.org/issues/40069416
issues.chromium.org/issues/40061275

I agree that this issue requires the shutdown, which can be downgraded and hence I didn't take too much time on the RCA analysis. However, I do put a lot of time minimizing the PoC for you to trigger it. Instead of tackling the underlying UaF issues, just closing it as so-called "can't reproduced" without more confimation and turing it into the functional bug as the PoC is somewhat "implausible" are beyond my imagination to be honst. If you fail to reproduce it, we could align the environment and I'm happy to provide more context to reproduce/investigate. 

### ar...@chromium.org (2025-01-13)

I am very sorry you feel that way. I would be happy to switch it back to `vulnerability` if we can show how an attacker could trigger.
Note that this bug is not closed. This is still a valid bug and needs to be fixed.

Using puppeteer is fine to automate a reproducer and simulate a user. However it seems to be using capabilities an attacker don't have.

```
async function close_browser(browser_) {
    await sleep2(5000);
    setTimeout(
        function () {
            process.exit(0);
        }, 5000
    )
    await browser_.close();
}

```

To reproduce, this relies on being able to execute a race in between:

- Sending the signal to kill the chrome process.
- Sending the devtool message: `ChromeDevToolsManagerDelegate::CloseBrowserSoon`

An attacker do not have access neither of both.

I am going to ask around whether bugs attackers can't trigger would still be considered vulnerabilities. I will add another reply this afternoon.

### ar...@chromium.org (2025-01-13)

To get around the certificate error, I minimized the test case. I found a lot of unnecessary steps. In particular, there are no need to send a kill signal to chrome to produce a race (there are no race). So, this is something you might be able to trigger without puppetter.

**run\_poc.mjs**

```
import puppeteer from 'puppeteer-core';

const chrome_path = "/home/arthursonzogni/asan/chrome"
const target_url = "https://functional-juicy-drop.glitch.me/";

const browser = await puppeteer.launch({
    args: [
        "--no-sandbox", // For convenience with ASAN.
        "--enable-experimental-web-platform-features", // Required.
        "--disable-popup-blocking", // For convenience.
        "--user-data-dir=/tmp/noexists", // For convenience.
        target_url
    ],
    ignoreDefaultArgs: true,
    dumpio: true,
    executablePath: chrome_path,
    env: {
        ...process.env,
        'ASAN_OPTIONS': 'detect_odr_violation=0',
    }
});
// Wait for the browser to open a new tab
await new Promise((resolve) => setTimeout(resolve, 5000));

// Close the browser
await browser.close();

```

**package.json**

```
{
  "name": "poc_1",
  "version": "1.0.0",
  "main": "run_poc.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "description": "",
  "dependencies": {
    "puppeteer-core": "^22.10"
  }
}

```

**Usage**

```
npm install
node ./run_poc.mjs

```

I hosted the minimized test case on <https://functional-juicy-drop.glitch.me/>. It was minimized by:

**index.html**

```
<script>
  window.open("/sub.html", '_blank', 'popin');
</script>

```

**sub.html**

```
~Empty file

```

### ar...@chromium.org (2025-01-13)

- `Severity`: High: UAF in the browser process, but only during shutdown)
- `Impact:`: None: Requires disabled by default flags: `--enable-experimental-web-platform-features`.

### ar...@chromium.org (2025-01-13)

[arichiv@chromium.org](mailto:arichiv@chromium.org): I believe you would be a great assignee for the popin bug. Could you please take a look?

### et...@chromium.org (2025-01-17)

Thanks for the very detailed bug.
I am able to reproduce on my cloudtop.

I sent to the CQ this check to see whether it would already be detected with our tests.
https://chromium-review.googlesource.com/c/chromium/src/+/6180235?tab=checks

I added logs and clearly the browser is no longer in the list when we do delete it.
[1491861:1491861:0116/225156.655861:ERROR:browser_close_manager.cc(192)] To delete: 0x7cb43dcd6080
[1491861:1491861:0116/225156.655905:ERROR:browser_close_manager.cc(192)] To delete: 0x7cb43de2f380
[1491861:1491861:0116/225156.655924:ERROR:browser_close_manager.cc(196)] delete: 0x7cb43dcd6080
[1491861:1491861:0116/225157.027506:ERROR:browser_close_manager.cc(196)] delete: 0x7cb43de2f380
[1491861:1491861:0116/225157.027580:ERROR:browser_close_manager.cc(198)] was deleted: 0x7cb43de2f380

It's deleted on the same thread; it's not a race. The cause is re-entrancy due to run-loop.

Here is a flamegraph of crashes that may help us find other cases where this could crash.
https://pprof.corp.google.com/?id=8aace16c3687812178bb127653fdfd1c&filter=focus:BrowserCloseManager%253A%253ACloseBrowsers



### et...@chromium.org (2025-01-17)

I added more logs and this is the stackframe where the both browser got deleted.

This repro was not on a ASAN build. We can still see the double browser removal from the list.

```
[1499140:1499209:0116/231834.128727:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT
[1499140:1499140:0116/231834.936356:ERROR:browser_close_manager.cc(192)] To delete: 0x7d4428cd6080
[1499140:1499140:0116/231834.936424:ERROR:browser_close_manager.cc(192)] To delete: 0x7d4428e38680
[1499140:1499140:0116/231834.936445:ERROR:browser_close_manager.cc(196)] delete: 0x7d4428cd6080
[1499140:1499140:0116/231835.161594:ERROR:browser_list.cc(111)] Remove browser: 0x7d4428e38680
[1499140:1499140:0116/231835.323300:ERROR:browser_list.cc(111)] Remove browser: 0x7d4428cd6080
[1499140:1499140:0116/231835.324750:ERROR:browser_close_manager.cc(196)] delete: 0x7d4428e38680
```
The two call to RemoveBrowser(....) do happens on that stackframe:

#0 0x55ed701ff532 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1053:7]
#1 0x55ed701e7aa0 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:254:20]
#2 0x55ed6e5b6ee3 BrowserList::RemoveBrowser() [../../chrome/browser/ui/browser_list.cc:114:17]
#3 0x55ed7429d3b6 Browser::~Browser() [../../chrome/browser/ui/browser.cc:734:3]
#4 0x55ed7429de7e Browser::~Browser() [../../chrome/browser/ui/browser.cc:698:21]
#5 0x55ed74653039 BrowserView::~BrowserView() [../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5]
#6 0x55ed74653668 BrowserView::~BrowserView() [../../chrome/browser/ui/views/frame/browser_view.cc:1126:29]
#7 0x55ed72e114bd views::View::~View() [../../ui/views/view.cc:289:9]
#8 0x55ed746cefca BrowserNonClientFrameView::~BrowserNonClientFrameView() [../../chrome/browser/ui/views/frame/browser_non_client_frame_view.cc:69:1]
#9 0x55ed74a64482 OpaqueBrowserFrameView::~OpaqueBrowserFrameView() [../../chrome/browser/ui/views/frame/opaque_browser_frame_view.cc:152:49]
#10 0x55ed74a47773 BrowserFrameViewLinux::~BrowserFrameViewLinux() [../../chrome/browser/ui/views/frame/browser_frame_view_linux.cc:41:47]
#11 0x55ed74aa4828 BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() [../../chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:51:59]
#12 0x55ed74aa49be BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() [../../chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:51:59]
#13 0x55ed72e5093d views::NonClientView::~NonClientView() [../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5]
#14 0x55ed72e50a5e views::NonClientView::~NonClientView() [../../ui/views/window/non_client_view.cc:179:33]
#15 0x55ed72e12dd9 views::View::DoRemoveChildView() [../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5]
#16 0x55ed72e12e55 views::View::RemoveAllChildViews() [../../ui/views/view.cc:365:5]
#17 0x55ed72e32f57 views::Widget::DestroyRootView() [../../ui/views/widget/widget.cc:2375:15]
#18 0x55ed72e326a6 views::Widget::~Widget() [../../ui/views/widget/widget.cc:275:3]
#19 0x55ed74647815 BrowserFrame::~BrowserFrame() [../../chrome/browser/ui/views/frame/browser_frame.cc:126:29]
#20 0x55ed7464790e BrowserFrame::~BrowserFrame() [../../chrome/browser/ui/views/frame/browser_frame.cc:126:29]
#21 0x55ed72e76088 views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() [../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5]
#22 0x55ed74aa56c0 DesktopBrowserFrameAura::~DesktopBrowserFrameAura() [../../chrome/browser/ui/views/frame/desktop_browser_frame_aura.cc:40:51]
#23 0x55ed746bd6e4 DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() [../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:32:61]
#24 0x55ed746bd79e DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() [../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:32:61]
#25 0x55ed72e768ca views::DesktopNativeWidgetAura::OnHostClosed() [../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:391:5]
#26 0x55ed72e8d886 views::DesktopWindowTreeHostPlatform::OnClosed() [../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:949:32]
#27 0x55ed698d87de ui::X11Window::Close() [../../ui/ozone/platform/x11/x11_window.cc:496:30]
#28 0x55ed72e8ad98 views::DesktopWindowTreeHostPlatform::CloseNow() [../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:421:22]
#29 0x55ed72e79f60 views::DesktopNativeWidgetAura::CloseNow() [../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:932:32]
#30 0x55ed72e35df5 views::Widget::CloseNow() [../../ui/views/widget/widget.cc:958:21]
#31 0x55ed7465cd4c BrowserView::DestroyBrowser() [../../chrome/browser/ui/views/frame/browser_view.cc:2962:11]
#32 0x55ed6fd9a611 BrowserCloseManager::CloseBrowsers() [../../chrome/browser/lifetime/browser_close_manager.cc:211:26]
#33 0x55ed6fd99ae8 chrome::CloseAllBrowsers() [../../chrome/browser/lifetime/application_lifetime_desktop.cc:181:26]
#34 0x55ed6fb909b2 chrome::ExitIgnoreUnloadHandlers() [../../chrome/browser/lifetime/application_lifetime.cc:49:39]
#35 0x55ed68d660d1 base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#36 0x55ed7015b02d base::TaskAnnotator::RunTaskImpl() [../../base/task/common/task_annotator.cc:210:34]
#37 0x55ed7018ee6b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl() [../../base/task/common/task_annotator.h:106:5]
#38 0x55ed7018e104 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40]
#39 0x55ed7018f605 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#40 0x55ed7021f629 base::MessagePumpGlib::Run() [../../base/message_loop/message_pump_glib.cc:702:48]
#41 0x55ed7018ffb1 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:643:12]
#42 0x55ed70134386 base::RunLoop::Run() [../../base/run_loop.cc:134:14]
#43 0x55ed6cddfd01 content::BrowserMainLoop::RunMainMessageLoop() [../../content/browser/browser_main_loop.cc:1092:18]
#44 0x55ed6cde2001 content::BrowserMainRunnerImpl::Run() [../../content/browser/browser_main_runner_impl.cc:156:15]
#45 0x55ed6cddbef0 content::BrowserMain() [../../content/browser/browser_main.cc:32:28]
#46 0x55ed6f0ddf18 content::RunBrowserProcessMain() [../../content/app/content_main_runner_impl.cc:710:10]
#47 0x55ed6f0e0899 content::ContentMainRunnerImpl::RunBrowser() [../../content/app/content_main_runner_impl.cc:1288:10]
#48 0x55ed6f0e0081 content::ContentMainRunnerImpl::Run() [../../content/app/content_main_runner_impl.cc:1140:12]
#49 0x55ed6f0dcab0 content::RunContentProcess() [../../content/app/content_main.cc:348:36]
#50 0x55ed6f0dcc94 content::ContentMain() [../../content/app/content_main.cc:361:10]
#51 0x55ed68b423f5 ChromeMain [../../chrome/app/chrome_main.cc:222:12]
#52 0x7f9d0dd67c8a (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29c89)
#53 0x7f9d0dd67d45 __libc_start_main
#54 0x55ed68b4202a _start


### ar...@chromium.org (2025-01-17)

Ooops, It looks like I wanted to add [arichiv@chromium.org](mailto:arichiv@chromium.org) (author of popin) in comment 20, but failed to do so.
+CC [arichiv@chromium.org](mailto:arichiv@chromium.org) for visibility.

You might want to reassign to him if the bug is indeed specific to the popin implementation.

### ar...@chromium.org (2025-01-22)

https://chromium-review.googlesource.com/c/chromium/src/+/6179704 looks like the right fix, thanks!

### ap...@google.com (2025-01-22)

Project: chromium/src  

Branch: main  

Author: Etienne Bergeron <[etienneb@chromium.org](mailto:etienneb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6179704>

Fix: Safely delete browsers on shutdown

---


Expand for full commit details
```
Fix: Safely delete browsers on shutdown 
 
The current code for deleting browsers on shutdown is not safe because closing a browser window may close other browser windows (e.g., popin feature). The current approach of copying the list of browsers before deleting is not enough to ensure safety. 
 
This change introduces an observer to keep the list of browsers up to date, ensuring that browsers are deleted safely. 
 
Bug: 388400226 
 
Change-Id: I158a22170bfbaf614fdd884d57ddd4dc653490c4 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179704 
Commit-Queue: Etienne Bergeron <etienneb@chromium.org> 
Reviewed-by: Gabriel Charette <gab@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1409687}

```

---

Files:

- M `chrome/browser/lifetime/browser_close_manager.cc`

---

Hash: 0883dc5859694ef5dbcab5006f9c8c81c8358028  

Date:  Wed Jan 22 08:26:55 2025


---

### ap...@google.com (2025-01-22)

Project: chromium/src  

Branch: main  

Author: [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) <[luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)>  

Link:      <https://chromium-review.googlesource.com/6192304>

Revert "Fix: Safely delete browsers on shutdown"

---


Expand for full commit details
```
Revert "Fix: Safely delete browsers on shutdown" 
 
This reverts commit 0883dc5859694ef5dbcab5006f9c8c81c8358028. 
 
Reason for revert: 
LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5703485266853888 
 
Sample build with failed test: https://ci.chromium.org/b/8725020453320881169 
Affected test(s): 
[ninja://chrome/test:browser_tests/TabManagerTest.DiscardTabsWithOccludedWindow/RetainedWebContents](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fchrome%2Ftest:browser_tests%2FTabManagerTest.DiscardTabsWithOccludedWindow%2FRetainedWebContents?q=VHash%3Addee393e1fa4b060) 
 
If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5703485266853888&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F6179704&type=BUG 
 
Original change's description: 
> Fix: Safely delete browsers on shutdown 
> 
> The current code for deleting browsers on shutdown is not safe because closing a browser window may close other browser windows (e.g., popin feature). The current approach of copying the list of browsers before deleting is not enough to ensure safety. 
> 
> This change introduces an observer to keep the list of browsers up to date, ensuring that browsers are deleted safely. 
> 
> Bug: 388400226 
> 
> Change-Id: I158a22170bfbaf614fdd884d57ddd4dc653490c4 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179704 
> Commit-Queue: Etienne Bergeron <etienneb@chromium.org> 
> Reviewed-by: Gabriel Charette <gab@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1409687} 
> 
 
Bug: 388400226 
Change-Id: Ia9f36e75cc081a9ea43a36742ae9f37a90fa397a 
No-Presubmit: true 
No-Tree-Checks: true 
No-Try: true 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6192304 
Reviewed-by: Solomon Kinard <solomonkinard@chromium.org> 
Owners-Override: Solomon Kinard <solomonkinard@google.com> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/heads/main@{#1409956}

```

---

Files:

- M `chrome/browser/lifetime/browser_close_manager.cc`

---

Hash: 34f953d4cb4e5019709dd93d4a32223dd487b9da  

Date:  Wed Jan 22 14:04:26 2025


---

### et...@chromium.org (2025-01-23)

The revert seems to be related to an other issue:

 ==162785==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x579cb8e5d581 in base::(anonymous namespace)::CopyStackSignalHandler(int, siginfo_t*, void*) ./../../base/profiler/stack_copier_signal.cc:167:22
    #1 0x579c96f252dd in SignalAction(int, void*, void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cpp:1136:3
    #2 0x79013964531f  (third_party/instrumented_libs/binaries/msan-chained-origins-noble-lib/lib/libc.so.6+0x4531f) (BuildId: 08134323d00289185684a4cd177d202f39c2a5f3)
    #3 0x7901399f6a63  (third_party/instrumented_libs/binaries/msan-chained-origins-noble-lib/lib/libgcc_s.so.1+0x25a63) (BuildId: 92123f0e6223c77754bac47062c0b9713ed363df)
    #4 0x7901399f2099  (third_party/instrumented_libs/binaries/msan-chained-origins-noble-lib/lib/libgcc_s.so.1+0x21099) (BuildId: 92123f0e6223c77754bac47062c0b9713ed363df)
    #5 0x7901399f432d  (third_party/instrumented_libs/binaries/msan-chained-origins-noble-lib/lib/libgcc_s.so.1+0x2332d) (BuildId: 92123f0e6223c77754bac47062c0b9713ed363df)
    #6 0x579c96ebfcca in __sanitizer::BufferedStackTrace::UnwindSlow(unsigned long, unsigned int) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_unwind_linux_libcdep.cpp:130:3
    #7 0x579c96eba29c in __sanitizer::BufferedStackTrace::Unwind(unsigned int, unsigned long, unsigned long, void*, unsigned long, unsigned long, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_stacktrace_libcdep.cpp:158:7
    #8 0x579c96ec6c14 in __sanitizer::BufferedStackTrace::UnwindImpl(unsigned long, unsigned long, void*, bool, unsigned int) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan.cpp:342:12
    #9 0x579c96ec684e in Unwind /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/../sanitizer_common/sanitizer_stacktrace.h:130:5
    #10 0x579c96ec684e in __msan::PrintWarningWithOrigin(unsigned long, unsigned long, unsigned int) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan.cpp:247:3
    #11 0x579c96ec7101 in __msan_warning_with_origin_noreturn /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan.cpp:422:3
    #12 0x579cb2e69868 in TabStripModel::GetActiveWebContents() const ./../../chrome/browser/ui/tabs/tab_strip_model.cc:636:10
    #13 0x579cb99ec4b9 in resource_coordinator::TabLifecycleUnitSource::UpdateFocusedTab() ./../../chrome/browser/resource_coordinator/tab_lifecycle_unit_source.cc:192:58
    #14 0x579cb224b4c2 in BrowserList::RemoveBrowser(Browser*) ./../../chrome/browser/ui/browser_list.cc:118:14
    #15 0x579ccccadb71 in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:734:3
    #16 0x579ccccaf0ab in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:698:21
    #17 0x579ccd4fabe3 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #18 0x579ccd4fabe3 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #19 0x579ccd4fabe3 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #20 0x579ccd4fabe3 in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:1185:1
    #21 0x579ccd57ef35 in ~BrowserViewAsh ./../../chrome/browser/ui/views/frame/browser_view_ash.h:27:38
    #22 0x579ccd57ef35 in non-virtual thunk to BrowserViewAsh::~BrowserViewAsh() ./../../chrome/browser/ui/views/frame/browser_view_ash.h:0:0
    #23 0x579cbdf0b237 in views::View::~View() ./../../ui/views/view.cc:290:9
    #24 0x579ccd20b25f in BrowserNonClientFrameViewChromeOS::~BrowserNonClientFrameViewChromeOS() ./../../chrome/browser/ui/views/frame/browser_non_client_frame_view_chromeos.cc:142:73
    #25 0x579cbdf94355 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #26 0x579cbdf94355 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7

### gr...@chromium.org (2025-01-24)

[etienneb@chromium.org](mailto:etienneb@chromium.org): your CL triggered a bug in those tests. :-( i've sent <https://crrev.com/c/6198184> up to fix it. try relanding after that.

### ap...@google.com (2025-01-24)

Project: chromium/src  

Branch: main  

Author: Greg Thompson <[grt@chromium.org](mailto:grt@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6198184>

Fix UAF in TabManagerTest

---


Expand for full commit details
```
Fix UAF in TabManagerTest 
 
Clear the TabLifecycleUnitSource's faked focused TabStripModel during 
shutdown before browsers are closed. 
 
Bug: 388400226 
Change-Id: I30536b735d1b9fbaf3804f61f33ee5e1d524d50b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6198184 
Commit-Queue: Francois Pierre Doray <fdoray@chromium.org> 
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org> 
Auto-Submit: Greg Thompson <grt@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1410888}

```

---

Files:

- M `chrome/browser/resource_coordinator/tab_manager_browsertest.cc`

---

Hash: 27f79197927062e1a558898a714c4ae52490de93  

Date:  Fri Jan 24 06:27:32 2025


---

### et...@chromium.org (2025-01-24)

Thanks grt@. I had the repro and I can confirm that your fix worked.

Relanding the original fix.

### ap...@google.com (2025-01-24)

Project: chromium/src  

Branch: main  

Author: Etienne Bergeron <[etienneb@chromium.org](mailto:etienneb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6196398>

Reland "Fix: Safely delete browsers on shutdown"

---


Expand for full commit details
```
Reland "Fix: Safely delete browsers on shutdown" 
 
This is a reland of commit 0883dc5859694ef5dbcab5006f9c8c81c8358028 
 
Original change's description: 
> Fix: Safely delete browsers on shutdown 
> 
> The current code for deleting browsers on shutdown is not safe because closing a browser window may close other browser windows (e.g., popin feature). The current approach of copying the list of browsers before deleting is not enough to ensure safety. 
> 
> This change introduces an observer to keep the list of browsers up to date, ensuring that browsers are deleted safely. 
> 
> Bug: 388400226 
> 
> Change-Id: I158a22170bfbaf614fdd884d57ddd4dc653490c4 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179704 
> Commit-Queue: Etienne Bergeron <etienneb@chromium.org> 
> Reviewed-by: Gabriel Charette <gab@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1409687} 
 
Bug: 388400226 
Change-Id: Ic8cc97fedb704f252fb644efad0004b23e130532 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6196398 
Commit-Queue: Etienne Bergeron <etienneb@chromium.org> 
Reviewed-by: Gabriel Charette <gab@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1410959}

```

---

Files:

- M `chrome/browser/lifetime/browser_close_manager.cc`

---

Hash: cb0cd51b322784292668d85b017dd3db767b6d71  

Date:  Fri Jan 24 08:35:12 2025


---

### ma...@google.com (2025-01-30)

[security shepherd] Does the latest reland fully address the issue here? Can we mark this issue as fixed?

### et...@chromium.org (2025-01-31)

Yes. We won't expect changes in the field since the feature was not launched.
I was waiting to see if I can find other crashes during shutdown that could be related to the same issue but nothing obvious.

### am...@chromium.org (2025-02-06)

This is significantly mitigated by two sets of shutdowns and a non-standard workflow required by a user to execute. Shutdown issues are already considered moderate mitigations on their own. This issue, as presented, is very unlikely to be able to be reasonably exploited in real-world scenario. Reducing the accordingly.

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Report of highly mitigated issue in a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations! Thank you for your efforts and reporting this issue to us.

### et...@chromium.org (2025-02-10)

Thanks, on my side, I have to say that the repro steps were super useful. :)

### ch...@google.com (2025-05-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/388400226)*
