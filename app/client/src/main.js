import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue, { createApp, configureCompat } from 'vue'
import App from './App.vue'
import jquery from 'jquery'
import router from './router/index.js'

// Import bootstrap components
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Qr Code Generator
import VueQRCodeComponent from 'vue-qr-generator'

// Bootstrap is not ready for vue3 yet, it is piggy backing on the migration 'Compat' tool.
// Many of the vue warn console messages are from bootstrap code.  I am turning off the
// console messages from compat untill boostrap-vue is ready for vue 3.  (Line Bellow)
// TODO: Complete Migration to Vue 3
// Guides: https://www.vuemastery.com/blog/vue-3-migration-build/?gad_source=1&gclid=Cj0KCQjwltKxBhDMARIsAG8KnqV3ss66yYwav1VNO5LBhaCEO9wytKyEBp4othQmkZgdt5YwotWstNUaAmoDEALw_wcB
// Guides: https://www.vuemastery.com/blog/migration/
configureCompat({
  WATCH_ARRAY: 'suppress-warning',
  RENDER_FUNCTION: 'suppress-warning',
  INSTANCE_LISTENERS: 'suppress-warning',
  COMPONENT_FUNCTIONAL: 'suppress-warning',
  OPTIONS_BEFORE_DESTROY: 'suppress-warning',
  INSTANCE_SCOPED_SLOTS: 'suppress-warning',
  OPTIONS_DATA_MERGE: 'suppress-warning',
  COMPONENT_V_MODEL: 'suppress-warning',
  CUSTOM_DIR: 'suppress-warning',
  INSTANCE_EVENT_EMITTER: 'suppress-warning',
  ATTR_FALSE_VALUE: 'suppress-warning',
  INSTANCE_ATTRS_CLASS_STYLE: 'suppress-warning',
  GLOBAL_PROTOTYPE: 'suppress-warning',
  GLOBAL_EXTEND: 'suppress-warning',
  GLOBAL_MOUNT: 'suppress-warning',
  OPTIONS_DESTROYED: 'suppress-warning',
  INSTANCE_DESTROY: 'suppress-warning',
  COMPILER_V_BIND_OBJECT_ORDER: 'suppress-warning'
})

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
const app = createApp(App)
app.use(router)
app.use(jquery)
app.component('qr-code', VueQRCodeComponent)
app.mount('#app')

// router.isReady().then(() => app.mount('#app'))
