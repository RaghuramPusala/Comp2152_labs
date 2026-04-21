# ============================================================
#  WEEK 14 LAB — Q2: HTTP SECURITY HEADER CHECKER
#  COMP2152 — [Raghuram Badavath]
# ============================================================

import urllib.request


# Security headers every website should have
REQUIRED_HEADERS = {
    "Content-Type":              "Defines the content format",
    "X-Frame-Options":           "Vulnerable to clickjacking",
    "X-Content-Type-Options":    "Vulnerable to MIME sniffing",
    "Strict-Transport-Security": "No HTTPS enforcement",
    "Content-Security-Policy":   "No XSS protection policy",
    "X-XSS-Protection":          "No XSS filter",
}


# Check headers from URL
def check_headers(url):
    try:
        with urllib.request.urlopen(url) as response:
            headers = dict(response.headers)

            # Normalize headers (case-insensitive)
            headers_lower = {k.lower(): v for k, v in headers.items()}

            results = []

            for header in REQUIRED_HEADERS:
                key = header.lower()
                if key in headers_lower:
                    results.append({
                        "header": header,
                        "present": True,
                        "value": headers_lower[key]
                    })
                else:
                    results.append({
                        "header": header,
                        "present": False,
                        "value": "MISSING"
                    })

            return results

    except Exception:
        return []


# Generate report
def generate_report(url, results):
    print(f"  URL: {url}")
    missing_count = 0

    for r in results:
        if r["present"]:
            print(f"  ✓ {r['header']}: {r['value']}")
        else:
            print(f"  ✗ {r['header']}: MISSING — {REQUIRED_HEADERS[r['header']]}")
            missing_count += 1

    print(f"  Missing {missing_count} of {len(results)} security headers!")


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: HTTP SECURITY HEADER CHECKER")
    print("=" * 60)

    urls = [
        "http://httpbin.org",
        "https://www.google.com",
    ]

    for url in urls:
        print(f"\n--- Checking {url} ---")
        results = check_headers(url)
        if results:
            generate_report(url, results)
        else:
            print("  (could not connect or not implemented)")

    print("\n" + "=" * 60)