<template>
  <div class="dashboard">
    <div class="header">
      <h2>🏢 Banker Dashboard</h2>
      <button class="logout" @click="logout">Logout</button>
    </div>

  
    <section class="section">
      <h3>👥 Manage Clients</h3>
      <form @submit.prevent="handleClientSubmit" class="form">
        <input v-model="clientForm.username" placeholder="Username" required />
        <input v-model="clientForm.password" placeholder="Password" required type="password" />
        <input v-model="clientForm.email" placeholder="Email" required />
        <select v-model="clientForm.role" required>
          <option disabled value="">Select Role</option>
          <option value="CLIENT">Client</option>
          <option value="BANKER">Banker</option>
        </select>
        <button type="submit">{{ editing ? 'Update' : 'Create' }}</button>
      </form>

      <ul>
        <li v-for="client in clients" :key="client.id" class="card">
          <p>
            <strong>{{ client.username }}</strong> ({{ client.email }})
            <span class="badge">{{ client.role }}</span>
          </p>
          <button @click="editClient(client)">✏️ Edit</button>
          <button @click="deleteClient(client.id)">🗑️ Delete</button>
        </li>
      </ul>
    </section>

  
    <section class="section">
      <h3>🕓 Pending Bank Account Requests</h3>
      <ul>
        <li v-for="acc in pendingAccounts" :key="acc.id" class="card">
          <p><strong>IBAN:</strong> {{ acc.iban }}</p>
          <p><strong>Owner:</strong> {{ acc.owner }}</p>
          <p><strong>Currency:</strong> {{ acc.currency }}</p>
          <button @click="approveAccount(acc.id)">✅ Approve</button>
          <button @click="rejectAccount(acc.id)">❌ Reject</button>
        </li>
      </ul>
    </section>

  
    <section class="section">
      <h3>🕓 Pending Debit Card Requests</h3>
      <ul>
        <li v-for="card in pendingCards" :key="card.id" class="card">
          <p><strong>Card ID:</strong> {{ card.id }}</p>
          <p><strong>Account:</strong> {{ card.account.iban }}</p>
          <p><strong>Owner:</strong> {{ card.account.owner }}</p>
          <button @click="approveCard(card.id)">✅ Approve</button>
          <button @click="rejectCard(card.id)">❌ Reject</button>
        </li>
      </ul>
    </section>

  
    <section class="section">
      <h3>🏦 All Bank Accounts</h3>
      <ul>
        <li v-for="acc in allAccounts" :key="acc.id" class="card">
          <p><strong>IBAN:</strong> {{ acc.iban }}</p>
          <p><strong>Balance:</strong> {{ acc.balance }}</p>
          <p><strong>Owner:</strong> {{ acc.owner }}</p>
        </li>
      </ul>
    </section>


    <section class="section">
      <h3>💳 All Debit Cards</h3>
      <ul>
        <li v-for="card in allCards" :key="card.id" class="card">
          <p><strong>Card ID:</strong> {{ card.id }}</p>
          <p><strong>Status:</strong>
            <span :class="['badge', card.is_approved ? 'approved' : 'pending']">
              {{ card.is_approved ? 'Approved' : 'Rejected' }}
            </span>
          </p>
          <p v-if="card.reject_reason"><strong>Reason:</strong> {{ card.reject_reason }}</p>
        </li>
      </ul>
    </section>

    
    <section class="section">
      <h3>📄 All Transactions</h3>
      <ul>
        <li v-for="txn in allTransactions" :key="txn.id" class="card">
          <p><strong>Account:</strong> {{ txn.bank_account }}</p>
          <p><strong>Type:</strong> {{ txn.type }}</p>
          <p><strong>Amount:</strong> {{ txn.amount }} {{ txn.currency }}</p>
        </li>
      </ul>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: localStorage.getItem('authToken'),
      clients: [],
      clientForm: { username: '', password: '', email: '', role: '' },
      editing: false,
      editingId: null,
      pendingAccounts: [],
      pendingCards: [],
      allAccounts: [],
      allCards: [],
      allTransactions: [],
      error: null,
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
      await Promise.all([
        this.fetchClients(),
        this.fetchBankAccounts(),
        this.fetchDebitCards(),
        this.fetchTransactions(),
      ]);
    },

  
    async fetchClients() {
      try {
        const res = await fetch('http://localhost:8000/api/clients/', {
          headers: { Authorization: `Token ${this.token}` },
        });
        if (!res.ok) throw new Error('Failed to fetch clients');
        this.clients = await res.json();
      } catch (err) {
        this.error = err.message;
      }
    },
    async handleClientSubmit() {
      const url = this.editing
        ? `http://localhost:8000/api/clients/${this.editingId}/`
        : `http://localhost:8000/api/clients/`;
      const method = this.editing ? 'PATCH' : 'POST';

      try {
        const res = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${this.token}`,
          },
          body: JSON.stringify(this.clientForm),
        });
        if (!res.ok) throw new Error('Failed to save client');
        this.clientForm = { username: '', password: '', email: '', role: '' };
        this.editing = false;
        this.editingId = null;
        await this.fetchClients();
      } catch (err) {
        this.error = err.message;
      }
    },
    editClient(client) {
      this.clientForm = {
        username: client.username,
        password: '',
        email: client.email,
        role: client.role,
      };
      this.editing = true;
      this.editingId = client.id;
    },
    async deleteClient(id) {
      if (!confirm('Are you sure?')) return;
      try {
        const res = await fetch(`http://localhost:8000/api/clients/${id}/`, {
          method: 'DELETE',
          headers: { Authorization: `Token ${this.token}` },
        });
        if (!res.ok) throw new Error('Failed to delete client');
        await this.fetchClients();
      } catch (err) {
        this.error = err.message;
      }
    },

  
    async fetchBankAccounts() {
      const res = await fetch('http://localhost:8000/api/bankaccounts/', {
        headers: { Authorization: `Token ${this.token}` },
      });
      const accounts = await res.json();
      this.pendingAccounts = accounts.filter(acc => acc.is_approved === false);
      this.allAccounts = accounts;
    },
    async approveAccount(id) {
      await this.updateApproval(`/api/bankaccounts/${id}/`, true);
    },
    async rejectAccount(id) {
      await this.updateApproval(`/api/bankaccounts/${id}/`, false);
    },

    
    async fetchDebitCards() {
      const res = await fetch('http://localhost:8000/api/debitcards/', {
        headers: { Authorization: `Token ${this.token}` },
      });
      const cards = await res.json();
      this.pendingCards = cards.filter(c => c.is_approved === false);
      this.allCards = cards;
    },
    async approveCard(id) {
      await this.updateApproval(`/api/debitcards/${id}/`, true);
    },
    async rejectCard(id) {
      const reason = prompt("Please enter the reason for rejection:");
      if (!reason) {
        alert("Rejection reason is required.");
        return;
      }

      try {
        const res = await fetch(`http://localhost:8000/api/debitcards/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${this.token}`,
          },
          body: JSON.stringify({
            is_approved: false,
            reject_reason: reason,
          }),
        });
        if (!res.ok) throw new Error('Failed to reject card');
        await this.fetchDebitCards();
      } catch (err) {
        this.error = err.message;
      }
    },

  
    async updateApproval(url, approve) {
      try {
        const res = await fetch(`http://localhost:8000${url}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${this.token}`,
          },
          body: JSON.stringify({ is_approved: approve }),
        });
        if (!res.ok) throw new Error('Update failed');
        await this.fetchBankAccounts();
        await this.fetchDebitCards();
      } catch (err) {
        this.error = err.message;
      }
    },

    
    async fetchTransactions() {
      try {
        const res = await fetch('http://localhost:8000/api/transactions/', {
          headers: { Authorization: `Token ${this.token}` },
        });
        if (!res.ok) throw new Error('Failed to fetch transactions');
        this.allTransactions = await res.json();
      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>


<style scoped>
.dashboard {
  max-width: 1000px;
  margin: auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout {
  background: crimson;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.logout:hover {
  background: darkred;
}

.section {
  margin-top: 30px;
}

.form {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

.form input,
.form select {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.card {
  background: #f9f9f9;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card button {
  margin-right: 10px;
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
}

.card button:hover {
  background: #ddd;
}

.badge {
  background: #ecf0f1;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 13px;
  font-weight: bold;
  margin-left: 10px;
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
</style>