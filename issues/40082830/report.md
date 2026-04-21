# Content script is able to eval code in background page of other extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40082830](https://issues.chromium.org/issues/40082830) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions |
| **Reporter** | 4b...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2015-09-09 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0

Steps to reproduce the problem:
1. Create and install extension that injects content scripts.
2. Create and install another extension with iframe in it's background page.
3. Make sure that first extension is able to inject scripts to the page you use in the iframe of second extension.
4. In injected script of first extension do:
try
{
alert(window.top.eval('document.location.href'));
alert(window.top.document.location.href);
}
catch(e)
{
alert(e);
}

What is the expected behavior?
eval should throw exception just like the direct access to document.location do. So I should see only one alert with exception message.

What went wrong?
I see two alerts. One with location retrieved by eval and another with exception message.

Did this work before? N/A 

Chrome version: 45.0.2454.85 m (64-bit)  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 18.0 r0

## Attachments

- [tests.zip](attachments/tests.zip) (application/zip, 1.7 KB)

## Timeline

### ri...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-09-10)

Nice find, this behavior looks pretty bad. I'm duping https://crbug.com/chromium/529796 against this, which was filed a little later. In https://crbug.com/chromium/529796, it was mentioned that this also works:

Install extension with content scripts for *://*.spiegel.de/*
The content script does window.parent.eval('alert(window.location)')

Open a non-spiegel.de page which iframes spiegel.de. The content script is then able to execute javascript in the context of the non-spiegel.de page.

### ri...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-09-10)

Oops, some more updates from https://crbug.com/chromium/529682 - it looks like this can be turned into UXSS from a content script (as in, the target origin does not necessarily need to iframe the whitelisted origin).

### ri...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-09-10)

What's the proposed behavior to fix this?  (I see https://codereview.chromium.org/1327263002/ but don't understand what the outcome will be.)

I'm concerned about whether cross-origin frame access will be allowed even if the extension has the target origin in the manifest, since this is incompatible with OOPIFs.  We can de-dupe https://crbug.com/chromium/529796 or open a new bug for that discussion if needed.

### cr...@chromium.org (2015-09-10)

Another question for kalman@ or devlin@: I thought content scripts weren't injected into web iframes of background pages.  Is that not the case?  The repro steps here make it sound like content scripts can inject into background page iframes.

### [Deleted User] (2015-09-10)

#10 I don't see any problem with it working, but I don't know whether it does, nor whether anybody assumes it works.

### dc...@chromium.org (2015-09-10)

#9 I /think/ that with that security token change, cross-origin traversal will be forbidden for content scripts as well. The security token is used as a way to skip canAccess checks. If the token matches, it's assumed that the two window objects can script each other, and canAccess() is not called. If the security tokens of two windows does not match (which it should not after this change), we would fall back to SecurityOrigin::canAccess(), which enforces the standard cross-origin checks.

### dc...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-10)

yeah, but the SecurityOrigin::canAccess check will compare the context's security origin (chrome-extension://id) with the frame's security origin (whatever url) which will never match.

### rd...@chromium.org (2015-09-10)

@10, right, content scripts should not be injected into web iframes of background pages, except their own (with the exception of whitelisted extensions like chromevox).

https://code.google.com/p/chromium/codesearch#chromium/src/extensions/renderer/extension_injection_host.cc&l=48&gs=cpp:extensions::class-ExtensionInjectionHost::CanExecuteOnFrame(const%2520GURL%2520&amp;,%2520content::RenderFrame%2520*,%2520int,%2520bool)-const@chromium/../../extensions/renderer/extension_injection_host.cc%257Cdef&gsn=CanExecuteOnFrame&ct=xref_usages

### cr...@chromium.org (2015-09-10)

#15: Looks like step 3 of the repro steps found that this can be violated.  (There's no attached repro, though; has anyone confirmed that particular bug?)

It sounds like there's three main concerns here:

1) Content scripts are able to access cross-origin frames, even when they're not listed in the extension's manifest.  This violates the extension security model.

2) Content scripts are being injected into web iframes of background pages.  Combined with the cross-origin access of content scripts, that allows one extension to use the privileges of another extension, which is another security bug.

3) Even if an extension has listed the target origin in its manifest, giving content scripts the ability to synchronously script cross-origin iframes is incompatible with Site Isolation.  Cross-origin iframes often won't live in the same process, so the content script won't be able to directly access that content.


