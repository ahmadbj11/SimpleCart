import json

from .settings import DEFAULT_PRICE

def test_product_detail_api(client):
    id = 3
    response = client.get(f"/api/products/{id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert id == data.get('id')
    assert DEFAULT_PRICE * id


def test_product_api(client):
    response = client.get("/api/products")
    assert response.status_code == 200

# post new cart
def test_post_cart(client):
    # Menentukan data cart yang akan diuji
    cart_data = {
        "coupon_code": "XYZ",
        "shipping_fee": 15000,
        "cart_items": [
            {"product_id": 1, "qty": 2},
            {"product_id": 2, "qty": 3}
        ]
    }

    # Mengirim permintaan POST untuk membuat keranjang baru
    response = client.post("/api/cart", json=cart_data)

    # Memeriksa apakah responsenya benar dan kode statusnya 200
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "data created"

    # Melakukan pengujian lebih lanjut terkait cart yang telah dibuat
    cart_id = int(response.headers["Location"].split("/")[-1])
    test_get_cart(client, cart_id)
    test_update_cart(client, cart_id)
    test_delete_cart(client, cart_id)

# fungsi untuk mendapatkan detail keranjang
def test_get_cart(client, cart_id):
    response = client.get(f"/api/cart/{cart_id}")
    assert response.status_code == 200
    data = json.loads(response.data)

    # Melakukan pemeriksaan lebih lanjut terkait detail keranjang
    assert data.get("id") == cart_id
    assert "coupon_code" in data
    assert "shipping_fee" in data
    assert "cart_items" in data
    assert "subtotal" in data
    assert "grandtotal" in data
    assert "eligible_promo" in data

# fungsi untuk memperbarui keranjang
def test_update_cart(client, cart_id):
    updated_cart_data = {
        "coupon_code": "NEWCODE",
        "cart_items": [
            {"product_id": 1, "qty": 1},
            {"product_id": 3, "qty": 2}
        ]
    }

    response = client.put(f"/api/cart/{cart_id}", json=updated_cart_data)
    assert response.status_code == 200

    # Melakukan pengujian lebih lanjut terkait perubahan pada keranjang
    test_get_cart(client, cart_id)

# fungsi untuk menghapus keranjang
def test_delete_cart(client, cart_id):
    response = client.delete(f"/api/cart/{cart_id}")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == f"cart-{cart_id} deleted"
