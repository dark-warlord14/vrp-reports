# Security: Web pages can load arbitrary extension modules

| Field | Value |
|-------|-------|
| **Issue ID** | [40084093](https://issues.chromium.org/issues/40084093) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-04-14 |
| **Bounty** | $4,000.00 |

## Description

Chrome version: 52.0.2709.0 and earlier (including 49.0.2623.75)

I've found several vulnerabilities in the extension module system that can be exploited from a web page without any user interaction.

Here's an overview of the vulnerabilities that I used to load arbitrary extension modules:

1. https://chromium.googlesource.com/chromium/src/+/c089219d5f8794747f7ab7b966b4676f49532e1f/extensions/renderer/resources/binding.js#543
   The generate() function loads a scheme and constructs an API. Then, the scheme is passed to runHooks_, which can be intercepted by web pages.

2. https://chromium.googlesource.com/chromium/src/+/2d124c0ce773bd5dd334e2c6168cbb66a4b224d6/extensions/renderer/v8_schema_registry.cc#68
   V8SchemaRegistry::GetSchema supplies the schema to step 1. The issue with this is that the schema object persists across page loads. So when step 1 modifies the scheme and reloads the page, the page can now generate arbitrary bindings.

3. https://chromium.googlesource.com/chromium/src/+/c089219d5f8794747f7ab7b966b4676f49532e1f/extensions/renderer/resources/binding.js#482
   https://chromium.googlesource.com/chromium/src/+/c089219d5f8794747f7ab7b966b4676f49532e1f/extensions/renderer/resources/binding.js#163
   With a crafted schema, we can now bypass several checks and ultimately load arbitrary JS extension modules... (starting at $ref at line 163, ending at 482).

4. https://chromium.googlesource.com/chromium/src/+/c089219d5f8794747f7ab7b966b4676f49532e1f/extensions/renderer/resources/binding.js#170
   The extension modules can be leaked by overriding Object.prototype.

5. So far, we were only able to load extension modules that were implemented in JavaScript. This is already quite powerful, but we can make even more use of this by importing the chrome.test API. This allows us to:
  - Access any extension module (chrome.test.getModuleSystem)
  - Load native modules (requireNative).
  - Bypass user gesture requirements (chrome.test.runWithoutUserGesture).
  - Trigger a use-after-free via another vulnerability (which I will report separately).



The attached proof of concept shows how the module system is abused to load native modules and:
  - Query the command line parameters and incognito state.
  - Detect whether an extension is installed (via the i18n native module - this is information leakage and ALSO a separate bug)


The most severe part of this bug is step 2, but all points should be addressed to reduce the risk of future exploits.

## Attachments

- [module-system-poc.html](attachments/module-system-poc.html) (text/plain, 9.4 KB)
- [webview-user-gesture.html](attachments/webview-user-gesture.html) (text/plain, 9.1 KB)
- [module-system-poc-v2.html](attachments/module-system-poc-v2.html) (text/plain, 10.1 KB)

## Timeline

### ts...@chromium.org (2016-04-15)

Guessing kalman@ may have some insight here, please re-assign as appropriate.

### ro...@robwu.nl (2016-04-15)

@tsepez
This bug affects all release channels. Shouldn't this be Security_Impact-Stable?

And is kalman back? I thought that he was gone.

### cl...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-04-15)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-04-15)

Nice finds, Rob.  A lot of these are being addressed, e.g. with https://crbug.com/chromium/601149 (I've cc'd you on it).  Specifically, this doesn't repro once https://codereview.chromium.org/1866103002/ lands, since that locks down runWithNativesEnabled, and other chrome.test functions are already locked down (e.g. runWith/WithoutUserGesture).  Also, it looks like this doesn't bypass all our access checks - e.g. hijacking tabs doesn't allow chrome.tabs.create because the context is still correctly classified as a web page.  So once we lock down our native functions better, hopefully this is a little less terrifying.

That said, this is yet-another-bindings-problem, so I'm leaning more and more towards trying to find a way to implement binding.js in C++.  But, well, it's painful.

### ro...@robwu.nl (2016-04-15)

Checking the feature availability in the native bindings is a good step towards hardening the module system (this is already enforced in the browser process and is why chrome.tabs.create does not work). But if there is a vulnerability to load modules (like this one), then it doesn't buy you much, because the functionality of native modules is exposed via Chrome's extension bindings in JS (which can be accessed via e.g. this bug).

For instance, even if chrome.test is locked down, the user gesture security can still be bypassed via https://chromium.googlesource.com/chromium/src/+/f89035216b627283b79731c3e6a7957707ed9034/extensions/renderer/resources/guest_view/web_view/web_view.js#218

// See attached PoC. This bug is used to leak webView, and the vulnerability from my last sentence is used to get something equivalent to chrome.test.runWithUserGesture.
webView.WebViewImpl.prototype.makeElementFullscreen.call({
  element:{
    webkitRequestFullScreen() {
      // This callback runs in the context of GuestViewInternalNatives.RunWithGesture, which disables user gesture security.
    }
  }
});

In this specific instance, I recommend to not expose a powerful completely-disable-user-gesture-security native message, but a more limited and special-purpose make-element-fullscreen binding.

### rd...@chromium.org (2016-04-16)

@6 whole-heartedly agree on the super-powerful guest view natives function.  We should change that.

### bu...@chromium.org (2016-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/585b125ef7168c104631e23ee5cad0108c838f52

commit 585b125ef7168c104631e23ee5cad0108c838f52
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Tue Apr 19 23:29:26 2016

[Extensions] More bindings improvements

Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
and broaden test access checks.

BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1899973002

Cr-Commit-Position: refs/heads/master@{#388353}

[modify] https://crrev.com/585b125ef7168c104631e23ee5cad0108c838f52/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/585b125ef7168c104631e23ee5cad0108c838f52/extensions/renderer/resources/binding.js
[modify] https://crrev.com/585b125ef7168c104631e23ee5cad0108c838f52/extensions/renderer/script_context.cc
[modify] https://crrev.com/585b125ef7168c104631e23ee5cad0108c838f52/extensions/renderer/v8_schema_registry.cc


### rd...@chromium.org (2016-04-20)

note: still to do - deep freeze schema.

### ro...@robwu.nl (2016-04-20)

Here's a new functional exploit.

runWithNatives is locked down in https://codereview.chromium.org/1866103002/, but this is not deterring exploitation because when a module is loaded by the module system, natives are already enabled.
Furthermore, GetAvailability()'s return value can trivially be spoofed because overriding Object.prototype.is_available in the second page (step 2) allows us to bypass the JS-side checks.

The JS-side availability check in bindings.js ought to prevent the API from showing up on the chrome object, and it is not solid. The fact that the module was loaded is a bigger issue, since the juicy native methods can already leak in several ways, e.g. by modifying APIFunctions.prototype.setHandleRequest (similar to my original PoC).

The most sensible way to move forward is to assume that all objects in JS are compromised, and then guard powerful C++ APIs.  The first few steps in my report bypassed checks, but were not harmful (in the context of this report). The vulnerabilities became exploitable because there is a call to require() that accepts arbitrary arguments without validation (step 3).

There is no need for createCustomType to be that powerful, so I've submitted a patch that makes it impossible to load arbitrary modules: https://codereview.chromium.org/1902263006

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/15574e83265d53f65ce653de0db34c738bdb89f9

commit 15574e83265d53f65ce653de0db34c738bdb89f9
Author: rob <rob@robwu.nl>
Date: Wed Apr 20 17:27:43 2016

Prevent module system from loading arbitrary modules

BUG=603725

Review URL: https://codereview.chromium.org/1902263006

Cr-Commit-Position: refs/heads/master@{#388526}

[modify] https://crrev.com/15574e83265d53f65ce653de0db34c738bdb89f9/extensions/renderer/resources/binding.js


### ro...@robwu.nl (2016-04-21)

1 was resolved by https://codereview.chromium.org/1902003003/
2 was partially resolved by https://codereview.chromium.org/1899973002/ and will fully be resolved by https://codereview.chromium.org/1906593002/
3 and 4 is resolved by 15574e83265d53f65ce653de0db34c738bdb89f9
5 is addressed by other issues and CLs.

With 15574e83265d53f65ce653de0db34c738bdb89f9, the vulnerabilities cannot be exploited to load arbitrary modules, so I'd like to merge this patch and close the bug.

### ti...@google.com (2016-04-21)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/75d1ac20150f0ace5c15c55c612de242d050c287

commit 75d1ac20150f0ace5c15c55c612de242d050c287
Author: Rob Wu <rob@robwu.nl>
Date: Thu Apr 21 20:00:21 2016

Prevent module system from loading arbitrary modules

BUG=603725

Review URL: https://codereview.chromium.org/1902263006

Cr-Commit-Position: refs/heads/master@{#388526}
(cherry picked from commit 15574e83265d53f65ce653de0db34c738bdb89f9)

Review URL: https://codereview.chromium.org/1912783002 .

Cr-Commit-Position: refs/branch-heads/2704@{#169}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/75d1ac20150f0ace5c15c55c612de242d050c287/extensions/renderer/resources/binding.js


### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5fb2548448bd1b76a59d941b729d7a7f90d53bc8

commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 21 23:19:24 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}

[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/binding.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/event.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/utils.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/v8_schema_registry.cc


### cl...@chromium.org (2016-04-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0f07d08bc3865436994b40aa620d8063fe7bbcc

commit f0f07d08bc3865436994b40aa620d8063fe7bbcc
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 28 22:26:20 2016

[Extensions] More bindings improvements

Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
and broaden test access checks.

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1899973002

Cr-Commit-Position: refs/heads/master@{#388353}
(cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)

Review URL: https://codereview.chromium.org/1930213002 .

Cr-Commit-Position: refs/branch-heads/2704@{#294}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/resources/binding.js
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/script_context.cc
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ed087c3f125239baa798fbbceded413d529674ed

commit ed087c3f125239baa798fbbceded413d529674ed
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 28 22:37:03 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}
(cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)

Review URL: https://codereview.chromium.org/1928783005 .

Cr-Commit-Position: refs/branch-heads/2704@{#295}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/binding.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/event.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/utils.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3f9ac15b6c55ed5fd923c469baff869a418852eb

commit 3f9ac15b6c55ed5fd923c469baff869a418852eb
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 00:24:32 2016

Revert of [Extensions] Finish freezing schema (patchset #1 id:1 of https://codereview.chromium.org/1928783005/ )

Reason for revert:
Compile failure

Original issue's description:
> [Extensions] Finish freezing schema
>
> BUG=604901
> BUG=603725
> BUG=591164
>
> Review URL: https://codereview.chromium.org/1906593002
>
> Cr-Commit-Position: refs/heads/master@{#388945}
> (cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)
>
> Committed: https://chromium.googlesource.com/chromium/src/+/ed087c3f125239baa798fbbceded413d529674ed

TBR=
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=604901

Review-Url: https://codereview.chromium.org/1928193002
Cr-Commit-Position: refs/branch-heads/2704@{#301}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/binding.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/event.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/utils.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0

commit 21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 00:33:47 2016

Revert of [Extensions] More bindings improvements (patchset #1 id:1 of https://codereview.chromium.org/1930213002/ )

Reason for revert:
Compile fail

Original issue's description:
> [Extensions] More bindings improvements
>
> Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
> and broaden test access checks.
>
> BUG=604901
> BUG=603725
> BUG=591164
>
> Review URL: https://codereview.chromium.org/1899973002
>
> Cr-Commit-Position: refs/heads/master@{#388353}
> (cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)
>
> Committed: https://chromium.googlesource.com/chromium/src/+/f0f07d08bc3865436994b40aa620d8063fe7bbcc

TBR=
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=604901

Review-Url: https://codereview.chromium.org/1926353002
Cr-Commit-Position: refs/branch-heads/2704@{#302}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/resources/binding.js
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/script_context.cc
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53

commit a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 20:48:30 2016

[Extensions] More bindings improvements

Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
and broaden test access checks.

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1899973002

Cr-Commit-Position: refs/heads/master@{#388353}
(cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)

Review URL: https://codereview.chromium.org/1930163004 .

Cr-Commit-Position: refs/branch-heads/2704@{#314}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/resources/binding.js
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/script_context.cc
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f73ae8fbece36f9f964e2b83f893ef708cca6e2

commit 6f73ae8fbece36f9f964e2b83f893ef708cca6e2
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 20:53:36 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}
(cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)

Review URL: https://codereview.chromium.org/1936673002 .

Cr-Commit-Position: refs/branch-heads/2704@{#315}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/binding.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/event.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/utils.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/v8_schema_registry.cc


### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-05-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

As noted in the release notes, $4,000 for your work here. Congrats!

### ti...@google.com (2016-06-07)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/603725?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084093)*
