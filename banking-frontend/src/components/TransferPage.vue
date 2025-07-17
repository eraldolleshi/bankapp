<template>
  <div>
    <h2>Make a Transfer</h2>
    <button @click="goBack">Back to Dashboard</button>

    <form @submit.prevent="submitTransfer">
      <label for="from_iban">From Account (IBAN):</label>
      <select v-model="fromIban" required>
        <option v-for="acc in approvedAccounts" :key="acc.id" :value="acc.iban">
          {{ acc.iban }} - Balance: {{ acc.balance }}
        </option>
      </select>
      <br /><br />

      <label for="to_iban">To Account (IBAN):</label>
      <input type="text" v-model="toIban" required />
      <br /><br />

      <label for="amount">Amount (€):</label>
      <input type="number" v-model.number="amount" required min="0.01" step="0.01" />
      <br /><br />

      <button type="submit">Send Transfer</button>
    </form>

    <p v-if="error" style="color:red">{{ error }}</p>
    <p v-if="success" style="color:green">{{ success }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: localStorage.getItem('authToken'),
      bankAccounts: [],
      fromIban: null,
      toIban: '',
      amount: null,
      error: null,
      success: null,
    }
  },
  computed: {
    approvedAccounts() {
      return this.bankAccounts.filter(acc => acc.is_approved)
    }
  },
  mounted() {
    this.loadAccounts()
  },
  methods: {
    goBack() {
      this.$router.push('/client-dashboard')
    },
    async loadAccounts() {
      try {
        const res = await fetch('http://localhost:8000/api/bankaccounts/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        if (!res.ok) throw new Error('Failed to load accounts')
        this.bankAccounts = await res.json()
      } catch (e) {
        this.error = e.message
      }
    },
    async submitTransfer() {
      this.error = null
      this.success = null

      try {
        const res = await fetch('http://localhost:8000/api/transfer/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${this.token}`
          },
          body: JSON.stringify({
            from_iban: this.fromIban,
            to_iban: this.toIban,
            amount: this.amount
          })
        })

        if (!res.ok) {
          const err = await res.json()
          this.error = JSON.stringify(err)
          return
        }

        this.success = 'Transfer successful!'
      } catch (e) {
        this.error = e.message
      }
    }
  }
}
</script>

<style scoped>
div {
  max-width: 500px;
  margin: 30px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin: 10px 0 5px;
  font-weight: bold;
}

select,
input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 15px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #218838;
}

p {
  margin-top: 15px;
  font-weight: bold;
}
</style>
