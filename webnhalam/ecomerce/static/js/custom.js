(function() {
	'use strict';

	var tinyslider = function() {
		var el = document.querySelectorAll('.testimonial-slider');
		if (el.length > 0) {
			var slider = tns({
				container: '.testimonial-slider',
				items: 1,
				axis: "horizontal",
				controlsContainer: "#testimonial-nav",
				swipeAngle: false,
				speed: 700,
				nav: true,
				controls: true,
				autoplay: true,
				autoplayHoverPause: true,
				autoplayTimeout: 3500,
				autoplayButtonOutput: false
			});
		}
	};
	tinyslider();

	var sitePlusMinus = function() {
		var value, quantity = document.getElementsByClassName('quantity-container');
		function createBindings(quantityContainer) {
	      var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0]; // lấy ô số lượng
	      var increase = quantityContainer.getElementsByClassName('increase')[0]; //Lấy dấu cộng
	      var decrease = quantityContainer.getElementsByClassName('decrease')[0]; //Lấy dấu trừ
	      increase.addEventListener('click', function (e) { increaseValue(e, quantityAmount); });
	      decrease.addEventListener('click', function (e) { decreaseValue(e, quantityAmount); });
	    }
	    function init() {
	        for (var i = 0; i < quantity.length; i++ ) {
						createBindings(quantity[i]);
	        }
	    };
	    function increaseValue(event, quantityAmount) { //nhấn nút cộng
			var idDetail = quantityAmount.dataset.product //lấy idDetail
	        value = parseInt(quantityAmount.value, 10);
	        value = isNaN(value) ? 0 : value;
			updateCart(idDetail,'add')
	        value++;
	        quantityAmount.value = value;
	    }
	    function decreaseValue(event, quantityAmount) {//nhấn nút trừ
			var idDetail = quantityAmount.dataset.product //lấy idDetail
	        value = parseInt(quantityAmount.value, 10);
	        value = isNaN(value) ? 0 : value;
	        if (value > 1){
				updateCart(idDetail,'minus')
				value--;
			}
	        quantityAmount.value = value;
	    }
	    init();
	};
	sitePlusMinus();

})()


var addSpans = document.getElementsByClassName('add-cart')
var updateBtn = document.getElementsByClassName('update-cart') // lấy btn xóa thui

//Thêm product mới
for (i = 0; i < addSpans.length; i++) {
	addSpans[i].addEventListener('click', function(){ //nghe su kien click
		var productId = this.dataset.product //lay id product
		if (user === "None") {
			alert("Hãy đăng nhập hoặc đăng ký để bắt đầu mua sắm ngay bây giờ !!!")
		}
		else{
			addProUserOder(productId)
		}
	})
}
function addProUserOder(product){
	fetch('/Ecomerce/addPro/',{
		method: 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken
		},
		body:JSON.stringify({'idPro':product})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
		alert(data)
	})
}

//Cập nhật cart
for (i = 0; i < updateBtn.length; i++) {
	updateBtn[i].addEventListener('click', function(){ //nghe su kien click
		var idDetail = this.dataset.product //lay id product

		updateCart(idDetail,'remove')
	})
}
function updateCart(idDetail, acction){
	fetch('/Ecomerce/updateCart/',{
		method: 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken
		},
		body:JSON.stringify({'idDetail':idDetail, 'acction':acction})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
		if(data.acction == "remove"){
			document.getElementById('row_'+idDetail).remove()
			document.getElementById('lastTotal').innerHTML = data.newTotal.toLocaleString('en-US') + ' VND'
		}
		else{
			document.getElementById('total_' + idDetail).innerHTML = data.total.toLocaleString('en-US')
			document.getElementById('lastTotal').innerHTML = data.newTotal.toLocaleString('en-US') + ' VND'
		}
	})
}