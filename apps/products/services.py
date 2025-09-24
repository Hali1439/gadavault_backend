import hashlib
import json

def pin_product_to_ipfs(product):
    """
    Demo stub for pinning product provenance.
    Returns a deterministic fake IPFS-like hash for demonstration.
    In production, replace with a real IPFS/Pinata integration.
    """
    payload = {
        "id": str(product.id),
        "name": product.name,
        "seller": str(product.seller_id),
        "story": product.story_markdown or "",
        "images": product.images or []
    }
    s = json.dumps(payload, sort_keys=True).encode()
    h = hashlib.sha256(s).hexdigest()
    return "Qm" + h[:44]