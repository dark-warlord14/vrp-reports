# Chromium sync session fixation + code execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40077683](https://issues.chromium.org/issues/40077683) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | is...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2013-06-19 |
| **Bounty** | $21,500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome SigninManager can be tricked to sign a user into attacker's account, XSS on any google.com subdomain will be enough for this.  

Later, another security issue with webstore updates can be leveraged to deliver NPAPI plugin dll and execute attacker's code with full user privilege.

**VERSION**  

Tested both on Chrome Version: [27.0.1453.116][stable] and on Chrome Version: [29.0.1541.0][dev]  

Operating System: [Windows, 6.1 (Windows 7, Windows Server 2008 R2)]

**REPRODUCTION CASE**  

First, CSRF check at <https://accounts.google.com/ServiceLogin?service=chromiumsync> can be bypassed in two different ways:

```
1. XSS on \*.google.com + Cookie tossing  
How to reproduce:  
	1. Go to https://www.google.com/ and emulate the XSS in console: document.cookie = 'GALX=abc; path=/ServiceLoginAuth; domain=.google.com';  
	2. Save the page at https://accounts.google.com/ServiceLogin, set the value of the input with name "GALX" to "abc", submit the form  
	3. Login is accepted, because our GALX cookie has a longer path than the legit CSRF token cookie, and therefore goes first in the Cookie header  
  
2. Direct XSS on accounts.google.com  
The OAuth 2.0 proxy at https://accounts.google.com/o/oauth2/postmessageRelay does not correctly validate the "parent" parameter for the "rmr" token transport type, and it can be tricked to load a javascript url. This "rmr" token transport means, that the proxy should create an iframe with src=parent:  
	  
  https://oauth.googleusercontent.com/gadgets/js/core:rpc:shindig.random:shindig.sha1.js?c=2:  
  
  gadgets.rpctx = gadgets.rpctx || {};  
  ...  
    var a = gadgets.util.getUrlParameters()["parent"];  
    ...  
    function l(q, o, p, n) {  
      var r = function() {  
      document.body.appendChild(q);  
      q.src = "about:blank";          <-- iframe inherits security origin  
      if (n) {  
        q.onload = function() {  
        m(n)  
        }  
      }  
      q.src = o + "#" + p            <-- javascript: url is loaded  
      };  

Repro steps inside attached oauth_xss_poc.html, or directly at http://dl.dropboxusercontent.com/s/h677k5l95dvgi4l/oauth_xss_poc.html  

```

At this point, victim is signed into attacker's google account, but to sign him in Chrome in order to perform an account sync requires additional effort. The main defense for Chrome sync/signin is based on the fact, that all signin operations should originate from a trusted Sign-In renderer process. For now, there exist two different variations of approach:

