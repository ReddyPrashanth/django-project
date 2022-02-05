      // This is your test publishable API key.
      const stripe = Stripe("pk_test_iluLgfWeyXsVnF8gN0t2PAhz003Qal1hso");

      // The items the customer wants to buy
      const items = [{ id: "xl-tshirt" }];
      
      let elements;
      
      initialize();
      checkStatus();
      
      document
        .querySelector("#payment-form")
        .addEventListener("submit", handleSubmit);
      
      // Fetches a payment intent and captures the client secret
      async function initialize() {
        const response = await fetch("/cart/create-payment-intent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ items }),
        });
        const { clientSecret } = await response.json();
      
        const appearance = {
          theme: 'stripe',
        };
        elements = stripe.elements({ appearance, clientSecret });
      
        const paymentElement = elements.create("payment");
        paymentElement.mount("#payment-element");
      }
      
      async function handleSubmit(e) {
        e.preventDefault();
        let event = new CustomEvent("loading");
        window.dispatchEvent(event)
        const { error } = await stripe.confirmPayment({
          elements,
          confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: "http://127.0.0.1:8000/cart/place-order/",
          },
        });
      
        // This point will only be reached if there is an immediate error when
        // confirming the payment. Otherwise, your customer will be redirected to
        // your `return_url`. For some payment methods like iDEAL, your customer will
        // be redirected to an intermediate site first to authorize the payment, then
        // redirected to the `return_url`.
        if (error.type === "card_error" || error.type === "validation_error") {
          showMessage(error.message);
        } else {
          showMessage("An unexpected error occured.");
        }
        window.dispatchEvent(event)
      }
      
      // Fetches the payment intent status after payment submission
      async function checkStatus() {
        const clientSecret = new URLSearchParams(window.location.search).get(
          "payment_intent_client_secret"
        );
      
        if (!clientSecret) {
          return;
        }
      
        const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
      
        switch (paymentIntent.status) {
          case "succeeded":
            showMessage("Payment succeeded!");
            break;
          case "processing":
            showMessage("Your payment is processing.");
            break;
          case "requires_payment_method":
            showMessage("Your payment was not successful, please try again.");
            break;
          default:
            showMessage("Something went wrong.");
            break;
        }
      }
      
      // ------- UI helpers -------
      
      function showMessage(messageText) {
        const messageContainer = document.querySelector("#payment-message");
      
        messageContainer.classList.remove("hidden");
        messageContainer.textContent = messageText;
      
        setTimeout(function () {
          messageContainer.classList.add("hidden");
          messageText.textContent = "";
        }, 4000);
      }
      