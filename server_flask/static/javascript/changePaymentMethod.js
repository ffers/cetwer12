



document.getElementById('ChangePaymentMethod').addEventListener('click', function() {
    // Видаляємо блок AdsressOld
    let oldAddressBlock = document.getElementById('paymentMethotRow');
    oldAddressBlock.parentNode.removeChild(oldAddressBlock);
  
    // Додаємо інший блок або виконайте інші дії, які вам потрібні
    var container = $('#paymentMethotGeneral');
    var newField = $('<div>')
        .html(`
			<footer><small class="text-muted">Способи оплати:</small></footer>
                <div class="col-sm">
					<input 
						type="radio" 
						class="form-check-input text-radio" 
						id="nalogka" name="payment_option" 
						value="1" {% if order.payment_method_id == 1 %}checked{% endif %} 
						onclick="togglePaybefore()"/>
					<label for="nalogka" class="form-check-label"> Післяплата</label>
				</div>
                <div class="col-sm">
					<input type="radio" 
						class="form-check-input text-radio" 
						id="card_pay" name="payment_option"
						value="2"{% if order.payment_method_id == 2 %}checked{% endif %} 
						onclick="togglePaybefore()"/>
					 <label for="card_pay" 
					 	class="form-check-label"> Оплата на рахунок</label></div>
                <div class="col-sm">
					<input type="radio" 
						class="form-check-input text-radio" 
						id="peredpalata" 
						name="payment_option" 
						value="3" 
						onclick="togglePaybefore()" {% if order.payment_method_id == 3 %}checked{% endif %}/>
					<label for="peredpalata" id="labelPayBe" class="form-check-label" > Передплата</label></div>
				<div id="hiddenFieldPay" style="display:none;" class="col">
					<input type="number" 
						style="text-align: center;" 
						class="form-control" 
						id="sum_before_goods" 
						name="sum_before_goods" 
						min="1" placeholder="Сумма" 
						value="{{ order.sum_before_goods }}" 
						required><br></div>
				<div class="col-sm">
					<input 
						type="radio" 
						class="form-check-input text-radio" 
						id="prom_oplata" 
						name="payment_option" 
						value="5" 
						onclick="togglePaybefore()"/>
						<label 
							for="peredpalata" 
							id="labelPayBe" 
							class="form-check-label" 
							required> ПромОплата
						</label>			
				</div>
				<div class="col-sm">
					<input 
						type="radio" 
						class="form-check-input text-radio" 
						id="rozetka_pay" 
						name="payment_option" 
						value="6" 
						onclick="togglePaybefore()"/>
						<label 
							for="peredpalata" 
							id="labelPayBe" 
							class="form-check-label" 
							required> RozetkaPay
						</label>			
				</div>
				<div class="col-sm">
					<input 
						type="radio" 
						class="form-check-input text-radio" 
						id="olx" 
						name="payment_option" 
						value="7" 
						onclick="togglePaybefore()"/>
						<label 
							for="peredpalata" 
							id="labelPayBe" 
							class="form-check-label" 
							required> OLX
						</label>			
				</div>
				<div class="col-sm">
					<input 
						type="radio" 
						class="form-check-input text-radio" 
						id="another" 
						name="payment_option" 
						value="8" 
						onclick="togglePaybefore()"/>
						<label 
							for="peredpalata" 
							id="labelPayBe" 
							class="form-check-label" 
							required> Інше
						</label>
                        <br>       
				</div>`  );

                // Добавление нового поля в контейнер
                container.append(newField);
});