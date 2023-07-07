import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import VueCookies from 'vue-cookies'
import { BootstrapVue, BootstrapVueIcons } from './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import jquery from 'jquery'

Vue.config.productionTip = false

new Vue({
  VueCookies,
  jquery,
  router,
  render: h => h(App)
}).$mount('#app')

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
