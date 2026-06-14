# Security: Saving WebPage with file: resources access SMB resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40084438](https://issues.chromium.org/issues/40084438) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Reporter** | gr...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2016-06-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Saving WebPage with file: resources access/saves SMB resources. This can potentially expose the user to SMB Relay Attack (stealing credentials). Loading of file: resource is blocked when page is viewed over http/https, however, when saving the page file: URLs are allowed.

**VERSION**  

Chrome Version: 51.0.2704.63 m (Stable)  

Operating System: Windows (All)

**REPRODUCTION CASE**

1. Visit <http://grpdmp.tk:27275/gchrome1/_SMB_Access.html>
2. Save Page (Complete)
3. Saved SMB resource is typically saved to C:\Users<Username>\Downloads\_SMB\_Access\_files ( In this case file://localhost/C$/windows/system32/calc.exe is saved to C:\Users<Username>\Downloads\_SMB\_Access\_files\calc.exe )

## Timeline

### fe...@chromium.org (2016-06-02)

Thank you for the report.

petewil@, can you please look into this?

[Monorail components: UI>Browser>Offline]

### gr...@gmail.com (2016-06-13)

FYI - Related https://crbug.com/chromium/617215 [Bypass Download Protection on using file:// WebDav URL]

### sh...@chromium.org (2016-06-15)

petewil: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2016-06-15)

I am probably not the best owner for this, but since it is assigned to me, I'll take a look.

### pe...@chromium.org (2016-06-16)

In render_frame_impl.cc, OnGetSavebleResourceLinks() uses a list of savable schemes to save resources by, and url::kFileScheme is in the list.  It seems that the list is not used elsewhere, so we could easily remove kFileScheme from the list.  However, I wonder if any scenarios might break, or if there is any reason we want to download files.

### gr...@gmail.com (2016-06-17)

(pasting the salient email contents I sent to Pete -- for future reference)

HTTP[S] resources when rendered in browser, do not allow loading of local resource schemes, however, when the user saves the complete page, these file:// resources get accessed. If the fetch is successful, it is written to disk.

This poses a few risks to the user:
#1 - Access to non-local resource through SMB is permitted through file: scheme. It exposes user to Potential SMB Relay Attack under specific scenarios.
 Ref http://www.darkreading.com/vulnerabilities---threats/new-smb-relay-attack-steals-user-credentials-over-internet/d/d-id/1321633
       https://www.blackhat.com/docs/us-15/materials/us-15-Brossard-SMBv2-Sharing-More-Than-Just-Your-Files.pdf
