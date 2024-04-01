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
var coupon = document.getElementsByClassName('coupon-btn') //btn dùng coupon
var pay = document.getElementsByClassName('pay') //btn dùng coupon

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

// coupon
for (i = 0; i < coupon.length; i++) {
	coupon[i].addEventListener('click', function(){ //nghe su kien click
		nameCoupon = inputField.value
		fetch('/Ecomerce/addCoupon/',{
			method: 'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken
			},
			body:JSON.stringify({'name':nameCoupon})
		})
		.then((response) => {
			return response.json()
		})
		.then((data) => {
			if(Object.keys(data).length === 0 && data.constructor === Object){
				document.getElementById('dis').innerHTML = ''
				document.getElementById('newTotal').innerHTML = ''
				alert("Mã khuyến mãi không hợp lệ !!!")
			}
			else{
				document.getElementById('dis').innerHTML = data.dis + '%'
				document.getElementById('newTotal').innerHTML = data.newTotal.toLocaleString('en-US')
			}
		})
	})
}

//pay
for (i = 0; i < pay.length; i++) {
	pay[i].addEventListener('click', function(event){ //nghe su kien click
		event.preventDefault();
		var radios = document.querySelectorAll('.radio-option');
		var selectedValue = null;
		radios.forEach(function(radio) {
			if (radio.checked) {
			selectedValue = radio.value;
			return;
			}
		});

		if (selectedValue !== null) {
			fetch('/Ecomerce/pay/',{
				method: 'POST',
				headers:{
					'Content-Type':'application/json',
					'X-CSRFToken': csrftoken
				},
				body:JSON.stringify({'idPay':selectedValue, "idCoupon":document.getElementById('coupon').value})
			})
			.then((response) => {
				return response.json()
			})
			.then(() => {
				alert('Cảm ơn bạn đã tin yêu tui !!!');
				window.location.href = "/Ecomerce"
			})
		} else {
			alert('Vui lòng chọn phương thức thanh toán !!!');
		}
	})
}


// Contact
document.addEventListener("DOMContentLoaded", () => {
	const name = document.getElementById("name")
	const email = document.getElementById("email")
	const mess = document.getElementById("message")
	const submit = document.getElementById("submit")
	if(submit){
		submit.addEventListener("click", (e) => {
		  e.preventDefault();
		  const data = {
			name: name.value,
			email: email.value,
			mess: mess.value
		  };
		  // postForm(data);
		  const formData = {
			'entry.751748849': data.name,
			'entry.346363371': data.email,
			'entry.1111552543': data.mess
		  };
	  
		  // Chuyển đổi đối tượng formData thành chuỗi query string
		  const params = new URLSearchParams(formData).toString();
	  
		  // URL của biểu mẫu Google Forms
		  const formURL = 'https://docs.google.com/forms/d/e/1FAIpQLSfQeW9PnHgkTrejZZQ_Zfrt3mSSaxCM-OFv9ytct5hXsO65Vg/formResponse';
	  
		  // Tạo URL hoàn chỉnh bao gồm dữ liệu biểu mẫu
		  const fullURL = `${formURL}?${params}`;
	  
		  // Gửi yêu cầu đến URL hoàn chỉnh
		  fetch(fullURL, { method: 'POST', mode:'no-cors' })
		  name.value = ''
		  email.value = ''
		  mess.value = ''
		  alert('Cảm ơn bạn đã liên hệ với tôi! Tôi sẽ sớm phản hồi cho bạn.')
		});
	}
  });