import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/barchart',
    name: 'barchart',
    component: () => import(/* webpackChunkName: "barchart" */ '../views/BarChart.vue')
  },
  {
    path: '/barcodereader',
    name: 'barcodereader',
    component: () => import(/* webpackChunkName: "barcodereader" */ '../views/BarcodeReader.vue')
  },
  {
    path: '/bootstrap',
    name: 'bootstrap',
    component: () => import(/* webpackChunkName: "bootstrap" */ '../views/BootstrapFour.vue')
  },
  {
    path: '/gridchart',
    name: 'gridchart',
    component: () => import(/* webpackChunkName: "gridchart" */ '../views/GridChart.vue')
  },
  {
    path: '/inventory',
    name: 'inventory',
    component: () => import(/* webpackChunkName: "inventory" */ '../views/inventory/InventoryHome.vue'),
    children: [
      {
        path: '/checkins',
        name: 'checkins',
        component: () => import(/* webpackChunkName: "checkins" */ '../views/inventory/InventoryHome.vue')
      },
      {
        path: '/checkouts',
        name: 'checkouts',
        component: () => import(/* webpackChunkName: "checkouts" */ '../views/inventory/InventoryHome.vue')
      }
    ]
  },
  {
    path: '/organizations',
    name: 'organizations',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationsHome.vue'),
    props: {
      labs_filter_prop: false,
      suppliers_filter_prop: false,
      clients_filter_prop: false
    },
    children: [
      {
        path: '/clients',
        name: 'clients',
        component: () => import(/* webpackChunkName: "clients" */ '../views/organizations/OrganizationsHome.vue'),
        props: {
          labs_filter_prop: false,
          suppliers_filter_prop: false,
          clients_filter_prop: true
        }
      },
      {
        path: '/suppliers',
        name: 'suppliers',
        component: () => import(/* webpackChunkName: "suppliers" */ '../views/organizations/OrganizationsHome.vue'),
        props: {
          labs_filter_prop: false,
          suppliers_filter_prop: true,
          clients_filter_prop: false
        }
      },
      {
        path: '/labs',
        name: 'labs',
        component: () => import(/* webpackChunkName: "labs" */ '../views/organizations/OrganizationsHome.vue'),
        props: {
          labs_filter_prop: true,
          suppliers_filter_prop: false,
          clients_filter_prop: false
        }
      }
    ]
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import(/* webpackChunkName: "orders" */ '../views/orders/OrdersHome.vue'),
    children: [
      {
        path: '/lot_numbers',
        name: 'lot_numbers',
        component: () => import(/* webpackChunkName: "lot_numbers" */ '../views/orders/OrdersHome.vue')
      },
      {
        path: '/sales_orders',
        name: 'sales_orders',
        component: () => import(/* webpackChunkName: "sales_orders" */ '../views/orders/OrdersHome.vue')
      },
      {
        path: '/purchase_orders',
        name: 'puchase_orders',
        component: () => import(/* webpackChunkName: "purchase_orders" */ '../views/orders/OrdersHome.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/LogIn.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

export default router
