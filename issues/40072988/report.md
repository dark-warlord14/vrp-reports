# Security: Android: URL spoofing in address bar if scheme is later in URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40072988](https://issues.chromium.org/issues/40072988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | en...@google.com |
| **Created** | 2023-09-21 |
| **Bounty** | $8,500.00 |

## Description

**VULNERABILITY DETAILS**  

On Android, Chrome Canary and Dev since at least version 119.0.6006.3, the address bar will not always show the URL's origin. The address bar will show another part of the URL if a scheme is present in the URL, such as the string "https" in a query parameter, path, or another part of the URL.

This can result in URL origin spoofing in address bar. The state is persistent even after focusing and unfocusing address bar, so it's not a "URL in edit mode" issue.

Discovered this moments before going to bed, so quick manual bisect shows commit 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 as likely suspect.

Not 100% sure about that bisect since it was based on manual commit analysis between versions 118.0.5993.2 and 119.0.6006.3: <https://chromium.googlesource.com/chromium/src/+log/118.0.5993.0..119.0.6006.0?pretty=fuller&n=10000>

A less likely suspect is commit 3ae9971c5637c9ea9fc3b4e5320baef9e6d68a77 but that should only kick in on URLs longer than 500 characters, and I can reproduce on much shorter URLs.

Will provide more info within a day or two when I can investigate further, maybe do an actual bisect, and provide better PoCs.

**VERSION**  

Chrome Version:  

Repro on 119.0.6020.0 Canary (latest as of report submission), 119.0.6006.3 Dev.  

Does NOT repro on 118.0.5993.2 Dev, 116.0.5845.173 Stable.  

Operating System: Android 12

**REPRODUCTION CASE**

1. Navigate to <https://example.com/https://accounts.google.com#/login>

Observed: Address bar shows "<https://accounts.google.com#>"  

Expected: Address bar shows "example.com/<https://account>"

Another basic repro:

1. Navigate to <http://example.com/?abcdef&123456&helloworld&moreparams&https>

Observed: Address bar shows "helloworld&moreparams&http"  

Expected: Address bar shows "example.com/?abcdef"

Seems to be some issue with parsing, since using / instead of ? changes behavior. And it seems you must use the same scheme as the actual URL (e.g. Use "https" string in https:// URL, use "http" string in http:// URL).

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [canary-repro.jpg](attachments/canary-repro.jpg) (image/jpeg, 171.9 KB)
- [stable-no-repro.jpg](attachments/stable-no-repro.jpg) (image/jpeg, 170.1 KB)
- [cct-stable-expected.jpg](attachments/cct-stable-expected.jpg) (image/jpeg, 111.5 KB)
- [cct-canary-observed.jpg](attachments/cct-canary-observed.jpg) (image/jpeg, 120.7 KB)

## Timeline

### al...@alesandroortiz.com (2023-09-21)

See attached screenshots of one of the PoC scenarios.

### [Deleted User] (2023-09-21)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-09-21)

Minor correction: Since "https" includes the string "http", you can use "http" on an https:// URL for repro.
For thoroughness, all of these work:
https://example.com/?abcdef&123456&helloworld&moreparams&https (https-https)
http://example.com/?abcdef&123456&helloworld&moreparams&http (http-http)
http://example.com/?abcdef&123456&helloworld&moreparams&https (http-https)

### me...@chromium.org (2023-09-21)

Thanks for the report. I can repro, seems like we are aligning the URL on the wrong side.

ender@, peilinwang@, could one of you please take a look?

[Monorail components: UI>Browser>Omnibox]

### me...@chromium.org (2023-09-21)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-09-22)

As the commit message suggests, this was intended to change some CCT behavior. I can confirm repro in CCT when I have WebView Canary set to the WebView provider. See attached screenshots.

Pre-requisites:
* Canary or Dev as WebView provider
* Gmail configured to use CCT to open links

Repro steps:
1. Add the following URL to a Gmail draft email: https://example.com/https://accounts.google.com?login&auth=code
2. Save the draft and open the draft again to see the clickable link
3. Click the URL

Observed: CCT address bar shows spoofed URL, including non-hostname/origin parts. "https://accounts.google.com?login&auth=code"
Expected: CCT address bar shows correct hostname/origin "example.com". CCT address bar only shows hostname/origin, not other parts of the URL.

### al...@alesandroortiz.com (2023-09-22)

Interestingly, the right-most character that is shown is determined by the right-most slash in the URL that is after the scheme string ("http"/"https").

e.g. https://example.com/?https&abcdef&moreparams&helloworld/thiswillnotbeshown

will result in the right-most characters being "helloworld" before the last slash.

but https://example.com/?abcdef&moreparams&helloworld/thiswillbeshownbecausehttpsafterthelastslash

will result in the very end of the URL being displayed because there isn't a slash after the "https" string in the URL.

This aligns with the logic changes made in commit 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 which look for scheme and then look for path using slash as separator. Something clearly isn't working as intended in the updated logic there, but I haven't examined exactly why yet.

### al...@alesandroortiz.com (2023-09-22)

Correction on https://crbug.com/chromium/1485446#c6 prerequisites:
WebView doesn't matter for CCT -- you need to set Canary as the default browser in system settings AND close Gmail (or any other app you're using for CCT) before attempting repro steps. If you don't close Gmail, it will continue using the previous default browser, hence my bad prereqs in earlier comment.

