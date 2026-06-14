# Response splitting with 302 redirects allows chrome sync session fixation

| Field | Value |
|-------|-------|
| **Issue ID** | [40078242](https://issues.chromium.org/issues/40078242) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | is...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2013-10-14 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

In the case of a 302-redirects chain, OneClickSigninHelper incorrectly extracts url of possible google signin response and thus can be forced to trust Google-Chrome-SignIn/Google-Accounts-SignIn headers from any domain.

void OneClickSigninHelper::ShowInfoBarIfPossible(net::URLRequest\* request,  

ProfileIOData\* io\_data,  

int child\_id,  

int route\_id) {  

std::string google\_chrome\_signin\_value;  

std::string google\_accounts\_signin\_value;  

request->GetResponseHeaderByName("Google-Chrome-SignIn",  

&google\_chrome\_signin\_value); <----- Headers from the last response  

request->GetResponseHeaderByName("Google-Accounts-SignIn",  

&google\_accounts\_signin\_value);

```
if (!google_accounts_signin_value.empty() ||  
  !google_chrome_signin_value.empty()) {  
VLOG(1) << "OneClickSigninHelper::ShowInfoBarIfPossible:"  
    << " g-a-s='" << google_accounts_signin_value << "'"  
    << " g-c-s='" << google_chrome_signin_value << "'";  
}  

if (!gaia::IsGaiaSignonRealm(request->original_url().GetOrigin())) <----- But original_url is the first url in the 302 redirects chain  
return;  

```

In order to exploit this up to session fixation, you can take any web authorization/authentication protocol, allowing 302 redirects: for example, Google's OAuth/OpenID. Since both OAuth and OpenID are binded to accounts. subdomain of google.com, the first request to the endpoint along with "service=chromiumsync" in query will turn a new renderer into a trusted signin process, then 302-directing Chrome to attacker's domain. The second response from a third party domain (chrome\_signin.php in repro) will deliver the signin headers, in turn redirecting browser to the final continue\_url and starting the synchronization without a confirmation.  

Restrictions:

1. You still need ServiceLoginAuth CSRF protection bypass / XSS on \*.google.com (or even social engineering is sufficient: to submit any PasswordForm from accounts.google.com and to prefill a password for attacker's account)
2. If current profile had already been synced with another account, a confirmation dialog will be shown anyway

**VERSION**  

Chrome Version: [30.0.1599.69] [stable]  

Operating System: [Windows, 6.1 (Windows 7, Windows Server 2008 R2)]

**REPRODUCTION CASE**

1. In a new profile go to <https://www.google.com/ServiceLoginAuth>, then emulate login CSRF check bypass by typing in console: document.cookie = 'GALX=abc; path=/ServiceLoginAuth; domain=.google.com';
2. Open the attached chrome\_signin.html, wait for 1-2 seconds until a new google account is established, then click on the "signin" link
3. Chrome will start syncing with [isciurus.test2@gmail.com](mailto:isciurus.test2@gmail.com)

PATCH  

Looks like the patch should be straightforward to verify last url in the chain of redirects instead of the original url  

TEST=A standard auth flow from menu->"Sign in to Chrome" should sign the user in successfully. Repro steps with chrome\_signin.html/chrome\_signin.php PoC should not sign into Chrome, but redirect back to /ServiceLogin instead.

Best,  

Andrey Labunets  

[isciurus@gmail.com](mailto:isciurus@gmail.com)

## Attachments

- [redirect_url_check.patch](attachments/redirect_url_check.patch) (text/x-diff; charset=us-ascii, 553 B)
- [chrome_signin.html](attachments/chrome_signin.html) (text/html; charset=us-ascii, 2.1 KB)
- [chrome_signin.php](attachments/chrome_signin.php) (text/plain; charset=us-ascii, 234 B)

## Timeline

### fe...@chromium.org (2013-10-14)

Thanks for the clear issue description.

### fe...@chromium.org (2013-10-14)

rogerta@, can you please take a look at this?

### cl...@chromium.org (2013-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-30)

rogerta@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-07)

rogerta@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-13)

Migrating old milestone labels.

### cl...@chromium.org (2013-11-15)

rogerta@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2013-11-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2013-11-19)

Sorry guys that I completely missed this.  I am looking at it now.

### ro...@chromium.org (2013-11-19)

This attack uses a technique that was also used in the security problem reported earlier this summer (crbug.com/151010, crbug.com/151062, by the same person).  It exploits the fact that "o/oauth2/auth" can redirect to any URL after doing its job.  However the specific problematic code in this bug report is distinct from those in the two previous ones.

