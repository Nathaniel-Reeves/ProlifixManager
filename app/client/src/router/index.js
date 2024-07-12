import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "barchart" */ '../views/HomeView.vue')
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
    path: '/catalogue/components',
    name: 'components',
    props: route => ({ type: route.query.type }),
    component: () => import(/* webpackChunkName: "CatalogueHome" */ '../views/catalogue/components/ComponentHome.vue')
  },
  {
    path: '/catalogue/components/create',
    name: 'NewComponent',
    component: () => import(/* webpackChunkName: "NewComponent" */ '../views/catalogue/components/NewComponent.vue')
  },
  {
    path: '/catalogue/components/:id',
    name: 'ComponentDetail',
    component: () => import(/* webpackChunkName: "ComponentDetail" */ '../views/catalogue/components/ComponentDetail.vue')
  },
  {
    path: '/catalogue/products',
    name: 'products',
    component: () => import(/* webpackChunkName: "ProductHome" */ '../views/catalogue/products/ProductHome.vue')
  },
  {
    path: '/catalogue/products/:id',
    name: 'ProductDetail',
    component: () => import(/* webpackChunkName: "ProductDetail" */ '../views/catalogue/products/ProductDetail.vue')
  },
  {
    path: '/catalogue/products/create',
    name: 'NewProduct',
    component: () => import(/* webpackChunkName: "NewProduct" */ '../views/catalogue/products/NewProduct.vue')
  },
  {
    path: '/organizations',
    name: 'organizations',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationsHome.vue')
  },
  {
    path: '/organizations/:id',
    name: 'OrganizationsDetail',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationDetail.vue')
  },
  {
    path: '/organizations/create',
    name: 'NewOrganization',
    component: () => import(/* webpackChunkName: "NewOrganization" */ '../views/organizations/NewOrganization.vue')
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
  },
  {
    path: '/interactflow',
    name: 'interactflow',
    component: () => import(/* webpackChunkName: "login" */ '../views/VueFlowInteraction.vue')
  },
  {
    path: '/basicflow',
    name: 'basicflow',
    component: () => import(/* webpackChunkName: "login" */ '../views/VueFlowBasic.vue')
  },
  {
    path: '/testapi',
    name: 'testapi',
    component: () => import(/* webpackChunkName: "login" */ '../views/TestAPI.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "login" */ '../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
