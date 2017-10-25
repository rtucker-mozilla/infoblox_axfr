$TTL 3600
domain.com.  3600  IN   SOA   ns.domain.org. sysadmins.domain.org. (
        2017072400     ; Serial
        180     ; Refresh
        180     ; Retry
        1209600     ; Expire
        3600     ; Minimum
)

domain.com.                             IN      NS      ns.domain.com
domain.com.                             IN      MX      10              mx1.scl3.domain.com.
domain.com.                             IN      MX      10              mx2.scl3.domain.com.
_dmarc.domain.com.                      IN      TXT     "v=DMARC1; p=none; rua=mailto:accounts@domain.com; ruf=mailto:accounts@domain.com; adkim=r; aspf=r"
domain.com.                             60      IN      TXT             "v=spf1 mx a include:domain.com -all"
domain.com.                             60      IN      TXT             "google-site-verification=asdfasdfsadfasdf"
www.domain.com.                         300     IN      CNAME           domain.com.
domain.com.                             60      IN      A               1.2.3.4
