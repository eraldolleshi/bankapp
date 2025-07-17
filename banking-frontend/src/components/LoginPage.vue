<template>
  <div class="login-container">
    <h2>Login</h2>

    <form @submit.prevent="handleLogin">
      <input
        v-model="username"
        placeholder="Username"
        required
      /><br /><br />

      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      /><br /><br />

      <button type="submit" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;
      this.loading = true;

      try {
        const response = await fetch('http://localhost:8000/api/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          this.error = data.detail || 'Login failed';
          this.loading = false;
          return;
        }

        localStorage.setItem('authToken', data.token);

      
        const userRes = await fetch('http://localhost:8000/api/user/', {
          headers: {
            'Authorization': `Token ${data.token}`,
          },
        });

        const userData = await userRes.json();
        localStorage.setItem('userRole', userData.role);

        
        if (userData.role === 'CLIENT') {
          this.$router.push('/client-dashboard');
        } else if (userData.role === 'BANKER') {
          this.$router.push('/banker-dashboard');
        } else {
          this.error = 'Unknown role';
        }
      } catch (err) {
        this.error = 'Network error';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 50px auto;
  text-align: center;
  font-family: sans-serif;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 15px;
}
</style>