```
1. On stable  
Codebase from stable channel has strict rule to accept email as a candidate in the only one case: if the target renderer is the signin-renderer:  
  
chrome\browser\ui\sync\one_click_signin_helper.cc:  

  bool OneClickSigninHelper::CanOffer(content::WebContents\* web_contents,  
    ...  
                
    // Only allow the dedicated signin process to sign the user into  
    // Chrome without intervention, because it doesn't load any untrusted  
    // pages.  In the interstitial case, since chrome will display a modal  
    // dialog, we don't need to make this check.  
    if (can_offer_for == CAN_OFFER_FOR_ALL &&  
      !manager->IsSigninProcess(  
        web_contents->GetRenderProcessHost()->GetID())) {  
      return false;  
    }  
    ...  

The statement "it doesn't load any untrusted pages" is not true due to poor signin web-flow identification logic and renderer processes behaviour. Using OAuth redirects we can load any url in the signin renderer, and then invoke a legit signin request from there:  
	  
	w = window.open(null, "signin");  
	w.opener = null;  
	w.document.location.replace("https://accounts.google.com/o/oauth2/auth?service=chromiumsync&client_id=YOUR_CLIENT_ID&scope=SCOPE&immediate=true&redirect_uri=YOUR_REDIRECT_URI&origin=YOUR_ORIGIN&response_type=token&state=123&authuser=0");  
  
Here, window.open along with "opener = null" forces Chrome to load url in a new renderer, but when searching for the appropriate renderer type and looking at the url, Chrome decides that this is actually a web-based signin flow:  
  
chrome\browser\chrome_content_browser_client.cc:  
  
  void ChromeContentBrowserClient::SiteInstanceGotProcess(  
    ...  
    // We only expect there to be one signin process as we use process-per-site  
    // for signin URLs. The signin process will be cleared from SigninManager  
    // when the renderer is destroyed.  
    if (SigninManager::IsWebBasedSigninFlowURL(site_instance->GetSiteURL())) {  
    SigninManager\* signin_manager =  
      SigninManagerFactory::GetForProfile(profile);  
    if (signin_manager)  
      signin_manager->SetSigninProcess(site_instance->GetProcess()->GetID());  
    ...  
      
chrome\browser\signin\signin_manager.cc:  
  
  bool SigninManager::IsWebBasedSigninFlowURL(const GURL& url) {  
    GURL effective(kChromeSigninEffectiveSite);  
    if (url.SchemeIs(effective.scheme().c_str()) &&  
      url.host() == effective.host()) {  
    return true;  
  }  

    GURL service_login(GaiaUrls::GetInstance()->service_login_url());  
    if (url.GetOrigin() != service_login.GetOrigin())                          <---- domain should be accounts.google.com  
    return false;  

    // Any login UI URLs with signin=chromiumsync should be considered a web   <---- "signin=chromiumsync" should be in query  
    // URL (relies on GAIA keeping the "service=chromiumsync" query string  
    // fragment present even when embedding inside a "continue" parameter).  
    return net::UnescapeURLComponent(  
      url.query(), net::UnescapeRule::URL_SPECIAL_CHARS)  
        .find(kChromiumSyncService) != std::string::npos;  
  }  

But what really happens, is that the OAuth 2.0 endpoint at "o/oauth2/auth" is being reached, which in turn 302-redirects the browser to YOUR_REDIRECT_URI (without token, of course). Note, that the renderer is not destroyed upon receiving 302 code, even with cross-domain redirects. Now, inside the trusted signin process, we submit the login form and initiate the signin flow.  
  
Repro steps in repro_stable.zip, or directly at http://dl.dropboxusercontent.com/s/jbq5tmex6kq724v/cr_link.html. Don't forget to use a new profile in chrome or just clear the GALX=abc cookie from previous experiments. Unfortunately, the signin will happen if only user is not already signed in Chrome under its own account.  
  
2. On dev  
Signin is designed a bit differently on development channel: now it allows signing in from an untrusted renderer, but shows a confirmation dialog in this case:  
  
chrome\browser\ui\sync\one_click_signin_helper.cc:  
  
  // Only allow the dedicated signin process to sign the user into  
  // Chrome without intervention, because it doesn't load any untrusted  
  // pages.  If at any point an untrusted page is detected, chrome will  
  // show a modal dialog asking the user to confirm.  
  ...  
  helper->untrusted_confirmation_required_ |=  
    (manager && !manager->IsSigninProcess(child_id));  
      
But if the user is supposed to turn on the sync manually, Chrome signs this user in without any confirmation:  
  
chrome\browser\ui\sync\one_click_signin_helper.cc:  
    
    ...  
  void StartSync(const StartSyncArgs& args,  
    ...  
    // If we are giving the user the option to configure sync, then that will  
    // suffice as a confirmation.  
    OneClickSigninSyncStarter::ConfirmationRequired confirmation =  
      args.confirmation_required;  
    if (start_mode == OneClickSigninSyncStarter::CONFIGURE_SYNC_FIRST &&  
      confirmation == OneClickSigninSyncStarter::CONFIRM_UNTRUSTED_SIGNIN) {  
    confirmation = OneClickSigninSyncStarter::CONFIRM_AFTER_SIGNIN;  
    }  
	    
Once the user is signed in, it becomes possible to re-sign him again, now with sync turned on automatically:  

chrome\browser\ui\sync\one_click_signin_sync_starter.cc:  

  void OneClickSigninSyncStarter::ConfirmSignin(const std::string& oauth_token) {  
    DCHECK(!oauth_token.empty());  
    SigninManager\* signin = SigninManagerFactory::GetForProfile(profile_);  
    // If this is a new signin (no authenticated username yet) try loading  
    // policy for this user now, before any signed in services are initialized.  
    // This callback is only invoked for the web-based signin flow - for the old  
    // ClientLogin flow, policy will get loaded once the TokenService finishes  
    // initializing (not ideal, but it's a reasonable fallback).  
    if (signin->GetAuthenticatedUsername().empty()) {                 <--- GetAuthenticatedUsername is now set  
  #if defined(ENABLE_CONFIGURATION_POLICY)  
    policy::UserPolicySigninService\* policy_service =  
      policy::UserPolicySigninServiceFactory::GetForProfile(profile_);  
    policy_service->RegisterPolicyClient(  
      signin->GetUsernameForAuthInProgress(),  
      oauth_token,  
      base::Bind(&OneClickSigninSyncStarter::OnRegisteredForPolicy,  
             weak_pointer_factory_.GetWeakPtr()));  
    return;  
  #else  
    ConfirmAndSignin();  
  #endif  
    } else {  
    // The user is already signed in - just tell SigninManager to continue  
    // with its re-auth flow.  
    signin->CompletePendingSignin();                                   <--- Starts sync without confirmation  
    }  
  }  

Repro at repro_dev.zip, or directly at http://dl.dropboxusercontent.com/s/5xgi91jv4hs7o2c/cr_link.html. Again, don't forget to use new profile, and you also should not be signed in to Chrome initially.  

```