The original post explains the bug pretty well.  Chrome looks for specific http headers that gaia sends after a sign in, and tries to validate that the headers were really send from gaia and not some random website.  It does that by checking the URL with the function gaia::IsGaiaSignonRealm().  However, chrome is checking the wrong URL if there is a chain of redirects, opening the door for this attack.

Since the suggested fix is quite simple, I have patched it into my source tree and verified that it does not break anything.  I have not yet verified that it actually fix the security problem though, still investigating.


### ro...@chromium.org (2013-11-19)

So I am able to repro the vulnerability with M33.  I can also confirm the suggested fix (patch in original comment) also corrects the problem.

### ro...@chromium.org (2013-11-20)

See https://codereview.chromium.org/77343002/ 

### bu...@chromium.org (2013-11-21)

------------------------------------------------------------------------
r236563 | rogerta@chromium.org | 2013-11-21T18:54:16.089404Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/sync/one_click_signin_helper.cc?r1=236563&r2=236562&pathrev=236563

During redirects in the one click sign in flow, check the current URL
instead of original URL to validate gaia http headers.

BUG=307159

Review URL: https://codereview.chromium.org/77343002
------------------------------------------------------------------------

### in...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### ka...@google.com (2013-12-02)

approved for m32. 

### bu...@chromium.org (2013-12-02)

------------------------------------------------------------------------
r238137 | rogerta@chromium.org | 2013-12-02T18:41:45.068423Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/chrome/browser/ui/sync/one_click_signin_helper.cc?r1=238137&r2=238136&pathrev=238137

Merge 236563 "During redirects in the one click sign in flow, ch..."

> During redirects in the one click sign in flow, check the current URL
> instead of original URL to validate gaia http headers.
> 
> BUG=307159
> 
> Review URL: https://codereview.chromium.org/77343002

TBR=rogerta@chromium.org

Review URL: https://codereview.chromium.org/99783002
------------------------------------------------------------------------

### la...@google.com (2013-12-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-12-03)

merged to m31 in r238432

### bu...@chromium.org (2013-12-03)

------------------------------------------------------------------------
r238432 | inferno@chromium.org | 2013-12-03T18:18:27.614874Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/chrome/browser/ui/sync/one_click_signin_helper.cc?r1=238432&r2=238431&pathrev=238432

Merge 236563 "During redirects in the one click sign in flow, ch..."

> During redirects in the one click sign in flow, check the current URL
> instead of original URL to validate gaia http headers.
> 
> BUG=307159
> 
> Review URL: https://codereview.chromium.org/77343002

TBR=rogerta@chromium.org

Review URL: https://codereview.chromium.org/102073004
------------------------------------------------------------------------

### mb...@chromium.org (2013-12-03)

Thanks for the report! This one qualifies for a special $1337 reward because it was an interesting attack in an area that we don't see many reports in.

### bu...@chromium.org (2013-12-03)

------------------------------------------------------------------------
r238481 | laforge@chromium.org | 2013-12-03T23:25:46.994266Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/chrome/browser/ui/sync/one_click_signin_helper.cc?r1=238481&r2=238480&pathrev=238481

Revert 238432 "Merge 236563 "During redirects in the one click s..."

> Merge 236563 "During redirects in the one click sign in flow, ch..."
> 
> > During redirects in the one click sign in flow, check the current URL
> > instead of original URL to validate gaia http headers.
> > 
> > BUG=307159
> > 
> > Review URL: https://codereview.chromium.org/77343002
> 
> TBR=rogerta@chromium.org
> 
> Review URL: https://codereview.chromium.org/102073004

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/100063003
------------------------------------------------------------------------

### bu...@chromium.org (2013-12-03)

------------------------------------------------------------------------
r238482 | inferno@chromium.org | 2013-12-03T23:29:22.462815Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/chrome/browser/ui/sync/one_click_signin_helper.cc?r1=238482&r2=238481&pathrev=238482

Revert 238481 "Revert 238432 "Merge 236563 "During redirects in ..."

> Revert 238432 "Merge 236563 "During redirects in the one click s..."
> 
> > Merge 236563 "During redirects in the one click sign in flow, ch..."
> > 
> > > During redirects in the one click sign in flow, check the current URL
> > > instead of original URL to validate gaia http headers.
> > > 
> > > BUG=307159
> > > 
> > > Review URL: https://codereview.chromium.org/77343002
> > 
> > TBR=rogerta@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/102073004
> 
> TBR=inferno@chromium.org
> 
> Review URL: https://codereview.chromium.org/100063003

TBR=laforge@chromium.org

Review URL: https://codereview.chromium.org/100063004
------------------------------------------------------------------------

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Just kicked off payment on this, which will take a few weeks to go through. Thanks again for your help improving Chrome security!

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/307159?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>SignIn, Services>Sync]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078242)*
