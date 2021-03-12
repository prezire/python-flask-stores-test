document.querySelector('.btn-checkout').addEventListener('click', () => {
  fetch('/checkout', {method: 'POST'})
  .then(result => {
    console.log(result);
    return result.json();
  })
  .then(data => {
    console.log(data);
    return Stripe(data.checkout_public_key)
      .redirectToCheckout({ sessionId: data.session_id });
  })
  .then(function(result) {
    if (result.error) {
      alert(result.error.message);
    }
  })
  .catch(function(error) {
    console.error('Error:', error);
  });
})