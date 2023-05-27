import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import 'bootstrap'
import App from './App.vue'
import router from './router'
import jquery from 'jquery'

Vue.config.productionTip = false

new Vue({
  jquery,
  router,
  render: h => h(App)
}).$mount('#app')
