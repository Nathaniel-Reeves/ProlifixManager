import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import jquery from 'jquery'

// Import bootstrap components
import './plugins/bootstrap-vue'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap'

// Qr Code Generator
import VueQRCodeComponent from 'vue-qr-generator'

Vue.config.productionTip = false

new Vue({
  jquery,
  router,
  render: h => h(App)
}).$mount('#app')

Vue.component('qr-code', VueQRCodeComponent)
