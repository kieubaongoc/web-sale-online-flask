function add_to_cart(id, name, price) {
            fetch("/api/cart", {
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: id,
                    name: name,
                    price: price
                })
            }).then(res => res.json()).then(data => {
                console.info(data);
                var stats = document.getElementById("cart-stats")
                stats.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
            })
}


function delete_product(productId) {
            var c = confirm("Bạn chắc chắn muốn xóa?");
            if (c == true) {
                fetch("/api/products/" + productId, {
                    method: "delete"
                }).then(function(res) {
                    return res.json();
                }).then(function(data) {
                    console.info(data);
                    var proId = data.data.product_id;
                    var p = document.getElementById("product" + proId);
                    p.style.display = "none";
                }).catch(function(err) {
                    console.error(err);
                });
            }
}


function del_item(itemId) {
    if (confirm("Bạn có chắc chắn xóa sản phẩm khỏi giỏ không?") == true)
    fetch(`/api/cart/${itemId}`, {
        'method': 'delete',
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.status == 200) {
            var x = document.getElementById(`item${data.itemId}`);
            x.style.display = "none";
        }
        else {
            alert('delete failed 1');
        }
    }).catch(err => alert('delete failed 2'));
}


function updateItem(obj, itemId) {
    fetch(`/api/cart/${itemId}`, {
        'method': 'post',
        'body': JSON.stringify({
            'quantity': obj.value
        }),
        'headers':{
            'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.status != 200)
                alert("update failed");
            else {
                document.getElementById('total_quantity').innerText = data.total_quantity;
                document.getElementById('total_amount').innerText = data.total_amount;
            }
                console.log("successful");
    }).catch(err => console.log("failed"));
}