#2 - Exposing a User's Real IP-Address when chrome specific proxy is configured in the browser [Eg: using --proxy-server cmdline param].
       ( In case Chrome is configured to use system-wide proxy; accessing WebDav resources won't expose real IP; but accessing SMB resources will )
#3 - Landing a blacklisted binary on disk that bypasses the SafeBrowsing layer [ its a combination of https://crbug.com/chromium/616424 and https://crbug.com/chromium/617215 ]
[a discussion in https://crbug.com/chromium/617215 indicated that a fix in SMB access issue *might* address it]

Access to SMB [local] resource can be demonstrated by saving the following URL
1. Visit http://grpdmp.tk/gchrome1/_SMB_Access.html
2. Save Page (Complete)
3. Saved SMB resource is typically saved to C:\Users\<Username>\Downloads\_SMB_Access_files ( In this case file://localhost/C$/windows/system32/calc.exe is saved to C:\Users\<Username>\Downloads\_SMB_Access_files\calc.exe )
[Please note that localhost can be replaced with any SMB network resource]

Access to WebDav [internet] resource can be demonstrated by saving the following URL.
1. Start "WebClient" windows services manually [See https://crbug.com/chromium/617215 for reference on why this is required]
2. Visit http://grpdmp.tk/gchrome1/1.html
3. Save Page (Complete)
4. Saved SMB resource is typically saved to C:\Users\<Username>\Downloads\1_files ( In this case file://grpdmp.tk/webdav/content.exe is saved to C:\Users\<Username>\Downloads\1_files\content.exe ). content.exe is the blacklisted malware test binary.
[ If Chrome was started with custom proxy (for all traffic), instead of using system proxy -- the above steps will expose User's real IP to the WebDav host ]

So, I have the following suggestions for Chromium:
1. Do not allow local schemes to be accessed when saving a page from http/https etc. ( following same policy as the renderer )
2. When directly access of file: URL with smb/webdav resource occurs [using OmniBar; or malicious extension (with no permissions) opens a new tab] .. To Address: https://crbug.com/chromium/617215 , then Either SafeBrowsing should subscribe and scan the downloaded content Or show some warning to the user that he/she is accessing a possible untrusted network resource.

### dc...@chromium.org (2016-06-17)

+lukasza, who is the save page expert.

I think we should do this generically: if a resource is blocked, for whatever reason, we need to make sure the serialized page reflects that.



### lu...@chromium.org (2016-06-17)

1. I should probably be the owner of this bug.  OTOH, I am heading on a really long vacation soon (coming back on July 15th).  Let ma also add to CC people who might have some ideas on how to fix this - yosin@ (for Blink HTML serialization code) and rdsmith@ + asanka@ (for c/browser/downloads).

2. dcheng@ is correct in observing that the impact is broader than just access to SMB resources.  For example once internet->intranet restrictions (https://crbug.com/590714, +mkwst@ as an FYI) are in place, we would also want to preserve them during Save-Page-As-Complete-Html operation.

3. I am not sure what is the best approach for solving this.

3.a. Only save resources from within the renderer (tracked by https://crbug.com/chromium/158957).  One way to implement this might be to merge MHTML and CompleteHtml serializers (tracked by https://crbug.com/chromium/328354).  OTOH, this seems tricky wrt preserving all data - I am guessing that some resources are only parsed by Blink and don't yet have corresponding serializers (css?);  additionally, some resources are handled outside of Blink and would need to be serialized by the corresponding plugins (pdf?).

3.b. The alternative approach would be to make sure that all resource requests made during Save-Page-As-Complete-HTML are performed with effective permissions of the renderer where the link came from.  This can be slightly tricky in case where the same link is used from 2 frames (one of which can have access, while the other doesn't).

3.c. We can also continue to process resource requests with user's authority, but verify in SavePackage::OnSavableResourceLinksResponse that savable resources reported by a frame are actually allowed for that frame.  This avoids the issue of deduplicating resources by link from 3b.  OTOH, it seems wrong to be duplicating the security checks between 1) SavePackage::OnSavableResourceLinksResponse and 2) the code that actually processes the resource requests (e.g. I am sure we would miss some checks [like SafeBrowsing?]).

4. It is not clear to me what is the urgency of doing "something" about this bug.  If we need to do something before M53 branch point, then maybe filtering URIs received in SavePackage::OnSavableResourceLinksResponse is one way to go (as proposed in https://crbug.com/chromium/616429#c6 and https://crbug.com/chromium/616429#c5).

### lu...@chromium.org (2016-06-17)

It seems that SaveFileManager::SaveLocalFile handles file: URIs itself (using base::CopyFile rather than handing off the URI to ResourceDispatcherHostImpl::Get()->BeginSaveFile).  I wonder if anything will break if I just yank out SaveFileManager::SaveLocalFile (i.e. unify code that handles SAVE_FILE_FROM_FILE and SAVE_FILE_FROM_NET).  And I wonder if this will also fix the security issue reported here.

### lu...@chromium.org (2016-06-17)

Yanking out SaveFileManager::SaveLocalFile still seems desirable, but is not sufficient to address the security issue here.  In particular, I see that ResourceDispatcherHostImpl::BeginSaveFile directly calls BeginRequestInternal and doesn't go through ShouldServiceRequest and/or ChildProcessSecurityPolicyImpl::CanRequestURL for authorization checks.

It is not clear to me whether ChildProcessSecurityPolicyImpl::CanRequestURL is sufficient here.  FWIW, calling it from ResourceDispatcherHostImpl::BeginSaveFile makes my browser test pass, so I'll go forward with this approach for now.

### lu...@chromium.org (2016-06-17)

BTW: the ChildProcessSecurityPolicyImpl::CanRequestURL is based on |child_id|.  The problem is that SavePackage always passes main frame's process id to SaveFileManager::SaveURL (in addition to passing main frame's routing_id and its render view routing id...).  Still - this will only be a concern once --site-per-process ships (AFAIK save-page feature is not considered a blocker for shipping --isolate-extensions).

### lu...@chromium.org (2016-06-18)

I published a draft of a fix at https://codereview.chromium.org/2075273002/

### lu...@chromium.org (2016-06-18)

In the draft of a fix I try to prevent access to an unauthorized resource in 2 scenarios: 1) when saving the webpage and 2) when opening the saved webpage.  AFAICT the fix works for all cases of scenario #1, but only for cases of scenario #2 where we rewrite resource links (so - only in case of links from html).  If the hostile link (i.e. to http://bob-s-intranet/give-all-money-to-eve.php) is embedded in css or other resource that we do not reserialize, then the resource request will be performed when the saved page is opened.

I don't see a good way to address this.  We do generate a mark-of-the-web in the saved html (see FrameSerializer::markOfTheWebDeclaration), but it is not clear how this could be used here (i.e. the saved page has to have access to file: resources that got saved into foo_files/, but at the same time [unlike other html files from local filesystem] it shouldn't have access to http://bob-s-intranet/give-all-money-to-eve.php [because mark-of-the-web] says that it came from eve-s-website.com.  To be honest, I think that right now we only write mark-of-the-web to saved pages, but never recognized one ourselves (when reading html files from the local filesystem).

### lu...@chromium.org (2016-06-20)

Another observation is that (in the proposed fix) protecting against requesting a restricted resource 1) works reasonably well while a website is being saved, 2) works only for non-compromised renderer when opening an already saved file.  In particular, a compromised renderer can forge a mark-of-the-web and/or include any links it pleases.  Right now the browser doesn't validate presence of the mark-of-the-web (in case of complete-html, in case of mhtml it could validate Content-Location header) and furthermore doesn't use the information from mark-of-the-web when opening the already saved file.

Given above, I am less sure if we should cripple legitimate scenarios, given that the protection gained only works assuming a non-compromised renderer.  (this comment obviously only applies to the open-already-saved-file attach vector;  we should still fix the no-unauthorized-resource-requests-while-saving scenario).

### lu...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Offline UI>Browser>Downloads]

### sh...@chromium.org (2016-07-05)

lukasza: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2016-07-07)

Setting status to started based on c#12.  However, note that Lukasz is on vacation at the moment, so this may not get fixed in the short-term time frame :-J.

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eff8e457298d01b437e4fd78194ad6de3c8d7ad6

commit eff8e457298d01b437e4fd78194ad6de3c8d7ad6
Author: lukasza <lukasza@chromium.org>
Date: Wed Jul 27 21:03:26 2016

Resource requests from Save-Page-As should go through CanRequestURL checks.

This CL:

- Added checks to ResourceDispatcherHostImpl::BeginSaveFile to verify if
  the renderer process is authorized to access a given resource.

- Removed separate code path for file: URIs that used to be implemented
  in SaveFileManager::SaveLocalFile.  Avoiding a separate code path
  helps consolidate all authorization checks in one place.

BUG=616429

Review-Url: https://codereview.chromium.org/2075273002
Cr-Commit-Position: refs/heads/master@{#408235}

[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/chrome/browser/download/save_page_browsertest.cc
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/chrome/test/data/save_page/frames-objects.htm
[add] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/chrome/test/data/save_page/text.txt
[add] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/chrome/test/data/save_page/unauthorized-access.htm
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/docs/save-page-as.md
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_file_manager.cc
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_file_resource_handler.cc
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_file_resource_handler.h
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_item.cc
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_item.h
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_package.cc
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/download/save_types.h
[modify] https://crrev.com/eff8e457298d01b437e4fd78194ad6de3c8d7ad6/content/browser/loader/resource_dispatcher_host_impl.cc


### lu...@chromium.org (2016-07-28)

[Empty comment from Monorail migration]

### lu...@chromium.org (2016-07-28)

commit eff8e457298d01b437e4fd78194ad6de3c8d7ad6 was initially in 54.0.2810.0

### lu...@chromium.org (2016-07-28)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-07-28)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0dbf3f74229c711ad91b21bd1ddc722580a7499e

commit 0dbf3f74229c711ad91b21bd1ddc722580a7499e
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date: Thu Jul 28 20:22:41 2016

Resource requests from Save-Page-As should go through CanRequestURL checks.

This CL:

- Added checks to ResourceDispatcherHostImpl::BeginSaveFile to verify if
  the renderer process is authorized to access a given resource.

- Removed separate code path for file: URIs that used to be implemented
  in SaveFileManager::SaveLocalFile.  Avoiding a separate code path
  helps consolidate all authorization checks in one place.

BUG=616429

Review-Url: https://codereview.chromium.org/2075273002
Cr-Commit-Position: refs/heads/master@{#408235}
(cherry picked from commit eff8e457298d01b437e4fd78194ad6de3c8d7ad6)

Review URL: https://codereview.chromium.org/2187353004 .

Cr-Commit-Position: refs/branch-heads/2785@{#394}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/chrome/browser/download/save_page_browsertest.cc
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/chrome/test/data/save_page/frames-objects.htm
[add] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/chrome/test/data/save_page/text.txt
[add] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/chrome/test/data/save_page/unauthorized-access.htm
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/docs/save-page-as.md
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_file_manager.cc
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_file_resource_handler.cc
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_file_resource_handler.h
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_item.cc
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_item.h
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_package.cc
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/download/save_types.h
[modify] https://crrev.com/0dbf3f74229c711ad91b21bd1ddc722580a7499e/content/browser/loader/resource_dispatcher_host_impl.cc


### sh...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-08-18)

Does this bug report qualify for the VRP ?

### lu...@chromium.org (2016-08-18)

Thanks for following up. I think it's eligible for a bounty but it isn't my decision. Adding reward-topanel which should put this in the queue.

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

yep, eligible for consideration and after consideration the panel awarded $1,000!


### gr...@gmail.com (2016-09-09)

Thank you for the reward :-)


### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/616429?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084438)*
