import ipaddress
import socket
from urllib.parse import urlparse


BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
}


def is_private_or_local_url(url: str) -> bool:
    """
    Return True if the URL points to a private,
    local, loopback, link-local, or reserved address.
    """

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        if not hostname:
            return True

        hostname = hostname.lower().strip()

        # Block local hostnames
        if hostname in BLOCKED_HOSTNAMES:
            return True

        # Direct IP address
        try:
            ip = ipaddress.ip_address(hostname)

            return (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_unspecified
            )

        except ValueError:
            pass

        # Resolve domain to IP addresses
        try:
            addresses = socket.getaddrinfo(
                hostname,
                None
            )

            for address in addresses:
                ip_text = address[4][0]

                try:
                    ip = ipaddress.ip_address(ip_text)

                    if (
                        ip.is_private
                        or ip.is_loopback
                        or ip.is_link_local
                        or ip.is_reserved
                        or ip.is_unspecified
                    ):
                        return True

                except ValueError:
                    continue

        except socket.gaierror:
            return False

        return False

    except Exception:
        return True