Finally, Chrome Sync is used to install an extension with NPAPI plugin and execute code. Though extensions with plugins cannot be installed through sync directly, they can be auto-updated, and the new version may contain plugins. To reproduce this, open two browsers and perform Chrome Signin on both with the same account. Then do the following:

```
1. Create an extension without plugins, but with a special "plugin" permission in the permissions list  
2. Install this extension in the first browser instance and observe it appearing in the parallel browser instance  
3. Upload the new version of the extension, now with a dll inside and with "plugins" section in manifest  
4. Install any other extension from webstore in the first browser instance, just to trigger auto-update in the second instance  

```

To overcome the main restriction — user should not be signed in Chrome — attacker can stop sync beforehand through <https://www.google.com/settings/chrome/sync> via a single XSS. This signs the current user out in Chrome as well (on stable).

My full exploit chain automates all those steps and pops the calc perfectly on both stable/dev, only a single click on the link is required. If you need, I can share the code with you by request.

Best,  

Andrey Labunets  

[isciurus@gmail.com](mailto:isciurus@gmail.com)

## Attachments

- [oauth_xss_poc.html](attachments/oauth_xss_poc.html) (text/html; charset=us-ascii, 1.4 KB)
- deleted (application/octet-stream, 0 B)
- [repro_stable.zip](attachments/repro_stable.zip) (application/zip; charset=binary, 2.8 KB)
- [npcalc_no_plugin.zip](attachments/npcalc_no_plugin.zip) (application/zip; charset=binary, 1.2 KB)
- [npcalc_with_plugin.zip](attachments/npcalc_with_plugin.zip) (application/zip; charset=binary, 21.0 KB)

## Timeline

### jl...@chromium.org (2013-06-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-19)

[Empty comment from Monorail migration]

### ev...@google.com (2013-06-19)

[Empty comment from Monorail migration]

### ta...@gmail.com (2013-06-19)

[Empty comment from Monorail migration]

### ev...@google.com (2013-06-19)

[Empty comment from Monorail migration]

### ev...@google.com (2013-06-19)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-19)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-19)

Adding Brian and Roger for Chrome signin manager.

### sc...@gmail.com (2013-06-19)

@isciurus: report received ;-) Thanks!

Initial plan of attack:

- Google Web team activated for the accounts.google.com XSS.
- @nasko to own investigation of the failings of the renderer process model vs. sign-in process isolation.
- I'll split out a new bug about the bypass of the sync+NPAPI restriction.

### sc...@gmail.com (2013-06-19)

Adding label reward-topanel, heh.

### sc...@gmail.com (2013-06-20)

@falmeida: is there any reason we can't fail the XSRF check if multiple GALX cookies are seen????

### ev...@google.com (2013-06-20)

there are other ways to csrf-login a user to GAIA.. while we could certainly prevent this one, we wouldn't solve the problem.

nice catch with the XSS though

### fa...@google.com (2013-06-20)

Yep. There are several other ways.

### sc...@gmail.com (2013-06-20)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-20)

NPAPI sync issue is now tracked in https://crbug.com/chromium/252034.

### th...@google.com (2013-06-20)

We're tracking this in buganizer at b/9502901.

### sc...@gmail.com (2013-06-20)

