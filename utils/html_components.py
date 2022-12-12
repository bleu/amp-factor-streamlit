import streamlit.components.v1 as components

class Components():
  def balance_container_as_text(self, token_data, total_amount_pool):
    balance = float(token_data["balance"])
    return f"""
        <div class="bg-[#001e3c] text-white flex flex-col justify-center items-center w-fit p-5">
          <p>Balance of
            <span class="font-bold">{token_data["name"]}</span>
          :</p>
          <p class="text-3xl">{balance:.2f}</p> 
          <p> {(balance/total_amount_pool)*100:.2f}% of the pool</p>
        </div>
      """

  def binary_balance_conteiner(self, token_data_x, token_data_y):
    total_amount_pool = float(token_data_x["balance"]) + float(token_data_y["balance"])
    return components.html(
      f"""
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="flex justify-between">
          {self.balance_container_as_text(token_data_x,total_amount_pool)}
          {self.balance_container_as_text(token_data_y,total_amount_pool)}
        </div>
      """
    )
  
  def amp_price_as_text(self, amp, type_token_buy, type_token_sell, amount_token_buy, price, default_price):
    price_variance = 100-((price/default_price)*100)
    if price_variance > 0:
      return f"""
          <div class="bg-[#001e3c] text-white flex flex-col justify-center items-center w-fit p-5">
            <p>With Amp Factor
              <span class="font-bold">{amp:.2f}</span>
            </p>
            <p>Will receive <span class="font-bold">{amount_token_buy:.2f}</span> of {type_token_buy}</p>
            <p>Price: {price}/{type_token_sell}</p>
            <p class="text-green-300"> {100-((price/default_price)*100):.2f}% &#8593;</p>
          </div>
        """
    elif price_variance < 0:
      return f"""
          <div class="bg-[#001e3c] text-white flex flex-col justify-center items-center w-fit p-5">
            <p>With Amp Factor
              <span class="font-bold">{amp:.2f}</span>
            </p>
            <p>Will receive <span class="font-bold">{amount_token_buy:.2f}</span> of {type_token_buy}</p>
            <p>Price: {price}/{type_token_sell}</p>
            <p class="text-red-300">{100-((price/default_price)*100):.2f}% &#8595;</p>
          </div>
        """
    else:
      return f"""
          <div class="bg-[#001e3c] text-white flex flex-col justify-center items-center w-fit p-5">
            <p>With Amp Factor
              <span class="font-bold">{amp:.2f}</span>
            </p>
            <p>Will receive <span class="font-bold">{amount_token_buy:.2f}</span> of {type_token_buy}</p>
            <p>Price: {price}/{type_token_sell}</p>
          </div>
        """


  def amp_price_conteiner(self, current_amp, new_amp, type_token_sell):
    if current_amp['amp'] == new_amp['amp']:
      return components.html(
        f"""
          <script src="https://cdn.tailwindcss.com"></script>
            <div class="flex w-full justify-center">
              {self.amp_price_as_text(new_amp['amp'], new_amp['type_token_buy'], type_token_sell, new_amp['amount_token_buy'], new_amp['price'], new_amp['default_price'])}
            </div>
        """
      )
    else:
      return components.html(
        f"""
          <script src="https://cdn.tailwindcss.com"></script>
          <div class="flex justify-between">
            {self.amp_price_as_text(new_amp['amp'], new_amp['type_token_buy'], type_token_sell, new_amp['amount_token_buy'], new_amp['price'], new_amp['default_price'])}
            {self.amp_price_as_text(current_amp['amp'], current_amp['type_token_buy'], type_token_sell ,current_amp['amount_token_buy'], current_amp['price'], current_amp['default_price'])}
          </div>
        """
    )
