<template>
  <div class="dashboard">
    <div class="header">
      <h2>👤 Client Dashboard</h2>
      <button class="logout" @click="logout">Logout</button>
    </div>

    <nav class="nav">
      <router-link to="/debit-card-request">💳 Request Debit Card</router-link>
      <router-link to="/transfer">💸 Transfer</router-link>
      <router-link to="/create-bank-account">🏦 Create Bank Account</router-link>
    </nav>

    <section class="section">
      <h3>🏦 Your Bank Accounts</h3>
      <ul v-if="bankAccounts.length">
        <li v-for="acc in bankAccounts" :key="acc.id" class="card">
          <p><strong>IBAN:</strong> {{ acc.iban }}</p>
          <p><strong>Balance:</strong> {{ acc.balance }} {{ acc.currency }}</p>
          <p>
            <strong>Status:</strong>
            <span :class="['status-tag', acc.is_approved ? 'approved' : 'pending']">
              {{ acc.is_approved ? 'Approved' : 'Pending' }}
            </span>
          </p>
        </li>
      </ul>
      <p v-else class="empty">No bank accounts yet.</p>
    </section>

    <section class="section">
      <h3>💳 Your Debit Cards</h3>
      <ul v-if="debitCards.length">
        <li v-for="card in debitCards" :key="card.id" class="card">
          <p><strong>Account:</strong> {{ card.account }}</p>
          <p>
            <strong>Status:</strong>
            <span :class="['status-tag', card.is_approved ? 'approved' : 'pending']">
              {{ card.is_approved ? 'Approved' : 'Pending' }}
            </span>
          </p>
        </li>
      </ul>
      <p v-else class="empty">No debit cards yet.</p>
    </section>

    <section class="section">
      <h3>📜 Your Transactions</h3>
      <ul v-if="transactions.length">
        <li v-for="tx in transactions" :key="tx.id" class="card">
          <p><strong>Type:</strong> {{ tx.type }}</p>
          <p><strong>Amount:</strong> {{ tx.amount }} {{ tx.currency }}</p>
          <p><strong>Account:</strong> {{ tx.bank_account }}</p>
        </li>
      </ul>
      <p v-else class="empty">No transactions yet.</p>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bankAccounts: [],
      debitCards: [],
      transactions: [],
      error: null,
      token: localStorage.getItem('authToken'),
    };
  },
  mounted() {
    this.fetchAllData();
  },
  methods: {
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push('/');
    },
    async fetchAllData() {
      this.error = null;
      try {
        const headers = { Authorization: `Token ${this.token}` };

        const [accRes, cardRes, txRes] = await Promise.all([
          fetch('http://localhost:8000/api/bankaccounts/', { headers }),
          fetch('http://localhost:8000/api/debitcards/', { headers }),
          fetch('http://localhost:8000/api/transactions/', { headers }),
        ]);

        if (!accRes.ok || !cardRes.ok || !txRes.ok) {
          this.error = 'Failed to fetch dashboard data';
          return;
        }

        this.bankAccounts = await accRes.json();
        this.debitCards = await cardRes.json();
        this.transactions = await txRes.json();
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

h2 {
  font-size: 26px;
}

.logout {
  padding: 8px 16px;
  background: #c0392b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.logout:hover {
  background: #a93226;
}

.nav {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.nav a {
  text-decoration: none;
  color: #2c3e50;
  background: #ecf0f1;
  padding: 10px 15px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav a:hover {
  background: #d0d3d4;
  color: #000;
}

.section {
  margin-bottom: 35px;
}

.section h3 {
  margin-bottom: 15px;
  font-size: 20px;
  color: #34495e;
}

.card {
  background: #fdfdfd;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.status-tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 13px;
}

.approved {
  background-color: #d4edda;
  color: #155724;
}

.pending {
  background-color: #fff3cd;
  color: #856404;
}

.error {
  color: red;
  margin-top: 20px;
  font-weight: bold;
}

.empty {
  font-style: italic;
  color: #777;
}
</style>