@isciurus: just a note that because the accounts.google.com XSS is peripheral to the Chrome issues, the Google Web VRP team will consider it for reward separately. Top work :-)

### fa...@google.com (2013-06-20)

Yes pretty good work chaining all these issues together.

### is...@gmail.com (2013-06-20)

[Comment Deleted]

### is...@gmail.com (2013-06-20)

@scarybeasts: Cool, thanks! I would not fully agree with the first part of your sentence, though.

### jl...@chromium.org (2013-06-20)

isciurus: this could be rephrased as "has impact beyond Chrome" if you prefer :)

### ev...@google.com (2013-06-20)

@isciurus, you found an XSS on all websites that use shindig.rpc, accounts.google.com being one of them. As you mention in your report, the XSS in a.g.c isn't really required, and so, we'll consider it for a reward as part of that.

This is important (for you), because considering them separate issues means more money.

I'll start a thread on this bug separately.

### yo...@chromium.org (2013-06-20)

For the NPAPI extension sync: when you say "upload the new version", is this to the webstore? How does it not work without an empty "plugins" section in the initial version?

### is...@gmail.com (2013-06-20)

@yoz: Yes, you should upload the new version to the webstore.
The extension/plugin does not and should not work in the initial version. We only wait until it is delivered to the target browser, from where it will get updated to the functional version on its own.
If I treated your question correctly.

### mp...@chromium.org (2013-06-20)

To put another way, we're confused about this step:
	1. Create an extension without plugins, but with a special "plugin" permission in the permissions list

Does this refer to a manifest with this field:
  "permissions": ["plugin"]
or with this field:
  "plugins": {}

It seems unnecessary to include the "plugins" key. If you just create an empty extension, it should sync and update identically to how it does with an empty "plugins" field.

The "plugin" permission doesn't do anything, AFAIK.

### jl...@chromium.org (2013-06-20)

The Chrome sign-in issue is now tracked in https://crbug.com/chromium/252062

### is...@gmail.com (2013-06-20)

@mpcomplete: This refers to a manifest with "permissions": ["plugin"].
I am attaching my original extension: both versions. I switch between them, while incrementing the version. The reason why I use a special permission is that once I've seen that the updated extension stopped working, because the new version required new permission (incurred by dll). It was switched off and needed manual turning on.

Initial manifest (npcalc_no_plugin):
{
	"manifest_version": 2,
	
	"name": "npapi_calc",
	"version": "2.85",
	"description": "a small calc helloworld example of npapi.",
	"background": {
		"persistent": true,
		"scripts": ["bg.js"] },
	"permissions": [
		"tabs",
		"<all_urls>",
		"cookies",
		"plugin"
	]
	
}

"Plugin" manifest (npcalc_with_plugin):
{
	"manifest_version": 2,
	
	"name": "npapi_calc",
	"version": "2.86",
	"description": "a small calc helloworld example of npapi.",
	"background": {
		"persistent": true,
		"scripts": ["bg.js"] },
	"permissions": [
		"tabs",
		"<all_urls>",
		"cookies",
		"plugin"
	]
	,"plugins":[ {"path":"npcalc.dll","public":true} ]
}

### me...@google.com (2013-06-20)

Filed http://b/9503474 for Web Store NPAPI bug.

### tm...@chromium.org (2013-06-20)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2013-06-20)

Stable Channel
I am still trying to understand the failure in the stable channel scenario.  While its true that "https://accounts.google.com/o/oauth2/auth?service=chromiumsync&client_id=YOUR_CLIENT_ID&scope=SCOPE&immediate=true&redirect_uri=YOUR_REDIRECT_URI&origin=YOUR_ORIGIN&response_type=token&state=123&authuser=0" would be consider a "safe" URL by IsWebBasedSigninFlowURL(), the 302 redirect should have caused a process swap since YOUR_REDIRECT_URI is not "safe".  The only case I know of where a process swap is not done (when it should be) is when an HTTP POST is performed.  Maybe @nasko can investigate this further.

Dev Channel
As for the failure in the dev channel, the cause is clearer.  Prior to M29, pressing cancel on the advanced sync settings dialog would also sign the user out.  Therefore we did not need to confirm the sign in explicitly.  However, in M29, we separated the notions of sign in and sync.  One side effect is that cancelling the advanced sync setup keeps the user signed in.