### me...@google.com (2023-09-22)

Thanks for further analysis! Assigning to ender@ per https://crbug.com/chromium/1485446#c7.

### [Deleted User] (2023-09-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@google.com (2023-09-22)

ender@ isn't in today, I reverted 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 locally and verified. meacer@ do we want to revert this asap since this has a high severity label?

### pe...@google.com (2023-09-22)

...locally and verified that it was causing the bug*

 (sorry some text got chopped off)

### me...@google.com (2023-09-22)

peilinwang: Yes, please, let's revert, especially ender@ can't take a look until next week. Assigning to you if you don't mind :)

### pe...@google.com (2023-09-22)

np, revert in progress :D

### al...@alesandroortiz.com (2023-09-22)

peilinwang@: Thanks for verifying bisect and starting revert.

### pe...@google.com (2023-09-22)

ccing reviewers

### en...@google.com (2023-09-22)

seems like both old and new mechanisms have their flaws..

the old one interprets "127.0.0.1:1234/index.html" as schema "127.0.0.1" and host "1234".

i'll look to reland that cl with appropriate tests. a bit surprising we don't have one..

### en...@google.com (2023-09-22)

adding Michael as there's something that baffles me a lot.

we shifted from URI.Parse (which has the problem described in https://crbug.com/chromium/1485446#c19) to GURL, assuming GURL schema would return, well, the schema. i'm not sure i understand how this all happened in the first place, is it possible there's a problem with GURL?

### pe...@google.com (2023-09-22)

revert landed: https://chromium-review.googlesource.com/c/chromium/src/+/4887295

assigning back to ender@

### en...@google.com (2023-09-22)

Thanks for the help Peilin. I will investigate this when I am back.
it definitely does not look right, but i wonder if we have a second place that parses URIs from string in UrlBar. It's either that or something about the GURL (i really doubt the latter, but hard to say rn).

### en...@google.com (2023-09-22)

dropping RBS because revert has landed; keeping the bug to investigate what causes this and to write tests to prevent reoccurrence

### be...@google.com (2023-09-22)

Adding Hotlist-RBS-Removed for tracking purposes.

### [Deleted User] (2023-09-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@google.com (2023-09-23)

ok, turns out i can't use this bug to fill gaps in testing.

marking this as closed, as revert landed (see https://crbug.com/chromium/1485446#c21). i'll file a separate bug to track follow up work.

### al...@alesandroortiz.com (2023-09-24)

Verified as fixed on 119.0.6026.0 Canary.

Before that, it repro'd up to 119.0.6024.2 Canary which was prior to fix.

Curious about the root cause, if you can share analysis here when available, or cc me in the new crbugs. Thanks!

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-09-27)

I was able to determine the cause of the unexpected behavior, after re-applying the original commit 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 and adding some logging to my Android Chromium build.

The reason is in `UrlBarData.java`'s `forUrlAndText()` function, shown below. The variables `displayText` and `displayTextStr` [1] do not have the scheme at the beginning of the URL, therefore the `displayTextStr.indexOf(scheme)` call [2] here returns -1 for URLs without the scheme, and the index of the scheme string in the non-origin part of the URL if the scheme is present in a non-origin part of the URL (e.g. index 34 for URL `https://example.com/?helloworld&holamundo&https&moreparams` since `displayTextStr` is `example.com/?helloworld&holamundo&https&moreparams`).

This causes `pathSearchOffset` [2] to return `39` in the example URL above.

If there is no path separator (`/`) after the scheme string, `pathOffset` is set to -1 [3] and the function returns in [4]. If there is a path separator, `pathOffset` is set to 50 (with e.g. `displayTextStr` = `example.com/?helloworld&holamundo&https&moreparams`) and the function returns in [5].

This is consistent with the observed behavior noted in my earlier comments, where the scheme text and path separator affected URL display.

https://chromium.googlesource.com/chromium/src/+/65283a6a62182ccbd1277a23a12a9ae4c73e22a5/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/UrlBarData.java#47
```
public static UrlBarData forUrlAndText(
            GURL url, CharSequence displayText, @Nullable String editingText) {
        assert url.isEmpty() || url.isValid();
        int pathSearchOffset = 0;
        String displayTextStr = displayText == null ? "" : displayText.toString();        // <--- [1]
        String scheme = url.getScheme();
        if (!TextUtils.isEmpty(scheme)) {
            if (!SCHEMES_TO_SPLIT.contains(scheme)) {
                return create(url, displayTextStr, 0, displayTextStr.length(), editingText);
            }
            if (UrlConstants.BLOB_SCHEME.equals(scheme)) {
                int innerSchemeSearchOffset =
                        findFirstIndexAfterSchemeSeparator(displayText, scheme.length());
                Uri innerUri = Uri.parse(displayTextStr.substring(innerSchemeSearchOffset));
                String innerScheme = innerUri.getScheme();
                // Substitute the scheme to allow for proper display of end of inner origin.
                if (!TextUtils.isEmpty(innerScheme)) {
                    scheme = innerScheme;
                }
            }
            pathSearchOffset = findFirstIndexAfterSchemeSeparator(
                    displayText, displayTextStr.indexOf(scheme) + scheme.length());     // <--- [2]
        }
        int pathOffset = -1;
        if (displayText != null && pathSearchOffset < displayText.length()) {
            pathOffset = displayTextStr.indexOf('/', pathSearchOffset);      // <--- [3]
        }
        if (pathOffset == -1) {
            return create(url, displayText, 0, displayText == null ? 0 : displayText.length(),     // <-- [4]
                    editingText);
        }
        // If the '/' is the last character and the beginning of the path, then just drop
        // the path entirely.
        if (displayText != null && pathOffset == displayText.length() - 1) {
            return create(
                    url, displayTextStr.subSequence(0, pathOffset), 0, pathOffset, editingText);
        }
        return create(url, displayText, 0, pathOffset, editingText);       // <--- [5]
    }
```

### al...@alesandroortiz.com (2023-09-27)

Minor correction to https://crbug.com/chromium/1485446#c31: The example URL in this section should end in "/thiswillnotbeshown"

"...If there is a path separator, `pathOffset` is set to 50 (with e.g. `displayTextStr` = `example.com/?helloworld&holamundo&https&moreparams/thiswillnotbeshown`)..."

### al...@alesandroortiz.com (2023-09-27)

I also added logging to the code before commit 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 to investigate why `forUrlAndText()` worked before.

The reason why `forUrlAndText()` as shown below worked before is because it set `scheme` to `Uri.parse(displayTextStr).getScheme()` [1].

For portless `displayTextStr` values, `scheme` is set to `null` (e.g. `null` for `example.com/hello`), since `displayTextStr` does not have a scheme and fails the `!TextUtils.isEmpty(scheme)` conditional [2].

For `displayTextStr` values with ports, `scheme` is set to the hostname (e.g. `example.com` or `127.0.0.1` for `displayTextStr` values `example.com:12345/hello` or `127.0.0.1:12345/hello`), since `Uri.parse()` cannot properly parse a URL with the format used in `displayTextStr` (a known issue). The hostname as scheme causes the `ACCEPTED_SCHEMES.contains(scheme)` conditional [3] to always return false.

In both cases (portless or portful URLs), `pathOffset` is set correctly in [4] and the function always returns in [5].

Because both `!TextUtils.isEmpty(scheme)` or `ACCEPTED_SCHEMES.contains(scheme)` always return false (`scheme` is always either `null` or the hostname), the reported issue in https://crbug.com/chromium/1485446#c0 was obscured until commit 65283a6a62182ccbd1277a23a12a9ae4c73e22a5 changed the code in a way that correctly extracted the scheme from the URL (the `url` argument). Because the updated code still assumed that `displayTextStr` would contain the scheme, the hidden issue started reproducing as I reported in https://crbug.com/chromium/1485446#c0.

https://chromium.googlesource.com/chromium/src/+/d02adf6b95efdeaed39d8ba44f81d68fcb34dc14/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/UrlBarData.java#70
```
    public static UrlBarData forUrlAndText(
            String url, CharSequence displayText, @Nullable String editingText) {
        int pathSearchOffset = 0;
        String displayTextStr = displayText == null ? "" : displayText.toString();
        String scheme = Uri.parse(displayTextStr).getScheme();                         // <--- [1]
        if (!TextUtils.isEmpty(scheme)) {                                                               // <--- [2]
            if (UNSUPPORTED_SCHEMES_TO_SPLIT.contains(scheme)) {
                return create(url, displayText, 0, displayText.length(), editingText);
            }
            if (UrlConstants.BLOB_SCHEME.equals(scheme)) {
                int innerSchemeSearchOffset =
                        findFirstIndexAfterSchemeSeparator(displayText, scheme.length());
                Uri innerUri = Uri.parse(displayTextStr.substring(innerSchemeSearchOffset));
                String innerScheme = innerUri.getScheme();
                // Substitute the scheme to allow for proper display of end of inner origin.
                if (!TextUtils.isEmpty(innerScheme)) {
                    scheme = innerScheme;
                }
            }
            if (ACCEPTED_SCHEMES.contains(scheme)) {                                 // <--- [3]
                pathSearchOffset = findFirstIndexAfterSchemeSeparator(
                        displayText, displayTextStr.indexOf(scheme) + scheme.length());
            }
        }
        int pathOffset = -1;
        if (displayText != null && pathSearchOffset < displayText.length()) {
            pathOffset = displayTextStr.indexOf('/', pathSearchOffset);                // <--- [4]
        }
        if (pathOffset == -1) {
            return create(url, displayText, 0, displayText == null ? 0 : displayText.length(),
                    editingText);
        }
        // If the '/' is the last character and the beginning of the path, then just drop
        // the path entirely.
        if (displayText != null && pathOffset == displayText.length() - 1) {
            return create(
                    url, displayTextStr.subSequence(0, pathOffset), 0, pathOffset, editingText);
        }
        return create(url, displayText, 0, pathOffset, editingText);                // <--- [5]
    }
```

### al...@alesandroortiz.com (2023-09-27)

This was really interesting to analyze. :) Seems like `forUrlAndText()` has been around since 2018 or before, with about the same logic over the years until September update.

Does anyone know if in the distant past `displayTextStr` would have always contained the scheme? The code seems to assume so. Purely out of curiosity, since this bug has probably been subtly hidden since the argument value changed.

### mt...@chromium.org (2023-09-27)

Great analysis, thanks!

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations, Alesandro! The Chrome VRP Panel has decided to award you $7500 for this bug + $1,000 bisect bonus. Thank you for your efforts and your high quality report of this very impactful bug -- great finding and excellent report!

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-09-30)

Thanks for the reward and quick VRP decision!

### [Deleted User] (2023-10-04)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@google.com (2023-10-04)

The revert is already in M119.

### al...@alesandroortiz.com (2023-10-16)

For future reference, follow-up tests and reland of reverted commit were made on Oct 4th and 6th, tracked in https://crbug.com/chromium/1486276.

### [Deleted User] (2023-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1485446?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072988)*
