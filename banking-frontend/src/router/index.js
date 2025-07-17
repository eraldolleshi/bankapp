import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginPage.vue'
import DebitCardRequest from '../components/DebitCardRequest.vue'
import BankAccountCreate from '@/components/BankAccountCreate.vue'
import Transfer from '../components/TransferPage.vue'
import ClientDashboard from '../components/ClientDashboard.vue';
import BankerDashboard from '../components/BankerDashboard.vue';


const routes = [
  { path: '/', name: 'Login', component: Login },
  
  { path: '/debit-card-request', name: 'DebitCardRequest', component: DebitCardRequest },
 
  { path: '/transfer', name: 'Transfer', component: Transfer },
  { path: '/create-bank-account', component: BankAccountCreate },
  { path: '/client-dashboard', component: ClientDashboard },
  { path: '/banker-dashboard', component: BankerDashboard },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