Worse, it appears that some popular extensions might use this cross-origin access behavior.  I'm assuming that based on the large volume of crashes in https://crbug.com/chromium/529667 which happened after the check epertoso@ added in https://crbug.com/chromium/455160.  I'm not sure whether that means https://codereview.chromium.org/1327263002/ will break those extensions as well (or how many of the above concerns it addresses).

We'll need to come up with a plan for how to address these issues.  Devlin, I'll try to find a chance to chat with you.

### ri...@chromium.org (2015-09-10)

I confirmed this bug (though I no longer have the files around, sorry)

### 4b...@gmail.com (2015-09-11)

Archive with two extensions attached.

### rd...@chromium.org (2015-09-11)

FYI, I've solved 2), and can have a patch up later today.

### cl...@chromium.org (2015-09-13)

meacer@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### cr...@chromium.org (2015-09-14)

I'm working with Devlin on this and have been triaging the various issues discussed in https://crbug.com/chromium/529682#c16, so I can take ownership to make sure they each get resolved.  I'll post an update tomorrow.

### cr...@chromium.org (2015-09-14)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-09-14)

A few highlights from my investigation so far:

The fact that content scripts can access cross-origin frames is a behavior change that occurred in May 2014, due to dcarney's https://codereview.chromium.org/261883004.  (git find-releases says this first arrived in 36.0.1972.0.)  There's no bug or test associated with that change, and as far as I can tell this outcome was unintended.

I've been manually testing the extensions that were present in the crash reports to see if I can reproduce the crash from https://crbug.com/chromium/455160, and I've found 3 extensions so far (after testing 10).  For these 3, I applied epertoso's proposed fix to enforce the Same Origin Policy (https://codereview.chromium.org/1327263002) and repeated the same steps, and I have not yet been able to observe any behavior change in the extensions.  They don't seem to break or even produce new error messages in the DevTools console.

While this is not yet conclusive, it suggests that these extensions may not be depending on the cross-origin frame access in critical ways.  For example, they may have simply been probing frames in try/catch blocks (as jochen@ suggested to me), without realizing that they had (inadvertently) been granted access to them.  I've confirmed this at a high level with one of the extension authors, who said their extension should work even without cross-origin access.

If this is true, we may be able to change the behavior so that cross-origin frame access in content scripts is not allowed (as was the case before M36).  That would fix #1, #2, and #3 from https://crbug.com/chromium/529682#c16.  (I think epertoso's CL would accomplish this.)

### jo...@chromium.org (2015-09-14)

This cl was part of the fix for https://crbug.com/chromium/20773

### cr...@chromium.org (2015-09-14)

jochen@: https://crbug.com/chromium/20773 looks like it was intended for same-origin frames.

### jo...@chromium.org (2015-09-14)

frames[] shouldn't be undefined for either same not cross origin frames.

Of course the main complaint was indeed that you couldn't access same origin frames.

### dc...@chromium.org (2015-09-14)

On https://crbug.com/chromium/20773, it looks like the Window objects weren't even visible: window.frames[n] was returning undefined for any n.

