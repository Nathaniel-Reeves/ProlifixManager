import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import VueCookies from 'vue-cookies'
import './plugins/bootstrap-vue'
import 'bootstrap'
import App from './App.vue'
import router from './router'
import jquery from 'jquery'
import 'bootstrap-icons/font/bootstrap-icons.css'

Vue.config.productionTip = false

new Vue({
  VueCookies,
  jquery,
  router,
  render: h => h(App)
}).$mount('#app')
