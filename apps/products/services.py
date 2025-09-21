# apps/products/services.py
import hashlib, json

def pin_product_to_ipfs(product):
    """
    Demo stub for pinning product provenance.
    Returns deterministic fake IPFS-like hash for demo.
    Replace with Pinata/Infura/actual IPFS client in production.
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