As long as we return Window objects, but enforce cross-origin restrictions, I think this should be OK: some developers explicitly mentioned wanting to use postMessage to deal with the cross-origin restrictions, but not being able to, due to the 'undefined' values (e.g. https://code.google.com/p/chromium/issues/detail?id=20773#c24)

### bu...@chromium.org (2015-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c318b93de2ee7b8cc78e506dd2dd161af7d6819d

commit c318b93de2ee7b8cc78e506dd2dd161af7d6819d
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Mon Sep 14 20:22:29 2015

[Extensions] Don't allow extensions to inject scripts into extension pages

Don't allow extensions to inject scripts into other extension pages, since this
is a security risk. This was meant to be addressed, but there was an incorrect
early-return. Also add a regression test.

BUG=529682

Review URL: https://codereview.chromium.org/1335083004

Cr-Commit-Position: refs/heads/master@{#348707}

[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/browser/extensions/content_script_apitest.cc
[add] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/background.html
[add] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/background.js
[add] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/manifest.json
[add] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/test/data/extensions/api_test/content_scripts/script_a_com/manifest.json
[add] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/chrome/test/data/extensions/api_test/content_scripts/script_a_com/script.js
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/extension_injection_host.cc
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/script_injection.cc
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/script_injection.h
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/script_injection_manager.cc
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/user_script_injector.cc
[modify] http://crrev.com/c318b93de2ee7b8cc78e506dd2dd161af7d6819d/extensions/renderer/user_script_set.cc


### bu...@chromium.org (2015-09-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202267

------------------------------------------------------------------
r202267 | epertoso@chromium.org | 2015-09-15T11:57:52.063313Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world-expected.txt?r1=202267&r2=202266&pathrev=202267
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world-expected.txt?r1=202267&r2=202266&pathrev=202267
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world.html?r1=202267&r2=202266&pathrev=202267
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/cross-frame-iframe-for-parent-isolated-world.html?r1=202267&r2=202266&pathrev=202267
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/ScriptController.cpp?r1=202267&r2=202266&pathrev=202267
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/WindowProxy.cpp?r1=202267&r2=202266&pathrev=202267
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world.html?r1=202267&r2=202266&pathrev=202267

Modifies WindowProxy::setSecurityToken so that the frame's SecurityOrigin is taken into account when setting the token for an extension.

Chrome extensions (or, in general, scripts that run in isolated worlds) can no longer do cross-origin access to the parent window or other iframes.

If the domain of one frame is explicitly set through the document.domain accessor from the main world, the security tokens of all the isolated worlds associated with that frame are also updated.

BUG=529682

Review URL: https://codereview.chromium.org/1327263002
-----------------------------------------------------------------

### jo...@chromium.org (2015-09-15)

should be fixed now. 

updating milestone to reflect impacts-stable

### cr...@chromium.org (2015-09-15)

Agreed-- that CL should take care of all the issues from https://crbug.com/chromium/529682#c16, and Devlin's change is a nice second line of defense.

Looks like this should be present in the 47.0.2509.0 canary.  We'll probably want to consider a merge for the security aspects as well if we can confirm that it looks good.

### cr...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-09-15)

My mistake; this isn't present in 47.0.2509.0, which was cut from Blink 202240 (before 202267).  We'll have to wait for the next canary to verify.

Giving amineer@ a heads up in case we need to merge this quickly for M45.

### am...@google.com (2015-09-15)

I'm going to proactively approve the merges here - if things look good in next canary, merge away.  If they don't, please remove the Merge-Approved-## labels and ping me if you still want this in the next 45 respin (you don't have much time).

Merge approved for M45 branch 2454 and M46 branch 2490.

### cl...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202327

------------------------------------------------------------------
r202327 | jochen@chromium.org | 2015-09-16T06:59:53.682032Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/bindings/core/v8/ScriptController.cpp?r1=202327&r2=202326&pathrev=202327
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/bindings/core/v8/WindowProxy.cpp?r1=202327&r2=202326&pathrev=202327
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world.html?r1=202327&r2=202326&pathrev=202327
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world-expected.txt?r1=202327&r2=202326&pathrev=202327
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world-expected.txt?r1=202327&r2=202326&pathrev=202327
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world.html?r1=202327&r2=202326&pathrev=202327
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/resources/cross-frame-iframe-for-parent-isolated-world.html?r1=202327&r2=202326&pathrev=202327

Merge 202267 "Modifies WindowProxy::setSecurityToken so that the..."

> Modifies WindowProxy::setSecurityToken so that the frame's SecurityOrigin is taken into account when setting the token for an extension.
> 
> Chrome extensions (or, in general, scripts that run in isolated worlds) can no longer do cross-origin access to the parent window or other iframes.
> 
> If the domain of one frame is explicitly set through the document.domain accessor from the main world, the security tokens of all the isolated worlds associated with that frame are also updated.
> 
> BUG=529682
> 
> Review URL: https://codereview.chromium.org/1327263002

TBR=epertoso@chromium.org

Review URL: https://codereview.chromium.org/1344173004
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202331

------------------------------------------------------------------
r202331 | jochen@chromium.org | 2015-09-16T07:06:30.082696Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world-expected.txt?r1=202331&r2=202330&pathrev=202331
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world.html?r1=202331&r2=202330&pathrev=202331
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/resources/cross-frame-iframe-for-parent-isolated-world.html?r1=202331&r2=202330&pathrev=202331
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/bindings/core/v8/ScriptController.cpp?r1=202331&r2=202330&pathrev=202331
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/bindings/core/v8/WindowProxy.cpp?r1=202331&r2=202330&pathrev=202331
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world.html?r1=202331&r2=202330&pathrev=202331
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world-expected.txt?r1=202331&r2=202330&pathrev=202331

Merge 202267 "Modifies WindowProxy::setSecurityToken so that the..."

> Modifies WindowProxy::setSecurityToken so that the frame's SecurityOrigin is taken into account when setting the token for an extension.
> 
> Chrome extensions (or, in general, scripts that run in isolated worlds) can no longer do cross-origin access to the parent window or other iframes.
> 
> If the domain of one frame is explicitly set through the document.domain accessor from the main world, the security tokens of all the isolated worlds associated with that frame are also updated.
> 
> BUG=529682
> 
> Review URL: https://codereview.chromium.org/1327263002

TBR=epertoso@chromium.org

Review URL: https://codereview.chromium.org/1351463002
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0

commit c3ef9af3c83ed946fd07a6c306e6729dd62f72e0
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Wed Sep 16 17:43:33 2015

[Extensions] Don't allow extensions to inject scripts into extension pages

Don't allow extensions to inject scripts into other extension pages, since this
is a security risk. This was meant to be addressed, but there was an incorrect
early-return. Also add a regression test.

BUG=529682
TBR=kalman@chromium.org
Review URL: https://codereview.chromium.org/1335083004

Cr-Commit-Position: refs/heads/master@{#348707}
(cherry picked from commit c318b93de2ee7b8cc78e506dd2dd161af7d6819d)

Review URL: https://codereview.chromium.org/1344213003 .

Cr-Commit-Position: refs/branch-heads/2490@{#293}
Cr-Branched-From: 7790a3535f2a81a03685eca31a32cf69ae0c114f-refs/heads/master@{#344925}

[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/browser/extensions/content_script_apitest.cc
[add] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/background.html
[add] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/background.js
[add] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/test/data/extensions/api_test/content_scripts/background_page_iframe/manifest.json
[add] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/test/data/extensions/api_test/content_scripts/script_a_com/manifest.json
[add] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/chrome/test/data/extensions/api_test/content_scripts/script_a_com/script.js
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/extension_injection_host.cc
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/script_injection.cc
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/script_injection.h
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/script_injection_manager.cc
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/user_script_injector.cc
[modify] http://crrev.com/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0/extensions/renderer/user_script_set.cc


### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/c3ef9af3c83ed946fd07a6c306e6729dd62f72e0

commit c3ef9af3c83ed946fd07a6c306e6729dd62f72e0
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Wed Sep 16 17:43:33 2015


### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a5d9c21478e5c669d9f2b7a377a111af84b95778

commit a5d9c21478e5c669d9f2b7a377a111af84b95778
Author: jochen@chromium.org <jochen@chromium.org>
Date: Wed Sep 16 06:59:53 2015

Merge 202267 "Modifies WindowProxy::setSecurityToken so that the..."

> Modifies WindowProxy::setSecurityToken so that the frame's SecurityOrigin is taken into account when setting the token for an extension.
> 
> Chrome extensions (or, in general, scripts that run in isolated worlds) can no longer do cross-origin access to the parent window or other iframes.
> 
> If the domain of one frame is explicitly set through the document.domain accessor from the main world, the security tokens of all the isolated worlds associated with that frame are also updated.
> 
> BUG=529682
> 
> Review URL: https://codereview.chromium.org/1327263002

TBR=epertoso@chromium.org

Review URL: https://codereview.chromium.org/1344173004

git-svn-id: svn://svn.chromium.org/blink/branches/chromium/2490@202327 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world-expected.txt
[add] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/LayoutTests/http/tests/security/cross-frame-access-parent-explicit-domain-isolated-world.html
[add] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world-expected.txt
[add] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/LayoutTests/http/tests/security/cross-frame-access-parent-isolated-world.html
[add] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/LayoutTests/http/tests/security/resources/cross-frame-iframe-for-parent-isolated-world.html
[modify] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp
[modify] http://crrev.com/a5d9c21478e5c669d9f2b7a377a111af84b95778/third_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp


### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/a5d9c21478e5c669d9f2b7a377a111af84b95778

commit a5d9c21478e5c669d9f2b7a377a111af84b95778
Author: jochen@chromium.org <jochen@chromium.org>
Date: Wed Sep 16 06:59:53 2015


### ti...@google.com (2015-09-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-22)

Bulk update: removing view restriction from closed bugs.

### as...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-30)

Hello - we found some old bugs that weren't voted on and took them to the reward panel last week. This was one of them.

Our reward panel decided to award you $3,000 for this report. 

Our finance team should be in touch within 7 days. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@google.com (2018-06-08)

The reward for this report is being donated to the Against Malaria Foundation :-)

### is...@google.com (2018-06-08)

This issue was migrated from crbug.com/chromium/529682?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/529796]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082830)*