The fix is to explicitly confirm sign in, even if the user has chosen to configure sync first.  This means the user will see an extra confirmation when:

1/ the user sign ins via one of the well known access points using a saml account, and chooses to configure sync first
2/ the user sign ins via the interstitial, and chooses to configure sync first

### ev...@google.com (2013-06-20)

[Empty comment from Monorail migration]

### bc...@chromium.org (2013-06-20)

[Empty comment from Monorail migration]

### fa...@google.com (2013-06-20)

Quick update: code push resolving xss finished late yesterday.

### ev...@google.com (2013-06-20)

btw, please keep the bug restricted from public view until we patch this in shindig :)

### is...@gmail.com (2013-06-28)

@rogerta:
As long as I understand, process swap is not supposed to happen after 302 redirects at all, and this is the main issue.

### an...@chromium.org (2013-06-28)

[Empty comment from Monorail migration]

### bc...@chromium.org (2013-06-28)

There's been a lot of discussion about why the process is/isn't getting marked "insecure" when we redirected out to the attacker's site.  But shouldn't there be equal opportunity to do the same when transitioning from the attacker's site back to accounts.google.com for the actual sign-in?  Why doesn't that cause loss of "secure" status?


### ro...@chromium.org (2013-06-28)

@isciurus: a process swap *should* happen after the 302 redirect, but it is not actually happening.  That is the main issue.  This has been worked around as part of https://crbug.com/chromium/252062 and merged into M28, see https://crbug.com/chromium/252010#c13 there for details.

@bcwhite: the transition from the attacker's site to a.g.c is done via an HTTP POST which also does not do a process swap when it should.  However this is a known issue and the code already deals with this situation.  The only unexpected behaviour was that 302 redirects don't do a process swap.

### is...@gmail.com (2013-07-01)

@rogerta:
I see. Thanks for the references, I'll have a look once I am granted the required permission.

### pb...@chromium.org (2013-07-01)

Checked the Issue using following steps provided by Nasko on chrome 28.0.1500.68 on Windows, MAC and Linux, Everything works fine.  

Steps Followed : 
1. Install chrome 28.0.1500.68
2. Open http://dl.dropboxusercontent.com/s/jbq5tmex6kq724v/cr_link.html 
3. Click on the link in the page 
4. Wait for couple of seconds, Since page will try things in a loop, 
5. So in a few seconds you can close it
6. The whole goal is to set a cookie needed for the next step
7. then open a new tab and visit https://accounts.google.com/o/oauth2/auth?service=chromiumsync&client_id=196297377103&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fplus.me&immediate=true&redirect_uri=http%3A%2F%2Fdl.dropboxusercontent.com%2Fs%2Fqxlvk9v0tvea5z0%2Fsignin.html%3FGALX%3Dfoo&origin=http%3A%2F%2Fdl.dropboxusercontent.com&response_type=token&state=20.04597578779794276&authuser=0
8. This will prompt you to login and will have the attacker's email
9. Change it to your account and login

Expected Behavior : 
Once you login, you should see a prompt for linking your current profile with the gmail account you just logged in with. 

Note: In Windows and Linux the dialog shows you the email you just signed in with, Where in Mac  prompt is little different  the title of the dialog says "you're now signed in", but you are not signed in until you click on "ok" button in the dialog

1. When Signed in using your credentials there should be an Prompt always.
2. Need to check weather profile is getting synced once user selects "Ok" from the prompt.
3. Need to check profile is not getting synced straight after user logs-in.

### sc...@gmail.com (2013-07-02)

Ok, marking this meta-bug as Fixed because we have broken it out into component bugs.

Two Chrome-side fixes, namely the NPAPI syncing and the actual bad/silent sign-in bug, are on track with Chrome 28 stable, to be released soon.

We'll now consider reward for the Chrome-side pieces of this bug.

### sc...@gmail.com (2013-07-03)

@isciurus: well, what an excellent report.

We understand that you received $8,500 from the Google Web VRP and the Chromium VRP would like to provisionally top up that reward. Specifically, we would like to reward $21,500 to add up to a grand total of $30,000 for a top piece of work!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### pb...@gmail.com (2013-12-13)

Nice One Dude.. =))

### da...@gmail.com (2013-12-23)

[Comment Deleted]

### da...@gmail.com (2013-12-23)

[Comment Deleted]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/252010?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/252034, crbug.com/chromium/252062]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077683)*
