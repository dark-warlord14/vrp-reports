# crypto/x509's URI name constraints parser is too permissive

| Field | Value |
|-------|-------|
| **Issue ID** | [487820706](https://issues.chromium.org/issues/487820706) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | BoringSSL>Crypto>X509 |
| **CVE IDs** | CVE-2024-45341 |
| **Reporter** | da...@google.com |
| **Assignee** | ch...@google.com |
| **Created** | 2026-02-26 |
| **Bounty** | $1,000.00 |

## Description

**Summary:** [HIGH] legacy nameConstraints nc\_uri misparses userinfo/port and can bypass permitted URI subtree

**Program:** OSS VRP

**URL:** <https://github.com/google/boringssl>

**Vulnerability type:** Other

### Details

## summary

the legacy `crypto/x509` nameConstraints helper for URI names (`nc_uri`) extracts the host by stopping at the first `:` (treating it as a port delimiter) and does not handle `userinfo@host` as defined by rfc3986. as a result, a URI SAN like `http://example.com:80@evil.com/` is treated as having host `example.com`, even though the effective host is `evil.com`.

in deployments that use permittedSubtrees(URI) as a containment control for constrained sub-cas (common in private pkis with URI-based identities), this becomes a certificate validation bypass: a constrained sub-ca can issue leaf certificates outside the intended permitted subtree but still pass `X509_verify_cert`.

## severity

HIGH

## affected code (pinned)

- legacy nameConstraints URI matching:
  - [https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/v3\\_ncons.cc#L457-L499](https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/v3%5C_ncons.cc#L457-L499)
- legacy verifier applies nameConstraints during chain validation:
  - [https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/x509\\_vfy.cc#L546-L606](https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/x509%5C_vfy.cc#L546-L606)

precedent (severity context):

- cve-2024-45341 (go crypto/x509): URI nameConstraints bypass due to improper URI parsing (<https://osv.dev/vulnerability/CVE-2024-45341>)

## steps to reproduce

canonical:

```
rm -rf poc
unzip poc.zip -d poc
cd poc

# build boringssl first (outside this directory), then point the PoC at your checkout and build dir:
# cmake -GNinja -B build && ninja -C build

make canonical BORINGSSL_DIR=/path/to/boringssl BORINGSSL_BUILD_DIR=/path/to/boringssl/build

```

output (excerpt):

```
[CALLSITE_HIT] crypto/x509/v3_ncons.cc:457 nc_uri (via X509_verify_cert -> check_name_constraints -> NAME_CONSTRAINTS_check)
ok=1 err=0 (ok)
[PROOF_MARKER] nc_uri_userinfo_port_confusion

```

control (same env, no vuln trigger):

```
rm -rf poc
unzip poc.zip -d poc
cd poc
make control BORINGSSL_DIR=/path/to/boringssl BORINGSSL_BUILD_DIR=/path/to/boringssl/build

```

output (excerpt):

```
[CALLSITE_HIT] crypto/x509/v3_ncons.cc:457 nc_uri (via X509_verify_cert -> check_name_constraints -> NAME_CONSTRAINTS_check)
ok=0 err=47 (permitted subtree violation)
[NC_MARKER] control correctly rejected

```
### Attack scenario

this bypasses a policy boundary: the verifier accepts a certificate chain that violates the issuer's permittedSubtrees(URI) constraint. if nameConstraints are used to contain a compromised constrained sub-ca, this expands the blast radius of that compromise beyond the intended URI namespace.

credit: 1seal (<https://github.com/1seal>)

## Attachments

- [PR_DESCRIPTION.md](attachments/PR_DESCRIPTION.md) (text/markdown, 418 B)
- [addendum.md](attachments/addendum.md) (text/markdown, 1.8 KB)
- [attack_scenario.md](attachments/attack_scenario.md) (text/markdown, 2.2 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 803.7 KB)

## Timeline

### sp...@google.com (2026-02-26)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Hey! Our automation saw that your report contained a link to github.com! Did you know that you can get rewarded for patching vulnerabilities? See our [Patch Rewards Program](https://bughunters.google.com/about/rules/4928084514701312/patch-rewards-program-rules) for more information!

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### sp...@google.com (2026-02-26)

*NOTE: This is an automatically generated email*

Hey,

We just want to let you know that your report was **triaged** and we're currently looking into it.

You should receive further information in a couple of days, but it might take up to a week if we're particularly busy. In the meantime, you might want to take a look at [the list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Thanks,   

Google Security Bot

### jk...@google.com (2026-03-06)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### me...@google.com (2026-03-06)

Thanks for the report.

chlily@: Could you please help with the triage? Thanks!

### ch...@chromium.org (2026-03-06)

Thanks for the report and POC with specific example of misparse. This class of problem is described in [crbug.com/409484309](https://crbug.com/409484309) and alluded to in code comments: <https://boringssl.googlesource.com/boringssl/+/5774eca6004ed7c7467bd644c057797ca96b65f2/crypto/x509/v3_ncons.cc#519>

That bug also describes the approach to fix this by being more strict about URI parsing.

### ch...@google.com (2026-03-07)

Setting milestone because of s2 severity.

### da...@chromium.org (2026-03-09)

That's a fun syntax overlap. URI SANs are terribly ill-defined (URI syntax is all over place) but this is a good nudge to finally go solve the (long-known) [issue 409484309](https://issues.chromium.org/issues/409484309).

The report is a bit odd. It really should swap `example.com` and `evil.com`. The attack scenario here is that the malicious sub-CA is legitimately authoritative for (and thus constrained to) `evil.com`. Their goal is to escape that constraint and issue for something under `example.com`. Thus the right example would:

- The sub-CA has a name constraint of `evil.com`
- The sub-CA issues a certificate with a SAN of `http://evil.com:80@example.com/`

Now, in terms of whether this has a meaningful security impact, it depends on whether the relying party ultimately does anything useful with `http://evil.com:80@example.com/`. If the relying party does not pay any attention to such SANs, this is also irrelevant.

In the Web and HTTPS in general, URI SANs do not exist, so there's no impact there. (Chrome also doesn't use this certificate verifier at all, but we're using the Chrome VRP for BoringSSL in general.) We also have no built-in logic to match URI SANs. That means that the claim of "high" severity is inappropriate. This is *at most* a low severity bug, but probably is just not a security bug, which we can duplicate into the existing [issue 409484309](https://issues.chromium.org/issues/409484309).

Now, although BoringSSL does not implement any kind of URI SAN processing, we do return the SAN list to the application, so the application may have done its own thing.

Looking generally, an application's reference identifier should not be under attacker control (otherwise the whole thing is suspect), and I think we can reasonably assume that no application would actually use something like `http://evil.com:80@example.com/` as a reference identifer.

The question then, is whether a URI SAN application might match an untrusted userinfo-full SAN URI against a trusted userinfo-less reference identifier. Doing so seems highly suspect. If the certificate claims it is authority for `http://foo@example.com/`, is it also authoritative for `http://bar@example.com/`? `http://example.com/`? Ignoring part of the SAN when matching reference identifiers doesn't make much sense.

The two URI-SAN-using applications I'm aware of are SIP and SPIFFE. [RFC 5922](https://www.rfc-editor.org/rfc/rfc5922.html#section-7.1) is not impacted because they explicitly ban this. Indeed their reasoning supports the observation that such a match would not make sense:

> If the scheme of the URI value is "sip", and the URI value
> that contains a userpart (there is an '@'), the
> implementation MUST NOT accept the value as a SIP domain
> identity (a value with a userpart identifies an individual
> user, not a domain).

SPIFFE is less clear about this. [X509-SVID](https://spiffe.io/docs/latest/spiffe-specs/x509-svid/) does not say a whole lot about this. However, [SPIFFE-ID](https://spiffe.io/docs/latest/spiffe-specs/spiffe-id/#21-trust-domain) is clear that URIs with a userinfo are not valid SPIFFE IDs. Thus I think any correct SPIFFE implementation would also not be affected.

Then there's RFC 9525. That one is fascinating because it claims that fields other than the scheme and host [are ignored](https://www.rfc-editor.org/rfc/rfc9525.html#name-uniform-resource-identifier). However, that seems to not match either how SIP uses it (the text above) or how SPIFFE use it. (SPIFFE [does](https://spiffe.io/docs/latest/spiffe-specs/x509-svid/#31-leaf-certificates) use paths.)

So this is all a mess, but all concrete signs so far point to "no impact". Do you have a concrete application that is impacted?

### ko...@gmail.com (2026-03-09)

thanks for the thorough analysis. you're right on the framing: the constrained sub-ca should be the one constrained to `evil.com`, trying to escape that constraint and issue for `example.com`. i had that direction backwards in the report.

i don't have a concrete impacted application to point to here. your analysis of the known uri-san consumers i'm aware of, and the distinction that boringssl returns sans to the application rather than implementing uri matching itself, addresses the impact question. i also agree the `CVE-2024-45341` comparison was weaker than i made it sound because go's `crypto/x509` performs its own matching.

given that, i'm not contesting that this is below `HIGH` severity in boringssl absent a concrete downstream consumer. i'm happy to have this folded into issue `409484309` as part of the broader uri parsing cleanup.

if useful, i'm also happy to help by refreshing the patch from the report to match the stricter parsing direction you want to take.

### ch...@google.com (2026-03-21)

chlily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-05-05)

Project: boringssl  

Branch:  main  

Author:  Lily Chen [chlily@google.com](mailto:chlily@google.com)  

Link:    <https://boringssl-review.googlesource.com/92687>

crypto/x509: Tighten URI name constraints parsing and matching

---


Expand for full commit details
```
     
    This change uses stricter URI parsing to validate the name constraint 
    and the name being matched. 
     
    Bug: 487820706, 502006234 
    Change-Id: I02210878af377505a903bb999f9a8ef46a6a6964 
    Reviewed-on: https://boringssl-review.googlesource.com/c/boringssl/+/92687 
    Reviewed-by: David Benjamin <davidben@google.com> 
    Commit-Queue: Lily Chen <chlily@google.com>

```

---

Files:

- M `crypto/x509/v3_ncons.cc`
- M `crypto/x509/x509_test.cc`

---

Hash: b84dc606410ec1d8e2f779de5ec6791d2951308e  

Date: Wed Apr 15 16:25:31 2026


---

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Web Platform Privilege Escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Web Platform Privilege Escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487820706)*
