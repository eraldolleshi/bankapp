<template>
  <div>
    <h2>Create Bank Account</h2>
    <form @submit.prevent="createAccount">
      <label>IBAN:</label><br />
      <input v-model="iban" required /><br /><br />

      <label>Currency:</label><br />
      <input v-model="currency" required /><br /><br />

      <label>Initial Balance:</label><br />
      <input type="number" v-model.number="balance" required /><br /><br />

      <button type="submit">Create</button>
    </form>

    <p v-if="error" style="color:red">{{ error }}</p>
    <p v-if="success" style="color:green">Account created successfully!</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      iban: '',
      currency: '',
      balance: 0,
      error: null,
      success: false,
      token: localStorage.getItem('authToken'),
    };
  },
  methods: {
    async createAccount() {
      this.error = null;
      this.success = false;

      try {
        const response = await fetch('http://localhost:8000/api/bankaccounts/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${this.token}`,
          },
          body: JSON.stringify({
            iban: this.iban,
            currency: this.currency,
            balance: this.balance
          }),
        });

        if (!response.ok) {
          const data = await response.json();
          this.error = JSON.stringify(data);
          return;
        }

        this.success = true;
        this.iban = '';
        this.currency = '';
        this.balance = 0;
      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>

<style scoped>
div {
  max-width: 450px;
  margin: 40px auto;
  padding: 25px;
  background: #f2f2f2;
  border-radius: 10px;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #222;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin: 10px 0 5px;
  font-weight: bold;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 20px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

p {
  margin-top: 15px;
  font-weight: bold;
}
</style>
